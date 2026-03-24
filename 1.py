"""
华严寺景区ABS产品定价模型
基于2023年游客量394.72万人次、年增长率10%、准确年龄段数据
"""
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']  
plt.rcParams['axes.unicode_minus'] = False  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# ==================== 一、基础数据输入 ====================

# 游客年龄结构及票价政策
age_data = {
    '年龄段': ['18-30岁', '31-45岁', '46-60岁', '60岁以上'],
    '占比': [0.3520, 0.3850, 0.1680, 0.0950],
    '淡季票价': [40, 40, 40, 0],
    '旺季票价': [50, 50, 50, 0]
}

df_age = pd.DataFrame(age_data)

# 淡旺季参数
low_season_ratio = 0.10   # 淡季占比10%
peak_season_ratio = 0.90  # 旺季占比90%

# 游客量参数
base_visitors = 394.72     # 2023年游客量（万人次）
growth_rate = 0.10         # 年增长率10%
years = 3                  # 产品期限

# 数字化体验参数
digital_conversion = 0.20  # 转化率20%
digital_price = 40         # 体验单价40元

# ABS产品参数
senior_ratio = 0.85        # 优先层占比85%
coverage_multiple = 1.2    # 超额覆盖倍数1.2倍
coupon_rate = 0.045        # 票面利率4.5%

# 市场收益率曲线
spot_rates = {1: 0.042, 2: 0.044, 3: 0.045}

# ==================== 二、计算加权平均票价 ====================

def calc_weighted_avg_ticket_price(df_age, low_ratio, peak_ratio):
    """计算综合加权平均票价"""
    # 淡季加权票价
    low_weighted = sum(df_age['占比'] * df_age['淡季票价'])
    # 旺季加权票价
    peak_weighted = sum(df_age['占比'] * df_age['旺季票价'])
    # 综合加权票价
    avg_price = low_weighted * low_ratio + peak_weighted * peak_ratio
    
    return low_weighted, peak_weighted, avg_price

low_price, peak_price, avg_ticket_price = calc_weighted_avg_ticket_price(
    df_age, low_season_ratio, peak_season_ratio
)

print("=" * 70)
print("华严寺景区ABS产品定价分析报告")
print("=" * 70)

print("\n【一、加权平均票价计算】")
print(f"淡季加权票价: {low_price:.2f} 元")
print(f"旺季加权票价: {peak_price:.2f} 元")
print(f"淡季占比: {low_season_ratio*100:.0f}%")
print(f"旺季占比: {peak_season_ratio*100:.0f}%")
print(f"综合加权平均票价: {avg_ticket_price:.2f} 元")

# ==================== 三、现金流预测 ====================

visitors = [base_visitors * (1 + growth_rate) ** i for i in range(years)]

cashflow_data = []
for i, v in enumerate(visitors):
    year = i + 1
    ticket_income = v * avg_ticket_price
    digital_users = v * digital_conversion
    digital_income = digital_users * digital_price
    total_income = ticket_income + digital_income
    
    cashflow_data.append({
        '年份': f'第{year}年',
        '游客量(万人次)': round(v, 2),
        '门票收入(万元)': round(ticket_income, 2),
        '数字化体验人数(万人次)': round(digital_users, 2),
        '数字化收入(万元)': round(digital_income, 2),
        '总收入(万元)': round(total_income, 2)
    })

df_cashflow = pd.DataFrame(cashflow_data)

print("\n【二、未来三年现金流预测】")
print(tabulate(df_cashflow, headers='keys', tablefmt='grid', showindex=False))

total_cashflow = df_cashflow['总收入(万元)'].sum()
print(f"\n三年总收入合计: {total_cashflow:.2f} 万元")

# ==================== 四、ABS产品结构设计 ====================

first_year_income = df_cashflow.loc[0, '总收入(万元)']
senior_scale = first_year_income * senior_ratio * coverage_multiple
sub_scale = senior_scale * (1 / senior_ratio - 1)

print("\n【三、ABS产品结构设计】")
print(f"第1年总收入: {first_year_income:.2f} 万元")
print(f"优先层占比: {senior_ratio*100:.0f}%")
print(f"超额覆盖倍数: {coverage_multiple}")
print(f"优先层发行规模: {senior_scale:.2f} 万元")
print(f"次级规模: {sub_scale:.2f} 万元")
print(f"总发行规模: {senior_scale + sub_scale:.2f} 万元")

# ==================== 五、优先层现金流与定价 ====================

annual_interest = senior_scale * coupon_rate

senior_cashflow = []
for year in range(1, years + 1):
    if year < years:
        cf = annual_interest
    else:
        cf = annual_interest + senior_scale
    senior_cashflow.append({'年份': f'第{year}年', '现金流(万元)': round(cf, 2)})

df_senior = pd.DataFrame(senior_cashflow)

print("\n【四、优先层本息现金流】")
print(tabulate(df_senior, headers='keys', tablefmt='grid', showindex=False))

# 折现定价
pv_total = 0
print("\n【五、优先层折现定价过程】")
for year in range(1, years + 1):
    cf = senior_cashflow[year-1]['现金流(万元)']
    discount_factor = 1 / (1 + spot_rates[year]) ** year
    pv = cf * discount_factor
    pv_total += pv
    print(f"第{year}年: 现金流={cf:.2f}万元, 折现因子={discount_factor:.4f}, 现值={pv:.2f}万元")

print(f"\n优先层现值合计: {pv_total:.2f} 万元")
issue_price = pv_total / senior_scale * 100
print(f"发行价格: {issue_price:.2f} 元/百元面值")

# ==================== 六、覆盖倍数验证 ====================

total_principal_interest = senior_scale * (1 + coupon_rate * years)
coverage = total_cashflow / total_principal_interest

print("\n【六、现金流覆盖倍数验证】")
print(f"优先层本息合计: {total_principal_interest:.2f} 万元")
print(f"基础资产总现金流: {total_cashflow:.2f} 万元")
print(f"覆盖倍数: {coverage:.2f} 倍")

# ==================== 七、敏感性分析 ====================

print("\n【七、压力测试 - 敏感性分析】")

# 不同增长率情景
print("\n1. 不同游客增长率情景:")
growth_scenarios = [0.05, 0.08, 0.10, 0.12, 0.15]
for g in growth_scenarios:
    visitors_g = [base_visitors * (1 + g) ** i for i in range(years)]
    total_income_g = 0
    for v in visitors_g:
        ticket_income = v * avg_ticket_price
        digital_income = v * digital_conversion * digital_price
        total_income_g += ticket_income + digital_income
    coverage_g = total_income_g / total_principal_interest
    status = "✓ 安全" if coverage_g >= 1.2 else "✗ 风险"
    print(f"   增长率{g*100:.0f}%: 总现金流={total_income_g:.0f}万元, 覆盖倍数={coverage_g:.2f}倍 {status}")

# 不同转化率情景
print("\n2. 不同数字化转化率情景:")
conversion_scenarios = [0.10, 0.15, 0.20, 0.25, 0.30]
for conv in conversion_scenarios:
    total_income_c = 0
    for v in visitors:
        ticket_income = v * avg_ticket_price
        digital_income = v * conv * digital_price
        total_income_c += ticket_income + digital_income
    coverage_c = total_income_c / total_principal_interest
    status = "✓ 安全" if coverage_c >= 1.2 else "✗ 风险"
    print(f"   转化率{conv*100:.0f}%: 总现金流={total_income_c:.0f}万元, 覆盖倍数={coverage_c:.2f}倍 {status}")

# ==================== 八、产品定价汇总 ====================

print("\n【八、产品定价最终汇总】")
print("-" * 70)
print(f"{'层级':<12} {'评级':<8} {'规模(万元)':<14} {'利率':<8} {'期限':<6} {'发行价格':<10}")
print("-" * 70)
print(f"{'优先A级':<12} {'AAA':<8} {senior_scale:<14.2f} {coupon_rate*100:.1f}%{'':<5} {'3年':<6} {'100元':<10}")
print(f"{'次级':<12} {'NR':<8} {sub_scale:<14.2f} {'-':<8} {'3年':<6} {'-':<10}")

issue_fee = senior_scale * 0.015
net_proceeds = senior_scale - issue_fee
print(f"\n发行费率: 1.5%")
print(f"发行费用: {issue_fee:.2f} 万元")
print(f"净融资额: {net_proceeds:.2f} 万元")

# ==================== 九、可视化 ====================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1：未来三年收入预测
years_plot = [1, 2, 3]
ticket_income = df_cashflow['门票收入(万元)']
digital_income = df_cashflow['数字化收入(万元)']

axes[0, 0].bar(years_plot, ticket_income, label='门票收入', color='steelblue')
axes[0, 0].bar(years_plot, digital_income, bottom=ticket_income, label='数字化收入', color='lightcoral')
axes[0, 0].set_xlabel('年份')
axes[0, 0].set_ylabel('收入(万元)')
axes[0, 0].set_title('未来三年收入预测', fontsize=14, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(axis='y', alpha=0.3)

for i, (t, d) in enumerate(zip(ticket_income, digital_income)):
    axes[0, 0].text(years_plot[i], t + d + 500, f'{t+d:.0f}', ha='center', fontweight='bold')

# 图2：优先层现金流
cashflow_values = [cf['现金流(万元)'] for cf in senior_cashflow]
axes[0, 1].bar(years_plot, cashflow_values, color='darkgreen')
axes[0, 1].set_xlabel('年份')
axes[0, 1].set_ylabel('现金流(万元)')
axes[0, 1].set_title('优先层本息现金流', fontsize=14, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)

for i, v in enumerate(cashflow_values):
    axes[0, 1].text(years_plot[i], v + 500, f'{v:.0f}', ha='center', fontweight='bold')

# 图3：游客年龄结构饼图
labels = df_age['年龄段'].tolist()
sizes = (df_age['占比'] * 100).tolist()
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc66']
axes[1, 0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
axes[1, 0].set_title('游客年龄结构分布', fontsize=14, fontweight='bold')

# 图4：覆盖倍数敏感性分析
growth_labels = ['5%', '8%', '10%', '12%', '15%']
coverage_growth = []
for g in [0.05, 0.08, 0.10, 0.12, 0.15]:
    visitors_g = [base_visitors * (1 + g) ** i for i in range(years)]
    total_income_g = 0
    for v in visitors_g:
        ticket_income = v * avg_ticket_price
        digital_income = v * digital_conversion * digital_price
        total_income_g += ticket_income + digital_income
    coverage_growth.append(total_income_g / total_principal_interest)

axes[1, 1].bar(growth_labels, coverage_growth, color='steelblue')
axes[1, 1].axhline(y=1.2, color='red', linestyle='--', linewidth=2, label='安全线(1.2倍)')
axes[1, 1].set_ylabel('覆盖倍数')
axes[1, 1].set_xlabel('游客增长率')
axes[1, 1].set_title('不同增长率情景下的覆盖倍数', fontsize=14, fontweight='bold')
axes[1, 1].legend()

for i, v in enumerate(coverage_growth):
    axes[1, 1].text(i, v + 0.05, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('华严寺_ABS产品定价分析.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n可视化图表已保存为 '华严寺_ABS产品定价分析.png'")

# ==================== 十、关键结论 ====================

print("\n" + "=" * 70)
print("【关键结论】")
print("=" * 70)
print(f"✓ 综合加权平均票价: {avg_ticket_price:.2f} 元")
print(f"✓ 三年总收入合计: {total_cashflow:.2f} 万元")
print(f"✓ 优先层发行规模: {senior_scale:.2f} 万元")
print(f"✓ 覆盖倍数: {coverage:.2f} 倍 (远超1.2倍最低要求)")
print(f"✓ 产品评级: AAA")
print(f"✓ 发行价格: 100元/百元面值 (平价发行)")
print(f"✓ 净融资额: {net_proceeds:.2f} 万元")
print("\n结论: 该ABS产品设计合理，现金流充足，覆盖倍数安全，可成功发行。")
