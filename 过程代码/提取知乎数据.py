# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:30:01 2026

@author: Kwan
"""

import pandas as pd
import os

# 知乎数据文件路径（根据你的实际路径调整）
zhihu_file = r"C:\Users\Kwan\Desktop\MediaCrawler\data\zhihu\csv\search_contents_2026-05-10.csv"

# 输出文件夹
output_dir = r"C:\Users\Kwan\Desktop\xhs分析"
os.makedirs(output_dir, exist_ok=True)

# 读取数据
print("正在读取知乎数据...")
df = pd.read_csv(zhihu_file)
print(f"原始数据共 {len(df)} 条")

# 查看列名
print("\n列名：")
print(df.columns.tolist())

# 找到时间列（可能是 created_time 或 publish_time）
time_col = None
for col in ['created_time', 'publish_time', 'time', 'created_at']:
    if col in df.columns:
        time_col = col
        break

if time_col is None:
    print("未找到时间列，请检查列名")
    exit()

print(f"\n使用时间列: {time_col}")

# 转换时间（如果是毫秒级时间戳）
if df[time_col].dtype in ['int64', 'float64']:
    # 判断是秒还是毫秒
    sample = df[time_col].iloc[0]
    if sample > 1e12:  # 毫秒级
        df['日期'] = pd.to_datetime(df[time_col], unit='ms')
    else:  # 秒级
        df['日期'] = pd.to_datetime(df[time_col], unit='s')
else:
    df['日期'] = pd.to_datetime(df[time_col])

print(f"时间范围: {df['日期'].min()} 至 {df['日期'].max()}")

# 筛选2025年数据
df_2025 = df[(df['日期'] >= '2025-01-01') & (df['日期'] <= '2025-12-31')].copy()
print(f"\n2025年数据共 {len(df_2025)} 条")

# 找到内容列（标题和正文）
title_col = None
content_col = None
for col in ['title', '标题', 'question_title']:
    if col in df_2025.columns:
        title_col = col
        break

for col in ['content', '内容', 'content_text', 'desc']:
    if col in df_2025.columns:
        content_col = col
        break

print(f"标题列: {title_col}, 内容列: {content_col}")

# 筛选珀莱雅相关（在标题或内容中搜索）
def is_proya(row):
    text = ""
    if title_col and pd.notna(row[title_col]):
        text += str(row[title_col])
    if content_col and pd.notna(row[content_col]):
        text += str(row[content_col])
    return '珀莱雅' in text

df_proya = df_2025[df_2025.apply(is_proya, axis=1)].copy()
print(f"珀莱雅相关: {len(df_proya)} 条")

# 添加时间字段
df_proya['月份'] = df_proya['日期'].dt.strftime('%Y-%m')
df_proya['周标签'] = df_proya['日期'].dt.strftime('%Y年第%W周')
df_proya['年份'] = df_proya['日期'].dt.year

# 生成周度统计
weekly_stats = df_proya.groupby('周标签').size().reset_index(name='讨论量')
weekly_stats = weekly_stats.sort_values('周标签')

# 生成月度统计
monthly_stats = df_proya.groupby('月份').size().reset_index(name='讨论量')
monthly_stats = monthly_stats.sort_values('月份')

# 保存文件
output_detail = os.path.join(output_dir, '知乎_珀莱雅_2025年详细数据.xlsx')
output_weekly = os.path.join(output_dir, '知乎_珀莱雅_2025年周度统计.xlsx')
output_monthly = os.path.join(output_dir, '知乎_珀莱雅_2025年月度统计.xlsx')

df_proya.to_excel(output_detail, index=False)
weekly_stats.to_excel(output_weekly, index=False)
monthly_stats.to_excel(output_monthly, index=False)

print("\n" + "="*50)
print("✅ 数据保存成功！")
print("="*50)
print(f"📊 详细数据: {output_detail}")
print(f"📊 周度统计: {output_weekly}")
print(f"📊 月度统计: {output_monthly}")

# 显示预览
print("\n📈 周度统计预览:")
print(weekly_stats.head(10))

print("\n📊 月度统计预览:")
print(monthly_stats)

# 数据概况
print("\n📊 数据概况:")
print(f"总讨论量: {len(df_proya)} 条")
print(f"覆盖周数: {len(weekly_stats)} 周")
print(f"覆盖月份: {len(monthly_stats)} 个月")
print(f"时间范围: {df_proya['日期'].min()} 至 {df_proya['日期'].max()}")