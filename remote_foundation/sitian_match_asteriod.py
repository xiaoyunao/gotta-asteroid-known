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

    # --- FIX: 过滤不良值（NaN / 999 等）并 wrap RA 到 0-360 ---
    valid_mask = np.isfinite(ephs['ra']) & np.isfinite(ephs['dec'])
    if 'ra' in ephs.colnames:
        # 可能存在 999 或 9999 的 sentinel 值
        valid_mask &= (ephs['ra'] < 3600 * u.deg)  # 宽松阈值，排除明显不合法的大值
    if 'dec' in ephs.colnames:
        valid_mask &= (np.abs(ephs['dec']) <= 3600 * u.deg)  # 宽松
    ephs = ephs[valid_mask]
    if len(ephs) == 0:
        return None
    
    # 强制把 RA 转成 float，不带单位
    ra_raw = np.array([val.value if hasattr(val, 'unit') else val for val in ephs['ra']], dtype=float)
    dec_raw = np.array([val.value if hasattr(val, 'unit') else val for val in ephs['dec']], dtype=float)

    # 过滤非法值
    valid = np.isfinite(ra_raw) & np.isfinite(dec_raw)
    valid &= (ra_raw > -3600) & (ra_raw < 3600)
    valid &= (dec_raw > -90) & (dec_raw < 90)

    ra_raw = ra_raw[valid]
    dec_raw = dec_raw[valid]
    ephs = ephs[valid]

    ras = Angle(ra_raw * u.deg).wrap_at(360*u.deg).degree
    decs = np.array(ephs['dec'], dtype=float)
    # 规范 dec（确保在 -90..90 范围内；非法的会被过滤掉）
    dec_valid = np.isfinite(decs) & (decs >= -90) & (decs <= 90)
    if not np.all(dec_valid):
        ras = ras[dec_valid]
        decs = decs[dec_valid]
        ephs = ephs[dec_valid]
        if len(ephs) == 0:
            return None

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


def wrap_ra_to_crval(ra_array_deg, crval_deg):
    """
    将 ra_array_deg (deg) wrap 到以 crval_deg 为中心的区间 [crval-180, crval+180)
    返回同样长度的 array（单位 deg）
    """
    # 确保 numpy 数组 float
    ra = np.array(ra_array_deg, dtype=float)
    crval = float(crval_deg)
    # 计算相对于 crval 的偏移，归一到 [-180, 180)
    delta = ( (ra - crval + 180.0) % 360.0 ) - 180.0
    return crval + delta


def main():
    # 配置参数
    root_dir = '/Volumes/Foundation/Asteroid/L2_data/L2_corr/'
    result_dir = '/Volumes/Foundation/Asteroid/asteroid_result/'
    os.makedirs(result_dir, exist_ok=True)

    sep_limit = 3 * u.arcsec
    mag_limit = 23
    lon, lat, height = 117.575, 40.393, 960
    observer = EarthLocation(lon=lon*u.deg, lat=lat*u.deg, height=height*u.m)
    njobs = 5

    filename = '/Volumes/Foundation/Asteroid/astorb/astorb.dat'
    q = Query(service='Lowell', filename=filename)

    global_all_asteroids = []
    global_all_matches = []

    # 所有 cat 文件
    files = sorted([f for f in os.listdir(root_dir) if f.endswith('_cat.fits.gz')])
    if not files:
        print("❌ 没有找到 *_cat.fits.gz 文件。")
        return

    # 按日期分组
    file_groups = {}
    for f in files:
        m = re.search(r'_(\d{8})_', f)
        if not m:
            continue
        date = m.group(1)
        file_groups.setdefault(date, []).append(f)


    for yyyymmdd, day_files in sorted(file_groups.items()):
        all_asteroids = []
        all_matches = []

        for fname in tqdm(day_files, desc=f"Processing {yyyymmdd}", dynamic_ncols=True, leave=False):
            gz_path = os.path.join(root_dir, fname)
            fits_path = gz_path[:-3]

            # 解压
            try:
                with gzip.open(gz_path, 'rb') as f_in, open(fits_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            except Exception as e:
                print(f"Failed to decompress {fname}: {e}")
                continue


            ### --- FITS 读取与 WCS ---
            try:
                with fits.open(fits_path, memmap=False) as hdul:
                    header = hdul[1].header
                    cat = Table(hdul[1].data)
                    w = WCS(header)

                    # 相机大小（你的相机固定值）
                    ny, nx = 9120, 8976

                    # 像素角点 → 世界坐标
                    pix_corners = np.array([[1, 1], [1, ny], [nx, 1], [nx, ny]])
                    world = w.all_pix2world(pix_corners, 1)
                    ra_vals, dec_vals = world[:, 0], world[:, 1]

                    ### --- FIX: wrap WCS RA to 0–360 & 可靠计算 circular mean for RA_center ---
                    ra_angles = Angle(ra_vals * u.deg).wrap_at(360 * u.deg)
                    # 使用向量平均来计算 circular mean，避免 359° 与 1° 平均变成 180°
                    ra_rad = ra_angles.to(u.rad).value
                    sin_mean = np.mean(np.sin(ra_rad))
                    cos_mean = np.mean(np.cos(ra_rad))
                    ra_center_rad = np.arctan2(sin_mean, cos_mean)
                    # arctan2 返回范围 -pi..pi，转回 0..360
                    if ra_center_rad < 0:
                        ra_center_rad += 2 * np.pi
                    ra_center = Angle(ra_center_rad * u.rad).wrap_at(360 * u.deg)

                    # 规范 dec_center（简单取中值）
                    dec_center = (dec_vals.min() + dec_vals.max()) / 2.0

                    # field center（确保单位正确）
                    field_center = SkyCoord(
                        ra=ra_center.degree * u.deg,
                        dec=dec_center * u.deg,
                        frame='icrs'
                    )

                    # 覆盖半径（你原来的逻辑保持不变）
                    corner_coords = SkyCoord(ra=ra_angles, dec=dec_vals * u.deg)
                    radii = field_center.separation(corner_coords)
                    max_diff = radii.max() + 0.05 * u.deg
                    confidence_radius = (max_diff.to(u.deg).value + 0.5) * u.deg
                    
                    # 时间
                    exptime = float(header.get('EXPTIME', 0.0)) / 86400
                    try:
                        epoch = Time(header['DATE-OBS'], format='isot', scale='utc') + exptime / 2
                        mjd = epoch.mjd
                    except Exception:
                        mjd = float(header.get('MJD', 0.0)) + exptime / 2
                        epoch = Time(mjd, format='mjd', scale='utc')

            except Exception as e:
                print(f"Failed to load {fname}: {e}")
                traceback.print_exc()
                # 清理临时 fits
                if os.path.exists(fits_path):
                    try:
                        os.remove(fits_path)
                    except:
                        pass
                continue


            ### --- 查询小行星 ---
            try:
                results = query_asteroids(
                    q, field_center, max_diff, epoch,
                    observer, mag_limit, njobs, fname, confidence_radius
                )
                if results is None:
                    continue

                ephs = Table(results)
                names = ephs['name']
                numbers = ephs['number']
                ras = ephs['ra']
                decs = ephs['dec']
                mags = ephs['mag']

                # world2pix：注意传入的 ra/dec 都应为度的浮点数组
                try:
                    # 读取 WCS header 中的 RA 参考值（CRVAL1）——兼容多种 astropy 版本
                    try:
                        crval1 = header.get('CRVAL1', None)
                        if crval1 is None:
                            # fallback to wcs object
                            crval1 = w.wcs.crval[0]
                    except Exception:
                        crval1 = w.wcs.crval[0]

                    # 把 ras wrap 到以 crval1 为中心的区间，这样与 WCS 一致（避免跨 0/360 导致大的伪角距）
                    ras_f = np.array(ras, dtype=float)
                    ras_for_wcs = wrap_ra_to_crval(ras_f, crval1)

                    decs_f = np.array(decs, dtype=float)

                    # some astropy versions expect shape (N,2) input; all_world2pix usually accepts (ra, dec, origin)
                    pix = w.all_world2pix(ras_for_wcs, decs_f, 1)
                    # 返回可能是 (N,2) 行列形式，确保取横纵正确
                    pix = np.array(pix)
                    if pix.ndim == 2 and pix.shape[1] == 2:
                        x_pix, y_pix = pix[:, 0], pix[:, 1]
                    else:
                        # 兼容旧式返回
                        x_pix, y_pix = pix

                except Exception as e:
                    print(f"world2pix error on {fname}: {e}")
                    continue

                # --- FIX: 给 inside_mask 增加 margin 防止边缘像素被误判在场外 ---
                margin = 5  # pix
                inside_mask = (
                    (x_pix >= 1 - margin) & (x_pix <= nx + margin) &
                    (y_pix >= 1 - margin) & (y_pix <= ny + margin)
                )
                if not np.any(inside_mask):
                    continue

                names = names[inside_mask]
                numbers = numbers[inside_mask]
                ras = ras[inside_mask]
                decs = decs[inside_mask]
                mags = mags[inside_mask]

                fname_list = [fname] * len(names)
                exptime_list = [float(mjd)] * len(names)

                asteroid_tbl = Table(
                    [names, numbers, ras, decs, mags, fname_list, exptime_list],
                    names=('name', 'number', 'ra', 'dec', 'mag', 'source_file', 'epoch')
                )
                all_asteroids.append(asteroid_tbl)

                ### --- FIX: wrap catalog RA、自动检测并修正单位，并做稳健匹配与 hstack --- 
                try:
                    # 自动检测 RA_Win 单位异常（若最大值 > 360 -> 假设是 1e4 倍，需要缩放）
                    raw_cat_ra = np.array(cat['RA_Win'], dtype=float)
                    if np.nanmax(raw_cat_ra) > 360:
                        # 很可能是 *1e4 的整数存储（根据你 pipeline 的实际情况可调整）
                        print(f"Warning: catalog RA_Win looks large (max={np.nanmax(raw_cat_ra):.1f}), applying /1e4 correction.")
                        raw_cat_ra = raw_cat_ra * 1e-4

                    cat_ra = Angle(raw_cat_ra * u.deg).wrap_at(360 * u.deg)
                    cat_dec = np.array(cat['DEC_Win'], dtype=float)
                    cat_coords = SkyCoord(cat_ra, cat_dec * u.deg)

                    asteroid_coords = SkyCoord(
                        Angle(np.array(ras, dtype=float) * u.deg).wrap_at(360 * u.deg),
                        np.array(decs, dtype=float) * u.deg
                    )

                    idx, sep2d, _ = match_coordinates_sky(asteroid_coords, cat_coords)
                    matched = sep2d < sep_limit

                    if np.any(matched):
                        matched_ast = asteroid_tbl[matched]
                        # matched_cat 可能是一个 view，复制以保证 hstack 安全
                        matched_cat = cat[idx[matched]].copy()
                        # 为避免 dtype/名字冲突，用 outer join
                        combined = hstack([matched_ast, matched_cat], join_type='outer')
                        all_matches.append(combined)

                except Exception as e:
                    print(f"Matching error on {fname}: {e}")
                    traceback.print_exc()
                    continue

            except Exception as e:
                print(f"Query failed on {fname}: {e}")
                traceback.print_exc()
                continue

            finally:
                if os.path.exists(fits_path):
                    try:
                        os.remove(fits_path)
                    except Exception as e:
                        print(f"Warning: failed to remove {fits_path}: {e}")


        # 每日结果保存
        if all_asteroids:
            total_ast = vstack(all_asteroids)
            total_ast.write(os.path.join(result_dir, f'{yyyymmdd}_all_asteroids.fits'), overwrite=True)
            global_all_asteroids.append(total_ast)

        if all_matches:
            total_match = vstack(all_matches)
            total_match.write(os.path.join(result_dir, f'{yyyymmdd}_matched_asteroids.fits'), overwrite=True)
            global_all_matches.append(total_match)

        print(f"Processed {yyyymmdd}: {len(all_asteroids)} asteroid tables, {len(all_matches)} match tables found.")


    # 全局结果
    if global_all_asteroids:
        total_all = vstack(global_all_asteroids)
        total_all.write(os.path.join(result_dir, 'all_asteroids.fits'), overwrite=True)
        print(f"Saved total asteroid catalog: {len(total_all)} entries")

    if global_all_matches:
        total_match_all = vstack(global_all_matches)
        total_match_all.write(os.path.join(result_dir, 'matched_asteroids.fits'), overwrite=True)
        print(f"Saved total matched catalog: {len(total_match_all)} entries")
    else:
        print("No matched sources found in any file.")


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
