import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['SimHei']   # 使用黑体
plt.rcParams['axes.unicode_minus'] = False     # 正常显示负号，负号别乱转义



# 1. 读取并解析时间
input_file = 'wind_farm.csv'
df = pd.read_csv(input_file, parse_dates=['time'], index_col='time')
df.sort_index(inplace=True)



# 2. 记录清洗前数量
original_len = len(df)

df.dropna(subset=['wind_speed', 'active_power'], inplace=True)

df = df[(df['wind_speed'] >= 0) & (df['active_power'] >= 0) & (df['active_power'] <= 3.0)]

cleaned_len = len(df)
print(f"清洗前：{original_len} 行，清洗后：{cleaned_len} 行，剔除 {original_len - cleaned_len} 行")



# 新数据存储到新文件
output_file = 'wind_farm_cleaned.csv'
df.to_csv(output_file, encoding='utf-8-sig')  # to_csv：把当前内存中的 df（DataFrame）完整写入硬盘文件；encoding='utf-8-sig' 是为了让 Excel 打开时不乱码。
print(f"清洗后的 {cleaned_len} 行数据已经保存为新的文件：{output_file}")


# 3. 按天聚合（使用 resample 更稳健）
# 先按天重采样，计算每日均值（自动处理缺失，但我们已经剔除，所以没问题）
daily = (df.resample('D'). # resample('D') 会按“天（Day）”对行进行分组；执行后，返回的类型是：pandas.core.resample.Resampler（一个分组器对象，还没计算）
         agg({'wind_speed': 'mean','active_power': 'mean'}).  # 它对每天的所有 wind_speed 求平均，对 active_power 求平均。结束后类型再变回原本的
         dropna())


# 计算日发电量（MWh）并输入数据
daily['energy_mwh'] = daily['active_power'] * 24
daily.to_csv('wind_farm_cleaned.csv', encoding='utf-8-sig')




# 4. 绘图
fig, ax1 = plt.subplots(figsize=(12, 6))
color1 = 'tab:blue'
ax1.set_xlabel('日期')
ax1.set_ylabel('日平均风速 (m/s)', color=color1)
ax1.plot(daily.index, daily['wind_speed'], marker='o', linestyle='-', color=color1, label='风速')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('日平均有功功率 (MW)', color=color2)
ax2.plot(daily.index, daily['active_power'], marker='s', linestyle='--', color=color2, label='功率')
ax2.tick_params(axis='y', labelcolor=color2)

# 添加图例（手动合并）
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('2026年7月风电场日平均风速与有功功率变化')
fig.tight_layout()
fig.savefig('filename.png', dpi=300, bbox_inches='tight')
plt.show()



# 5. 统计最大值
max_power = daily['active_power'].max()
max_date = daily['active_power'].idxmax()
print(f"清洗后，日平均有功功率最大值为 {max_power:.3f} MW，发生在 {max_date.strftime('%Y-%m-%d')}")



# 解释语句
print("\n" + "="*60)
print(f"原本打开的 '{input_file}' 不做改变")
print(f"过滤后文件：【{output_file}】。")
print("="*60 + "\n")
