# compute_asteroid_params_fits.py
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, GCRS, ITRS, CartesianRepresentation
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric_posvel

from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from poliastro.core.elements import M_to_nu

solar_system_ephemeris.set("builtin")

# ========== 配置 ==========
INPUT_FITS = "./matched_asteroids_sbdb.fits"
OUTPUT_FITS = "asteroids_with_params.fits"

# 兴隆站
xinglong = EarthLocation(lat=40.3925*u.deg, lon=117.5766*u.deg, height=960*u.m)


# ---------- 自动解析带单位的字符串 ----------
def parse_quantity(x, default_unit=None):
    """
    x 可以是:
        float
        int
        "2.65 AU"
        "9.1e-07 deg"
        "0.1234"
    如果没有单位，则使用 default_unit
    """
    if isinstance(x, (float, int, np.floating, np.integer)):
        if default_unit is None:
            raise ValueError("没有 default_unit 不能解析纯数字")
        return x * default_unit

    s = str(x).strip()

    # 包含空格 => 带单位
    if " " in s:
        val_str, unit_str = s.split()
        return float(val_str) * u.Unit(unit_str)

    # 不带单位 => 用默认单位
    if default_unit is None:
        raise ValueError(f"字符串 {s} 不能被解析为 Quantity")
    return float(s) * default_unit


# ----------- 主程序 -----------
tbl = Table.read(INPUT_FITS)

# 轨道根数列（全部 string）
col_e     = "orbit_elements_e"
col_a     = "orbit_elements_a"
col_i     = "orbit_elements_i"
col_Omega = "orbit_elements_om"
col_omega = "orbit_elements_w"
col_M     = "orbit_elements_ma"
col_epoch = "orbit_epoch"     # SBDB 给轨道 epoch

# 观测时间列
col_mjd = "MJD"
col_dateobs = "DATEOBS"

# 输出容器
r_list = []
delta_list = []
phase_list = []
ang_deg_day_list = []
ang_arcsec_hour_list = []

for row in tbl:
    # ---- 解析轨道要素 ----
    a = parse_quantity(row[col_a], default_unit=u.AU)
    e = float(parse_quantity(row[col_e], default_unit=u.one).value)
    inc = parse_quantity(row[col_i], default_unit=u.deg)
    raan = parse_quantity(row[col_Omega], default_unit=u.deg)
    argp = parse_quantity(row[col_omega], default_unit=u.deg)
    M_deg = parse_quantity(row[col_M], default_unit=u.deg)

    # ---- 轨道 epoch ----
    epoch_str = row[col_epoch].strip()
    # SBDB epoch 一般为 JD
    t_epoch = Time(epoch_str, format="jd")

    # ---- 观测时间 ----
    if not np.isnan(row[col_mjd]):
        t_obs = Time(row[col_mjd], format="mjd")
    else:
        t_obs = Time(row[col_dateobs])

    # ---- 求 true anomaly ----
    nu = M_to_nu(M_deg.to(u.rad).value, e) * u.rad

    # ---- 轨道对象（poliastro） ----
    orb_epoch = Orbit.from_classical(Sun, a, e, inc, raan, argp, nu, epoch=t_epoch)

    # ---- propagate ----
    dt = (t_obs - t_epoch).to(u.day)
    orb_obs = orb_epoch.propagate(dt)

    r_ast = orb_obs.r.to(u.AU)
    r_mag = np.linalg.norm(r_ast.xyz.value) * u.AU

    # ---- 观测者位置 ----
    earth_posvel = get_body_barycentric_posvel("earth", t_obs)
    earth_xyz = earth_posvel[0].xyz.to(u.AU).value

    itrs = xinglong.get_itrs(t_obs)
    gcrs = itrs.transform_to(GCRS(obstime=t_obs))
    obs_xyz = gcrs.cartesian.xyz.to(u.AU).value

    obs_bary = earth_xyz + obs_xyz

    # ---- delta ----
    delta_vec = r_ast.xyz.value - obs_bary
    delta_mag = np.linalg.norm(delta_vec) * u.AU

    # ---- phase angle ----
    cos_alpha = np.dot(r_ast.xyz.value, delta_vec) / (np.linalg.norm(r_ast.xyz.value) * np.linalg.norm(delta_vec))
    cos_alpha = np.clip(cos_alpha, -1, 1)
    phase = np.arccos(cos_alpha) * u.rad
    phase_deg = phase.to(u.deg)

    # ---- angular rate via finite difference ----
    dt_small = 1 * u.minute

    def pos_at(t):
        orb = orb_epoch.propagate((t - t_epoch).to(u.day))
        r = orb.r.to(u.AU).xyz.value
        earth = get_body_barycentric_posvel("earth", t)[0].xyz.to(u.AU).value
        it = xinglong.get_itrs(t).transform_to(GCRS(obstime=t)).cartesian.xyz.to(u.AU).value
        return r - (earth + it)

    vec_p = pos_at(t_obs + dt_small)
    vec_m = pos_at(t_obs - dt_small)

    coord_p = SkyCoord(CartesianRepresentation(vec_p * u.AU), frame="icrs")
    coord_m = SkyCoord(CartesianRepresentation(vec_m * u.AU), frame="icrs")

    ra_p, dec_p = coord_p.ra.deg, coord_p.dec.deg
    ra_m, dec_m = coord_m.ra.deg, coord_m.dec.deg

    dra = ra_p - ra_m
    if dra > 180: dra -= 360
    if dra < -180: dra += 360

    ddec = dec_p - dec_m
    dt_day = (2 * dt_small).to(u.day).value

    dra_dt = dra / dt_day
    ddec_dt = ddec / dt_day

    omega_deg_day = np.sqrt((dra_dt * np.cos(np.deg2rad((dec_p+dec_m)/2)))**2 + ddec_dt**2)
    omega_arcsec_hour = omega_deg_day * 3600 / 24

    # ---- append ----
    r_list.append(r_mag.value)
    delta_list.append(delta_mag.value)
    phase_list.append(phase_deg.value)
    ang_deg_day_list.append(omega_deg_day)
    ang_arcsec_hour_list.append(omega_arcsec_hour)


# ----- 添加列写回 FITS -----
tbl["r_AU"] = r_list
tbl["delta_AU"] = delta_list
tbl["phase_deg"] = phase_list
tbl["ang_rate_deg_day"] = ang_deg_day_list
tbl["ang_rate_arcsec_hour"] = ang_arcsec_hour_list

tbl.write(OUTPUT_FITS, overwrite=True)
print("Wrote:", OUTPUT_FITS)
