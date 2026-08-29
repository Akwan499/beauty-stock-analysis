# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:08:27 2026

@author: Kwan
"""

import pandas as pd
import os

# 读取小红书数据
file_path = r"C:\Users\Kwan\Desktop\MediaCrawler\data\xhs\csv\search_contents_2026-05-12.csv"
df = pd.read_csv(file_path)

# 转换时间
df['日期'] = pd.to_datetime(df['time'], unit='ms')

# 提取2025年数据
df_2025 = df[(df['日期'] >= '2025-01-01') & (df['日期'] <= '2025-12-31')].copy()

# 添加周标签
df_2025['周标签'] = df_2025['日期'].dt.strftime('%Y年第%W周')

# 保存
output_path = r"C:\Users\Kwan\Desktop\xhs分析\小红书_珀莱雅_2025年数据.xlsx"
df_2025.to_excel(output_path, index=False)

print(f"✅ 2025年数据已保存：{len(df_2025)} 条")
print(f"时间范围：{df_2025['日期'].min()} 至 {df_2025['日期'].max()}")