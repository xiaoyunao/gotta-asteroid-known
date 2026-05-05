import numpy as np
import rebound
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, get_body_barycentric_posvel, solar_system_ephemeris
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.bodies import Sun

# ============================================================
# 1. 读取 astorb.dat
# ============================================================

def getfl(s):
    try:
        return float(s)
    except ValueError:
        return np.nan

def unpack_epoch(epoch_str, source="astorb"):
    try:
        mjd = float(epoch_str)
        return Time(mjd, format="mjd", scale="tdb").jd
    except ValueError:
        return np.nan

def read_astorb(astorb_file, asteroid_name, source="astorb"):
    with open(astorb_file, "r") as f:
        for s in f:
            if s.startswith("#"):
                continue
            name = s[7:25].strip()
            if name != asteroid_name:
                continue
            e = getfl(s[158:168])
            a = getfl(s[168:181])
            incl = getfl(s[147:157])
            raan = getfl(s[137:147])
            argp = getfl(s[126:136])
            M = getfl(s[115:125])
            epoch = unpack_epoch(s[106:114], source=source)
            return dict(
                a=a,
                e=e,
                inc=incl,
                raan=raan,
                argp=argp,
                M=M,
                epoch=epoch
            )
    raise ValueError(f"Asteroid '{asteroid_name}' not found in astorb.dat")

# ============================================================
# 2. 将轨道根数转 Cartesian 状态
# ============================================================

def elements_to_state(elements):
    epoch = Time(elements["epoch"], format="jd", scale="tdb")
    orb = Orbit.from_classical(
        Sun,
        elements["a"] * u.AU,
        elements["e"] * u.one,
        elements["inc"] * u.deg,
        elements["raan"] * u.deg,
        elements["argp"] * u.deg,
        elements["M"] * u.deg,
        epoch=epoch
    )
    r = orb.r.to(u.au).value
    v = orb.v.to(u.au / u.day).value
    return np.hstack([r, v])

# ============================================================
# 3. 太阳系状态
# ============================================================

def get_SS_states(epoch):
    planets = ["mercury","venus","earth-moon-barycenter","mars","jupiter","saturn","uranus","neptune"]
    sun_pos, sun_vel = get_body_barycentric_posvel("sun", epoch)
    sun_state = np.array([sun_pos.x.value, sun_pos.y.value, sun_pos.z.value,
                          sun_vel.x.to(u.au/u.day).value,
                          sun_vel.y.to(u.au/u.day).value,
                          sun_vel.z.to(u.au/u.day).value])
    states = [sun_state]
    for p in planets:
        pos, vel = get_body_barycentric_posvel(p, epoch)
        pos = pos - sun_pos
        vel = vel - sun_vel
        states.append(np.array([pos.x.value,pos.y.value,pos.z.value,
                                vel.x.to(u.au/u.day).value,
                                vel.y.to(u.au/u.day).value,
                                vel.z.to(u.au/u.day).value]))
    return np.array(states)

# ============================================================
# 4. N-body 积分 + RA/Dec 计算
# ============================================================

au_to_d = (1 * u.au / (3e8 * u.m / u.s)).to(u.day).value
solar_system_ephemeris.set('/Volumes/Foundation/Asteroid/de442s.bsp')

def asteroid_radec_nbody(elements, epochs, observer):
    state_ast = elements_to_state(elements)
    ss_states = get_SS_states(Time(elements["epoch"], format="jd", scale="tdb"))
    
    sim = rebound.Simulation()
    sim.units = ('d','AU','Msun')
    masses = [1, 1.6601141530543488e-07, 2.4478382877847715e-06, 3.040432648022642e-06,
              3.2271560375549977e-07, 0.0009547919152112404, 0.0002858856727222417,
              4.36624373583127e-05, 5.151383772628674e-05]
    for i, st in enumerate(ss_states):
        sim.add(m=masses[i], x=st[0], y=st[1], z=st[2],
                vx=st[3], vy=st[4], vz=st[5])
    sim.add(x=state_ast[0], y=state_ast[1], z=state_ast[2],
            vx=state_ast[3], vy=state_ast[4], vz=state_ast[5])
    
    ra_list = []
    dec_list = []
    for t in epochs:
        delta_t = (t - Time(elements["epoch"], format="jd", scale="tdb")).to(u.day).value
        sim.integrate(delta_t)
        obs_pos, _ = get_body_barycentric_posvel("earth", t)
        obsx, obsy, obsz = obs_pos.x.value, obs_pos.y.value, obs_pos.z.value
        ast = sim.particles[-1]
        sun = sim.particles[0]
        
        # 光行差修正
        gdist = np.sqrt((ast.x-sun.x-obsx)**2 + (ast.y-sun.y-obsy)**2 + (ast.z-sun.z-obsz)**2)
        lighttime = gdist * au_to_d
        t_corr = delta_t - lighttime
        sim.integrate(t_corr)
        ast = sim.particles[-1]
        
        x_geo = ast.x - sun.x - obsx
        y_geo = ast.y - sun.y - obsy
        z_geo = ast.z - sun.z - obsz
        
        ra = np.arctan2(y_geo, x_geo)
        dec = np.arctan2(z_geo, np.sqrt(x_geo**2 + y_geo**2))
        if ra < 0: ra += 2*np.pi
        
        ra_list.append(ra * u.rad)
        dec_list.append(dec * u.rad)
    
    return np.array(ra_list), np.array(dec_list)

# ============================================================
# 5. 高级接口：计算轨迹
# ============================================================

def compute_trajectory(astorb_file, asteroid_name, observer, t_start, t_end, n_points=1000):
    elements = read_astorb(astorb_file, asteroid_name)
    epochs = Time(np.linspace(t_start.mjd, t_end.mjd, n_points), format="mjd", scale="utc")
    ra, dec = asteroid_radec_nbody(elements, epochs, observer)
    return epochs, ra, dec

# ============================================================
# 示例使用
# ============================================================
if __name__ == "__main__":
    observer = EarthLocation.of_site('greenwich')
    t_start = Time('2025-12-21T00:00:00', scale='tdb')
    t_end = Time('2025-12-22T00:00:00', scale='tdb')
    astorb_file = '/Volumes/Foundation/Asteroid/astorb/astorb.dat'
    asteroid_name = 'Ceres'
    
    epochs, ra, dec = compute_trajectory(astorb_file, asteroid_name, observer, t_start, t_end, n_points=50)
    
    for t, r, d in zip(epochs, ra, dec):
        print(t.iso, r.to(u.deg), d.to(u.deg))
