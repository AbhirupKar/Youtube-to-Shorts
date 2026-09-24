import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Clip 1: Monthly payment comparison
labels1 = ['Grace period\n(month 1-60)', 'After grace\n(35-year term)', 'After grace\n(40-year term)']
values1 = [15000, 36000, 32000]
colors1 = ['#4C72B0', '#C44E52', '#DD8452']

fig, ax = plt.subplots(figsize=(8, 10))
bars = ax.bar(labels1, values1, color=colors1, width=0.6)
ax.set_title('Monthly Payment on NT$10M Loan\nSource: The Reporter', fontsize=14, pad=20)
ax.set_ylabel('NT$ per month', fontsize=12)
ax.set_ylim(0, 42000)
for bar, val in zip(bars, values1):
    ax.text(bar.get_x() + bar.get_width()/2, val + 800,
            f'NT${val:,}', ha='center', fontsize=13, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart1_payments.png', dpi=300, bbox_inches='tight')
plt.close()

# Clip 2: Tainan Anping price per ping
labels2 = ['Before\nNew Housing Policy', 'After\nNew Housing Policy']
values2 = [325000, 400000]
fig, ax = plt.subplots(figsize=(8, 10))
bars = ax.bar(labels2, values2, color=['#55A868', '#C44E52'], width=0.5)
ax.set_title('Tainan Anping New Build Price per Ping\nSource: The Reporter', fontsize=14, pad=20)
ax.set_ylabel('NT$ per ping', fontsize=12)
ax.set_ylim(0, 450000)
for bar, val in zip(bars, values2):
    ax.text(bar.get_x() + bar.get_width()/2, val + 8000,
            f'NT${val:,}', ha='center', fontsize=13, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart2_tainan.png', dpi=300, bbox_inches='tight')
plt.close()

# Clip 3: Mortgage burden ratio
labels3 = ['Taipei', 'Taichung\n(approaching)', 'Other central\n& south cities']
values3 = [60, 45, 40]
fig, ax = plt.subplots(figsize=(8, 10))
bars = ax.bar(labels3, values3, color=['#C44E52', '#DD8452', '#4C72B0'], width=0.6)
ax.set_title('Mortgage Burden Ratio\n(% of income spent on housing)\nSource: The Reporter', fontsize=14, pad=20)
ax.set_ylabel('% of monthly income', fontsize=12)
ax.set_ylim(0, 70)
for bar, val in zip(bars, values3):
    ax.text(bar.get_x() + bar.get_width()/2, val + 1.5,
            f'{val}%', ha='center', fontsize=13, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart3_burden.png', dpi=300, bbox_inches='tight')
plt.close()

print("Charts generated: chart1_payments.png, chart2_tainan.png, chart3_burden.png")
