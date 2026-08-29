# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:13:50 2026

@author: wty07
"""
# -*- coding: utf-8 -*-
"""
2025年珀莱雅：小红书+知乎+股价 相关性+情绪分析
适配PyCharm、无额外依赖、直接运行
"""
# ===================== 1. 导入库 =====================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 中文显示设置（避免乱码）
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ===================== 2. 定义文件路径（直接用你给的） =====================
# 小红书原始数据
xhs_path = r"D:\学校事务\大三下\python课程\week13pre还有后续\25_结合社交平台的珀莱雅数据分析\小红书_珀莱雅_2025年数据.xlsx"
# 股价周度数据
stock_path = r"D:\学校事务\大三下\python课程\week13pre还有后续\25_结合社交平台的珀莱雅数据分析\珀莱雅_股价_周度数据_2025.xlsx"
# 知乎周度统计
zhihu_path = r"D:\学校事务\大三下\python课程\week13pre还有后续\25_结合社交平台的珀莱雅数据分析\知乎_珀莱雅_2025年周度统计.xlsx"

# 输出文件保存路径
output_folder = r"D:\学校事务\大三下\python课程\week13pre还有后续\25_结合社交平台的珀莱雅数据分析"
output_path = output_folder + r"\分析结果汇总.xlsx"

# ===================== 3. 读取并预处理数据 =====================
# 读取数据
df_xhs = pd.read_excel(xhs_path)
df_stock = pd.read_excel(stock_path)
df_zhihu = pd.read_excel(zhihu_path)

# 小红书按周统计讨论量
df_xhs_week = df_xhs.groupby("周标签").size().reset_index(name="小红书讨论量")

# ===================== 任务1：描述性统计 =====================
print("="*80)
print("【任务1】2025珀莱雅 描述性统计汇总")
print("="*80)

# 小红书统计
stat_xhs = df_xhs_week["小红书讨论量"].describe()
# 知乎统计
stat_zhihu = df_zhihu["讨论量"].describe()
# 股价统计
stat_stock = df_stock["周涨跌幅_实际"].describe()

# 汇总表
desc_df = pd.DataFrame({
    "指标": ["总讨论量/均值", "最大值", "最小值", "均值", "标准差"],
    "小红书讨论量": [df_xhs_week["小红书讨论量"].sum(), stat_xhs["max"], stat_xhs["min"], stat_xhs["mean"], stat_xhs["std"]],
    "知乎讨论量": [df_zhihu["讨论量"].sum(), stat_zhihu["max"], stat_zhihu["min"], stat_zhihu["mean"], stat_zhihu["std"]],
    "股价周涨跌幅(%)": ["-", stat_stock["max"], stat_stock["min"], stat_stock["mean"], stat_stock["std"]]
})
print(desc_df.round(2))

# ===================== 数据合并（按周标签） =====================
df_merge = pd.merge(df_xhs_week, df_zhihu, on="周标签", how="left")
df_merge = pd.merge(df_merge, df_stock[["周标签", "周涨跌幅_实际"]], on="周标签", how="left")
df_merge.rename(columns={"讨论量": "知乎讨论量"}, inplace=True)
df_merge.fillna(0, inplace=True)

# ===================== 任务2：相关性分析 =====================
print("\n" + "="*80)
print("【任务2】相关性分析（Pearson）")
print("="*80)

# 小红书 ↔ 股价
r1, p1 = stats.pearsonr(df_merge["小红书讨论量"], df_merge["周涨跌幅_实际"])
# 知乎 ↔ 股价
r2, p2 = stats.pearsonr(df_merge["知乎讨论量"], df_merge["周涨跌幅_实际"])

corr_df = pd.DataFrame({
    "指标对": ["小红书讨论量 ↔ 股价涨跌幅", "知乎讨论量 ↔ 股价涨跌幅"],
    "相关系数r": [round(r1,4), round(r2,4)],
    "P值": [round(p1,4), round(p2,4)],
    "显著性": ["显著(p<0.05)" if p1<0.05 else "不显著", "显著(p<0.05)" if p2<0.05 else "不显著"]
})
print(corr_df)

# ===================== 任务3：小红书情绪分析（关键词法，无需snownlp） =====================
print("\n" + "="*80)
print("【任务3】小红书标题情绪分析（关键词匹配法）")
print("="*80)

# 定义情绪关键词（根据美妆场景优化）
positive_words = ["好用", "推荐", "喜欢", "神仙", "绝了", "yyds", "爱了", "无限回购", "巨好", "无敌", "效果好", "温和", "保湿", "提亮", "去黄", "维稳", "修复", "不踩雷", "闭眼入", "本命"]
negative_words = ["踩雷", "避雷", "垃圾", "难用", "没用", "失望", "不好用", "烂", "踩坑", "不推荐", "搓泥", "过敏", "闷痘", "油腻", "搓泥", "没效果", "踩雷", "劝退"]

# 抽取150条标题
sample_titles = df_xhs["title"].dropna().sample(150, random_state=42).to_frame()

# 关键词情绪判断
def simple_sentiment(text):
    text = str(text).lower()
    pos_count = sum(1 for word in positive_words if word in text)
    neg_count = sum(1 for word in negative_words if word in text)
    if pos_count > neg_count:
        return "正面"
    elif neg_count > pos_count:
        return "负面"
    else:
        return "中性"

sample_titles["情绪分类"] = sample_titles["title"].apply(simple_sentiment)
sentiment_count = sample_titles["情绪分类"].value_counts()
sentiment_ratio = sentiment_count / sentiment_count.sum() * 100

# 输出情绪统计
print("150条小红书标题情绪统计：")
for cat, cnt in sentiment_count.items():
    print(f"{cat}：{cnt}条 ({sentiment_ratio[cat]:.1f}%)")

# 计算周均情绪得分（正面倾向占比）
def get_positive_score(text):
    text = str(text).lower()
    pos_count = sum(1 for word in positive_words if word in text)
    neg_count = sum(1 for word in negative_words if word in text)
    total = pos_count + neg_count
    return pos_count / total if total > 0 else 0.5

df_xhs["正面倾向得分"] = df_xhs["title"].apply(get_positive_score)
week_sentiment = df_xhs.groupby("周标签")["正面倾向得分"].mean().reset_index(name="周均情绪得分")
df_merge = pd.merge(df_merge, week_sentiment, on="周标签", how="left")
df_merge["周均情绪得分"].fillna(0.5, inplace=True)

# ===================== 任务5：可视化（5张图） =====================
print("\n开始生成图表...")

# 图1：小红书讨论量 vs 股价涨跌幅
plt.figure(figsize=(12,5))
ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.plot(df_merge["周标签"], df_merge["小红书讨论量"], "r-o", linewidth=2, markersize=6, label="小红书讨论量")
ax2.plot(df_merge["周标签"], df_merge["周涨跌幅_实际"], "b--o", linewidth=2, markersize=6, label="股价涨跌幅(%)")
ax1.set_xlabel("周标签", fontsize=12)
ax1.set_ylabel("小红书讨论量", color="r", fontsize=12)
ax2.set_ylabel("股价周涨跌幅(%)", color="b", fontsize=12)
plt.title("2025珀莱雅：小红书讨论量 vs 股价涨跌幅", fontsize=14)
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(output_folder + r"\小红书_股价趋势图.png", dpi=300, bbox_inches="tight")
plt.close()

# 图2：知乎讨论量 vs 股价涨跌幅
plt.figure(figsize=(12,5))
ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.plot(df_merge["周标签"], df_merge["知乎讨论量"], "g-o", linewidth=2, markersize=6, label="知乎讨论量")
ax2.plot(df_merge["周标签"], df_merge["周涨跌幅_实际"], "b--o", linewidth=2, markersize=6, label="股价涨跌幅(%)")
ax1.set_xlabel("周标签", fontsize=12)
ax1.set_ylabel("知乎讨论量", color="g", fontsize=12)
ax2.set_ylabel("股价周涨跌幅(%)", color="b", fontsize=12)
plt.title("2025珀莱雅：知乎讨论量 vs 股价涨跌幅", fontsize=14)
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(output_folder + r"\知乎_股价趋势图.png", dpi=300, bbox_inches="tight")
plt.close()

# 图3：情绪分类饼图
plt.figure(figsize=(6,6))
plt.pie(sentiment_count, labels=sentiment_count.index, autopct="%.1f%%", colors=["#ff9999","#66b3ff","#99ff99"], startangle=90)
plt.title("2025珀莱雅小红书标题情绪分布", fontsize=14)
plt.tight_layout()
plt.savefig(output_folder + r"\情绪饼图.png", dpi=300)
plt.close()

# 图4：周均情绪得分 vs 股价涨跌幅
plt.figure(figsize=(12,5))
ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.plot(df_merge["周标签"], df_merge["周均情绪得分"], "m-o", linewidth=2, markersize=6, label="周均情绪得分")
ax2.plot(df_merge["周标签"], df_merge["周涨跌幅_实际"], "b--o", linewidth=2, markersize=6, label="股价涨跌幅(%)")
ax1.set_xlabel("周标签", fontsize=12)
ax1.set_ylabel("周均情绪得分", color="m", fontsize=12)
ax2.set_ylabel("股价周涨跌幅(%)", color="b", fontsize=12)
plt.title("2025珀莱雅：周均情绪得分 vs 股价涨跌幅", fontsize=14)
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(output_folder + r"\情绪_股价趋势图.png", dpi=300, bbox_inches="tight")
plt.close()

# 图5：相关性热力图
corr_data = df_merge[["小红书讨论量","知乎讨论量","周涨跌幅_实际","周均情绪得分"]].corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr_data, annot=True, cmap="RdBu_r", fmt=".2f", vmin=-1, vmax=1, linewidths=0.5)
plt.title("多指标相关性热力图", fontsize=14)
plt.tight_layout()
plt.savefig(output_folder + r"\相关性热力图.png", dpi=300)
plt.close()

# ===================== 保存所有结果 =====================
with pd.ExcelWriter(output_path) as writer:
    desc_df.to_excel(writer, sheet_name="描述性统计", index=False)
    corr_df.to_excel(writer, sheet_name="相关性分析", index=False)
    sample_titles.to_excel(writer, sheet_name="150条情绪标注", index=False)
    df_merge.to_excel(writer, sheet_name="周度合并数据", index=False)

print("\n✅ 全部分析完成！")
print(f"📊 结果文件已保存至：{output_path}")
print("🖼️ 5张图表已保存至文件夹")
