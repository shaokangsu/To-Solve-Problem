# 积木块 1：导包与读文件（建立通道）
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams['font.sans-serif'] = ['SimHei']   # 使用黑体
plt.rcParams['axes.unicode_minus'] = False     # 正常显示负号
df = pd.read_csv('wind_farm.csv')


# 积木块 2：时间转换与索引（赋予灵魂）
df['time'] = pd.to_datetime(df['time'])  # 把这一列的每个字符串，逐一“翻译”成 Python 内部的时间对象（Timestamp）
df = df.set_index('time')  # 它把 time 这一列从“普通列”提拔为“行索引（index）




# 积木块 3：清洗数据
before = len(df)
df.dropna(inplace=True)  # dropna = drop (删除) + na (Not Available，即空值)；
# inplace=True 的意思是：“直接在原来的 df 上动手删，别复制新的”。删掉的是任何一列包含 NaN 的行。
df = df[(df['wind_speed'] >=0) &
        (df['active_power'] >=0)&(df['active_power'] <=3.0)]  #
after = len(df)
print(f'清洗前{before}行，清洗后{after}行')



# 积木块 4：按天分组求平均
df['date'] = df.index.date  # .date 就能把精确到秒的时间（比如 2026-07-01 00:10:00）裁剪成纯日期（2026-07-01）
daily = df.groupby('date').agg({'wind_speed':'mean','active_power':'mean'})  # 它扫描 date 列，把所有相同日期的行归成一堆。.agg({...})（聚合）：对着刚才的分组，对 wind_speed 列调用 'mean'（平均值），对 active_power 列也调用 'mean'。

daily['daily_energy'] = daily['active_power']*24  # 新增一列，用每日平均功率乘以 24，得到日发电量（MWh）



# 积木块 5：绘图（双轴折线图）
fig,ax1 = plt.subplots()  # 创建一个“画板（fig）”和“左边的主坐标轴（ax1）”。ax1 就像是这个坐标轴的遥控器。
ax1.plot(daily.index,daily['wind_speed'], 'b-', label = '风速')  # daily.index 是所有日期（横坐标）；daily['wind_speed'] 是每天平均风速（纵坐标）；b=蓝色（blue），-=实线。
ax1.set_xlabel('日期')
ax1.set_ylabel('风速(m/s)',color='b')
ax2 = ax1.twinx()  # 创建一个全新的右坐标轴，但它和 ax1 共享同一个 X 轴（日期）。两条曲线可以共用横坐标，但纵坐标刻度完全独立
ax2.plot(daily.index,daily['active_power'], 'r-', label = '功率')  # 在右轴上画红色实线
ax2.set_ylabel('功率(MW)',color='r')
plt.title('日平均风速与有功功率')
fig.tight_layout()  # 自动调整图边距，防止标签被切掉
plt.show()  # 把图画到屏幕上（如果是脚本，会弹出窗口）

# 积木块 6：输出最大值
max_power = daily['active_power'].max()
max_date = daily['active_power'].idxmax()  # idxmax 返回最大值对应的索引（即日期）
print(f'最大日平均功率{max_power:.2f}MW出现在{max_date}')
