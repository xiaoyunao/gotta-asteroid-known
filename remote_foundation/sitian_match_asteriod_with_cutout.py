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
from astropy.nddata import Cutout2D
from astropy.visualization import ZScaleInterval
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from astropy.coordinates import SkyCoord, EarthLocation, match_coordinates_sky, Angle
import warnings
import traceback
from tqdm import tqdm
warnings.filterwarnings("ignore")
import multiprocessing as mp

def query_asteroids(q, field_center, field_radius, epoch, observer, mag_limit, njobs, fname, confidence_radius):
    ephs = q.query_mixed_cat(field_center=field_center,
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
    ras, decs = ephs['ra'], ephs['dec']
    v_mags = ephs['V']
    numbers, names = ephs['number'], ephs['name']
    dtype = [('name', 'U32'),
         ('number', 'f8'),
         ('ra', 'f8'),
         ('dec', 'f8'),
         ('mag', 'f4')]
    result_array = np.zeros(len(ephs), dtype=dtype)
    result_array['name'] = names
    result_array['number'] = numbers
    result_array['ra'] = ras
    result_array['dec'] = decs
    result_array['mag'] = v_mags
    return result_array

def main():
    # 配置参数
    root_dir = '/Volumes/Foundation/sitian/'
    sep_limit = 3 * u.arcsec
    mag_limit = 23
    lon, lat, height = 117.575, 40.393, 960
    observer = EarthLocation(lon=lon*u.deg, lat=lat*u.deg, height=height*u.m)
    njobs = 5
    filename = '/Volumes/Foundation/Asteroid/astorb/astorb.dat'
    q = Query(service='Lowell', filename=filename)

    global_all_asteroids = []
    global_all_matches = []

    # 遍历所有 stp1_yyyymmdd_test 文件夹
    folders = sorted([d for d in os.listdir(root_dir) if re.fullmatch(r'stp1_(\d{8})_test', d) and os.path.isdir(os.path.join(root_dir, d))])

    for day_folder in folders:
        # 提取 yyyymmdd 作为输出文件前缀
        yyyymmdd = re.match(r'stp1_(\d{8})_test', day_folder).group(1)

        l2_dir = os.path.join(root_dir, day_folder, 'L2')
        if not os.path.exists(l2_dir):
            continue
        
        # 匹配 .fits.gz 文件
        files = [f for f in os.listdir(l2_dir) if f.endswith('_cat.fits.gz')]
        if not files:
            continue
        
        all_asteroids = []
        all_matches = []

        for fname in tqdm(files, desc=f"Processing {day_folder}", dynamic_ncols=True, leave=False):
            gz_path = os.path.join(l2_dir, fname)
            fits_path = gz_path[:-3]  # 临时解压的 fits 文件路径

            # 解压
            try:
                with gzip.open(gz_path, 'rb') as f_in, open(fits_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            except Exception as e:
                print(f"Failed to decompress {fname}: {e}")
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
                    ra_span = ra_angles.max() - ra_angles.min()
                    
                    if ra_span > 180 * u.deg:
                        ra_span = (ra_angles.wrap_at(180 * u.deg).max() - ra_angles.wrap_at(180 * u.deg).min()).wrap_at(360 * u.deg)

                    corner_coords = SkyCoord(ra=ra_vals * u.deg, dec=dec_vals * u.deg)
                    field_center = SkyCoord(ra=ra_center, dec=dec_center * u.deg, frame='icrs')
                    radii = field_center.separation(corner_coords)
                    max_diff = radii.max() + 0.05 * u.deg
                    confidence_radius = (max_diff.to(u.deg).value + 0.5) * u.deg
                    exptime = float(header['EXPTIME']) / 86400
                    try:
                        epoch = Time(header['DATE-OBS'], format='isot', scale='utc') + exptime / 2
                        mjd = epoch.mjd
                    except:
                        mjd = float(header['MJD']) + exptime / 2
                        epoch = Time(mjd, format='mjd', scale='utc')

            except Exception as e:
                print(f"Failed to load {fname}: {e}")
                traceback.print_exc()
                os.remove(fits_path)  # 删除临时 fits
                continue

            try:
                results = query_asteroids(q, field_center, max_diff, epoch, observer, mag_limit, njobs, fname, confidence_radius)
                
                if results is None:
                    os.remove(fits_path)
                    continue
                
                ephs = Table(results)
                names, numbers, ras, decs, mags = ephs['name'], ephs['number'], ephs['ra'], ephs['dec'], ephs['mag']
                pix_coords = w.all_world2pix(ras, decs, 1)
                x_pix, y_pix = pix_coords
                inside_mask = (x_pix >= 1) & (x_pix <= nx) & (y_pix >= 1) & (y_pix <= ny)

                if not np.any(inside_mask):
                    os.remove(fits_path)
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

                # === Cutout 操作 ===
                try:
                    l1_dir = os.path.join(root_dir, day_folder, 'L1')
                    # 对应的 L1 图像文件名
                    fimg_name = fname.replace('_cat.fits.gz', '.fits.gz')
                    gz_path_img = os.path.join(l1_dir, fimg_name)
                    
                    if not os.path.exists(gz_path_img):
                        print(f"Image file not found for cutout: {gz_path_img}")
                    else:
                        # 解压 .fits.gz
                        fits_path_img = gz_path_img[:-3]
                        with gzip.open(gz_path_img, 'rb') as f_in, open(fits_path_img, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                        
                        try:
                            with fits.open(fits_path_img) as hdul_img:
                                img_data = hdul_img[1].data
                                w_img = WCS(hdul_img[1].header)

                                # 输出文件夹
                                base_name = os.path.splitext(fname)[0].replace('_cat', '')
                                out_dir = os.path.join(root_dir, day_folder, 'cutouts', base_name)
                                os.makedirs(out_dir, exist_ok=True)

                                # RA/DEC → pixel
                                asteroid_coords = SkyCoord(ras * u.deg, decs * u.deg)
                                x_pixs, y_pixs = w_img.world_to_pixel(asteroid_coords)

                                interval = ZScaleInterval()

                                for i, (x_pix, y_pix, row) in enumerate(zip(x_pixs, y_pixs, asteroid_tbl)):
                                    try:
                                        cutout = Cutout2D(img_data, (x_pix, y_pix), (300, 300), wcs=w_img)
                                        cut_data = cutout.data
                                        vmin, vmax = interval.get_limits(cut_data)
                                        norm_data = ((cut_data - vmin) / (vmax - vmin)).clip(0, 1)

                                        cutout_name = f'{i:03d}_{row["name"].replace(" ", "_")}.png'
                                        cutout_path = os.path.join(out_dir, cutout_name)

                                        fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
                                        ax.imshow(norm_data, cmap='gray', origin='lower')
                                        circ = Circle((150, 150), radius=10, edgecolor='lime', facecolor='none', linewidth=1.5)
                                        ax.add_patch(circ)
                                        ax.axis('off')
                                        plt.tight_layout(pad=0)
                                        plt.savefig(cutout_path, bbox_inches='tight', pad_inches=0)
                                        plt.close(fig)
                                    except Exception as e:
                                        print(f"Cutout failed for {row['name']}: {e}")
                        finally:
                            # 删除临时解压的 fits 文件
                            if os.path.exists(fits_path_img):
                                os.remove(fits_path_img)
                except Exception as e:
                    print(f"General cutout error on {fname}: {e}")

            # 交叉匹配
                try:
                    asteroid_coords = SkyCoord(ras * u.deg, decs * u.deg)
                    cat_coords = SkyCoord(cat['RA'] * u.deg, cat['DEC'] * u.deg)
                    idx, sep2d, _ = match_coordinates_sky(asteroid_coords, cat_coords)
                    matched = sep2d < sep_limit

                    if any(matched):
                        matched_ast = asteroid_tbl[matched]
                        matched_cat = cat[idx[matched]]
                        combined = hstack([matched_ast, matched_cat], join_type='exact')
                        all_matches.append(combined)

                except Exception as e:
                    print(f"Matching error on {fname}: {e}")
                    continue

            except Exception as e:
                print(f"Query failed on {fname}: {e}")
                traceback.print_exc()
                continue
            finally:
                # 删除临时 fits 文件
                os.remove(fits_path)

        # 保存每日结果
        if all_asteroids:
            total_ast = vstack(all_asteroids)
            total_ast.write(os.path.join(root_dir, f'{yyyymmdd}_all_asteroids.fits'), overwrite=True)
            global_all_asteroids.append(total_ast)

        if all_matches:
            total_match = vstack(all_matches)
            total_match.write(os.path.join(root_dir, f'{yyyymmdd}_matched_asteroids.fits'), overwrite=True)
            global_all_matches.append(total_match)
            
        print(f"Processed {day_folder}: {len(all_asteroids)} asteroids, {len(all_matches)} matches found.")

    # 保存全局结果
    if global_all_asteroids:
        total_all = vstack(global_all_asteroids)
        total_all.write(os.path.join(root_dir, 'all_asteroids.fits'), overwrite=True)
        print(f"Saved total asteroid catalog: {len(total_all)} entries")

    if global_all_matches:
        total_match_all = vstack(global_all_matches)
        total_match_all.write(os.path.join(root_dir, 'matched_asteroids.fits'), overwrite=True)
        print(f"Saved total matched catalog: {len(total_match_all)} entries")
    else:
        print("No matched sources found in any folder.")


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
    