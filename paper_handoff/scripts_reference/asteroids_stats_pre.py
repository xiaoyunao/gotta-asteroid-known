# ===========================================================
# SITIAN ASTEROID PIPELINE — CLEAN VERSION (FULL WORKING CODE)
# 不计算 r, Δ, α
# ===========================================================

from astropy.table import Table
import pandas as pd
import numpy as np
import re

# ===========================================================
# 1. 读取 FITS → df
# ===========================================================
input_fits = "matched_asteroids_sbdb.fits"
tbl = Table.read(input_fits, format="fits")
df = tbl.to_pandas()

# 把 object 列统一为字符串
for c in df.columns:
    if df[c].dtype == object:
        df[c] = df[c].astype(str).str.strip()

print("Loaded", len(df), "rows from FITS.")
print(df.head().T)


# ===========================================================
# 工具函数
# ===========================================================
def coalesce_columns(df, candidates):
    """返回 df 中第一个存在且非空的列值序列（按优先级）。"""
    for c in candidates:
        if c in df.columns:
            series = pd.to_numeric(df[c], errors='coerce')
            if series.notnull().any():
                return series
    return pd.Series([np.nan]*len(df), index=df.index)

def parse_numeric_with_unit(x):
    """
    解析如 '7.3e-10 AU' / '3.7e-08 deg' / '1.234 rad'
    返回 float 数字部分（不做单位转换）。
    """
    if x is None:
        return np.nan
    if not isinstance(x, str):
        return x
    x = x.strip()
    match = re.match(r'^([+-]?\d+(\.\d+)?([eE][+-]?\d+)?)\s*[A-Za-z/]*$', x)
    if match:
        try:
            return float(match.group(1))
        except:
            return np.nan
    return np.nan


# ===========================================================
# 2. 实测位置 RA_Win / DEC_Win
# ===========================================================
df['ra_obs']  = pd.to_numeric(df.get('RA_Win', np.nan), errors='coerce')
df['dec_obs'] = pd.to_numeric(df.get('DEC_Win', np.nan), errors='coerce')


# ===========================================================
# 3. 实测亮度优先级：PSF → Kron → Aper1..20
# ===========================================================
mag_candidates = []
if 'Mag_PSF' in df.columns:   mag_candidates.append('Mag_PSF')
if 'Mag_Kron' in df.columns:  mag_candidates.append('Mag_Kron')

for i in range(1, 20+1):
    col = f"Mag_Aper{i}"
    if col in df.columns:
        mag_candidates.append(col)

df['mag_obs'] = coalesce_columns(df, mag_candidates)

# 误差同理
magerr_candidates = []
if 'MagErr_PSF' in df.columns:   magerr_candidates.append('MagErr_PSF')
if 'MagErr_Kron' in df.columns:  magerr_candidates.append('MagErr_Kron')
for i in range(1,21):
    col = f"MagErr_Aper{i}"
    if col in df.columns:
        magerr_candidates.append(col)

df['mag_obs_err'] = coalesce_columns(df, magerr_candidates)


# ===========================================================
# 4. MPC 预报亮度
# ===========================================================
df['mag_mpc_pred_raw'] = pd.to_numeric(df.get('mag', np.nan), errors='coerce')


# ===========================================================
# 5. 观测时间 epoch（若不存在，再尝试 MJD）
# ===========================================================
df['epoch_mjd'] = pd.to_numeric(df.get('epoch', np.nan), errors='coerce')
if df['epoch_mjd'].isnull().all() and 'MJD' in df.columns:
    df['epoch_mjd'] = pd.to_numeric(df['MJD'], errors='coerce')


# ===========================================================
# 6. 轨道元素解析（全部为字符串，需要解析数字 + 单位）
# ===========================================================
orbit_string_cols = {
    'orbit_elements_a'  : 'a',
    'orbit_elements_e'  : 'e',
    'orbit_elements_i'  : 'i',
    'orbit_elements_om' : 'Omega',
    'orbit_elements_w'  : 'omega',
    'orbit_elements_ma' : 'M',     # mean anomaly
    'orbit_elements_q'  : 'q',
    'orbit_elements_ad' : 'Q',
    'orbit_elements_per': 'period',
    'orbit_elements_tp' : 'tp',
    'orbit_elements_n'  : 'n'
}

for src, newname in orbit_string_cols.items():
    if src in df.columns:
        df[newname] = df[src].apply(parse_numeric_with_unit)


# ===========================================================
# 7. 绝对星等 H
# ===========================================================
if 'H' in df.columns:
    df['H'] = pd.to_numeric(df['H'], errors='coerce')
elif 'orbit_elements_H' in df.columns:
    df['H'] = pd.to_numeric(df['orbit_elements_H'], errors='coerce')


# ===========================================================
# 8. 将 MPC 预报亮度估计到 g band（简单 color offset）
# ===========================================================
def mpc_pred_to_g(mpc_mag, tax=None, default_offset=0.35,
                  type_offsets={'C':0.20,'S':0.45}):
    mpc_mag = np.array(mpc_mag, dtype=float)
    g = np.full_like(mpc_mag, np.nan)
    mask = np.isfinite(mpc_mag)
    g[mask] = mpc_mag[mask] + default_offset
    if tax is not None:
        for t, off in type_offsets.items():
            idx = mask & (tax == t)
            g[idx] = mpc_mag[idx] + off
    return g

tax_series = df['taxonomy'].astype(str) if 'taxonomy' in df.columns else None
df['mag_mpc_pred_g'] = mpc_pred_to_g(df['mag_mpc_pred_raw'], tax=tax_series)


# ===========================================================
# 9. 构建干净表 df_clean
# ===========================================================
cols_needed = [
    'name','epoch_mjd','ra_obs','dec_obs','mag_obs','mag_obs_err',
    'mag_mpc_pred_raw','mag_mpc_pred_g',
    'a','e','i','Omega','omega','M','q','Q','period','tp','n','H',
    'object_orbit_class_name','object_spkid','object_des'
]

cols_keep = [c for c in cols_needed if c in df.columns]
df_clean = df[cols_keep].copy()

print("Constructed df_clean with columns:")
print(df_clean.columns.tolist())
print(df_clean.head().T)


# ===========================================================
# 10. 对每个小行星计算光度散布 sigma_mag
# ===========================================================
sigma = (
    df_clean.groupby('name')['mag_obs']
    .agg(['count','mean','std'])
    .rename(columns={'mean':'mag_obs_mean','std':'sigma_mag'})
    .reset_index()
)
sigma = sigma[sigma['count'] >= 2]  # 至少 2 次观测才有 sigma
print(f"Computed sigma_mag for {len(sigma)} objects.")
print(sigma.head())


# ===========================================================
# 11. 输出结果
# ===========================================================
df_clean.to_csv("sitian_clean_catalog.csv", index=False)
sigma.to_csv("sigma_mag_from_mag_obs.csv", index=False)

print("Saved sitian_clean_catalog.csv and sigma_mag_from_mag_obs.csv")
# ===========================================================
