"""
Stage 2, Step 2d: Analysis tables and statistics.

Produces all 7 tables/statistics from the spec:
1. Classification distribution by product type
2. Mean continuous scores by product type
3. eMFD scores by classification
4. eMFD scores by product type
5. Correlation matrix (delegative_score, evaluative_score, 5 eMFD foundations)
6. Confidence distribution by classification category
7. Cross-tabulation: product x classification x confidence level
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

CLASSIFIED_PATH = "/workspaces/HumanxAI-2026/output/cfpb_classified_9000.csv"
EMFD_PATH = "/workspaces/HumanxAI-2026/output/cfpb_emfd_scores.csv"
OUTPUT_DIR = "/workspaces/HumanxAI-2026/output"
TABLES_DIR = os.path.join(OUTPUT_DIR, "stage2_tables")
os.makedirs(TABLES_DIR, exist_ok=True)

SUMMARY_PATH = os.path.join(OUTPUT_DIR, "cfpb_analysis_summary.md")

FOUNDATIONS = ['care', 'fairness', 'loyalty', 'authority', 'sanctity']
PRODUCT_ORDER = ['mortgage', 'checking_savings', 'credit_card']
CLASS_ORDER = ['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE']

print("Loading data...")
df = pd.read_csv(CLASSIFIED_PATH, dtype={'complaint_id': 'int64'})
emfd = pd.read_csv(EMFD_PATH, dtype={'complaint_id': 'int64'})

# Merge
df = df.merge(emfd, on='complaint_id', how='left')

# Exclude parse errors from analysis
valid = df[df['classification'].isin(CLASS_ORDER)].copy()
parse_errors = len(df) - len(valid)
print(f"Total: {len(df):,}, Valid: {len(valid):,}, Parse errors: {parse_errors}")

# Ensure numeric types
for col in ['delegative_score', 'evaluative_score', 'confidence']:
    valid[col] = pd.to_numeric(valid[col], errors='coerce')
for f in FOUNDATIONS:
    valid[f'{f}_p'] = pd.to_numeric(valid[f'{f}_p'], errors='coerce')

summary_lines = []

def add(text=""):
    summary_lines.append(text)
    print(text)

add("# CFPB Stage 2: Classification & eMFD Analysis Results")
add(f"\nTotal narratives classified: {len(df):,}")
add(f"Valid classifications: {len(valid):,}")
if parse_errors > 0:
    add(f"Parse errors: {parse_errors}")
add("")

# ============================================================
# TABLE 1: Classification distribution by product type
# ============================================================
add("## Table 1: Classification Distribution by Product Type")
add("")

ct = pd.crosstab(valid['product_group'], valid['classification'])
ct = ct.reindex(index=PRODUCT_ORDER, columns=CLASS_ORDER, fill_value=0)
ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100

add("| Product | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |")
add("|---------|----------:|----------:|---------------:|------:|")
for prod in PRODUCT_ORDER:
    row = ct.loc[prod]
    prow = ct_pct.loc[prod]
    total = row.sum()
    add(f"| {prod} | {row['EVALUATIVE']:,} ({prow['EVALUATIVE']:.1f}%) | "
        f"{row['DELEGATIVE']:,} ({prow['DELEGATIVE']:.1f}%) | "
        f"{row['UNCLASSIFIABLE']:,} ({prow['UNCLASSIFIABLE']:.1f}%) | {total:,} |")

totals = ct.sum()
total_pct = totals / totals.sum() * 100
add(f"| **Total** | {totals['EVALUATIVE']:,} ({total_pct['EVALUATIVE']:.1f}%) | "
    f"{totals['DELEGATIVE']:,} ({total_pct['DELEGATIVE']:.1f}%) | "
    f"{totals['UNCLASSIFIABLE']:,} ({total_pct['UNCLASSIFIABLE']:.1f}%) | {totals.sum():,} |")
add("")

# Save table
ct_out = ct.copy()
ct_out['pct_evaluative'] = ct_pct['EVALUATIVE']
ct_out['pct_delegative'] = ct_pct['DELEGATIVE']
ct_out['pct_unclassifiable'] = ct_pct['UNCLASSIFIABLE']
ct_out.to_csv(os.path.join(TABLES_DIR, "table1_classification_by_product.csv"))

# ============================================================
# TABLE 2: Mean continuous scores by product type
# ============================================================
add("## Table 2: Mean Continuous Scores by Product Type")
add("")
add("| Product | Delegative Score | Evaluative Score |")
add("|---------|---------------:|----------------:|")

for prod in PRODUCT_ORDER:
    g = valid[valid['product_group'] == prod]
    d_mean = g['delegative_score'].mean()
    d_sd = g['delegative_score'].std()
    e_mean = g['evaluative_score'].mean()
    e_sd = g['evaluative_score'].std()
    add(f"| {prod} | {d_mean:.3f} (SD={d_sd:.3f}) | {e_mean:.3f} (SD={e_sd:.3f}) |")

d_all = valid['delegative_score']
e_all = valid['evaluative_score']
add(f"| **Overall** | {d_all.mean():.3f} (SD={d_all.std():.3f}) | {e_all.mean():.3f} (SD={e_all.std():.3f}) |")
add("")

# Cross-product comparisons
add("### Cross-Product Comparisons (Mortgage vs Credit Card)")
add("")

mort = valid[valid['product_group'] == 'mortgage']
cc = valid[valid['product_group'] == 'credit_card']

# Delegative score comparison
u_stat_d, p_val_d = stats.mannwhitneyu(
    mort['delegative_score'].dropna(), cc['delegative_score'].dropna(), alternative='two-sided'
)
# Effect size (rank-biserial correlation)
n1, n2 = len(mort['delegative_score'].dropna()), len(cc['delegative_score'].dropna())
r_d = 1 - (2 * u_stat_d) / (n1 * n2)

# Cohen's d
d_cohens_d = (mort['delegative_score'].mean() - cc['delegative_score'].mean()) / np.sqrt(
    (mort['delegative_score'].std()**2 + cc['delegative_score'].std()**2) / 2
)

add(f"- Delegative score: mortgage mean={mort['delegative_score'].mean():.3f}, "
    f"credit_card mean={cc['delegative_score'].mean():.3f}")
add(f"  Mann-Whitney U={u_stat_d:,.0f}, p={p_val_d:.2e}, Cohen's d={d_cohens_d:.3f}")
add("")

# Evaluative score comparison
u_stat_e, p_val_e = stats.mannwhitneyu(
    mort['evaluative_score'].dropna(), cc['evaluative_score'].dropna(), alternative='two-sided'
)
e_cohens_d = (mort['evaluative_score'].mean() - cc['evaluative_score'].mean()) / np.sqrt(
    (mort['evaluative_score'].std()**2 + cc['evaluative_score'].std()**2) / 2
)
add(f"- Evaluative score: mortgage mean={mort['evaluative_score'].mean():.3f}, "
    f"credit_card mean={cc['evaluative_score'].mean():.3f}")
add(f"  Mann-Whitney U={u_stat_e:,.0f}, p={p_val_e:.2e}, Cohen's d={e_cohens_d:.3f}")
add("")

# Also test mortgage vs checking_savings
cs = valid[valid['product_group'] == 'checking_savings']
u_d_mc, p_d_mc = stats.mannwhitneyu(
    mort['delegative_score'].dropna(), cs['delegative_score'].dropna(), alternative='two-sided')
d_mc = (mort['delegative_score'].mean() - cs['delegative_score'].mean()) / np.sqrt(
    (mort['delegative_score'].std()**2 + cs['delegative_score'].std()**2) / 2)
add(f"### Mortgage vs Checking/Savings")
add(f"- Delegative score: mortgage={mort['delegative_score'].mean():.3f}, "
    f"checking_savings={cs['delegative_score'].mean():.3f}, "
    f"p={p_d_mc:.2e}, Cohen's d={d_mc:.3f}")

u_e_mc, p_e_mc = stats.mannwhitneyu(
    mort['evaluative_score'].dropna(), cs['evaluative_score'].dropna(), alternative='two-sided')
e_mc = (mort['evaluative_score'].mean() - cs['evaluative_score'].mean()) / np.sqrt(
    (mort['evaluative_score'].std()**2 + cs['evaluative_score'].std()**2) / 2)
add(f"- Evaluative score: mortgage={mort['evaluative_score'].mean():.3f}, "
    f"checking_savings={cs['evaluative_score'].mean():.3f}, "
    f"p={p_e_mc:.2e}, Cohen's d={e_mc:.3f}")
add("")

# ============================================================
# TABLE 3: eMFD scores by classification
# ============================================================
add("## Table 3: eMFD Scores by Classification Category")
add("")
header = "| Foundation |"
for cls in CLASS_ORDER:
    header += f" {cls} |"
add(header)
add("|------------|" + "---------|" * len(CLASS_ORDER))

for f in FOUNDATIONS:
    col = f'{f}_p'
    row_str = f"| {f.capitalize()} |"
    for cls in CLASS_ORDER:
        g = valid[valid['classification'] == cls]
        m = g[col].mean()
        s = g[col].std()
        row_str += f" {m:.5f} ({s:.5f}) |"
    add(row_str)
add("")

# Statistical tests: EVALUATIVE vs DELEGATIVE on each foundation
add("### EVALUATIVE vs DELEGATIVE (Mann-Whitney U tests)")
add("")
eval_rows = valid[valid['classification'] == 'EVALUATIVE']
deleg_rows = valid[valid['classification'] == 'DELEGATIVE']

for f in FOUNDATIONS:
    col = f'{f}_p'
    u, p = stats.mannwhitneyu(
        eval_rows[col].dropna(), deleg_rows[col].dropna(), alternative='two-sided')
    cd = (deleg_rows[col].mean() - eval_rows[col].mean()) / np.sqrt(
        (deleg_rows[col].std()**2 + eval_rows[col].std()**2) / 2)
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    add(f"- {f.capitalize()}: DELEG mean={deleg_rows[col].mean():.5f}, "
        f"EVAL mean={eval_rows[col].mean():.5f}, "
        f"p={p:.2e}, Cohen's d={cd:.3f} {sig}")
add("")

# ============================================================
# TABLE 4: eMFD scores by product type
# ============================================================
add("## Table 4: eMFD Scores by Product Type")
add("")
header = "| Foundation |"
for prod in PRODUCT_ORDER:
    header += f" {prod} |"
add(header)
add("|------------|" + "---------|" * len(PRODUCT_ORDER))

for f in FOUNDATIONS:
    col = f'{f}_p'
    row_str = f"| {f.capitalize()} |"
    for prod in PRODUCT_ORDER:
        g = valid[valid['product_group'] == prod]
        m = g[col].mean()
        s = g[col].std()
        row_str += f" {m:.5f} ({s:.5f}) |"
    add(row_str)
add("")

# ============================================================
# TABLE 5: Correlation matrix
# ============================================================
add("## Table 5: Correlation Matrix")
add("")
add("Spearman correlations between classification scores and eMFD foundations.")
add("")

corr_cols = ['delegative_score', 'evaluative_score'] + [f'{f}_p' for f in FOUNDATIONS]
corr_labels = ['Deleg', 'Eval'] + [f.capitalize()[:4] for f in FOUNDATIONS]

corr_matrix = valid[corr_cols].corr(method='spearman')

header = "| |"
for label in corr_labels:
    header += f" {label} |"
add(header)
add("|---|" + "---:|" * len(corr_labels))

for i, (col, label) in enumerate(zip(corr_cols, corr_labels)):
    row_str = f"| {label} |"
    for j, col2 in enumerate(corr_cols):
        val = corr_matrix.loc[col, col2]
        if i == j:
            row_str += " 1.00 |"
        else:
            row_str += f" {val:.3f} |"
    add(row_str)
add("")

# Highlight key correlations with p-values
add("### Key correlations (with p-values)")
add("")
key_pairs = [
    ('delegative_score', 'care_p', 'Delegative x Care'),
    ('delegative_score', 'fairness_p', 'Delegative x Fairness'),
    ('delegative_score', 'loyalty_p', 'Delegative x Loyalty'),
    ('evaluative_score', 'care_p', 'Evaluative x Care'),
    ('evaluative_score', 'fairness_p', 'Evaluative x Fairness'),
    ('evaluative_score', 'loyalty_p', 'Evaluative x Loyalty'),
]

for col1, col2, label in key_pairs:
    rho, p = stats.spearmanr(valid[col1].dropna(), valid[col2].dropna())
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    add(f"- {label}: rho={rho:.3f}, p={p:.2e} {sig}")
add("")

# ============================================================
# TABLE 6: Confidence distribution by classification
# ============================================================
add("## Table 6: Confidence Distribution by Classification")
add("")
add("| Classification | Mean | Median | SD | Min | Max | N |")
add("|----------------|-----:|-------:|---:|----:|----:|--:|")

for cls in CLASS_ORDER:
    g = valid[valid['classification'] == cls]['confidence']
    add(f"| {cls} | {g.mean():.3f} | {g.median():.3f} | {g.std():.3f} | "
        f"{g.min():.2f} | {g.max():.2f} | {len(g):,} |")
add("")

# Test: is DELEGATIVE confidence lower than EVALUATIVE?
u_conf, p_conf = stats.mannwhitneyu(
    valid[valid['classification'] == 'DELEGATIVE']['confidence'].dropna(),
    valid[valid['classification'] == 'EVALUATIVE']['confidence'].dropna(),
    alternative='less'  # testing if DELEGATIVE < EVALUATIVE
)
add(f"One-sided test (DELEGATIVE confidence < EVALUATIVE confidence): "
    f"U={u_conf:,.0f}, p={p_conf:.2e}")
add("")

# ============================================================
# TABLE 7: Cross-tabulation
# ============================================================
add("## Table 7: Product x Classification x Confidence Level")
add("")

def conf_level(c):
    if pd.isna(c):
        return 'unknown'
    if c > 0.7:
        return 'high'
    elif c >= 0.4:
        return 'medium'
    else:
        return 'low'

valid['conf_level'] = valid['confidence'].apply(conf_level)

add("| Product | Classification | High (>0.7) | Medium (0.4-0.7) | Low (<0.4) |")
add("|---------|----------------|----------:|----------------:|-----------:|")

for prod in PRODUCT_ORDER:
    for cls in CLASS_ORDER:
        g = valid[(valid['product_group'] == prod) & (valid['classification'] == cls)]
        high = len(g[g['conf_level'] == 'high'])
        med = len(g[g['conf_level'] == 'medium'])
        low = len(g[g['conf_level'] == 'low'])
        total = high + med + low
        if total > 0:
            add(f"| {prod} | {cls} | {high} ({high/total*100:.0f}%) | "
                f"{med} ({med/total*100:.0f}%) | {low} ({low/total*100:.0f}%) |")
        else:
            add(f"| {prod} | {cls} | 0 | 0 | 0 |")
add("")

# ============================================================
# SAVE
# ============================================================
summary_text = "\n".join(summary_lines)
with open(SUMMARY_PATH, 'w') as f:
    f.write(summary_text)

print(f"\n{'=' * 70}")
print(f"Analysis saved to: {SUMMARY_PATH}")
print(f"Table CSVs in: {TABLES_DIR}")
print(f"{'=' * 70}")
print("\nSTEP 2 COMPLETE — AWAITING YOUR REVIEW")
