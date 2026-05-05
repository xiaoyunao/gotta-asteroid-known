from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt

# ===== 1. 读取 FITS 数据 =====
t = Table.read('./matched_asteroids_sbdb_updated.fits')
names = np.unique(t['name'])
print(f"总共有 {len(names)} 颗不同的小行星被观测到。")
# ===== 2. 统计每个小行星的观测次数和时间跨度 =====
obs_counts = []
time_spans = []

for name in names:
    mjds = t['MJD'][t['name'] == name]
    n_obs = len(mjds)
    obs_counts.append(n_obs)
    if n_obs > 1:
        span_hours = (max(mjds) - min(mjds)) * 24
    else:
        span_hours = 0
    time_spans.append(span_hours)

obs_counts = np.array(obs_counts)
time_spans = np.array(time_spans)

min_k = obs_counts.min()
max_k = obs_counts.max()
bins_counts = np.arange(min_k - 0.5, max_k + 0.5 + 1e-8, 1.0)

# ===== 3. 设置字体 =====
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30

# ===== 4. 绘制观测次数分布 =====
plt.figure(figsize=(14, 8))
plt.yscale('log')
plt.hist(obs_counts, bins=bins_counts)
plt.xlabel('Number of Observations')
plt.ylabel('Number of Asteroids')
plt.title('Distribution of Observation Counts')
plt.tight_layout()
plt.savefig('asteroid_observation_counts.png', dpi=300)
plt.show()

# ===== 5. 绘制最长观测间隔分布 =====
plt.figure(figsize=(14, 8))
plt.yscale('log')
plt.hist(time_spans, bins=30, edgecolor='black')
plt.xlabel('Longest Time Span (hours)')
plt.ylabel('Number of Asteroids')
plt.title('Distribution of Observation Time Spans')
plt.tight_layout()
plt.savefig('asteroid_observation_time_spans.png', dpi=300)
plt.show()

# ===== 6. 稳健地筛选并保存观测次数 > 20 的小行星 =====
from astropy.table import Table

# 诊断：查看前几项和 dtype，帮助判断 name 字段是什么格式
print("示例 name 值（前 10）：", t['name'][:10])
print("name dtype:", t['name'].dtype)

# 把所有 name 统一转换为纯 Python str，并去掉前后空白
def to_str(x):
    # 处理 bytes 或 numpy.bytes_，以及普通 str
    if isinstance(x, (bytes, np.bytes_)):
        try:
            return x.decode('utf-8').strip()
        except Exception:
            return x.decode('latin1').strip()
    else:
        return str(x).strip()

name_str = np.array([to_str(x) for x in t['name']])

# 再诊断一下
unique_names, counts = np.unique(name_str, return_counts=True)
print("unique_names (示例前 10):", unique_names[:10])
print("对应 counts (示例前 10):", counts[:10])

# 找出观测次数 > 19 的名字
selected_names = unique_names[counts > 19]
print(f"观测次数 > 19 的小行星数量：{len(selected_names)}")

# 用转换后的 name_str 做 mask（避免类型不匹配）
mask = np.isin(name_str, selected_names)

# 检查 mask 是否工作
n_rows_selected = mask.sum()
print(f"筛选后行数：{n_rows_selected}")

# 如果你还想确认筛选到的 unique name 数量也匹配
print("筛选后不同小行星数：", np.unique(name_str[mask]).size)

# 构造新表并保存
t_selected = t[mask]
if len(t_selected) == 0:
    print("警告：t_selected 为空 —— 请检查上面的诊断输出（dtype / 示例 name）。")
else:
    t_selected.write('asteroids_over19.fits', overwrite=True)
    print("已保存到 asteroids_over19.fits，行数：", len(t_selected))
