# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:28:04 2026

@author: wty07
"""

# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

file_path = r"D:\学校事务\大三下\python课程\week13 pre\周度百度指数_股价_合并表.xlsx"
df = pd.read_excel(file_path)

print("数据基本信息：")
print("数据行数：", len(df))
print("数据列名：", list(df.columns))
print("-" * 60)

x1 = df["珀莱雅_百度指数"]
y1 = df["珀莱雅_股价"]
corr1, p_value1 = stats.pearsonr(x1, y1)

x2 = df["上海家化_百度指数"]
y2 = df["上海家化_股价"]
corr2, p_value2 = stats.pearsonr(x2, y2)

print("珀莱雅周均百度指数与股价相关性分析结果")
print(f"Pearson相关系数(r值)：{corr1:.4f}")
print(f"P值：{p_value1:.4f}")
print("-" * 60)

print("上海家化周均百度指数与股价相关性分析结果")
print(f"Pearson相关系数(r值)：{corr2:.4f}")
print(f"P值：{p_value2:.4f}")
print("-" * 60)

plt.figure(figsize=(10, 6))
#绘制散点
plt.scatter(x1, y1, color="steelblue", alpha=0.7, label="观测点")
#计算线性拟合参数
slope1, intercept1, r_value1, p_val1, std_err1 = stats.linregress(x1, y1)
# 生成拟合直线数据
line1 = slope1 * x1 + intercept1
# 绘制趋势线
plt.plot(x1, line1, color="darkred", linewidth=2, label="趋势线")
# 设置图表标题与坐标轴
plt.title("珀莱雅周均百度指数与股价散点图及趋势图", fontsize=14)
plt.xlabel("周均百度指数", fontsize=12)
plt.ylabel("周均股价", fontsize=12)
# 添加相关系数标注
plt.text(0.05, 0.95, f"相关系数 r = {r_value1:.4f}", 
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white"))
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
# 保存图片
plt.savefig(r"D:\学校事务\大三下\python课程\week13 pre\珀莱雅_百度指数_股价散点趋势图.png", dpi=300)
plt.close()

# 5. 绘制上海家化散点图+趋势图
plt.figure(figsize=(10, 6))
# 绘制散点
plt.scatter(x2, y2, color="forestgreen", alpha=0.7, label="观测点")
# 计算线性拟合参数
slope2, intercept2, r_value2, p_val2, std_err2 = stats.linregress(x2, y2)
# 生成拟合直线数据
line2 = slope2 * x2 + intercept2
# 绘制趋势线
plt.plot(x2, line2, color="darkred", linewidth=2, label="趋势线")
# 设置图表标题与坐标轴
plt.title("上海家化周均百度指数与股价散点图及趋势图", fontsize=14)
plt.xlabel("周均百度指数", fontsize=12)
plt.ylabel("周均股价", fontsize=12)
# 添加相关系数标注
plt.text(0.05, 0.95, f"相关系数 r = {r_value2:.4f}", 
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white"))
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
# 保存图片
plt.savefig(r"D:\学校事务\大三下\python课程\week13 pre\上海家化_百度指数_股价散点趋势图.png", dpi=300)
plt.close()
