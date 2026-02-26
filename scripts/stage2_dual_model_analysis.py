"""
Dual-model (Sonnet + GPT-4o) analysis of 9,000 CFPB narrative classifications.
Produces numbered tables for the paper and saves intermediate CSVs.
"""

import pandas as pd
import numpy as np
from scipy import stats
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────
SONNET_PATH = "/workspaces/HumanxAI-2026/output/cfpb_classified_9000.csv"
GPT4O_PATH = "/workspaces/HumanxAI-2026/output/cfpb_gpt4o_classified_9000.csv"
EMFD_PATH = "/workspaces/HumanxAI-2026/output/cfpb_emfd_scores.csv"
OUT_DIR = "/workspaces/HumanxAI-2026/output"
REPORT_PATH = f"{OUT_DIR}/cfpb_dual_model_analysis.md"

PRODUCT_ORDER = ['mortgage', 'checking_savings', 'credit_card']
CLASS_ORDER = ['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE']
EMFD_FOUNDATIONS = ['care_p', 'fairness_p', 'loyalty_p', 'authority_p', 'sanctity_p']
EMFD_LABELS = {'care_p': 'Care', 'fairness_p': 'Fairness', 'loyalty_p': 'Loyalty',
               'authority_p': 'Authority', 'sanctity_p': 'Sanctity'}


def cohens_d(a, b):
    na, nb = len(a), len(b)
    pooled_std = np.sqrt(((na - 1) * a.std()**2 + (nb - 1) * b.std()**2) / (na + nb - 2))
    return (a.mean() - b.mean()) / pooled_std if pooled_std > 0 else 0.0


def cohens_kappa(matrix):
    """Cohen's kappa from a confusion matrix (numpy array)."""
    n = matrix.sum()
    po = np.diag(matrix).sum() / n
    row_sums = matrix.sum(axis=1)
    col_sums = matrix.sum(axis=0)
    pe = (row_sums * col_sums).sum() / n**2
    return (po - pe) / (1 - pe) if (1 - pe) != 0 else 0.0


def fmt_p(p):
    if p < 0.001:
        return f"{p:.2e}"
    elif p < 0.01:
        return f"{p:.4f}"
    else:
        return f"{p:.3f}"


def stars(p):
    if p < 0.001: return "***"
    if p < 0.01: return "**"
    if p < 0.05: return "*"
    return ""


# ── Load data ──────────────────────────────────────────────────────────
print("Loading data...")
sonnet = pd.read_csv(SONNET_PATH, dtype={'complaint_id': 'int64'})
gpt4o = pd.read_csv(GPT4O_PATH, dtype={'complaint_id': 'int64'})
emfd = pd.read_csv(EMFD_PATH, dtype={'complaint_id': 'int64'})

print(f"  Sonnet: {len(sonnet)} rows")
print(f"  GPT-4o: {len(gpt4o)} rows")
print(f"  eMFD:   {len(emfd)} rows")

# Standardize column names for merge
sonnet_cols = sonnet[['complaint_id', 'product_group', 'classification', 'confidence',
                       'delegative_score', 'evaluative_score']].copy()
sonnet_cols.columns = ['complaint_id', 'product_group', 's_class', 's_conf',
                        's_deleg', 's_eval']

gpt4o_cols = gpt4o[['complaint_id', 'product_group', 'classification', 'confidence',
                      'delegative_score', 'evaluative_score']].copy()
gpt4o_cols.columns = ['complaint_id', 'product_group', 'g_class', 'g_conf',
                        'g_deleg', 'g_eval']

# Merge
df = sonnet_cols.merge(gpt4o_cols[['complaint_id', 'g_class', 'g_conf', 'g_deleg', 'g_eval']],
                       on='complaint_id', how='inner')
df = df.merge(emfd, on='complaint_id', how='left')
print(f"  Merged: {len(df)} rows")

# Filter out parse errors from either model
valid_classes = set(CLASS_ORDER)
df_valid = df[(df['s_class'].isin(valid_classes)) & (df['g_class'].isin(valid_classes))].copy()
print(f"  Valid (no parse errors): {len(df_valid)} rows")

report_lines = []
def W(line=""):
    report_lines.append(line)


# ======================================================================
# TABLE 1: GPT-4o Classification Distribution by Product Type
# ======================================================================
W("# Dual-Model Classification Analysis: Sonnet & GPT-4o (N=9,000)")
W()
W("---")
W()
W("## Table 1: GPT-4o Classification Distribution by Product Type")
W()

t1_data = []
for prod in PRODUCT_ORDER:
    subset = df_valid[df_valid['product_group'] == prod]
    n = len(subset)
    row = {'Product': prod}
    for cls in CLASS_ORDER:
        count = (subset['g_class'] == cls).sum()
        pct = count / n * 100 if n > 0 else 0
        row[cls] = f"{count:,} ({pct:.1f}%)"
    row['Total'] = f"{n:,}"
    t1_data.append(row)

# Total row
total_n = len(df_valid)
total_row = {'Product': '**Total**'}
for cls in CLASS_ORDER:
    count = (df_valid['g_class'] == cls).sum()
    pct = count / total_n * 100
    total_row[cls] = f"**{count:,} ({pct:.1f}%)**"
total_row['Total'] = f"**{total_n:,}**"
t1_data.append(total_row)

W("| Product | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |")
W("|---------|----------:|----------:|---------------:|------:|")
for row in t1_data:
    W(f"| {row['Product']} | {row['EVALUATIVE']} | {row['DELEGATIVE']} | {row['UNCLASSIFIABLE']} | {row['Total']} |")
W()

# ======================================================================
# TABLE 2: GPT-4o Continuous Scores by Product Type
# ======================================================================
W("## Table 2: GPT-4o Continuous Scores by Product Type")
W()
W("| Product | Delegative Score | Evaluative Score |")
W("|---------|---------------:|----------------:|")

for prod in PRODUCT_ORDER:
    s = df_valid[df_valid['product_group'] == prod]
    W(f"| {prod} | {s['g_deleg'].mean():.3f} (SD={s['g_deleg'].std():.3f}) "
      f"| {s['g_eval'].mean():.3f} (SD={s['g_eval'].std():.3f}) |")

W(f"| **Overall** | {df_valid['g_deleg'].mean():.3f} (SD={df_valid['g_deleg'].std():.3f}) "
  f"| {df_valid['g_eval'].mean():.3f} (SD={df_valid['g_eval'].std():.3f}) |")
W()

# Mann-Whitney comparisons
comparisons = [('mortgage', 'credit_card'), ('mortgage', 'checking_savings')]
W("### Cross-Product Comparisons")
W()
for prod_a, prod_b in comparisons:
    W(f"**{prod_a} vs {prod_b}:**")
    a = df_valid[df_valid['product_group'] == prod_a]
    b = df_valid[df_valid['product_group'] == prod_b]
    for score, label in [('g_deleg', 'Delegative'), ('g_eval', 'Evaluative')]:
        u, p = stats.mannwhitneyu(a[score], b[score], alternative='two-sided')
        d = cohens_d(a[score], b[score])
        W(f"- {label}: {prod_a} mean={a[score].mean():.3f}, {prod_b} mean={b[score].mean():.3f}, "
          f"U={u:,.0f}, p={fmt_p(p)} {stars(p)}, Cohen's d={d:.3f}")
    W()

# ======================================================================
# TABLE 3: Dual-Model Concordance (3×3 Confusion Matrix)
# ======================================================================
W("## Table 3: Dual-Model Concordance Table (Sonnet × GPT-4o)")
W()

conf_matrix = np.zeros((3, 3), dtype=int)
for i, s_cls in enumerate(CLASS_ORDER):
    for j, g_cls in enumerate(CLASS_ORDER):
        conf_matrix[i, j] = ((df_valid['s_class'] == s_cls) & (df_valid['g_class'] == g_cls)).sum()

W("| Sonnet \\ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Sonnet Total |")
W("|-----------------|----------:|----------:|---------------:|------------:|")
for i, s_cls in enumerate(CLASS_ORDER):
    row_total = conf_matrix[i].sum()
    cells = " | ".join(f"{conf_matrix[i, j]:,}" for j in range(3))
    W(f"| {s_cls} | {cells} | {row_total:,} |")

col_totals = conf_matrix.sum(axis=0)
W(f"| **GPT-4o Total** | {col_totals[0]:,} | {col_totals[1]:,} | {col_totals[2]:,} | {conf_matrix.sum():,} |")
W()

agree = np.diag(conf_matrix).sum()
agree_rate = agree / conf_matrix.sum() * 100
kappa = cohens_kappa(conf_matrix)
W(f"**Overall agreement:** {agree:,}/{conf_matrix.sum():,} ({agree_rate:.1f}%)")
W(f"**Cohen's Kappa:** {kappa:.3f}")
W()

# ======================================================================
# TABLE 4: Concordant-Only Classification Distribution by Product Type
# ======================================================================
W("## Table 4: Concordant-Only Classification Distribution by Product Type")
W()

df_valid['concordant'] = df_valid['s_class'] == df_valid['g_class']
concordant = df_valid[df_valid['concordant']].copy()
discordant = df_valid[~df_valid['concordant']].copy()

W(f"**Concordant narratives:** {len(concordant):,} ({len(concordant)/len(df_valid)*100:.1f}%)")
W(f"**Discordant narratives:** {len(discordant):,} ({len(discordant)/len(df_valid)*100:.1f}%)")
W()

# Concordance by product
W("**Concordance by product type:**")
W()
W("| Product | Concordant | Discordant | Agreement Rate |")
W("|---------|----------:|----------:|--------------:|")
for prod in PRODUCT_ORDER:
    s = df_valid[df_valid['product_group'] == prod]
    c = s['concordant'].sum()
    d = len(s) - c
    W(f"| {prod} | {c:,} | {d:,} | {c/len(s)*100:.1f}% |")
W()

# Distribution table for concordant only
W("**Classification distribution (concordant cases only):**")
W()
W("| Product | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |")
W("|---------|----------:|----------:|---------------:|------:|")

t4_data = []
for prod in PRODUCT_ORDER:
    subset = concordant[concordant['product_group'] == prod]
    n = len(subset)
    row = {'Product': prod}
    for cls in CLASS_ORDER:
        count = (subset['s_class'] == cls).sum()
        pct = count / n * 100 if n > 0 else 0
        row[cls] = f"{count:,} ({pct:.1f}%)"
    row['Total'] = f"{n:,}"
    t4_data.append(row)

total_conc = len(concordant)
total_row = {'Product': '**Total**'}
for cls in CLASS_ORDER:
    count = (concordant['s_class'] == cls).sum()
    pct = count / total_conc * 100
    total_row[cls] = f"**{count:,} ({pct:.1f}%)**"
total_row['Total'] = f"**{total_conc:,}**"
t4_data.append(total_row)

for row in t4_data:
    W(f"| {row['Product']} | {row['EVALUATIVE']} | {row['DELEGATIVE']} | {row['UNCLASSIFIABLE']} | {row['Total']} |")
W()

# ======================================================================
# TABLE 5: Concordant-Only Continuous Scores (Averaged)
# ======================================================================
W("## Table 5: Concordant-Only Continuous Scores by Product Type (Averaged)")
W()

concordant['avg_deleg'] = (concordant['s_deleg'] + concordant['g_deleg']) / 2
concordant['avg_eval'] = (concordant['s_eval'] + concordant['g_eval']) / 2

W("| Product | Avg Delegative Score | Avg Evaluative Score |")
W("|---------|--------------------:|--------------------:|")
for prod in PRODUCT_ORDER:
    s = concordant[concordant['product_group'] == prod]
    W(f"| {prod} | {s['avg_deleg'].mean():.3f} (SD={s['avg_deleg'].std():.3f}) "
      f"| {s['avg_eval'].mean():.3f} (SD={s['avg_eval'].std():.3f}) |")

W(f"| **Overall** | {concordant['avg_deleg'].mean():.3f} (SD={concordant['avg_deleg'].std():.3f}) "
  f"| {concordant['avg_eval'].mean():.3f} (SD={concordant['avg_eval'].std():.3f}) |")
W()

W("### Cross-Product Comparisons (concordant, averaged scores)")
W()
for prod_a, prod_b in comparisons:
    W(f"**{prod_a} vs {prod_b}:**")
    a = concordant[concordant['product_group'] == prod_a]
    b = concordant[concordant['product_group'] == prod_b]
    for score, label in [('avg_deleg', 'Delegative'), ('avg_eval', 'Evaluative')]:
        u, p = stats.mannwhitneyu(a[score], b[score], alternative='two-sided')
        d = cohens_d(a[score], b[score])
        W(f"- {label}: {prod_a} mean={a[score].mean():.3f}, {prod_b} mean={b[score].mean():.3f}, "
          f"U={u:,.0f}, p={fmt_p(p)} {stars(p)}, Cohen's d={d:.3f}")
    W()

# ======================================================================
# TABLE 6: Cross-Product Pattern Comparison
# ======================================================================
W("## Table 6: Cross-Product Pattern Comparison — DELEGATIVE Proportion")
W()
W("| Product | Sonnet | GPT-4o | Concordant | Predicted Order |")
W("|---------|-------:|-------:|----------:|:--------------:|")

# Check monotonic ordering: mortgage > checking_savings > credit_card
def get_deleg_pcts(data, class_col):
    pcts = {}
    for prod in PRODUCT_ORDER:
        s = data[data['product_group'] == prod]
        pcts[prod] = (s[class_col] == 'DELEGATIVE').sum() / len(s) * 100 if len(s) > 0 else 0
    return pcts

sonnet_pcts = get_deleg_pcts(df_valid, 's_class')
gpt4o_pcts = get_deleg_pcts(df_valid, 'g_class')
conc_pcts = get_deleg_pcts(concordant, 's_class')  # s_class == g_class for concordant

def check_ordering(pcts):
    return pcts['mortgage'] > pcts['checking_savings'] > pcts['credit_card']

for prod in PRODUCT_ORDER:
    W(f"| {prod} | {sonnet_pcts[prod]:.1f}% | {gpt4o_pcts[prod]:.1f}% | {conc_pcts[prod]:.1f}% | |")

W()
W(f"**Monotonic ordering (mort > check > cc) holds?**")
W(f"- Sonnet: {'Yes' if check_ordering(sonnet_pcts) else 'No'} "
  f"({sonnet_pcts['mortgage']:.1f}% > {sonnet_pcts['checking_savings']:.1f}% > {sonnet_pcts['credit_card']:.1f}%)")
W(f"- GPT-4o: {'Yes' if check_ordering(gpt4o_pcts) else 'No'} "
  f"({gpt4o_pcts['mortgage']:.1f}% > {gpt4o_pcts['checking_savings']:.1f}% > {gpt4o_pcts['credit_card']:.1f}%)")
W(f"- Concordant: {'Yes' if check_ordering(conc_pcts) else 'No'} "
  f"({conc_pcts['mortgage']:.1f}% > {conc_pcts['checking_savings']:.1f}% > {conc_pcts['credit_card']:.1f}%)")
W()

# ======================================================================
# TABLE 7: Continuous Score Correlations Between Models
# ======================================================================
W("## Table 7: Continuous Score Correlations Between Models (N={:,})".format(len(df_valid)))
W()

W("| Score Pair | Pearson r | p-value | Spearman rho | p-value |")
W("|------------|----------:|--------:|-------------:|--------:|")

for s_col, g_col, label in [('s_deleg', 'g_deleg', 'Delegative'),
                              ('s_eval', 'g_eval', 'Evaluative')]:
    pr, pp = stats.pearsonr(df_valid[s_col], df_valid[g_col])
    sr, sp = stats.spearmanr(df_valid[s_col], df_valid[g_col])
    W(f"| {label} (Sonnet vs GPT-4o) | {pr:.3f} | {fmt_p(pp)} {stars(pp)} "
      f"| {sr:.3f} | {fmt_p(sp)} {stars(sp)} |")
W()

# ======================================================================
# TABLE 8: eMFD Correlations — GPT-4o vs Sonnet Side by Side
# ======================================================================
W("## Table 8: eMFD Correlations with Classification Scores (Spearman)")
W()
W("| Foundation | Sonnet Deleg | GPT-4o Deleg | Sonnet Eval | GPT-4o Eval |")
W("|------------|------------:|------------:|-----------:|-----------:|")

for fnd in EMFD_FOUNDATIONS:
    label = EMFD_LABELS[fnd]
    # Sonnet delegative
    sr_sd, sp_sd = stats.spearmanr(df_valid['s_deleg'], df_valid[fnd])
    # GPT-4o delegative
    sr_gd, sp_gd = stats.spearmanr(df_valid['g_deleg'], df_valid[fnd])
    # Sonnet evaluative
    sr_se, sp_se = stats.spearmanr(df_valid['s_eval'], df_valid[fnd])
    # GPT-4o evaluative
    sr_ge, sp_ge = stats.spearmanr(df_valid['g_eval'], df_valid[fnd])

    W(f"| {label} | {sr_sd:.3f} {stars(sp_sd)} | {sr_gd:.3f} {stars(sp_gd)} "
      f"| {sr_se:.3f} {stars(sp_se)} | {sr_ge:.3f} {stars(sp_ge)} |")
W()
W("*Significance: \\*p<.05, \\*\\*p<.01, \\*\\*\\*p<.001*")
W()

# ======================================================================
# TABLE 9: Confidence-Stratified Concordance
# ======================================================================
W("## Table 9: Confidence-Stratified Concordance")
W()

df_valid['avg_conf'] = (df_valid['s_conf'] + df_valid['g_conf']) / 2
tercile_labels = ['Low', 'Medium', 'High']
df_valid['conf_tercile'] = pd.qcut(df_valid['avg_conf'], q=3, labels=tercile_labels)

W("| Confidence Tercile | Range | N | Agreement Rate | Cohen's Kappa |")
W("|-------------------|------:|--:|--------------:|--------------:|")

for tercile in tercile_labels:
    subset = df_valid[df_valid['conf_tercile'] == tercile]
    n = len(subset)
    lo = subset['avg_conf'].min()
    hi = subset['avg_conf'].max()
    agree = (subset['s_class'] == subset['g_class']).sum()
    agree_rate = agree / n * 100 if n > 0 else 0

    # Kappa for this tercile
    m = np.zeros((3, 3), dtype=int)
    for i, s_cls in enumerate(CLASS_ORDER):
        for j, g_cls in enumerate(CLASS_ORDER):
            m[i, j] = ((subset['s_class'] == s_cls) & (subset['g_class'] == g_cls)).sum()
    k = cohens_kappa(m)

    W(f"| {tercile} | {lo:.2f}–{hi:.2f} | {n:,} | {agree_rate:.1f}% | {k:.3f} |")
W()

# ======================================================================
# Save concordant-cases CSV
# ======================================================================
print("Saving concordant cases CSV...")
conc_out = concordant[['complaint_id', 'product_group', 's_class', 'g_class']].copy()
conc_out.columns = ['complaint_id', 'product_group', 'sonnet_classification', 'gpt4o_classification']
conc_out['concordant_classification'] = concordant['s_class'].values
conc_out['avg_delegative_score'] = concordant['avg_deleg'].values
conc_out['avg_evaluative_score'] = concordant['avg_eval'].values

# Add eMFD scores
for fnd in EMFD_FOUNDATIONS:
    conc_out[fnd] = concordant[fnd].values

conc_out.to_csv(f"{OUT_DIR}/cfpb_concordant_classifications.csv", index=False)
print(f"  Saved {len(conc_out)} concordant cases")

# Save full merged dataframe for further analysis
df_valid.to_csv(f"{OUT_DIR}/cfpb_dual_model_merged.csv", index=False)
print(f"  Saved {len(df_valid)} merged rows")

# ======================================================================
# Write report
# ======================================================================
report_text = "\n".join(report_lines)
with open(REPORT_PATH, 'w') as f:
    f.write(report_text)
print(f"\nReport saved to: {REPORT_PATH}")
print("Done.")
