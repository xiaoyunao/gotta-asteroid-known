# compute_asteroid_params_horizons_parallel.py
import numpy as np
from astropy.table import Table
from astropy.time import Time
from astroquery.jplhorizons import Horizons

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

# ========== 配置 ==========
INPUT_FITS  = "/Users/yunaoxiao/Desktop/all_asteroids.fits"
OUTPUT_FITS = "/Users/yunaoxiao/Desktop/all_asteroids_new.fits"

XINGLONG_LOC = {"lon": 117.5766, "lat": 40.3925, "elevation": 0.960}

MAX_EPOCHS_PER_CALL = 200

# 并行线程数：别太大，容易触发对方限流
MAX_WORKERS = 6

# 重试参数
RETRIES = 4
SLEEP0 = 0.7          # 初始退避秒数（建议 >=0.5）
JITTER = 0.25         # 抖动幅度（秒）


def make_query_id(num, name):
    if num is np.ma.masked or num is None:
        return str(name).strip()
    try:
        if np.isfinite(num):
            return str(int(num))
    except Exception:
        pass
    s = str(num).strip()
    if s and s.lower() != "nan":
        try:
            return str(int(float(s)))
        except Exception:
            return s
    return str(name).strip()


def get_tobs(row, col_mjd="epoch", col_dateobs="DATEOBS"):
    mjd = row[col_mjd]
    if mjd is not np.ma.masked and np.isfinite(mjd):
        return Time(mjd, format="mjd", scale="utc")
    return Time(str(row[col_dateobs]).strip(), scale="utc")


def round_jd(jd, ndp=6):
    return float(np.round(jd, ndp))


def _query_chunk(obj_id, jds):
    """单次 Horizons ephemerides 调用（不含重试）"""
    h = Horizons(id=obj_id, id_type="smallbody", location=XINGLONG_LOC, epochs=jds)
    eph = h.ephemerides()
    out = {}
    for r in eph:
        jd = round_jd(float(r["datetime_jd"]))
        out[jd] = (
            float(r["r"]),
            float(r["delta"]),
            float(r["alpha"]),
            float(r["RA_rate"]),     # dRA*cosD, arcsec/hour
            float(r["DEC_rate"]),    # arcsec/hour
        )
    return out


def query_horizons_one(obj_id, jd_list):
    """
    对单个目标、多个时刻查询 Horizons ephemerides（含分块+重试）。
    返回 dict: {rounded_jd: (r_AU, delta_AU, alpha_deg, ra_rate_ash, dec_rate_ash)}
    """
    out = {}

    for i0 in range(0, len(jd_list), MAX_EPOCHS_PER_CALL):
        jds = jd_list[i0:i0 + MAX_EPOCHS_PER_CALL]

        last_err = None
        for k in range(RETRIES + 1):
            try:
                out.update(_query_chunk(obj_id, jds))
                last_err = None
                break
            except Exception as e:
                last_err = e
                # 指数退避 + 抖动，避免所有线程同时重试
                sleep = SLEEP0 * (2 ** k) + random.uniform(0, JITTER)
                time.sleep(sleep)

        # 这一块如果最终失败，就继续（该 chunk 的点会缺失，后面回填 nan）
        if last_err is not None:
            # 你也可以在这里 print 更详细信息
            # print(f"[WARN] chunk failed: {obj_id} {len(jds)} epochs err={last_err}")
            pass

    return out


def main():
    t = Table.read(INPUT_FITS)

    # 1) 构造 obj_id + tobs
    obj_ids = [make_query_id(num, name) for num, name in zip(t["number"], t["name"])]
    tobs = [get_tobs(row) for row in t]
    jd_obs = [round_jd(tt.jd) for tt in tobs]

    # 2) 分组：obj_id -> list of jd
    jd_by_id = defaultdict(list)
    for oid, jd in zip(obj_ids, jd_obs):
        jd_by_id[oid].append(jd)

    for oid in jd_by_id:
        jd_by_id[oid] = sorted(set(jd_by_id[oid]))

    n_targets = len(jd_by_id)
    print(f"Total rows={len(t)}, unique targets={n_targets}, MAX_WORKERS={MAX_WORKERS}")

    # 3) 并行查询（按目标）
    results = {}
    failed_targets = set()

    # 为了输出顺序稳定，先把 items 固定成 list
    items = list(jd_by_id.items())

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(query_horizons_one, oid, jds): (oid, len(jds)) for oid, jds in items}
        done = 0
        for fut in as_completed(futs):
            oid, njd = futs[fut]
            done += 1
            try:
                results[oid] = fut.result()
                ok_pts = len(results[oid])
                # 进度条式输出
                if done % 20 == 0 or done == n_targets:
                    dt = time.time() - t0
                    print(f"[{done}/{n_targets}] last={oid} epochs={njd} returned={ok_pts} elapsed={dt:.1f}s")
            except Exception as e:
                results[oid] = {}
                failed_targets.add(oid)
                print(f"[{done}/{n_targets}] FAIL {oid}: {e}")

    if failed_targets:
        print(f"[WARN] {len(failed_targets)} targets failed completely (all epochs missing)")

    # 4) 回填每一行
    r_list = []
    delta_list = []
    phase_list = []
    ang_arcsec_hour_list = []
    ang_deg_day_list = []
    ra_rate_list = []
    dec_rate_list = []
    failed_list = []

    for oid, jd in zip(obj_ids, jd_obs):
        rec = results.get(oid, {}).get(jd, None)
        if rec is None:
            r_list.append(np.nan)
            delta_list.append(np.nan)
            phase_list.append(np.nan)
            ang_arcsec_hour_list.append(np.nan)
            ang_deg_day_list.append(np.nan)
            ra_rate_list.append(np.nan)
            dec_rate_list.append(np.nan)
            failed_list.append(True)
            continue

        r_au, delta_au, alpha_deg, ra_rate_ash, dec_rate_ash = rec
        omega_ash = np.hypot(ra_rate_ash, dec_rate_ash)   # arcsec/hour
        omega_deg_day = omega_ash / 3600.0 * 24.0         # deg/day

        r_list.append(r_au)
        delta_list.append(delta_au)
        phase_list.append(alpha_deg)
        ra_rate_list.append(ra_rate_ash)
        dec_rate_list.append(dec_rate_ash)
        ang_arcsec_hour_list.append(omega_ash)
        ang_deg_day_list.append(omega_deg_day)
        failed_list.append(False)

    # 5) 写列
    t["r_AU"] = r_list
    t["delta_AU"] = delta_list
    t["phase_deg"] = phase_list
    t["RA_rate_arcsec_hour"] = ra_rate_list     # dRA*cosD
    t["DEC_rate_arcsec_hour"] = dec_rate_list
    t["ang_rate_arcsec_hour"] = ang_arcsec_hour_list
    t["ang_rate_deg_day"] = ang_deg_day_list
    t["horizons_failed"] = failed_list

    # ===============================
    # Column descriptions (FITS metadata)
    # ===============================

    t["r_AU"].description = (
        "Heliocentric distance of the asteroid at the observation epoch "
        "(Sun–asteroid distance, computed by JPL Horizons)"
    )
    t["r_AU"].unit = "AU"

    t["delta_AU"].description = (
        "Topocentric distance between the asteroid and the observer at Xinglong Observatory "
        "(observer–asteroid distance)"
    )
    t["delta_AU"].unit = "AU"

    t["phase_deg"].description = (
        "Solar phase angle (Sun–asteroid–observer angle) at the observation epoch"
    )
    t["phase_deg"].unit = "deg"

    t["RA_rate_arcsec_hour"].description = (
        "Apparent rate of change of right ascension multiplied by cos(Dec), "
        "d(RA*cosDec)/dt, from JPL Horizons"
    )
    t["RA_rate_arcsec_hour"].unit = "arcsec/hour"

    t["DEC_rate_arcsec_hour"].description = (
        "Apparent rate of change of declination, dDec/dt, from JPL Horizons"
    )
    t["DEC_rate_arcsec_hour"].unit = "arcsec/hour"

    t["ang_rate_arcsec_hour"].description = (
        "Total apparent angular rate on the sky (proper motion magnitude), "
        "sqrt[(dRA*cosDec/dt)^2 + (dDec/dt)^2]"
    )
    t["ang_rate_arcsec_hour"].unit = "arcsec/hour"

    t["ang_rate_deg_day"].description = (
        "Total apparent angular rate on the sky, converted from arcsec/hour to deg/day"
    )
    t["ang_rate_deg_day"].unit = "deg/day"

    t["horizons_failed"].description = (
        "True if the JPL Horizons query failed for this object and epoch"
    )

    t.write(OUTPUT_FITS, overwrite=True)
    print("Wrote:", OUTPUT_FITS)


if __name__ == "__main__":
    main()
