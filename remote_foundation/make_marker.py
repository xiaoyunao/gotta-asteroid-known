import numpy as np
from astropy.io import fits
from astropy.visualization import ZScaleInterval
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from reproject import reproject_interp
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from astropy.table import Table
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, ConnectionPatch
from astropy.time import Time
import os
import re
import warnings
warnings.filterwarnings("ignore", category=UserWarning, append=True)

# ============================================================
# 字体设置
# ============================================================
font = {'family': 'Times New Roman', 'size': 15, 'weight': 'bold'}
plt.rc('font', **font)

# ============================================================
# 参数
# ============================================================
fits_dir = "./MP_0949/"
png_dir = "./MP_0949_png/"
os.makedirs(png_dir, exist_ok=True)
dpi = 150

# 主图空心十字样式（你可自己调）
cross_len = 100
inset_gap = 35
marker_lw = 1.5

# cutout 内空心十字样式（你可自己调）
cut_cross_len = 25
cut_inset_gap = 10
cut_marker_lw = 2.0

text_alpha = 0.8      # 主图文字透明度，防重叠
edge_pad = 10          # 离边界多少像素就认为“贴边”

# 文字标注偏移（像素）
text_dx = 30
text_dy = 20

# cutout 大小
cutout_size = 250  # pixel（125*125）

# ============================================================
# 你只需要改这里：只输入三颗小行星的 name（要与表 mp_table['name'] 完全一致）
# 例如 '(99942) Apophis' 这种
# ============================================================
target_names = [
    '2000 RF33',
    '1999 XJ90',
    '2002 GV125',
]

# ============================================================
# 工具函数
# ============================================================
def format_name(name: str) -> str:
    if name is None:
        return ""
    s = str(name).strip()
    s = re.sub(r'^\((\d+)\)\s*', r'\1 ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_cutout_fixed(data, x, y, size, fill=np.nan):
    """
    永远返回 (size, size) 的 cutout；超出原图的部分用 fill 补齐。
    同时返回：原图中 cutout 左下角对应的 (x_left, y_bottom)，用于坐标换算。
    """
    half = size // 2
    x = int(round(x))
    y = int(round(y))

    # 原图中想要的范围
    x1 = x - half
    x2 = x + half
    y1 = y - half
    y2 = y + half

    # 与原图的交集
    xs1 = max(0, x1)
    xs2 = min(data.shape[1], x2)
    ys1 = max(0, y1)
    ys2 = min(data.shape[0], y2)

    # 在 cutout 内要放到哪里
    cx1 = xs1 - x1
    cx2 = cx1 + (xs2 - xs1)
    cy1 = ys1 - y1
    cy2 = cy1 + (ys2 - ys1)

    cut = np.full((size, size), fill, dtype=float)
    if xs2 > xs1 and ys2 > ys1:
        cut[cy1:cy2, cx1:cx2] = data[ys1:ys2, xs1:xs2]

    # 这里返回的是“理想 cutout 的左下角”在原图坐标系下的位置（即 x1,y1）
    return cut, x1, y1

def draw_hollow_cross(ax, x, y, color, L, gap, lw=1.2):
    ax.plot([x - L, x - gap], [y, y], color=color, lw=lw)
    ax.plot([x + gap, x + L], [y, y], color=color, lw=lw)
    ax.plot([x, x], [y - L, y - gap], color=color, lw=lw)
    ax.plot([x, x], [y + gap, y + L], color=color, lw=lw)

def parse_night_key(date_str: str) -> str:
    """
    把 header 里的 DATE/DATE-OBS 变成 "YYYY-MM-DD" 作为“同一晚”分组 key。
    """
    if date_str is None:
        return "UNKNOWN"
    s = str(date_str).strip()
    # 常见：'YYYY-MM-DD', 'YYYY-MM-DDThh:mm:ss', 'YYYY-MM-DD hh:mm:ss'
    s2 = s.replace(' ', 'T')
    try:
        t = Time(s2, format='isot', scale='utc')
        return t.to_datetime().date().isoformat()
    except Exception:
        # 兜底：截前10位
        return s[:10] if len(s) >= 10 else s

# ============================================================
# 读取小行星匹配表
# ============================================================
matched_table = Table.read("./asteroids_over14.fits")

mask = [sf.startswith("OBJ_MP_0949_") for sf in matched_table['source_file']]
mp_table = matched_table[mask]

mp_table['fits_file'] = [f.replace("_cat.fits.gz", ".fits.gz") for f in mp_table['source_file']]

# exposure 按 MJD 排序（每个 fits_file 取最小 MJD）
exposure_table = mp_table.group_by('fits_file').groups.aggregate(np.min)
exposure_table.sort('MJD')
exposure_files_sorted = list(exposure_table['fits_file'])

# 颜色映射（按 mp_table 里出现过的 name）
unique_names = np.unique(mp_table['name'])
colors = plt.cm.hsv(np.linspace(0, 1, len(unique_names)))
name_color = {name: to_hex(colors[i]) for i, name in enumerate(unique_names)}

# ============================================================
# 读取 reference frame
# ============================================================
ref_fits = exposure_files_sorted[0]
with fits.open(os.path.join(fits_dir, ref_fits)) as hdul:
    ref_data = hdul[1].data.astype(float)
    ref_wcs = WCS(hdul[1].header)
ref_shape = ref_data.shape

# ============================================================
# 预扫：为每个 fits_file 读取 night_key（只读 header，不做重投影）
# ============================================================
fits_to_night = {}
fits_to_dateobs = {}

for fits_file in exposure_files_sorted:
    fits_path = os.path.join(fits_dir, fits_file)
    if not os.path.exists(fits_path):
        fits_to_night[fits_file] = "MISSING"
        fits_to_dateobs[fits_file] = "MISSING"
        continue
    with fits.open(fits_path) as hdul:
        hdr = hdul[1].header
        date_obs = hdr.get('DATE-OBS', hdr.get('DATE', 'UNKNOWN'))
    fits_to_dateobs[fits_file] = date_obs
    fits_to_night[fits_file] = parse_night_key(date_obs)

# ============================================================
# 为每一晚、每个目标小行星，确定 cutout 中心：
# 取“当晚最早能找到该小行星的那一帧”在 reference frame 下的像素位置
# ============================================================
# night -> list of fits_files (按时间顺序)
night_to_files = {}
for f in exposure_files_sorted:
    nk = fits_to_night.get(f, "UNKNOWN")
    night_to_files.setdefault(nk, []).append(f)

# centers[(night_key, name)] = (x_ref, y_ref)
centers = {}

for night_key, file_list in night_to_files.items():
    if night_key in ("MISSING", "UNKNOWN"):
        continue

    for name in target_names:
        found = False

        # 从当晚最早帧开始往后找，直到这颗小行星在 mp_table 里出现
        for fits_file in file_list:
            rows = mp_table[(mp_table['fits_file'] == fits_file) & (mp_table['name'] == name)]
            if len(rows) == 0:
                continue

            fits_path = os.path.join(fits_dir, fits_file)
            if not os.path.exists(fits_path):
                continue

            with fits.open(fits_path) as hdul:
                wcs = WCS(hdul[1].header)

            # 用这一帧里第一条该小行星记录
            row = rows[0]
            x0, y0 = row['X_Win'], row['Y_Win']
            sky = wcs.pixel_to_world(x0, y0)
            xr, yr = ref_wcs.world_to_pixel(sky)

            centers[(night_key, name)] = (float(xr), float(yr))
            found = True
            break

        if not found:
            # 这一晚没找到这颗小行星，就不画它的 cutout（该晚）
            pass

# ============================================================
# 逐帧绘图
# ============================================================
for i, fits_file in enumerate(exposure_files_sorted):
    print(f"Processing {fits_file} ({i+1}/{len(exposure_files_sorted)})")

    fits_path = os.path.join(fits_dir, fits_file)
    if not os.path.exists(fits_path):
        print(f"  Missing {fits_path}")
        continue

    night_key = fits_to_night.get(fits_file, "UNKNOWN")

    with fits.open(fits_path) as hdul:
        data = hdul[1].data.astype(float)
        wcs = WCS(hdul[1].header)
        date_obs = fits_to_dateobs.get(fits_file, hdul[1].header.get('DATE-OBS', hdul[1].header.get('DATE', 'UNKNOWN')))

    # ---------- reproject 到 reference frame ----------
    img_data, _ = reproject_interp((data, wcs), ref_wcs, shape_out=ref_shape)

    vmin, vmax = ZScaleInterval().get_limits(img_data)
    rows_all = mp_table[mp_table['fits_file'] == fits_file]

    # ========================================================
    # Figure & layout：主图(9x9) + 右侧3个(3x3) 无缝拼接
    # ========================================================
    fig = plt.figure(figsize=(12, 9), dpi=dpi)
    gs = GridSpec(
        3, 2,
        width_ratios=[9, 3],
        height_ratios=[3, 3, 3],
        wspace=0.0,
        hspace=0.0
    )
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)

    # ---------- 主图 ----------
    ax = fig.add_subplot(gs[:, 0])
    ax.imshow(img_data, origin='lower', cmap='gray', vmin=vmin, vmax=vmax)
    ax.axis('off')

    # ---------- 主图：小行星空心十字 + 同色文字 ----------
    for row in rows_all:
        nm = row['name']
        c = name_color.get(nm, "yellow")

        sky = wcs.pixel_to_world(row['X_Win'], row['Y_Win'])
        x, y = ref_wcs.world_to_pixel(sky)

        draw_hollow_cross(ax, x, y, c, L=cross_len, gap=inset_gap, lw=marker_lw)

        label = format_name(nm)

        # 默认放右上
        tx = x + text_dx
        ty = y + text_dy
        ha = 'left'

        # 如果右侧会出界，就放到左侧（并右对齐）
        if tx > (ref_shape[1] - edge_pad):
            tx = x - text_dx
            ha = 'right'

        ax.text(
            tx, ty, label,
            color=c, fontsize=15,
            ha=ha, va='bottom',
            alpha=text_alpha
        )

    # ---------- 正北箭头 ----------
    x0 = ref_shape[1] * 0.85
    y0 = ref_shape[0] * 0.88
    sky0 = ref_wcs.pixel_to_world(x0, y0)
    sky_north = SkyCoord(ra=sky0.ra, dec=sky0.dec + 1000 * u.arcsec, frame=sky0.frame)
    x1, y1 = ref_wcs.world_to_pixel(sky_north)

    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='red', lw=1.5))
    ax.text(x0 - 200, y0 + 100, 'N', color='red', fontsize=20, ha='center', va='top')

    # ---------- 日期 ----------
    ax.text(0.5, 0.02, f"{date_obs}", color='yellow', fontsize=15,
            transform=ax.transAxes, va='bottom', ha='center',
            bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

    # ========================================================
    # 右侧 cutouts：同一晚用 centers[(night, name)] 固定中心；跨夜自动换
    # 只在 cutout 里画“给定 name”的 marker；若该帧跑出 cutout 则不画
    # ========================================================
    for j, name in enumerate(target_names):
        axc = fig.add_subplot(gs[j, 1])
        axc.axis('off')

        key = (night_key, name)
        if key not in centers:
            # 这晚找不到该小行星的中心 => 这一格空着
            continue

        cx, cy = centers[key]
        c = name_color.get(name, "yellow")

        cut_img, x_left, y_bottom = extract_cutout_fixed(img_data, cx, cy, cutout_size, fill=np.nan)
        if cut_img.size == 0:
            continue

        vmin_c, vmax_c = ZScaleInterval().get_limits(cut_img[np.isfinite(cut_img)])
        axc.imshow(cut_img, origin='lower', cmap='gray', vmin=vmin_c, vmax=vmax_c)

        # 标题
        axc.text(0.5, 0.9, format_name(name),
                 transform=axc.transAxes, ha='center', va='top',
                 fontsize=11, color='yellow',
                 bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

        # ---- cutout 内 marker：只画这颗 name，且必须在 cutout 范围内 ----
        rows_target = rows_all[rows_all['name'] == name]
        for row in rows_target:
            sky = wcs.pixel_to_world(row['X_Win'], row['Y_Win'])
            xr, yr = ref_wcs.world_to_pixel(sky)

            xc = xr - x_left
            yc = yr - y_bottom

            # 这一步确保：跑出 cutout 就不画
            if 0 <= xc < cut_img.shape[1] and 0 <= yc < cut_img.shape[0]:
                draw_hollow_cross(axc, xc, yc, c,
                                  L=cut_cross_len, gap=cut_inset_gap, lw=cut_marker_lw)

        # ---- 主图框 + 虚线连接（右上角 & 左下角），右侧不画框 ----
        half = cutout_size / 2.0

        # 主图上的 cutout 框仍然画
        rect_main = Rectangle(
            (cx - half, cy - half), cutout_size, cutout_size,
            fill=False, edgecolor=c, linewidth=1.5
        )
        ax.add_patch(rect_main)

        # 角点：主图框（TR/BL）
        main_tr = (cx + half, cy + half)
        main_bl = (cx - half, cy - half)

        # 角点：右侧 cutout 图像角（TR/BL）
        h, w_ = cut_img.shape
        cut_tr = (w_, h)
        cut_bl = (0, 0)

        # 连接虚线：TR->TR, BL->BL
        con1 = ConnectionPatch(
            xyA=main_tr, coordsA=ax.transData,
            xyB=cut_tr,  coordsB=axc.transData,
            linestyle='--', linewidth=1.2, color=c
        )
        con2 = ConnectionPatch(
            xyA=main_bl, coordsA=ax.transData,
            xyB=cut_bl,  coordsB=axc.transData,
            linestyle='--', linewidth=1.2, color=c
        )
        fig.add_artist(con1)
        fig.add_artist(con2)

    # ---------- 保存 ----------
    png_name = f"{i+1:02d}.png"
    out_path = os.path.join(png_dir, png_name)
    fig.savefig(out_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

print(f"所有帧 PNG 已生成到 {png_dir}")
