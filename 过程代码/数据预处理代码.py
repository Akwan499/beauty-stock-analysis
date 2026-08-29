# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:10:43 2026

@author: wty07
"""

# -*- coding: utf-8 -*-
"""
Spyder 周度百度指数平均值计算
功能：按周数分组，求日度百度指数的周平均值
输出：周数 | 起始日期 | 珀莱雅_百度指数(周均) | 上海家化_百度指数(周均)
"""

import pandas as pd

file_path = r"D:\学校事务\大三下\python课程\week13 pre\美妆关联度爬虫数据\美妆关联度爬虫数据\百度指数_日度数据.xlsx"

df = pd.read_excel(file_path)

# 查看原始数据（可选，运行后可在变量浏览器查看）
print("原始数据前5行：")
print(df.head())

grouped = df.groupby("周数").agg({
    "日期": "min",          # 每周的起始日期（取该周最小日期）
    "珀莱雅_百度指数": "mean",
    "上海家化_百度指数": "mean"
}).reset_index()

result = grouped.rename(columns={
    "日期": "起始日期",
    "珀莱雅_百度指数": "珀莱雅_百度指数",
    "上海家化_百度指数": "上海家化_百度指数"
})

result = result[["周数", "起始日期", "珀莱雅_百度指数", "上海家化_百度指数"]]

print("\n===== 周度平均百度指数最终结果 =====")
print(result)

result.to_excel(r"D:\学校事务\大三下\python课程\week13 pre\周度百度指数结果.xlsx", index=False)
print("\n 已导出：周度百度指数结果.xlsx")



























