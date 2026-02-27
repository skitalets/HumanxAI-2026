#!/usr/bin/env python3
"""
Pre-Registered Hypothesis Tests (H1–H5) and Exploratory Analyses
AsPredicted #275,531

Input: output/cleaned_matched_data.csv
Output: Multiple CSV files in output/ + stdout summaries
"""

import sys
import warnings
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from itertools import combinations

warnings.filterwarnings('ignore', category=FutureWarning)

# Try to import pingouin for Cronbach's alpha and effect sizes
try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False

# =============================================================================
# LOAD DATA
# =============================================================================
DATA_PATH = "output/cleaned_matched_data.csv"
OUTPUT_DIR = "output/"

df = pd.read_csv(DATA_PATH)
print(f"{'='*80}")
print(f"PRE-REGISTERED HYPOTHESIS TESTS (H1–H5) AND EXPLORATORY ANALYSES")
print(f"AsPredicted #275,531")
print(f"{'='*80}")
print(f"\nLoaded {len(df)} rows from {DATA_PATH}")
print(f"Columns: {list(df.columns)}\n")

# =============================================================================
# LIKERT CODING
# =============================================================================
LIKERT_MAP = {
    'strongly disagree': 1,
    'moderately disagree': 2,
    'somewhat disagree': 3,
    'neither agree nor disagree': 4,
    'somewhat agree': 5,
    'moderately agree': 6,
    'strongly agree': 7,
}

likert_cols = ['B1_1', 'B1_2', 'B1_3', 'B1_4', 'B1_5', 'D1_1', 'D1_2', 'D1_3', 'D1_4', 'D6']

print("--- LIKERT CODING ---")
for col in likert_cols:
    raw = df[col].copy()
    mapped = raw.str.strip().str.lower().map(LIKERT_MAP)
    unmapped = raw[mapped.isna() & raw.notna()]
    if len(unmapped) > 0:
        print(f"  WARNING: {col} has {len(unmapped)} unmapped values: {unmapped.unique()}")
    df[f'{col}_num'] = mapped

# Verify coding direction
print("\nLikert coding verification (means by condition):")
for col in ['B1_1', 'B1_2', 'B1_3', 'B1_4', 'B1_5']:
    means = df.groupby('condition')[f'{col}_num'].mean()
    print(f"  {col}: A={means.get('A', np.nan):.2f}, B={means.get('B', np.nan):.2f}, C={means.get('C', np.nan):.2f}")

# =============================================================================
# COMPOSITE VARIABLES
# =============================================================================
print("\n--- COMPOSITE VARIABLES ---")

df['evaluative_trust'] = df[['B1_1_num', 'B1_2_num']].mean(axis=1)
df['delegative_trust'] = df[['B1_3_num', 'B1_4_num', 'B1_5_num']].mean(axis=1)
df['betrayal'] = df['D1_1_num']
df['disappointment'] = df['D1_2_num']
df['betrayal_premium'] = df['D1_1_num'] - df['D1_2_num']
df['general_exit'] = df['D1_3_num']
df['algorithm_aversion'] = df['D1_4_num']

print(f"  Evaluative trust (B1_1, B1_2): M={df['evaluative_trust'].mean():.3f}, SD={df['evaluative_trust'].std():.3f}")
print(f"  Delegative trust (B1_3, B1_4, B1_5): M={df['delegative_trust'].mean():.3f}, SD={df['delegative_trust'].std():.3f}")
print(f"  Betrayal premium (D1_1 - D1_2): M={df['betrayal_premium'].mean():.3f}, SD={df['betrayal_premium'].std():.3f}")

# =============================================================================
# FINANCIAL LITERACY
# =============================================================================
print("\n--- FINANCIAL LITERACY ---")

df['FL1_correct'] = (df['FL1'].str.strip() == 'More than $102').astype(int)
df['FL2_correct'] = (df['FL2'].str.strip() == 'Less than today').astype(int)
df['FL3_correct'] = (df['FL3'].str.strip() == 'False').astype(int)
df['fin_lit_score'] = df['FL1_correct'] + df['FL2_correct'] + df['FL3_correct']

fl_median = df['fin_lit_score'].median()
df['fin_lit_high'] = (df['fin_lit_score'] >= fl_median).astype(int)
n_high = df['fin_lit_high'].sum()
n_low = len(df) - n_high

print(f"  FL1 correct: {df['FL1_correct'].sum()} ({df['FL1_correct'].mean()*100:.1f}%)")
print(f"  FL2 correct: {df['FL2_correct'].sum()} ({df['FL2_correct'].mean()*100:.1f}%)")
print(f"  FL3 correct: {df['FL3_correct'].sum()} ({df['FL3_correct'].mean()*100:.1f}%)")
print(f"  Financial literacy score: M={df['fin_lit_score'].mean():.2f}, SD={df['fin_lit_score'].std():.2f}")
print(f"  Median split: median={fl_median}, High={n_high}, Low={n_low}")

# =============================================================================
# CHECK VARIABLES
# =============================================================================
print("\n--- CHECK VARIABLES ---")

df['attention_pass'] = df['D6'].str.strip().str.lower().eq('somewhat disagree').astype(int)
df['comprehension_pass'] = df['C2'].str.strip().eq('WealthPath performed worse than the market').astype(int)

print(f"  Attention check pass: {df['attention_pass'].sum()} ({df['attention_pass'].mean()*100:.1f}%)")
print(f"  Comprehension check pass: {df['comprehension_pass'].sum()} ({df['comprehension_pass'].mean()*100:.1f}%)")

# =============================================================================
# COVARIATES
# =============================================================================
print("\n--- COVARIATES ---")

# Age
df['age'] = pd.to_numeric(df['Age'], errors='coerce')
# Also check D1 column for age (the prompt says "Column D1 (numeric, years)")
# Looking at data, D1 appears to be the age from Qualtrics, Age from Prolific
# Use Age column (from Prolific) as it's cleaner
print(f"  Age: M={df['age'].mean():.1f}, SD={df['age'].std():.1f}, range={df['age'].min()}-{df['age'].max()}")

# Robo-advisor experience
df['robo_experience'] = df['D5'].str.lower().str.contains('robo-advisor', na=False).astype(int)
print(f"  Robo-advisor experience: {df['robo_experience'].sum()} ({df['robo_experience'].mean()*100:.1f}%)")

# Condition dummies (C as reference)
df['cond_A'] = (df['condition'] == 'A').astype(int)
df['cond_B'] = (df['condition'] == 'B').astype(int)

print(f"  Conditions: A={df['cond_A'].sum()}, B={df['cond_B'].sum()}, C={(df['condition']=='C').sum()}")

# =============================================================================
# DESCRIPTIVE STATISTICS
# =============================================================================
print(f"\n{'='*80}")
print("DESCRIPTIVE STATISTICS")
print(f"{'='*80}")

# 1. Sample summary
print(f"\n--- 1. SAMPLE SUMMARY ---")
print(f"  Overall N: {len(df)}")
print(f"  N per condition: A={sum(df['condition']=='A')}, B={sum(df['condition']=='B')}, C={sum(df['condition']=='C')}")
print(f"  Mean age: {df['age'].mean():.1f} (SD={df['age'].std():.1f})")

print(f"\n  Gender distribution:")
gender_counts = df['Sex'].value_counts()
for g, n in gender_counts.items():
    print(f"    {g}: {n} ({n/len(df)*100:.1f}%)")

if 'D4' in df.columns:
    print(f"\n  Education distribution (D4):")
    edu_counts = df['D4'].value_counts()
    for e, n in edu_counts.items():
        print(f"    {e}: {n} ({n/len(df)*100:.1f}%)")

if 'D3' in df.columns:
    print(f"\n  Income distribution (D3):")
    inc_counts = df['D3'].value_counts()
    for i, n in inc_counts.items():
        print(f"    {i}: {n} ({n/len(df)*100:.1f}%)")

# 2. Condition balance check
print(f"\n--- 2. CONDITION BALANCE CHECK ---")

# Age by condition
print(f"\n  Age by condition:")
for cond in ['A', 'B', 'C']:
    subset = df[df['condition'] == cond]
    print(f"    {cond}: M={subset['age'].mean():.1f}, SD={subset['age'].std():.1f}")
f_age, p_age = stats.f_oneway(
    df[df['condition']=='A']['age'].dropna(),
    df[df['condition']=='B']['age'].dropna(),
    df[df['condition']=='C']['age'].dropna()
)
print(f"    ANOVA: F={f_age:.3f}, p={p_age:.4f} {'*** IMBALANCE' if p_age < .05 else '(balanced)'}")

# Financial literacy by condition
print(f"\n  Financial literacy by condition:")
for cond in ['A', 'B', 'C']:
    subset = df[df['condition'] == cond]
    print(f"    {cond}: M={subset['fin_lit_score'].mean():.2f}, SD={subset['fin_lit_score'].std():.2f}")
f_fl, p_fl = stats.f_oneway(
    df[df['condition']=='A']['fin_lit_score'].dropna(),
    df[df['condition']=='B']['fin_lit_score'].dropna(),
    df[df['condition']=='C']['fin_lit_score'].dropna()
)
print(f"    ANOVA: F={f_fl:.3f}, p={p_fl:.4f} {'*** IMBALANCE' if p_fl < .05 else '(balanced)'}")

# Robo-advisor experience by condition
print(f"\n  Robo-advisor experience by condition:")
for cond in ['A', 'B', 'C']:
    subset = df[df['condition'] == cond]
    print(f"    {cond}: {subset['robo_experience'].mean()*100:.1f}%")
# Chi-square
ct_robo = pd.crosstab(df['condition'], df['robo_experience'])
chi2_robo, p_robo, dof_robo, _ = stats.chi2_contingency(ct_robo)
print(f"    Chi-square: χ²={chi2_robo:.3f}, df={dof_robo}, p={p_robo:.4f} {'*** IMBALANCE' if p_robo < .05 else '(balanced)'}")

# Gender by condition
print(f"\n  Gender by condition:")
ct_gender = pd.crosstab(df['condition'], df['Sex'])
print(ct_gender)
chi2_gen, p_gen, dof_gen, _ = stats.chi2_contingency(ct_gender)
print(f"    Chi-square: χ²={chi2_gen:.3f}, df={dof_gen}, p={p_gen:.4f} {'*** IMBALANCE' if p_gen < .05 else '(balanced)'}")

# 3. Dependent variable descriptives
print(f"\n--- 3. DEPENDENT VARIABLE DESCRIPTIVES ---")
dvs = ['evaluative_trust', 'delegative_trust', 'betrayal', 'disappointment',
       'betrayal_premium', 'general_exit', 'algorithm_aversion']

desc_rows = []
print(f"\n  {'Variable':<22} {'Overall M(SD)':<16} {'A M(SD)':<16} {'B M(SD)':<16} {'C M(SD)':<16}")
print(f"  {'-'*86}")
for dv in dvs:
    overall_m = df[dv].mean()
    overall_sd = df[dv].std()
    row = {'Variable': dv, 'Overall_M': overall_m, 'Overall_SD': overall_sd, 'Overall_N': df[dv].notna().sum()}
    line = f"  {dv:<22} {overall_m:.2f} ({overall_sd:.2f})  "
    for cond in ['A', 'B', 'C']:
        subset = df[df['condition'] == cond][dv]
        m, sd = subset.mean(), subset.std()
        row[f'{cond}_M'] = m
        row[f'{cond}_SD'] = sd
        row[f'{cond}_N'] = subset.notna().sum()
        line += f"  {m:.2f} ({sd:.2f})  "
    print(line)
    desc_rows.append(row)

desc_df = pd.DataFrame(desc_rows)
desc_df.to_csv(f"{OUTPUT_DIR}descriptive_tables.csv", index=False)
print(f"\n  Saved: {OUTPUT_DIR}descriptive_tables.csv")

# 4. Reliability (Cronbach's alpha)
print(f"\n--- 4. RELIABILITY ---")

def cronbachs_alpha(items_df):
    """Compute Cronbach's alpha for a set of items."""
    items = items_df.dropna()
    k = items.shape[1]
    if k < 2:
        return np.nan
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    alpha = (k / (k - 1)) * (1 - item_vars.sum() / total_var)
    return alpha

eval_items = df[['B1_1_num', 'B1_2_num']]
deleg_items = df[['B1_3_num', 'B1_4_num', 'B1_5_num']]

alpha_eval = cronbachs_alpha(eval_items)
alpha_deleg = cronbachs_alpha(deleg_items)

print(f"  Evaluative trust (B1_1, B1_2): Cronbach's α = {alpha_eval:.3f}")
print(f"  Delegative trust (B1_3, B1_4, B1_5): Cronbach's α = {alpha_deleg:.3f}")

if HAS_PINGOUIN:
    # Cross-check with pingouin
    alpha_eval_pg = pg.cronbach_alpha(eval_items.dropna())
    alpha_deleg_pg = pg.cronbach_alpha(deleg_items.dropna())
    print(f"  (pingouin check) Evaluative: α = {alpha_eval_pg[0]:.3f}, 95% CI [{alpha_eval_pg[1][0]:.3f}, {alpha_eval_pg[1][1]:.3f}]")
    print(f"  (pingouin check) Delegative: α = {alpha_deleg_pg[0]:.3f}, 95% CI [{alpha_deleg_pg[1][0]:.3f}, {alpha_deleg_pg[1][1]:.3f}]")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def eta_squared_from_anova(f_stat, df_between, df_within):
    """Compute eta-squared from F, df_between, df_within."""
    return (f_stat * df_between) / (f_stat * df_between + df_within)

def tukey_hsd(data, groups, alpha=0.05):
    """Perform Tukey HSD using scipy."""
    unique_groups = sorted(data.groupby(groups).groups.keys())
    group_data = [data[data[groups] == g].dropna() for g in unique_groups]

    # Use scipy Tukey HSD
    result = stats.tukey_hsd(*[g.values for g in group_data])
    return result, unique_groups

def run_anova_with_tukey(df_in, dv_col, group_col='condition', label=''):
    """Run one-way ANOVA with Tukey HSD and report."""
    groups = sorted(df_in[group_col].unique())
    group_data = [df_in[df_in[group_col] == g][dv_col].dropna() for g in groups]

    # One-way ANOVA
    f_stat, p_val = stats.f_oneway(*group_data)
    n_total = sum(len(g) for g in group_data)
    k = len(groups)
    df_between = k - 1
    df_within = n_total - k
    eta_sq = eta_squared_from_anova(f_stat, df_between, df_within)

    print(f"\n  One-way ANOVA: {label}")
    print(f"    F({df_between}, {df_within}) = {f_stat:.4f}, p = {p_val:.6f}, η² = {eta_sq:.4f}")

    # Group means
    for g, d in zip(groups, group_data):
        print(f"    {g}: M={d.mean():.3f}, SD={d.std():.3f}, N={len(d)}")

    # Tukey HSD
    print(f"\n    Tukey HSD pairwise comparisons:")
    tukey_result = stats.tukey_hsd(*[d.values for d in group_data])

    pairs = list(combinations(range(k), 2))
    for i, j in pairs:
        mean_diff = group_data[i].mean() - group_data[j].mean()
        p_tukey = tukey_result.pvalue[i, j]
        # Confidence interval from tukey_result
        ci = tukey_result.confidence_interval(confidence_level=0.95)
        ci_low = ci.low[i, j]
        ci_high = ci.high[i, j]
        sig = '*' if p_tukey < .05 else ''
        print(f"    {groups[i]} vs {groups[j]}: Δ = {mean_diff:.3f}, p = {p_tukey:.6f}, 95% CI [{ci_low:.3f}, {ci_high:.3f}] {sig}")

    return f_stat, p_val, df_between, df_within, eta_sq

def run_ols_regression(df_in, formula, dv_name):
    """Run OLS regression and return results + formatted table."""
    # Drop rows with missing values in used columns
    model = smf.ols(formula, data=df_in).fit()

    print(f"\n  OLS Regression: DV = {dv_name}")
    print(f"    R² = {model.rsquared:.4f}, Adjusted R² = {model.rsquared_adj:.4f}")
    print(f"    F({model.df_model:.0f}, {model.df_resid:.0f}) = {model.fvalue:.4f}, p = {model.f_pvalue:.6f}")
    print(f"    N = {int(model.nobs)}")

    # Build table
    table_rows = []
    print(f"\n    {'Predictor':<30} {'B':>8} {'SE':>8} {'β':>8} {'t':>8} {'p':>10} {'95% CI':>20}")
    print(f"    {'-'*93}")

    # Compute standardized betas using the design matrix
    y_std = model.model.endog.std()
    exog_array = model.model.exog  # N × k design matrix
    exog_names = model.model.exog_names

    for idx, name in enumerate(model.params.index):
        b = model.params[name]
        se = model.bse[name]
        t = model.tvalues[name]
        p = model.pvalues[name]
        ci = model.conf_int().loc[name]

        # Compute standardized beta from the design matrix column
        if name == 'Intercept':
            beta_std = np.nan
        else:
            col_idx = exog_names.index(name)
            x_std = exog_array[:, col_idx].std()
            if x_std > 0 and y_std > 0:
                beta_std = b * (x_std / y_std)
            else:
                beta_std = np.nan

        beta_str = f"{beta_std:.3f}" if pd.notna(beta_std) else "—"
        print(f"    {name:<30} {b:>8.3f} {se:>8.3f} {beta_str:>8} {t:>8.3f} {p:>10.6f} [{ci[0]:>8.3f}, {ci[1]:>8.3f}]")

        table_rows.append({
            'Predictor': name,
            'B': round(b, 4),
            'SE': round(se, 4),
            'Standardized_Beta': round(beta_std, 4) if pd.notna(beta_std) else '',
            't': round(t, 4),
            'p': round(p, 6),
            'CI_lower': round(ci[0], 4),
            'CI_upper': round(ci[1], 4),
        })

    reg_table = pd.DataFrame(table_rows)
    # Add model summary row
    summary_row = pd.DataFrame([{
        'Predictor': 'MODEL SUMMARY',
        'B': '',
        'SE': '',
        'Standardized_Beta': '',
        't': '',
        'p': '',
        'CI_lower': f'R²={model.rsquared:.4f}',
        'CI_upper': f'Adj R²={model.rsquared_adj:.4f}',
    }])
    reg_table = pd.concat([reg_table, summary_row], ignore_index=True)

    return model, reg_table


# =============================================================================
# H1: TRUST MODE SEPARATION
# =============================================================================
print(f"\n{'='*80}")
print("H1: TRUST MODE SEPARATION")
print("Prediction: Cond A > Cond B on delegative trust; Cond B > Cond A on evaluative trust")
print(f"{'='*80}")

h1a_f, h1a_p, h1a_dfb, h1a_dfw, h1a_eta = run_anova_with_tukey(df, 'delegative_trust', label='(a) Delegative trust')
h1b_f, h1b_p, h1b_dfb, h1b_dfw, h1b_eta = run_anova_with_tukey(df, 'evaluative_trust', label='(b) Evaluative trust')

# Check predictions
mean_deleg_A = df[df['condition']=='A']['delegative_trust'].mean()
mean_deleg_B = df[df['condition']=='B']['delegative_trust'].mean()
mean_eval_A = df[df['condition']=='A']['evaluative_trust'].mean()
mean_eval_B = df[df['condition']=='B']['evaluative_trust'].mean()

h1a_direction = mean_deleg_A > mean_deleg_B
h1b_direction = mean_eval_B > mean_eval_A

print(f"\n  Prediction check (H1a): A > B on delegative? {h1a_direction} (A={mean_deleg_A:.3f}, B={mean_deleg_B:.3f})")
print(f"  Prediction check (H1b): B > A on evaluative? {h1b_direction} (B={mean_eval_B:.3f}, A={mean_eval_A:.3f})")


# =============================================================================
# H2: BETRAYAL PREMIUM
# =============================================================================
print(f"\n{'='*80}")
print("H2: BETRAYAL PREMIUM")
print("Prediction: Condition A > Condition B on betrayal premium (D1_1 - D1_2)")
print(f"{'='*80}")

h2_f, h2_p, h2_dfb, h2_dfw, h2_eta = run_anova_with_tukey(df, 'betrayal_premium', label='Betrayal premium (D1_1 - D1_2)')

# Also report betrayal and disappointment separately
print(f"\n  Betrayal (D1_1) by condition:")
for cond in ['A', 'B', 'C']:
    subset = df[df['condition'] == cond]['betrayal']
    print(f"    {cond}: M={subset.mean():.3f}, SD={subset.std():.3f}")

print(f"\n  Disappointment (D1_2) by condition:")
for cond in ['A', 'B', 'C']:
    subset = df[df['condition'] == cond]['disappointment']
    print(f"    {cond}: M={subset.mean():.3f}, SD={subset.std():.3f}")

mean_bp_A = df[df['condition']=='A']['betrayal_premium'].mean()
mean_bp_B = df[df['condition']=='B']['betrayal_premium'].mean()
h2_direction = mean_bp_A > mean_bp_B
print(f"\n  Prediction check: A > B on betrayal premium? {h2_direction} (A={mean_bp_A:.3f}, B={mean_bp_B:.3f})")


# =============================================================================
# H3: ALGORITHM AVERSION MECHANISM
# =============================================================================
print(f"\n{'='*80}")
print("H3: ALGORITHM AVERSION MECHANISM")
print("Prediction: Evaluative trust (+) predicts alg aversion; delegative trust does not")
print(f"{'='*80}")

# Prepare clean dataset for regressions (drop missing)
reg_cols = ['algorithm_aversion', 'evaluative_trust', 'delegative_trust',
            'cond_A', 'cond_B', 'age', 'fin_lit_score', 'robo_experience',
            'comprehension_pass', 'attention_pass', 'general_exit',
            'condition', 'fin_lit_high']
df_reg = df[reg_cols].copy().dropna(subset=reg_cols[:11])
print(f"  Regression sample N = {len(df_reg)}")

formula_h3 = 'algorithm_aversion ~ evaluative_trust + delegative_trust + cond_A + cond_B + age + fin_lit_score + robo_experience + comprehension_pass + attention_pass'
model_h3, table_h3 = run_ols_regression(df_reg, formula_h3, 'algorithm_aversion')
table_h3.to_csv(f"{OUTPUT_DIR}regression_h3.csv", index=False)
print(f"\n  Saved: {OUTPUT_DIR}regression_h3.csv")

# Check predictions
eval_p = model_h3.pvalues.get('evaluative_trust', np.nan)
deleg_p = model_h3.pvalues.get('delegative_trust', np.nan)
eval_b = model_h3.params.get('evaluative_trust', np.nan)
deleg_b = model_h3.params.get('delegative_trust', np.nan)
h3_eval_sig = eval_p < .05 and eval_b > 0
h3_deleg_nonsig = deleg_p >= .05
print(f"\n  Prediction check: Evaluative trust positive & significant? {h3_eval_sig} (B={eval_b:.3f}, p={eval_p:.4f})")
print(f"  Prediction check: Delegative trust non-significant? {h3_deleg_nonsig} (B={deleg_b:.3f}, p={deleg_p:.4f})")


# =============================================================================
# H4: DELEGATIVE RESILIENCE
# =============================================================================
print(f"\n{'='*80}")
print("H4: DELEGATIVE RESILIENCE")
print("Prediction: Higher delegative trust predicts lower general exit (negative B)")
print(f"{'='*80}")

formula_h4 = 'general_exit ~ delegative_trust + evaluative_trust + cond_A + cond_B + age + fin_lit_score + robo_experience + comprehension_pass + attention_pass'
model_h4, table_h4 = run_ols_regression(df_reg, formula_h4, 'general_exit')
table_h4.to_csv(f"{OUTPUT_DIR}regression_h4.csv", index=False)
print(f"\n  Saved: {OUTPUT_DIR}regression_h4.csv")

deleg_b_h4 = model_h4.params.get('delegative_trust', np.nan)
deleg_p_h4 = model_h4.pvalues.get('delegative_trust', np.nan)
h4_supported = deleg_b_h4 < 0 and deleg_p_h4 < .05
print(f"\n  Prediction check: Delegative trust negative & significant? {h4_supported} (B={deleg_b_h4:.3f}, p={deleg_p_h4:.4f})")


# =============================================================================
# H5: FINANCIAL LITERACY × CONDITION INTERACTION
# =============================================================================
print(f"\n{'='*80}")
print("H5: FINANCIAL LITERACY × CONDITION INTERACTION")
print("Prediction: A vs B difference on delegative trust is LARGER for high-literacy")
print(f"{'='*80}")

formula_h5 = 'delegative_trust ~ cond_A + cond_B + fin_lit_high + cond_A:fin_lit_high + cond_B:fin_lit_high + age + robo_experience + comprehension_pass + attention_pass'
model_h5, table_h5 = run_ols_regression(df_reg, formula_h5, 'delegative_trust')
table_h5.to_csv(f"{OUTPUT_DIR}regression_h5.csv", index=False)
print(f"\n  Saved: {OUTPUT_DIR}regression_h5.csv")

# Simple effects: 2×3 table
print(f"\n  Simple effects: Mean delegative trust by Condition × Financial Literacy")
print(f"  {'Condition':<12} {'Low FL M(SD)':<20} {'High FL M(SD)':<20}")
print(f"  {'-'*52}")
for cond in ['A', 'B', 'C']:
    for fl_label, fl_val in [('Low', 0), ('High', 1)]:
        subset = df_reg[(df_reg['condition'] == cond) & (df_reg['fin_lit_high'] == fl_val)]['delegative_trust']
        if fl_label == 'Low':
            line = f"  {cond:<12} {subset.mean():.3f} ({subset.std():.3f}) N={len(subset):<4}"
        else:
            line += f" {subset.mean():.3f} ({subset.std():.3f}) N={len(subset)}"
            print(line)

# Check interaction
int_A = model_h5.params.get('cond_A:fin_lit_high', np.nan)
int_A_p = model_h5.pvalues.get('cond_A:fin_lit_high', np.nan)
int_B = model_h5.params.get('cond_B:fin_lit_high', np.nan)
int_B_p = model_h5.pvalues.get('cond_B:fin_lit_high', np.nan)
print(f"\n  Interaction cond_A × fin_lit_high: B={int_A:.3f}, p={int_A_p:.4f}")
print(f"  Interaction cond_B × fin_lit_high: B={int_B:.3f}, p={int_B_p:.4f}")


# =============================================================================
# RESULTS SUMMARY TABLE (H1-H5)
# =============================================================================
print(f"\n{'='*80}")
print("H1-H5 RESULTS SUMMARY")
print(f"{'='*80}")

results_rows = []

# H1a
h1a_supported = 'Yes' if (h1a_direction and h1a_p < .05) else ('Partial' if h1a_direction else 'No')
results_rows.append({
    'Hypothesis': 'H1a', 'Test': 'One-way ANOVA', 'DV': 'Delegative trust',
    'Statistic': f'F({h1a_dfb},{h1a_dfw})={h1a_f:.4f}', 'p_value': round(h1a_p, 6),
    'Effect_size': f'η²={h1a_eta:.4f}', 'Prediction_supported': h1a_supported
})

# H1b
h1b_supported = 'Yes' if (h1b_direction and h1b_p < .05) else ('Partial' if h1b_direction else 'No')
results_rows.append({
    'Hypothesis': 'H1b', 'Test': 'One-way ANOVA', 'DV': 'Evaluative trust',
    'Statistic': f'F({h1b_dfb},{h1b_dfw})={h1b_f:.4f}', 'p_value': round(h1b_p, 6),
    'Effect_size': f'η²={h1b_eta:.4f}', 'Prediction_supported': h1b_supported
})

# H2
h2_supported = 'Yes' if (h2_direction and h2_p < .05) else ('Partial' if h2_direction else 'No')
results_rows.append({
    'Hypothesis': 'H2', 'Test': 'One-way ANOVA', 'DV': 'Betrayal premium',
    'Statistic': f'F({h2_dfb},{h2_dfw})={h2_f:.4f}', 'p_value': round(h2_p, 6),
    'Effect_size': f'η²={h2_eta:.4f}', 'Prediction_supported': h2_supported
})

# H3
h3_supported = 'Yes' if (h3_eval_sig and h3_deleg_nonsig) else 'Partial' if (h3_eval_sig or h3_deleg_nonsig) else 'No'
results_rows.append({
    'Hypothesis': 'H3', 'Test': 'OLS Regression', 'DV': 'Algorithm aversion',
    'Statistic': f'F({model_h3.df_model:.0f},{model_h3.df_resid:.0f})={model_h3.fvalue:.4f}',
    'p_value': round(model_h3.f_pvalue, 6),
    'Effect_size': f'R²={model_h3.rsquared:.4f}', 'Prediction_supported': h3_supported
})

# H4
h4_supported_str = 'Yes' if h4_supported else ('Partial' if deleg_b_h4 < 0 else 'No')
results_rows.append({
    'Hypothesis': 'H4', 'Test': 'OLS Regression', 'DV': 'General exit',
    'Statistic': f'F({model_h4.df_model:.0f},{model_h4.df_resid:.0f})={model_h4.fvalue:.4f}',
    'p_value': round(model_h4.f_pvalue, 6),
    'Effect_size': f'R²={model_h4.rsquared:.4f}', 'Prediction_supported': h4_supported_str
})

# H5
h5_interaction_sig = int_A_p < .05 if pd.notna(int_A_p) else False
h5_direction_correct = int_A > 0 if pd.notna(int_A) else False
h5_supported = 'Yes' if (h5_interaction_sig and h5_direction_correct) else ('Partial' if h5_direction_correct else 'No')
results_rows.append({
    'Hypothesis': 'H5', 'Test': 'OLS Regression w/ interaction', 'DV': 'Delegative trust',
    'Statistic': f'F({model_h5.df_model:.0f},{model_h5.df_resid:.0f})={model_h5.fvalue:.4f}',
    'p_value': round(model_h5.f_pvalue, 6),
    'Effect_size': f'R²={model_h5.rsquared:.4f}', 'Prediction_supported': h5_supported
})

results_df = pd.DataFrame(results_rows)
results_df.to_csv(f"{OUTPUT_DIR}h1_h5_results.csv", index=False)
print(results_df.to_string(index=False))
print(f"\n  Saved: {OUTPUT_DIR}h1_h5_results.csv")


# =============================================================================
# ROBUSTNESS CHECKS
# =============================================================================
print(f"\n{'='*80}")
print("ROBUSTNESS CHECKS")
print(f"{'='*80}")

def run_robustness(df_subset, label, primary_results):
    """Run all H1-H5 on a subset and compare to primary results."""
    print(f"\n--- {label} (N={len(df_subset)}) ---")
    results = {}

    # H1a: Delegative trust ANOVA
    groups_h1a = [df_subset[df_subset['condition']==c]['delegative_trust'].dropna() for c in ['A','B','C']]
    if all(len(g) > 1 for g in groups_h1a):
        f, p = stats.f_oneway(*groups_h1a)
        direction = groups_h1a[0].mean() > groups_h1a[1].mean()  # A > B
        results['H1a'] = {'N': len(df_subset), 'direction': 'A > B' if direction else 'B >= A',
                          'significant': p < .05, 'p': p}
    else:
        results['H1a'] = {'N': len(df_subset), 'direction': 'insufficient data', 'significant': False, 'p': np.nan}

    # H1b: Evaluative trust ANOVA
    groups_h1b = [df_subset[df_subset['condition']==c]['evaluative_trust'].dropna() for c in ['A','B','C']]
    if all(len(g) > 1 for g in groups_h1b):
        f, p = stats.f_oneway(*groups_h1b)
        direction = groups_h1b[1].mean() > groups_h1b[0].mean()  # B > A
        results['H1b'] = {'N': len(df_subset), 'direction': 'B > A' if direction else 'A >= B',
                          'significant': p < .05, 'p': p}
    else:
        results['H1b'] = {'N': len(df_subset), 'direction': 'insufficient data', 'significant': False, 'p': np.nan}

    # H2: Betrayal premium ANOVA
    groups_h2 = [df_subset[df_subset['condition']==c]['betrayal_premium'].dropna() for c in ['A','B','C']]
    if all(len(g) > 1 for g in groups_h2):
        f, p = stats.f_oneway(*groups_h2)
        direction = groups_h2[0].mean() > groups_h2[1].mean()  # A > B
        results['H2'] = {'N': len(df_subset), 'direction': 'A > B' if direction else 'B >= A',
                         'significant': p < .05, 'p': p}
    else:
        results['H2'] = {'N': len(df_subset), 'direction': 'insufficient data', 'significant': False, 'p': np.nan}

    # H3: Algorithm aversion regression
    reg_data = df_subset.dropna(subset=['algorithm_aversion', 'evaluative_trust', 'delegative_trust',
                                         'cond_A', 'cond_B', 'age', 'fin_lit_score', 'robo_experience',
                                         'comprehension_pass', 'attention_pass'])
    if len(reg_data) > 15:
        m3 = smf.ols(formula_h3, data=reg_data).fit()
        eval_sig = m3.pvalues.get('evaluative_trust', 1) < .05 and m3.params.get('evaluative_trust', 0) > 0
        deleg_nonsig = m3.pvalues.get('delegative_trust', 0) >= .05
        results['H3'] = {'N': len(reg_data),
                         'direction': f"eval_B={m3.params.get('evaluative_trust',0):.3f}, deleg_B={m3.params.get('delegative_trust',0):.3f}",
                         'significant': eval_sig and deleg_nonsig,
                         'p': m3.pvalues.get('evaluative_trust', np.nan)}
    else:
        results['H3'] = {'N': len(reg_data), 'direction': 'insufficient data', 'significant': False, 'p': np.nan}

    # H4: General exit regression
    if len(reg_data) > 15:
        m4 = smf.ols(formula_h4, data=reg_data).fit()
        deleg_neg = m4.params.get('delegative_trust', 0) < 0
        deleg_sig = m4.pvalues.get('delegative_trust', 1) < .05
        results['H4'] = {'N': len(reg_data),
                         'direction': f"deleg_B={m4.params.get('delegative_trust',0):.3f}",
                         'significant': deleg_neg and deleg_sig,
                         'p': m4.pvalues.get('delegative_trust', np.nan)}
    else:
        results['H4'] = {'N': len(reg_data), 'direction': 'insufficient data', 'significant': False, 'p': np.nan}

    # H5: Interaction regression
    reg_data_h5 = df_subset.dropna(subset=['delegative_trust', 'cond_A', 'cond_B', 'fin_lit_high',
                                             'age', 'robo_experience', 'comprehension_pass', 'attention_pass'])
    if len(reg_data_h5) > 15:
        m5 = smf.ols(formula_h5, data=reg_data_h5).fit()
        int_coef = m5.params.get('cond_A:fin_lit_high', np.nan)
        int_p = m5.pvalues.get('cond_A:fin_lit_high', np.nan)
        results['H5'] = {'N': len(reg_data_h5),
                         'direction': f"int_B={int_coef:.3f}" if pd.notna(int_coef) else 'N/A',
                         'significant': int_p < .05 if pd.notna(int_p) else False,
                         'p': int_p}
    else:
        results['H5'] = {'N': len(reg_data_h5), 'direction': 'insufficient data', 'significant': False, 'p': np.nan}

    # Print summary
    for hyp, res in results.items():
        primary = primary_results.get(hyp, {})
        primary_sig = primary.get('significant', None)
        if primary_sig is not None:
            if res['significant'] == primary_sig:
                change = 'SAME'
            elif res['significant'] and not primary_sig:
                change = 'NOW SIGNIFICANT'
            else:
                change = 'LOST SIGNIFICANCE'
        else:
            change = 'N/A'
        p_str = f"p={res['p']:.6f}" if pd.notna(res['p']) else 'p=N/A'
        print(f"  {hyp}: {res['direction']}, sig={res['significant']}, {p_str} [{change}]")

    return results

# Store primary results for comparison
primary_results = {
    'H1a': {'significant': h1a_p < .05},
    'H1b': {'significant': h1b_p < .05},
    'H2': {'significant': h2_p < .05},
    'H3': {'significant': h3_eval_sig and h3_deleg_nonsig},
    'H4': {'significant': h4_supported},
    'H5': {'significant': h5_interaction_sig and h5_direction_correct},
}

# (a) Strict attention exclusion
df_strict_attn = df[df['attention_pass'] == 1].copy()
robust_attn = run_robustness(df_strict_attn, "(a) Strict attention exclusion", primary_results)

# (b) Strict comprehension exclusion
df_strict_comp = df[df['comprehension_pass'] == 1].copy()
robust_comp = run_robustness(df_strict_comp, "(b) Strict comprehension exclusion", primary_results)

# Save robustness summary
robust_rows = []
for hyp in ['H1a', 'H1b', 'H2', 'H3', 'H4', 'H5']:
    for check_name, check_results in [('Strict attention', robust_attn), ('Strict comprehension', robust_comp)]:
        res = check_results.get(hyp, {})
        primary_sig = primary_results.get(hyp, {}).get('significant', None)
        if res.get('significant') == primary_sig:
            change = 'Same'
        elif res.get('significant') and not primary_sig:
            change = 'Now significant'
        elif not res.get('significant') and primary_sig:
            change = 'Lost significance'
        else:
            change = 'Changed direction'

        robust_rows.append({
            'Hypothesis': hyp,
            'Robustness_check': check_name,
            'N': res.get('N', ''),
            'Direction': res.get('direction', ''),
            'Significant': res.get('significant', ''),
            'p_value': round(res.get('p', np.nan), 6) if pd.notna(res.get('p', np.nan)) else '',
            'Change_from_primary': change
        })

robust_df = pd.DataFrame(robust_rows)
robust_df.to_csv(f"{OUTPUT_DIR}robustness_summary.csv", index=False)
print(f"\n  Saved: {OUTPUT_DIR}robustness_summary.csv")


# =============================================================================
# EXPLORATORY ANALYSES
# =============================================================================
print(f"\n{'='*80}")
print("EXPLORATORY ANALYSES (clearly labeled as exploratory)")
print(f"{'='*80}")

exploratory_rows = []

# E1: Variance Prediction (Levene's test)
print(f"\n--- E1: VARIANCE PREDICTION ---")
print("Prediction: Condition A produces higher variance on delegative trust")

groups_e1 = [df[df['condition']==c]['delegative_trust'].dropna() for c in ['A','B','C']]
levene_stat, levene_p = stats.levene(*groups_e1)
df_lev = 2  # k-1
df_lev_within = sum(len(g) for g in groups_e1) - 3

print(f"  Levene's test: F({df_lev}, {df_lev_within}) = {levene_stat:.4f}, p = {levene_p:.6f}")
print(f"\n  Variance (SD²) by condition:")
for cond, g in zip(['A','B','C'], groups_e1):
    print(f"    {cond}: Var={g.var():.4f}, SD={g.std():.4f}")

a_var_highest = groups_e1[0].var() > max(groups_e1[1].var(), groups_e1[2].var())
print(f"\n  Prediction check: A has highest variance? {a_var_highest}")

exploratory_rows.append({
    'Analysis': 'E1: Variance prediction',
    'Test': "Levene's test",
    'Statistic': f'F({df_lev},{df_lev_within})={levene_stat:.4f}',
    'p_value': round(levene_p, 6),
    'Result': f"A_var={groups_e1[0].var():.4f}, B_var={groups_e1[1].var():.4f}, C_var={groups_e1[2].var():.4f}",
    'Prediction_supported': 'Yes' if (a_var_highest and levene_p < .05) else ('Partial' if a_var_highest else 'No')
})


# E2: Comprehension Check as Signal
print(f"\n--- E2: COMPREHENSION CHECK AS SIGNAL ---")
print("Prediction: Comprehension failures show higher delegative, lower evaluative trust")

# t-tests
comp_pass = df[df['comprehension_pass'] == 1]
comp_fail = df[df['comprehension_pass'] == 0]

t_deleg, p_deleg = stats.ttest_ind(comp_pass['delegative_trust'].dropna(), comp_fail['delegative_trust'].dropna())
t_eval, p_eval = stats.ttest_ind(comp_pass['evaluative_trust'].dropna(), comp_fail['evaluative_trust'].dropna())

print(f"\n  (a) Delegative trust: pass M={comp_pass['delegative_trust'].mean():.3f}, fail M={comp_fail['delegative_trust'].mean():.3f}")
print(f"      t = {t_deleg:.4f}, p = {p_deleg:.6f}")
fail_higher_deleg = comp_fail['delegative_trust'].mean() > comp_pass['delegative_trust'].mean()
print(f"      Prediction (fail > pass): {fail_higher_deleg}")

print(f"\n  (b) Evaluative trust: pass M={comp_pass['evaluative_trust'].mean():.3f}, fail M={comp_fail['evaluative_trust'].mean():.3f}")
print(f"      t = {t_eval:.4f}, p = {p_eval:.6f}")
fail_lower_eval = comp_fail['evaluative_trust'].mean() < comp_pass['evaluative_trust'].mean()
print(f"      Prediction (fail < pass): {fail_lower_eval}")

# Cross-tab: comprehension pass/fail by condition
print(f"\n  Comprehension pass/fail by condition:")
ct_comp = pd.crosstab(df['condition'], df['comprehension_pass'], margins=True)
ct_comp.columns = ['Fail', 'Pass', 'Total']
ct_comp.index = [n if n != 'All' else 'Total' for n in ct_comp.index]
print(ct_comp)

# Percentages
ct_pct = pd.crosstab(df['condition'], df['comprehension_pass'], normalize='index') * 100
ct_pct.columns = ['Fail_%', 'Pass_%']
print(f"\n  Percentages:")
print(ct_pct.round(1))

# Save comprehension cross-tab
comp_cross = pd.crosstab(df['condition'], df['comprehension_pass'], margins=True)
comp_cross.columns = ['Fail', 'Pass', 'Total'] if len(comp_cross.columns) == 3 else comp_cross.columns
comp_pct = pd.crosstab(df['condition'], df['comprehension_pass'], normalize='index') * 100
comp_pct.columns = ['Fail_pct', 'Pass_pct']
comp_combined = comp_cross.join(comp_pct, how='left')
comp_combined.to_csv(f"{OUTPUT_DIR}comprehension_by_condition.csv")
print(f"\n  Saved: {OUTPUT_DIR}comprehension_by_condition.csv")

exploratory_rows.append({
    'Analysis': 'E2a: Comp check → delegative trust',
    'Test': 'Independent t-test',
    'Statistic': f't={t_deleg:.4f}',
    'p_value': round(p_deleg, 6),
    'Result': f"pass_M={comp_pass['delegative_trust'].mean():.3f}, fail_M={comp_fail['delegative_trust'].mean():.3f}",
    'Prediction_supported': 'Yes' if (fail_higher_deleg and p_deleg < .05) else ('Partial' if fail_higher_deleg else 'No')
})

exploratory_rows.append({
    'Analysis': 'E2b: Comp check → evaluative trust',
    'Test': 'Independent t-test',
    'Statistic': f't={t_eval:.4f}',
    'p_value': round(p_eval, 6),
    'Result': f"pass_M={comp_pass['evaluative_trust'].mean():.3f}, fail_M={comp_fail['evaluative_trust'].mean():.3f}",
    'Prediction_supported': 'Yes' if (fail_lower_eval and p_eval < .05) else ('Partial' if fail_lower_eval else 'No')
})


# E3: Robo-Advisor Experience Interaction
print(f"\n--- E3: ROBO-ADVISOR EXPERIENCE INTERACTION ---")

e3_dvs = ['evaluative_trust', 'delegative_trust', 'betrayal', 'disappointment',
          'betrayal_premium', 'general_exit', 'algorithm_aversion']

e3_reg_cols = ['cond_A', 'cond_B', 'robo_experience', 'age', 'fin_lit_score',
               'comprehension_pass', 'attention_pass']

df_e3 = df.dropna(subset=e3_reg_cols + e3_dvs)

for dv in e3_dvs:
    formula_e3 = f'{dv} ~ cond_A + cond_B + robo_experience + cond_A:robo_experience + cond_B:robo_experience + age + fin_lit_score + comprehension_pass + attention_pass'
    model_e3 = smf.ols(formula_e3, data=df_e3).fit()

    # Check interaction terms
    int_A_robo_p = model_e3.pvalues.get('cond_A:robo_experience', np.nan)
    int_B_robo_p = model_e3.pvalues.get('cond_B:robo_experience', np.nan)
    int_A_robo_b = model_e3.params.get('cond_A:robo_experience', np.nan)
    int_B_robo_b = model_e3.params.get('cond_B:robo_experience', np.nan)

    any_sig = (int_A_robo_p < .05 if pd.notna(int_A_robo_p) else False) or \
              (int_B_robo_p < .05 if pd.notna(int_B_robo_p) else False)

    sig_str = '***' if any_sig else ''
    print(f"\n  {dv}: cond_A×robo B={int_A_robo_b:.3f} p={int_A_robo_p:.4f}, "
          f"cond_B×robo B={int_B_robo_b:.3f} p={int_B_robo_p:.4f} {sig_str}")

    if any_sig:
        print(f"    SIGNIFICANT INTERACTION — Full table:")
        print(model_e3.summary().tables[1])

    exploratory_rows.append({
        'Analysis': f'E3: Robo experience × Condition → {dv}',
        'Test': 'OLS w/ interaction',
        'Statistic': f'int_A_B={int_A_robo_b:.3f}, int_B_B={int_B_robo_b:.3f}',
        'p_value': f'int_A_p={int_A_robo_p:.6f}, int_B_p={int_B_robo_p:.6f}',
        'Result': 'Significant' if any_sig else 'Not significant',
        'Prediction_supported': 'N/A (exploratory)'
    })

exploratory_df = pd.DataFrame(exploratory_rows)
exploratory_df.to_csv(f"{OUTPUT_DIR}exploratory_results.csv", index=False)
print(f"\n  Saved: {OUTPUT_DIR}exploratory_results.csv")


# =============================================================================
# FINAL SUMMARY
# =============================================================================
print(f"\n{'='*80}")
print("FINAL SUMMARY")
print(f"{'='*80}")
print(f"\nTotal N: {len(df)}")
print(f"Conditions: A={sum(df['condition']=='A')}, B={sum(df['condition']=='B')}, C={sum(df['condition']=='C')}")
print(f"\nHypothesis results:")
for _, row in results_df.iterrows():
    print(f"  {row['Hypothesis']}: {row['Prediction_supported']} (p={row['p_value']})")

print(f"\nOutput files saved to {OUTPUT_DIR}:")
print(f"  1. descriptive_tables.csv")
print(f"  2. h1_h5_results.csv")
print(f"  3. regression_h3.csv")
print(f"  4. regression_h4.csv")
print(f"  5. regression_h5.csv")
print(f"  6. robustness_summary.csv")
print(f"  7. exploratory_results.csv")
print(f"  8. comprehension_by_condition.csv")
print(f"\nDone.")
