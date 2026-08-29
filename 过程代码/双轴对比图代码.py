# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:39:47 2026

@author: wty07
"""
# -*- coding: utf-8 -*-
"""
Python课程作业
双11窗口期百度指数与股价双轴对比分析
功能：筛选38-48周数据，绘制双轴对比图，重点标注第43周
"""

# 导入所需库
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体，解决图表中文显示问题
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 1. 读取合并后的数据集
file_path = r"D:\学校事务\大三下\python课程\week13 pre\周度百度指数_股价_合并表.xlsx"
df = pd.read_excel(file_path)

# 2. 筛选双11窗口期数据：38-48周
df_window = df[(df["周数"] >= 38) & (df["周数"] <= 48)].copy()
# 重置索引，方便绘图
df_window.reset_index(drop=True, inplace=True)

# 输出筛选后的数据信息，用于核对
print("双11窗口期数据信息：")
print(f"数据周数范围：{df_window['周数'].min()} 周 - {df_window['周数'].max()} 周")
print(f"有效数据行数：{len(df_window)}")
print("-" * 60)

# 3. 绘制双轴对比图
# 创建画布与基础坐标轴
fig, ax1 = plt.subplots(figsize=(12, 7), dpi=100)

# 左Y轴：百度指数
color_1 = "#1f77b4"  # 珀莱雅百度指数主色
color_2 = "#2ca02c"  # 上海家化百度指数主色
# 绘制两家公司百度指数折线
line1, = ax1.plot(df_window["周数"], df_window["珀莱雅_百度指数"], 
                   color=color_1, linewidth=2, marker="o", label="珀莱雅-百度指数")
line2, = ax1.plot(df_window["周数"], df_window["上海家化_百度指数"], 
                   color=color_2, linewidth=2, marker="s", label="上海家化-百度指数")
# 左轴设置
ax1.set_xlabel("周数", fontsize=12)
ax1.set_ylabel("周均百度指数", fontsize=12, color="#333333")
ax1.tick_params(axis="y", labelcolor="#333333")
ax1.grid(axis="y", alpha=0.3)
# 设置X轴刻度为周数，保证清晰
ax1.set_xticks(df_window["周数"])

# 右Y轴：股价
ax2 = ax1.twinx()
color_3 = "#ff7f0e"  # 珀莱雅股价主色
color_4 = "#d62728"  # 上海家化股价主色
# 绘制两家公司股价折线
line3, = ax2.plot(df_window["周数"], df_window["珀莱雅_股价"], 
                   color=color_3, linewidth=2, linestyle="--", marker="^", label="珀莱雅-股价")
line4, = ax2.plot(df_window["周数"], df_window["上海家化_股价"], 
                   color=color_4, linewidth=2, linestyle="--", marker="v", label="上海家化-股价")
# 右轴设置
ax2.set_ylabel("周均股价", fontsize=12, color="#333333")
ax2.tick_params(axis="y", labelcolor="#333333")

# 4. 重点标注第43周（双11核心周）
target_week = 43
# 绘制垂直标注线
ax1.axvline(x=target_week, color="#9467bd", linewidth=2.5, linestyle="-.")
# 添加文本标注
ax1.text(target_week + 0.1, ax1.get_ylim()[1] * 0.95, 
         "双11核心周（第43周）", fontsize=11, 
         color="#9467bd", verticalalignment="top")

# 5. 图表标题与图例
plt.title("双11窗口期（38-48周）百度指数与股价双轴对比图", fontsize=14, fontweight="bold")
# 合并两个轴的图例，统一展示
lines = [line1, line2, line3, line4]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize=10)

# 调整布局，避免标签重叠
plt.tight_layout()

# 6. 保存高清图表
save_path = r"D:\学校事务\大三下\python课程\week13 pre\双11窗口期_百度指数_股价双轴对比图.png"
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()

# 程序结束提示
print(f"双11窗口期双轴对比图已成功保存至：\n{save_path}")
print("分析完成")