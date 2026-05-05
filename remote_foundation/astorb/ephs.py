from aleph.Query import Query
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time
from astropy import units as u
from astropy.io import fits
from glob import glob
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
import sys
from convenience_functions import show_image_pos
import matplotlib.pyplot as plt

if len(sys.argv) < 1:
    print('Usage: python ephs.py fits_path [lon] [lat] [height] [njobs]\n')
    exit(-1)

filename = '/Volumes/Foundation/Asteroid/astorb/astorb.dat'
q = Query(service='Lowell', filename=filename)

try:
    path = sys.argv[1]
    files = glob(f'{path}/*.fits')
except:
    path = '/Volumes/Foundation/Asteroid/test'
    files = glob(f'{path}/*.fits')
    
try:
    njobs = int(sys.argv[2])
except:
    njobs = 1

try:
    lon = float(sys.argv[3])
    lat = float(sys.argv[4])
    height = float(sys.argv[5])
    observer = EarthLocation(lon=lon*u.deg, lat=lat*u.deg, height=height*u.m)
except:
    lon = 117.575
    lat = 40.393
    height = 960
    observer = EarthLocation(lon=lon*u.deg, lat=lat*u.deg, height=height*u.m)


for i in files:
    hdul=fits.open(i)
    header=hdul[0].header
    naxis1=header['NAXIS1']
    naxis2=header['NAXIS2'] 
    exptime=float(header['EXPTIME'])/86400
    try:
        # date=header['DATE-OBS']
        # time=header['TIME-OBS']
        # epoch=Time(f'{date}T{time}',format='isot',scale='utc')
        epoch=Time(header['DATE-OBS'],format='isot',scale='utc')+exptime/2
    except:
        mjd=float(header['MJD-OBS'])-0.75+exptime/2
        epoch=Time(mjd,format='mjd',scale='utc')
    ra=header['OBJ_RA']
    dec=header['OBJ_DEC']
    ra = sum(float(x) / 60 ** i for i, x in enumerate(ra.split(':'))) * 15
    dec = sum(float(x) / 60 ** i for i, x in enumerate(dec.split(':')))
    field_center=SkyCoord(ra*u.deg,dec*u.deg)
    w = WCS(header)
    pixel_scales = proj_plane_pixel_scales(w)
    pixelscale=(pixel_scales[0]+pixel_scales[1])/2
    field_radius=2 * pixelscale * header['NAXIS1'] / 2*u.deg
    ephs = q.query_mixed_cat(field_center, field_radius, epoch=epoch, observer=observer, njobs=njobs, method='nbody')
    x,y=w.world_to_pixel_values(ephs['ra'],ephs['dec'])
    idx=(x>0)*(x<naxis1)*(y>0)*(y<naxis2)
    ephs=ephs[idx]
    x=x[idx]
    y=y[idx]
    ephs.write(f'{i}.ecsv',overwrite=True)
    show_image_pos(hdul[0].data,x1=x,y1=y,figsize=(15,15))
    for idxx,j in enumerate(ephs):
        v=j['V']
        number=j['number']
        name=j['name']
        plt.text(x[idxx],y[idxx],f'{v:.1f}',color='b')
    plt.savefig(f'{i}.png',dpi=300)
