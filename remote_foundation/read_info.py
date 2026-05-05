import os
import glob
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
from astropy.time import Time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

def process_fits(fpath):
    try:
        with fits.open(fpath) as hdul:
            
            header = hdul[0].header
            w = WCS(header)

            ny, nx = 9576, 6388
            if ny is None or nx is None:
                return None

            pix_corners = [[1, 1], [1, ny], [nx, 1], [nx, ny]]
            world = w.all_pix2world(pix_corners, 1)

            ra_vals = world[:, 0]
            dec_vals = world[:, 1]
            ra1, ra2 = ra_vals.min(), ra_vals.max()
            dec1, dec2 = dec_vals.min(), dec_vals.max()

            jd = header['JD']
            date_obs = header['DATE-OBS']
            exptime = header['EXPTIME']

            if jd is not None:
                mjd = jd - 2400000.5
            else:
                mjd = -999
                
            print(f"✅ 成功解析: {fpath}")
            
            return {
                "filepath": fpath,
                "ra_min": ra1, "ra_max": ra2,
                "dec_min": dec1, "dec_max": dec2,
                "mjd": mjd,
                "date_obs": date_obs if date_obs else "",
                "exptime": exptime
            }
            
    except Exception as e:
        print(f"❌ 解析失败: {fpath} - {e}")
        return None

# 所有路径模式
search_paths = [
    "/Volumes/Foundation/SMT_data/20250210/*.fits"
]

# 匹配所有 fits 文件路径
all_fits = []
for pattern in search_paths:
    all_fits.extend(glob.glob(pattern))

print(f"🔍 共找到 {len(all_fits)} 个 _cat.fits 文件，开始并行处理...")

# 用线程池并行处理
results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_fits, f): f for f in all_fits}
    for future in tqdm(as_completed(futures), total=len(futures), desc="处理中"):
        result = future.result()
        if result:
            results.append(result)

# 写入 FITS 表格
if results:
    table = Table(rows=results)
    output_path = "summary_cat_info.fits"
    table.write(output_path, overwrite=True)
    print(f"✅ 提取完成，保存为：{output_path}")
else:
    print("⚠ 没有成功处理任何文件。")
