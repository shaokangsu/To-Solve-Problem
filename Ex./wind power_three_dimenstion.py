import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from _pytest import mark
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取原始数据
input_file = 'wind_farm_cleaned.csv'  # 原始文件
df = pd.read_csv(input_file, parse_dates=['time'], index_col='time')
df.sort_index(inplace=True)  # 将当前数据表，严格按照时间索引（从早到晚）重新排序

# 2. 清洗
df.dropna(subset=['wind_speed', 'active_power'], inplace=True)
df = df[(df['wind_speed'] >= 0) & (df['active_power'] >= 0) & (df['active_power'] <= 3.0)]

# 3. 按天聚合
daily = df.resample('D').agg({'wind_speed': 'mean', 'active_power': 'mean'}).dropna()
daily['energy_mwh'] = daily['active_power'] * 24

# 现在 daily 有四列？不，只有三列：wind_speed, active_power, energy_mwh。索引是time。这符合表头 time,wind_speed,active_power,energy_mwh。

# 4. 三维图
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 将时间索引转换为数值，便于绘图（例如从0开始的天数）
x = np.arange(len(daily))  # 或者用 (daily.index - daily.index[0]).days
y = daily['wind_speed']
z = daily['active_power']
c = daily['energy_mwh']

# 绘制三维曲线，颜色映射能量
sc = ax.scatter(x, y, z, c=c, cmap='viridis', s=80, label='数据点')
ax.plot(x, y, z, color='tab:gray',alpha=0.5, linewidth=0.8)

# 设置坐标轴标签
ax.set_xlabel('时间 (天)',labelpad=10)
ax.set_ylabel('日平均风速 (m/s)')
ax.set_zlabel('日平均有功功率 (MW)')

# 添加颜色条
cbar = fig.colorbar(sc, ax=ax, shrink=0.5, pad=0.1)  # 指定颜色条与哪个坐标轴对齐；缩放颜色条的长度
cbar.set_label('日发电量 (MWh)')

# 设置X轴刻度标签为实际日期（可选）
# 将x轴刻度设置为日期
ticks = np.arange(0, len(daily), max(1, len(daily)//6))  # 选择一些刻度，生成一个等差数列，从 0 开始，不超过 len(daily)-1，步长为 max(1, len(daily)//10)
ax.set_xticks(ticks)
ax.set_xticklabels([daily.index[i].strftime('%m-%d') for i in ticks], rotation=45)  # 将标签旋转 45 度，避免标签过长时相互重叠

plt.title('风电场日平均风速、有功功率与发电量三维图')
fig.savefig('wind_3d.png', dpi=300, bbox_inches='tight')
plt.show()