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


# ================================================================
# 🔍 你原来使用的 query_asteroids（我没有动）
# ================================================================
def query_asteroids(q, field_center, field_radius, epoch, observer, mag_limit, njobs, fname, confidence_radius):
    ephs = q.query_mixed_cat(field_center=field_center,
                             radius=field_radius,
                             epoch=epoch,
                             observer=observer,
                             njobs=njobs,
                             confidence_radius=confidence_radius
                             )
    print(f"  小行星查询结果统计：共查询到 {0 if ephs is None else len(ephs)} 颗小行星（包含所有亮度）")
    if ephs is None or len(ephs) == 0:
        return None
    
    mask = ephs['V'] < mag_limit
    ephs = ephs[mask]

    valid_mask = np.isfinite(ephs['ra']) & np.isfinite(ephs['dec'])
    if 'ra' in ephs.colnames:
        valid_mask &= (ephs['ra'] < 3600 * u.deg)
    if 'dec' in ephs.colnames:
        valid_mask &= (np.abs(ephs['dec']) <= 3600 * u.deg)
    ephs = ephs[valid_mask]
    if len(ephs) == 0:
        return None
    
    ra_raw = np.array([val.value if hasattr(val, 'unit') else val for val in ephs['ra']], dtype=float)
    dec_raw = np.array([val.value if hasattr(val, 'unit') else val for val in ephs['dec']], dtype=float)

    valid = np.isfinite(ra_raw) & np.isfinite(dec_raw)
    valid &= (ra_raw > -3600) & (ra_raw < 3600)
    valid &= (dec_raw > -90) & (dec_raw < 90)

    ra_raw = ra_raw[valid]
    dec_raw = dec_raw[valid]
    ephs = ephs[valid]

    ras = Angle(ra_raw * u.deg).wrap_at(360*u.deg).degree
    decs = np.array(ephs['dec'], dtype=float)

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



# ================================================================
# 🆕 新的主入口：你直接手动输入 RA/Dec、FoV、时间
# ================================================================
def TestManual():
    # -------- 你在下面修改这些参数即可 --------
    # 参数
    field_center_ra  = 355.000     # deg
    field_center_dec = 0.000      # deg
    fov_radius_deg   = 4.0        # deg
    obstime          = "2025-01-17T22:15:17.144"
    mag_limit        = 23
    njobs            = 5

    # 转换成 astropy 对象
    field_center = SkyCoord(ra=field_center_ra*u.deg, dec=field_center_dec*u.deg, frame='icrs')
    ra = field_center.ra
    ra[ra>180*u.deg] -= 360*u.deg
    field_center = SkyCoord(ra=ra, dec=field_center.dec, frame=field_center.frame)
    print(field_center.ra.rad)

    print(field_center)
    field_radius = fov_radius_deg * u.deg
    epoch = Time(obstime, scale='utc', format='isot')
    observer = EarthLocation(lon=117.575*u.deg, lat=40.393*u.deg, height=960*u.m)
    confidence_radius = (fov_radius_deg + 1.0) * u.deg  # 要比 field_radius 大

    # 观测地点（保持与你的原代码一致）
    lon, lat, height = 117.575, 40.393, 960
    observer = EarthLocation(lon=lon*u.deg, lat=lat*u.deg, height=height*u.m)

    # astorb 数据库
    filename = '/Volumes/Foundation/Asteroid/astorb/astorb.dat'
    q = Query(service='Lowell', filename=filename)

    # 直接运行
    results = query_asteroids(
        q, field_center, field_radius, epoch,
        observer, mag_limit, njobs,
        fname="Manual Input", confidence_radius=confidence_radius
    )


# ================================================================
# 运行入口
# ================================================================
if __name__ == "__main__":
    try:
        mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass

    TestManual()
