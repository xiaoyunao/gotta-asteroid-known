import numpy as np
import os
import re
import gzip
import shutil
from aleph.Query import Query
import astropy.units as u
from astropy.wcs import WCS
from astropy.io import fits
from astropy.time import Time
from astropy.table import Table, vstack, hstack
from astropy.coordinates import SkyCoord, EarthLocation, match_coordinates_sky, Angle
import warnings
import traceback
from tqdm import tqdm
import multiprocessing as mp

warnings.filterwarnings("ignore")


def query_asteroids(q, field_center, field_radius, epoch, observer, mag_limit, njobs, fname, confidence_radius):
    ephs = q.query_mixed_cat(
        field_center=field_center,
        radius=field_radius,
        epoch=epoch,
        observer=observer,
        njobs=njobs,
        confidence_radius=confidence_radius
    )

    if ephs is None or len(ephs) == 0:
        return None

    mask = ephs['V'] < mag_limit
    ephs = ephs[mask]
    if len(ephs) == 0:
        return None

    dtype = [('name', 'U32'),
             ('number', 'f8'),
             ('ra', 'f8'),
             ('dec', 'f8'),
             ('mag', 'f4')]
    result_array = np.zeros(len(ephs), dtype=dtype)
    result_array['name'] = ephs['name']
    result_array['number'] = ephs['number']
    result_array['ra'] = ephs['ra']
    result_array['dec'] = ephs['dec']
    result_array['mag'] = ephs['V']
    return result_array


def process_one_day(args):
    """单个日期的处理逻辑（在子进程中执行）"""
    yyyymmdd, day_files, cfg = args
    root_dir, result_dir, sep_limit, mag_limit, observer, njobs, q = cfg

    all_asteroids = []
    all_matches = []

    for fname in tqdm(day_files, desc=f"Processing {yyyymmdd}", dynamic_ncols=True, leave=False):
        gz_path = os.path.join(root_dir, fname)
        fits_path = gz_path[:-3]

        try:
            with gzip.open(gz_path, 'rb') as f_in, open(fits_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            print(f"[{yyyymmdd}] Failed to decompress {fname}: {e}")
            continue

        try:
            with fits.open(fits_path, memmap=False) as hdul:
                header = hdul[1].header
                cat = Table(hdul[1].data)
                w = WCS(header)
                ny, nx = 9120, 8976
                pix_corners = [[1, 1], [1, ny], [nx, 1], [nx, ny]]
                world = w.all_pix2world(pix_corners, 1)
                ra_vals, dec_vals = world[:, 0], world[:, 1]
                ra_angles = Angle(ra_vals * u.deg)
                ra_center = ra_angles.wrap_at(180 * u.deg).mean()
                ra_center = ra_center.wrap_at(360 * u.deg)
                dec_center = (dec_vals.min() + dec_vals.max()) / 2

                corner_coords = SkyCoord(ra=ra_vals * u.deg, dec=dec_vals * u.deg)
                field_center = SkyCoord(ra=ra_center, dec=dec_center * u.deg, frame='icrs')
                radii = field_center.separation(corner_coords)
                max_diff = radii.max() + 0.05 * u.deg
                confidence_radius = (max_diff.to(u.deg).value + 0.5) * u.deg
                exptime = float(header['EXPTIME']) / 86400
                try:
                    epoch = Time(header['DATE-OBS'], format='isot', scale='utc') + exptime / 2
                    mjd = epoch.mjd
                except Exception:
                    mjd = float(header['MJD']) + exptime / 2
                    epoch = Time(mjd, format='mjd', scale='utc')

        except Exception as e:
            print(f"[{yyyymmdd}] Failed to load {fname}: {e}")
            traceback.print_exc()
            if os.path.exists(fits_path):
                os.remove(fits_path)
            continue

        try:
            results = query_asteroids(q, field_center, max_diff, epoch,
                                      observer, mag_limit, njobs, fname, confidence_radius)
            if results is None:
                continue

            ephs = Table(results)
            names, numbers, ras, decs, mags = ephs['name'], ephs['number'], ephs['ra'], ephs['dec'], ephs['mag']
            x_pix, y_pix = w.all_world2pix(ras, decs, 1)
            inside_mask = (x_pix >= 1) & (x_pix <= nx) & (y_pix >= 1) & (y_pix <= ny)
            if not np.any(inside_mask):
                continue

            names = names[inside_mask]
            numbers = numbers[inside_mask]
            ras = ras[inside_mask]
            decs = decs[inside_mask]
            mags = mags[inside_mask]
            fname_list = [fname] * len(names)
            exptime_list = [float(mjd)] * len(names)

            asteroid_tbl = Table([names, numbers, ras, decs, mags, fname_list, exptime_list],
                                 names=('name', 'number', 'ra', 'dec', 'mag', 'source_file', 'epoch'))
            all_asteroids.append(asteroid_tbl)

            # 匹配星表
            try:
                asteroid_coords = SkyCoord(ras * u.deg, decs * u.deg)
                cat_coords = SkyCoord(cat['RA_Win'] * u.deg, cat['DEC_Win'] * u.deg)
                idx, sep2d, _ = match_coordinates_sky(asteroid_coords, cat_coords)
                matched = sep2d < sep_limit
                if np.any(matched):
                    matched_ast = asteroid_tbl[matched]
                    matched_cat = cat[idx[matched]]
                    combined = hstack([matched_ast, matched_cat], join_type='exact')
                    all_matches.append(combined)
            except Exception as e:
                print(f"[{yyyymmdd}] Matching error on {fname}: {e}")
                continue

        except Exception as e:
            print(f"[{yyyymmdd}] Query failed on {fname}: {e}")
            traceback.print_exc()
        finally:
            if os.path.exists(fits_path):
                os.remove(fits_path)

    # 每天结果保存
    if all_asteroids:
        total_ast = vstack(all_asteroids)
        total_ast.write(os.path.join(result_dir, f'{yyyymmdd}_all_asteroids.fits'), overwrite=True)
    else:
        total_ast = None

    if all_matches:
        total_match = vstack(all_matches)
        total_match.write(os.path.join(result_dir, f'{yyyymmdd}_matched_asteroids.fits'), overwrite=True)
    else:
        total_match = None

    print(f"✅ {yyyymmdd} done: {len(all_asteroids)} asteroid tables, {len(all_matches)} match tables.")
    return total_ast, total_match


def main():
    # 全局配置
    root_dir = '/Volumes/Foundation/L2_data/'
    result_dir = '/Volumes/Foundation/asteroid_result/'
    os.makedirs(result_dir, exist_ok=True)

    sep_limit = 3 * u.arcsec
    mag_limit = 23
    lon, lat, height = 117.575, 40.393, 960
    observer = EarthLocation(lon=lon*u.deg, lat=lat*u.deg, height=height*u.m)
    njobs = 5
    filename = '/Volumes/Foundation/Asteroid/astorb/astorb.dat'
    q = Query(service='Lowell', filename=filename)

    # 文件按日期分组
    files = sorted([f for f in os.listdir(root_dir) if f.endswith('_cat.fits.gz')])
    file_groups = {}
    for f in files:
        m = re.search(r'_(\d{8})_', f)
        if m:
            file_groups.setdefault(m.group(1), []).append(f)

    if not file_groups:
        print("❌ 没有找到匹配文件")
        return

    # 多进程并行处理每天
    cfg = (root_dir, result_dir, sep_limit, mag_limit, observer, njobs, q)
    tasks = [(d, fs, cfg) for d, fs in sorted(file_groups.items())]

    with mp.Pool(processes=min(len(tasks), 6)) as pool:
        results = list(pool.imap_unordered(process_one_day, tasks))

    # 汇总全局结果
    all_ast, all_match = [], []
    for a, m in results:
        if a is not None:
            all_ast.append(a)
        if m is not None:
            all_match.append(m)

    if all_ast:
        total_all = vstack(all_ast)
        total_all.write(os.path.join(result_dir, 'all_asteroids.fits'), overwrite=True)
        print(f"💾 Saved total asteroid catalog: {len(total_all)} entries")

    if all_match:
        total_match_all = vstack(all_match)
        total_match_all.write(os.path.join(result_dir, 'matched_asteroids.fits'), overwrite=True)
        print(f"💾 Saved total matched catalog: {len(total_match_all)} entries")


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
