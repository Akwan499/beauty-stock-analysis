# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:18:06 2026

@author: wty07
"""

# -*- coding: utf-8 -*-

import pandas as pd


path_baidu = r"D:\学校事务\大三下\python课程\week13 pre\美妆关联度爬虫数据\美妆关联度爬虫数据\百度指数_周度数据.xlsx"
path_price = r"D:\学校事务\大三下\python课程\week13 pre\美妆关联度爬虫数据\美妆关联度爬虫数据\股价_周度数据.xlsx"

df_baidu = pd.read_excel(path_baidu)
df_price = pd.read_excel(path_price)


print("\n" + "="*60)
print("百度指数周度数据 - 描述性统计")
print("="*60)
print(df_baidu.describe())

print("\n" + "="*60)
print("股价周度数据 - 描述性统计")
print("="*60)
print(df_price.describe())

df_merge = pd.merge(
    df_baidu,
    df_price,
    on="周数",  
    how="inner"  
)

df_merge.rename(columns={"日期": "起始日期"}, inplace=True)

final_cols = [
    "周数",
    "起始日期",
    "珀莱雅_百度指数",
    "珀莱雅_股价",
    "上海家化_百度指数",
    "上海家化_股价"
]

df_final = df_merge[final_cols]


save_path = r"D:\学校事务\大三下\python课程\week13 pre\周度百度指数_股价_合并表.xlsx"
df_final.to_excel(save_path, index=False)

print(f"\n 保存至：\n{save_path}")
print("\n最终表格列名：")
print(list(df_final.columns))