# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:51:06 2026

@author: Kwan
"""

import baostock as bs
import pandas as pd

# ==================== 1. 登录系统 ====================
print("正在登录 baostock...")
lg = bs.login()
if lg.error_code != '0':
    print(f"登录失败：{lg.error_msg}")
    exit()
print("✅ 登录成功")

# ==================== 2. 定义获取数据的函数 ====================
def get_stock_data(code, start_date, end_date):
    """
    获取股票日K线数据
    code格式：sh.603605 或 sz.000001
    """
    print(f"正在获取 {code} 的数据...")
    
    # 查询日K线数据
    rs = bs.query_history_k_data_plus(
        code,
        "date,open,high,low,close,volume,amount,pctChg",
        start_date=start_date,
        end_date=end_date,
        frequency="d",      # d=日线，w=周线，m=月线
        adjustflag="2"      # 2=前复权，3=不复权，1=后复权
    )
    
    if rs.error_code != '0':
        print(f"获取失败：{rs.error_msg}")
        return None
    
    # 转换为 DataFrame
    data_list = []
    while rs.next():
        data_list.append(rs.get_row_data())
    
    df = pd.DataFrame(data_list, columns=rs.fields)
    
    # 数据类型转换
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'amount', 'pctChg']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])
    
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"✅ {code} 获取成功，共 {len(df)} 条数据")
    return df

# ==================== 3. 获取珀莱雅数据 ====================
print("\n" + "="*50)
print("开始获取珀莱雅（603605）股价数据")
print("="*50)

proya_df = get_stock_data(
    code="sh.603605",           # 上海证券交易所
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# ==================== 4. 生成周度数据（用于与小红书对齐） ====================
if proya_df is not None and not proya_df.empty:
    # 添加周标签（与小红书数据格式一致）
    proya_df['周标签'] = proya_df['date'].dt.strftime('%Y年第%W周')
    
    # 按周聚合
    weekly = proya_df.groupby('周标签').agg({
        'open': 'first',      # 周一开盘价
        'close': 'last',      # 周五收盘价
        'high': 'max',        # 周最高价
        'low': 'min',         # 周最低价
        'volume': 'sum',      # 周总成交量
        'amount': 'sum',      # 周总成交额
        'pctChg': 'mean'      # 周均涨跌幅
    }).round(2)
    
    # 计算周涨跌幅（使用周五收盘价 vs 周一开盘价）
    weekly['周涨跌幅_实际'] = (weekly['close'] - weekly['open']) / weekly['open'] * 100
    weekly = weekly.reset_index()
    
    # 保存文件
    output_path = r"C:\Users\Kwan\Desktop\xhs分析\珀莱雅_股价_周度数据_2025.xlsx"
    weekly.to_excel(output_path, index=False)
    
    print("\n" + "="*50)
    print("✅ 数据保存成功！")
    print("="*50)
    print(f"📊 文件位置：{output_path}")
    print(f"📊 总交易周数：{len(weekly)} 周")
    print("\n📈 周度数据预览（前10周）：")
    print(weekly[['周标签', 'open', 'close', '周涨跌幅_实际']].head(10))
else:
    print("❌ 获取数据失败，请检查网络后重试")

# ==================== 5. 登出系统 ====================
bs.logout()
print("\n✅ 已登出 baostock")