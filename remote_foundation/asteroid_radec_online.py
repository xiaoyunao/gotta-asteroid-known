import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation
from astroquery.jplhorizons import Horizons
from astropy import units as u

# ============================================================
# 1. 高级接口：调用 JPL Horizons 获取轨迹
# ============================================================

def get_asteroid_radec_jpl(name, t_start, t_end, n_points=100, observer="@earth"):
    """
    直接使用 JPL Horizons API 计算小行星的 RA/Dec。
    
    Parameters
    ----------
    name : str
        小行星名称或 Horizons ID
    t_start : astropy.time.Time
        起始时间
    t_end : astropy.time.Time
        结束时间
    n_points : int
        时间采样点数
    observer : str
        观测点代码，如 '@earth' 或 EarthLocation 对象
        
    Returns
    -------
    epochs : astropy.time.Time
        时间数组
    ra : np.ndarray
        赤经 (deg)
    dec : np.ndarray
        赤纬 (deg)
    """
    # 构造时间列表
    epochs = Time(
        np.linspace(t_start.tdb.mjd, t_end.tdb.mjd, n_points),
        format="mjd", scale="tdb"
    )

    # Horizons 对象
    obj = Horizons(
        id=name,
        location=observer if isinstance(observer, str) else "@399",  # 399=地球
        epochs=epochs.tdb.jd,
        id_type="majorbody"  # 小行星用 "smallbody" 也可以
    )

    # 请求视位置
    eph = obj.ephemerides(
        quantities=[1, 3],  # 1=RA/Dec, 3=range等
        extra_precision=True
    )

    ra = eph["RA"]  # deg
    dec = eph["DEC"]  # deg

    return epochs, np.array(ra), np.array(dec)

# ============================================================
# 2. 示例使用
# ============================================================

if __name__ == "__main__":
    # 观测点
    observer = EarthLocation.of_site("greenwich")  # 可以改为其他地面观测站
    
    # 起止时间
    t_start = Time("2025-12-21T00:00:00", scale="tdb")
    t_end = Time("2025-12-22T00:00:00", scale="tdb")
    
    # 小行星名称
    asteroid_name = "Ceres"
    
    # 计算轨迹
    epochs, ra, dec = get_asteroid_radec_jpl(asteroid_name, t_start, t_end, n_points=50, observer="@earth")
    
    # 输出结果
    for t, r, d in zip(epochs, ra, dec):
        print(t.iso, f"{r:.6f} deg", f"{d:.6f} deg")
