# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:43:12 2026

@author: wty07
"""

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Python课程作业
股吧发帖量分公司日度统计
功能：清洗官方账号数据、拆分公司帖子、统计窗口期日发帖量
"""

import pandas as pd

# ====================== 1. 核心配置 ======================
# 股吧数据文件路径
guba_path = r"D:\学校事务\大三下\python课程\week13 pre\Guba_珀莱雅_上海家化_2024.xlsx"
# 要排除的官方发布人列表
exclude_authors = ["上海家化资讯", "珀莱雅资讯", "万华化学咨询"]
# 统计时间范围
start_date = "2024-04-24"
end_date = "2024-05-02"
# 公司行号拆分（Excel行号）
shanghai_excel_row_end = 12001  # 上海家化帖子到Excel第12001行结束

# ====================== 2. 读取并清洗数据 ======================
# 读取股吧数据
df_guba = pd.read_excel(guba_path)

# 去除官方发布人帖子
df_clean = df_guba[~df_guba["发布人"].isin(exclude_authors)].copy()

# 统一日期格式
df_clean["日期"] = pd.to_datetime(df_clean["发布日期"])

# 筛选窗口期数据
df_window = df_clean[(df_clean["日期"] >= start_date) & (df_clean["日期"] <= end_date)].copy()

# ====================== 3. 按行号拆分两家公司帖子 ======================
# Excel行号转pandas索引（Excel行1对应索引0）
shanghai_index_end = shanghai_excel_row_end - 1

# 拆分上海家化和珀莱雅数据
df_shanghai = df_window[df_window.index <= shanghai_index_end].copy()
df_polaiya = df_window[df_window.index > shanghai_index_end].copy()

# ====================== 4. 统计每日发帖数量 ======================
# 上海家化日发帖数
count_shanghai = df_shanghai.groupby("日期").size().reset_index(name="上海家化发帖数")
# 珀莱雅日发帖数
count_polaiya = df_polaiya.groupby("日期").size().reset_index(name="珀莱雅发帖数")

# 合并两个统计结果，补全无数据的日期
df_final = pd.merge(
    count_shanghai,
    count_polaiya,
    on="日期",
    how="outer"
).fillna(0)  # 无数据的日期填充0

# 按日期升序排序
df_final = df_final.sort_values("日期").reset_index(drop=True)

# 调整列顺序
df_final = df_final[["日期", "上海家化发帖数", "珀莱雅发帖数"]]

# ====================== 5. 输出结果 ======================
print("="*60)
print("2024.04.24-2024.05.02 股吧日发帖量统计结果")
print("="*60)
print(df_final)

# 保存为Excel文件
save_path = r"D:\学校事务\大三下\python课程\week13 pre\股吧_两家公司日发帖量统计.xlsx"
df_final.to_excel(save_path, index=False)

print(f"\n文件已成功保存至：{save_path}")