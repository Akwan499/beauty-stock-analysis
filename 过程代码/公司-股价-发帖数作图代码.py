# -*- coding: utf-8 -*-
"""
Created on Wed May  6 23:09:23 2026

@author: wty07
"""

# -*- coding: utf-8 -*-
"""
Python课程作业
股吧发帖数与股价涨跌幅相关性分析
功能：分别计算珀莱雅、上海家化发帖数与涨跌幅的相关系数，并绘制散点趋势图
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False

# ====================== 1. 读取合并后的数据 ======================
file_path = r"D:\学校事务\大三下\python课程\week13 pre\股吧_两家公司日发帖量统计.xlsx"
df = pd.read_excel(file_path)

# 去除涨跌幅为空的行（仅保留你说的3组有效数据）
df = df.dropna(subset=["上海家化涨跌额", "珀莱雅涨跌额"], how="all")

print("有效数据预览：")
print(df)

# ====================== 2. 上海家化 相关性分析 ======================
# 提取有效数据
shanghai_data = df.dropna(subset=["上海家化涨跌额"])
x_sh = shanghai_data["上海家化发帖数"]
y_sh = shanghai_data["上海家化涨跌额"]

# 计算相关系数
corr_sh, p_sh = stats.pearsonr(x_sh, y_sh)

print("\n===== 上海家化 相关性结果 =====")
print(f"Pearson相关系数 r = {corr_sh:.4f}")
print(f"P值 = {p_sh:.4f}")

# 绘制散点+趋势图
plt.figure(figsize=(8, 5), dpi=120)
plt.scatter(x_sh, y_sh, color="forestgreen", s=60, alpha=0.7, label="观测点")

# 线性拟合
slope_sh, intercept_sh, *_ = stats.linregress(x_sh, y_sh)
line_sh = slope_sh * x_sh + intercept_sh
plt.plot(x_sh, line_sh, color="darkred", linewidth=2, label="趋势线")

# 标注相关系数
plt.text(0.05, 0.90, f"r = {corr_sh:.4f}",
         transform=plt.gca().transAxes,
         bbox=dict(facecolor="white", alpha=0.8),
         fontsize=11)

plt.title("上海家化 股吧发帖数与股价涨跌幅相关性", fontsize=13)
plt.xlabel("股吧发帖数", fontsize=11)
plt.ylabel("股价涨跌幅(%)", fontsize=11)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(r"D:\学校事务\大三下\python课程\week13 pre\上海家化_发帖数_涨跌幅_相关性图.png", dpi=300)
plt.close()

# ====================== 3. 珀莱雅 相关性分析 ======================
# 提取有效数据
polaiya_data = df.dropna(subset=["珀莱雅涨跌额"])
x_po = polaiya_data["珀莱雅发帖数"]
y_po = polaiya_data["珀莱雅涨跌额"]

# 计算相关系数
corr_po, p_po = stats.pearsonr(x_po, y_po)

print("\n===== 珀莱雅 相关性结果 =====")
print(f"Pearson相关系数 r = {corr_po:.4f}")
print(f"P值 = {p_po:.4f}")

# 绘制散点+趋势图
plt.figure(figsize=(8, 5), dpi=120)
plt.scatter(x_po, y_po, color="steelblue", s=60, alpha=0.7, label="观测点")

# 线性拟合
slope_po, intercept_po, *_ = stats.linregress(x_po, y_po)
line_po = slope_po * x_po + intercept_po
plt.plot(x_po, line_po, color="darkred", linewidth=2, label="趋势线")

# 标注相关系数
plt.text(0.05, 0.90, f"r = {corr_po:.4f}",
         transform=plt.gca().transAxes,
         bbox=dict(facecolor="white", alpha=0.8),
         fontsize=11)

plt.title("珀莱雅 股吧发帖数与股价涨跌幅相关性", fontsize=13)
plt.xlabel("股吧发帖数", fontsize=11)
plt.ylabel("股价涨跌幅(%)", fontsize=11)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(r"D:\学校事务\大三下\python课程\week13 pre\珀莱雅_发帖数_涨跌幅_相关性图.png", dpi=300)
plt.close()

print("\n 两张相关性散点趋势图已保存完成")