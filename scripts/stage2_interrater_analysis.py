"""
Inter-rater reliability analysis: Human vs. Claude Sonnet vs. GPT-4o
on 100 CFPB hand-validation narratives.

Outputs:
  output/interrater_reliability_report.md  — Analyses 1–5
  output/disagreement_cases_full.md        — Analysis 6 (full narratives)
  output/disagreement_cases.csv            — Analysis 6 (CSV)
  output/interrater_correlation_matrix.csv — Analysis 2 raw data
"""

import pandas as pd
import numpy as np
import json
import os
from scipy import stats
from sklearn.metrics import cohen_kappa_score, confusion_matrix

# ── Paths ──────────────────────────────────────────────────────────────

BASE = "/workspaces/HumanxAI-2026"
HUMAN_PATH = os.path.join(BASE, "output", "cfpb_handcode_100_responses.json")
SONNET_PATH = os.path.join(BASE, "output", "cfpb_handcode_100_key.csv")
GPT4O_PATH = os.path.join(BASE, "output", "cfpb_handcode_100_gpt4o.csv")
BLIND_PATH = os.path.join(BASE, "output", "cfpb_handcode_100_blind.csv")

OUT_REPORT = os.path.join(BASE, "output", "interrater_reliability_report.md")
OUT_DISAGREE_MD = os.path.join(BASE, "output", "disagreement_cases_full.md")
OUT_DISAGREE_CSV = os.path.join(BASE, "output", "disagreement_cases.csv")
OUT_CORR_CSV = os.path.join(BASE, "output", "interrater_correlation_matrix.csv")

CATEGORIES = ['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE']

# ── Load data ──────────────────────────────────────────────────────────

def load_data():
    # Human
    with open(HUMAN_PATH) as f:
        human_raw = json.load(f)
    human_rows = []
    for key, val in human_raw.items():
        human_rows.append({
            'narrative_number': int(val['narrative_number']),
            'complaint_id': int(val['complaint_id']),
            'h_classification': val['classification'],
            'h_delegative_score': float(val['delegative_score']),
            'h_evaluative_score': float(val['evaluative_score']),
            'h_confidence': val.get('confidence', ''),
            'h_justification': val.get('justification', ''),
        })
    human_df = pd.DataFrame(human_rows)

    # Sonnet
    sonnet_df = pd.read_csv(SONNET_PATH, dtype={'complaint_id': 'int64'})
    sonnet_df = sonnet_df.rename(columns={
        'classification': 's_classification',
        'confidence': 's_confidence',
        'delegative_score': 's_delegative_score',
        'evaluative_score': 's_evaluative_score',
        'primary_evidence': 's_primary_evidence',
        'secondary_signals': 's_secondary_signals',
        'conf_bin': 's_conf_bin',
    })

    # GPT-4o
    gpt_df = pd.read_csv(GPT4O_PATH, dtype={'complaint_id': 'int64'})
    gpt_df = gpt_df.rename(columns={
        'classification': 'g_classification',
        'confidence': 'g_confidence',
        'delegative_score': 'g_delegative_score',
        'evaluative_score': 'g_evaluative_score',
        'primary_evidence': 'g_primary_evidence',
        'secondary_signals': 'g_secondary_signals',
    })

    # Blind narratives (full text)
    blind_df = pd.read_csv(BLIND_PATH, dtype={'complaint_id': 'int64'})

    # Merge all on narrative_number
    merged = human_df.merge(sonnet_df, on='narrative_number', how='inner', suffixes=('', '_s'))
    merged = merged.merge(gpt_df[['narrative_number', 'g_classification', 'g_confidence',
                                   'g_delegative_score', 'g_evaluative_score',
                                   'g_primary_evidence', 'g_secondary_signals']],
                          on='narrative_number', how='inner')
    merged = merged.merge(blind_df[['narrative_number', 'narrative_text', 'product_type',
                                     'company', 'date']],
                          on='narrative_number', how='inner')

    return merged


# ── Analysis 1: Cohen's Kappa ──────────────────────────────────────────

def kappa_ci_bootstrap(y1, y2, n_boot=2000, seed=42):
    """Cohen's kappa with bootstrap 95% CI."""
    rng = np.random.RandomState(seed)
    kappa = cohen_kappa_score(y1, y2)
    n = len(y1)
    boot_kappas = []
    for _ in range(n_boot):
        idx = rng.randint(0, n, size=n)
        try:
            k = cohen_kappa_score(np.array(y1)[idx], np.array(y2)[idx])
            boot_kappas.append(k)
        except Exception:
            pass
    boot_kappas = np.array(boot_kappas)
    ci_low = np.percentile(boot_kappas, 2.5)
    ci_high = np.percentile(boot_kappas, 97.5)
    return kappa, ci_low, ci_high


def pct_agreement(y1, y2):
    return np.mean(np.array(y1) == np.array(y2)) * 100


def analysis_1(df):
    pairs = [
        ('Human vs. Sonnet', df['h_classification'].values, df['s_classification'].values),
        ('Human vs. GPT-4o', df['h_classification'].values, df['g_classification'].values),
        ('Sonnet vs. GPT-4o', df['s_classification'].values, df['g_classification'].values),
    ]
    lines = []
    lines.append("## Analysis 1: Pairwise Cohen's Kappa (Categorical)\n")
    lines.append("Three-way classification: EVALUATIVE / DELEGATIVE / UNCLASSIFIABLE\n")
    lines.append("| Pair | Cohen's Kappa | 95% CI | % Agreement | Interpretation |")
    lines.append("|------|---------------|--------|-------------|----------------|")

    for name, y1, y2 in pairs:
        kappa, ci_low, ci_high = kappa_ci_bootstrap(y1, y2)
        agree = pct_agreement(y1, y2)
        if kappa > 0.80:
            interp = "Almost perfect"
        elif kappa > 0.60:
            interp = "Substantial"
        elif kappa > 0.40:
            interp = "Moderate"
        elif kappa > 0.20:
            interp = "Fair"
        else:
            interp = "Poor"
        lines.append(f"| {name} | {kappa:.3f} | [{ci_low:.3f}, {ci_high:.3f}] | {agree:.1f}% | {interp} |")

    lines.append("")
    lines.append("**Interpretation benchmarks:** <0.20 poor, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect.")
    lines.append("")
    return "\n".join(lines)


# ── Analysis 2: Pairwise Correlations ─────────────────────────────────

def analysis_2(df):
    lines = []
    lines.append("## Analysis 2: Pairwise Correlations (Continuous Scores)\n")

    # Note on human score granularity
    lines.append("**Note:** Human scores are rounded to 0.1 increments (slider input); LLM scores are")
    lines.append("arbitrary floats. Correlations are computed on the raw values.\n")

    rater_pairs = [
        ('Human vs. Sonnet', 'h', 's'),
        ('Human vs. GPT-4o', 'h', 'g'),
        ('Sonnet vs. GPT-4o', 's', 'g'),
    ]

    corr_rows = []

    lines.append("### Delegative Score Correlations\n")
    lines.append("| Pair | Pearson r | p-value | Spearman rho | p-value |")
    lines.append("|------|-----------|---------|--------------|---------|")
    for name, p1, p2 in rater_pairs:
        x = df[f'{p1}_delegative_score'].values
        y = df[f'{p2}_delegative_score'].values
        pr, pp = stats.pearsonr(x, y)
        sr, sp = stats.spearmanr(x, y)
        lines.append(f"| {name} | {pr:.3f} | {pp:.2e} | {sr:.3f} | {sp:.2e} |")
        corr_rows.append({'pair': name, 'measure': 'delegative_score',
                          'pearson_r': pr, 'pearson_p': pp,
                          'spearman_rho': sr, 'spearman_p': sp})

    lines.append("")
    lines.append("### Evaluative Score Correlations\n")
    lines.append("| Pair | Pearson r | p-value | Spearman rho | p-value |")
    lines.append("|------|-----------|---------|--------------|---------|")
    for name, p1, p2 in rater_pairs:
        x = df[f'{p1}_evaluative_score'].values
        y = df[f'{p2}_evaluative_score'].values
        pr, pp = stats.pearsonr(x, y)
        sr, sp = stats.spearmanr(x, y)
        lines.append(f"| {name} | {pr:.3f} | {pp:.2e} | {sr:.3f} | {sp:.2e} |")
        corr_rows.append({'pair': name, 'measure': 'evaluative_score',
                          'pearson_r': pr, 'pearson_p': pp,
                          'spearman_rho': sr, 'spearman_p': sp})

    lines.append("")

    # Save raw correlation matrix
    corr_df = pd.DataFrame(corr_rows)
    corr_df.to_csv(OUT_CORR_CSV, index=False)

    return "\n".join(lines)


# ── Analysis 3: Confusion Matrices ────────────────────────────────────

def format_confusion_matrix(y_true, y_pred, name_true, name_pred):
    """Format a 3x3 confusion matrix as markdown table."""
    labels = CATEGORIES
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    lines = []
    # Header
    header = f"| {name_true} \\ {name_pred} | " + " | ".join(labels) + " | Total |"
    sep = "|" + "---|" * (len(labels) + 2)
    lines.append(header)
    lines.append(sep)

    # Find most common disagreement
    max_disagree_val = 0
    max_disagree_desc = ""

    for i, row_label in enumerate(labels):
        row_vals = [str(cm[i, j]) for j in range(len(labels))]
        row_total = sum(cm[i])
        lines.append(f"| **{row_label}** | " + " | ".join(row_vals) + f" | {row_total} |")

        for j, col_label in enumerate(labels):
            if i != j and cm[i, j] > max_disagree_val:
                max_disagree_val = cm[i, j]
                max_disagree_desc = (f"{name_pred} says {col_label} when "
                                     f"{name_true} says {row_label}")

    # Column totals
    col_totals = [str(cm[:, j].sum()) for j in range(len(labels))]
    lines.append(f"| **Total** | " + " | ".join(col_totals) + f" | {cm.sum()} |")

    lines.append("")
    lines.append(f"**Most common disagreement:** {max_disagree_desc} — N={max_disagree_val}")
    lines.append("")
    return "\n".join(lines)


def analysis_3(df):
    lines = []
    lines.append("## Analysis 3: Confusion Matrices\n")

    lines.append("### Human vs. Sonnet\n")
    lines.append(format_confusion_matrix(
        df['h_classification'].values, df['s_classification'].values,
        'Human', 'Sonnet'))

    lines.append("### Human vs. GPT-4o\n")
    lines.append(format_confusion_matrix(
        df['h_classification'].values, df['g_classification'].values,
        'Human', 'GPT-4o'))

    lines.append("### Sonnet vs. GPT-4o\n")
    lines.append(format_confusion_matrix(
        df['s_classification'].values, df['g_classification'].values,
        'Sonnet', 'GPT-4o'))

    return "\n".join(lines)


# ── Analysis 4: Agreement by Confidence Level ─────────────────────────

def analysis_4(df):
    lines = []
    lines.append("## Analysis 4: Agreement by Sonnet Confidence Bin\n")
    lines.append("Confidence bins from Step 3 stratified sampling: "
                 "low (<0.75), medium (0.75–0.85), high (>0.85).\n")

    # Human confidence is categorical (HIGH/MEDIUM/LOW/empty), not directly
    # comparable to Sonnet float. Use Sonnet conf_bin for stratification.
    lines.append("**Note:** Human confidence was recorded as categorical "
                 "(HIGH/MEDIUM/LOW), not float. Using Sonnet's confidence bins "
                 "for stratification since those drove the sampling design.\n")

    bins = ['low', 'medium', 'high']
    pair_names = [
        ('Human-Sonnet', 'h_classification', 's_classification'),
        ('Human-GPT-4o', 'h_classification', 'g_classification'),
        ('Sonnet-GPT-4o', 's_classification', 'g_classification'),
    ]

    lines.append("| Confidence Bin | N | Human-Sonnet | Human-GPT-4o | Sonnet-GPT-4o |")
    lines.append("|----------------|---|--------------|--------------|---------------|")

    for b in bins:
        subset = df[df['s_conf_bin'] == b]
        n = len(subset)
        rates = []
        for pname, c1, c2 in pair_names:
            if n > 0:
                agree = pct_agreement(subset[c1].values, subset[c2].values)
                rates.append(f"{agree:.1f}%")
            else:
                rates.append("—")
        lines.append(f"| {b} | {n} | {rates[0]} | {rates[1]} | {rates[2]} |")

    lines.append("")
    return "\n".join(lines)


# ── Analysis 5: Distribution Comparison ───────────────────────────────

def analysis_5(df):
    lines = []
    lines.append("## Analysis 5: Distribution Comparison\n")

    lines.append("### Classification Counts\n")
    lines.append("| Category | Human | Sonnet | GPT-4o |")
    lines.append("|----------|-------|--------|--------|")

    for cat in CATEGORIES:
        h = (df['h_classification'] == cat).sum()
        s = (df['s_classification'] == cat).sum()
        g = (df['g_classification'] == cat).sum()
        lines.append(f"| {cat} | {h} ({h}%) | {s} ({s}%) | {g} ({g}%) |")

    lines.append("")

    # Systematic biases
    lines.append("### Systematic Biases\n")

    h_counts = df['h_classification'].value_counts()
    s_counts = df['s_classification'].value_counts()
    g_counts = df['g_classification'].value_counts()

    biases = []
    for cat in CATEGORIES:
        hc = h_counts.get(cat, 0)
        sc = s_counts.get(cat, 0)
        gc = g_counts.get(cat, 0)
        vals = {'Human': hc, 'Sonnet': sc, 'GPT-4o': gc}
        max_rater = max(vals, key=vals.get)
        min_rater = min(vals, key=vals.get)
        if vals[max_rater] - vals[min_rater] >= 5:
            biases.append(f"- **{cat}:** {max_rater} classifies the most ({vals[max_rater]}), "
                         f"{min_rater} the fewest ({vals[min_rater]}). "
                         f"Spread: {vals[max_rater] - vals[min_rater]}.")

    if biases:
        for b in biases:
            lines.append(b)
    else:
        lines.append("No large systematic biases detected (all spreads < 5).")

    lines.append("")

    # Mean continuous scores
    lines.append("### Mean Continuous Scores\n")
    lines.append("**Note:** Human scores use 0.1 increments (slider); LLM scores are "
                 "continuous floats. Human tends to assign 0.0 for non-matching categories, "
                 "producing lower means.\n")

    lines.append("| Measure | Human | Sonnet | GPT-4o |")
    lines.append("|---------|-------|--------|--------|")

    for score in ['delegative_score', 'evaluative_score']:
        hm = df[f'h_{score}'].mean()
        hs = df[f'h_{score}'].std()
        sm = df[f's_{score}'].mean()
        ss = df[f's_{score}'].std()
        gm = df[f'g_{score}'].mean()
        gs = df[f'g_{score}'].std()
        lines.append(f"| {score} | {hm:.3f} (SD={hs:.3f}) | {sm:.3f} (SD={ss:.3f}) | {gm:.3f} (SD={gs:.3f}) |")

    lines.append("")
    return "\n".join(lines)


# ── Analysis 6: Disagreement Cases ────────────────────────────────────

def analysis_6(df):
    """Generate disagreement cases markdown and CSV, plus unanimous examples."""

    # Identify disagreements: at least two of three raters disagree
    df['all_agree'] = ((df['h_classification'] == df['s_classification']) &
                       (df['s_classification'] == df['g_classification']))
    df['any_disagree'] = ~df['all_agree']

    disagree = df[df['any_disagree']].copy()
    agree = df[df['all_agree']].copy()

    # ── CSV output ──
    csv_rows = []
    for _, row in disagree.iterrows():
        csv_rows.append({
            'narrative_number': row['narrative_number'],
            'complaint_id': row['complaint_id'],
            'product_type': row['product_type'],
            'company': row['company'],
            'date': row['date'],
            'human_classification': row['h_classification'],
            'human_delegative_score': row['h_delegative_score'],
            'human_evaluative_score': row['h_evaluative_score'],
            'human_confidence': row['h_confidence'],
            'human_justification': row['h_justification'],
            'sonnet_classification': row['s_classification'],
            'sonnet_confidence': row['s_confidence'],
            'sonnet_delegative_score': row['s_delegative_score'],
            'sonnet_evaluative_score': row['s_evaluative_score'],
            'sonnet_primary_evidence': row['s_primary_evidence'],
            'gpt4o_classification': row['g_classification'],
            'gpt4o_confidence': row['g_confidence'],
            'gpt4o_delegative_score': row['g_delegative_score'],
            'gpt4o_evaluative_score': row['g_evaluative_score'],
            'gpt4o_primary_evidence': row['g_primary_evidence'],
        })
    csv_df = pd.DataFrame(csv_rows)
    csv_df.to_csv(OUT_DISAGREE_CSV, index=False)

    # ── Markdown output ──
    md = []
    md.append("# Inter-Rater Disagreement Cases\n")
    md.append(f"**Total narratives:** 100")
    md.append(f"**Unanimous agreement:** {len(agree)} ({len(agree)}%)")
    md.append(f"**Any disagreement:** {len(disagree)} ({len(disagree)}%)\n")

    # Disagreement pattern summary
    md.append("## Disagreement Pattern Summary\n")
    patterns = {}
    for _, row in disagree.iterrows():
        key = (row['h_classification'], row['s_classification'], row['g_classification'])
        patterns[key] = patterns.get(key, 0) + 1
    sorted_patterns = sorted(patterns.items(), key=lambda x: -x[1])
    md.append("| Human | Sonnet | GPT-4o | Count |")
    md.append("|-------|--------|--------|-------|")
    for (h, s, g), count in sorted_patterns:
        md.append(f"| {h} | {s} | {g} | {count} |")
    md.append("")

    # ── Each disagreement case ──
    md.append("---\n")
    md.append("## Disagreement Cases\n")

    for _, row in disagree.sort_values('narrative_number').iterrows():
        md.append(f"### Narrative #{int(row['narrative_number'])} — "
                  f"Complaint {int(row['complaint_id'])}\n")
        md.append(f"**Product:** {row['product_type']} | "
                  f"**Company:** {row['company']} | "
                  f"**Date:** {row['date']}\n")

        # Full narrative in blockquote
        narrative = str(row['narrative_text']).strip()
        # Blockquote each line
        bq_lines = []
        for line in narrative.split('\n'):
            bq_lines.append(f"> {line}")
        md.append("\n".join(bq_lines))
        md.append("")

        # Rater assessments
        md.append("**Human (Chris):**")
        md.append(f"- Classification: **{row['h_classification']}**")
        md.append(f"- Delegative: {row['h_delegative_score']:.1f} | "
                  f"Evaluative: {row['h_evaluative_score']:.1f}")
        if row['h_confidence']:
            md.append(f"- Confidence: {row['h_confidence']}")
        md.append(f"- Justification: {row['h_justification']}\n")

        md.append("**Claude Sonnet:**")
        md.append(f"- Classification: **{row['s_classification']}**")
        md.append(f"- Delegative: {row['s_delegative_score']:.2f} | "
                  f"Evaluative: {row['s_evaluative_score']:.2f} | "
                  f"Confidence: {row['s_confidence']:.2f}")
        md.append(f"- Evidence: {row['s_primary_evidence']}\n")

        md.append("**GPT-4o:**")
        md.append(f"- Classification: **{row['g_classification']}**")
        md.append(f"- Delegative: {row['g_delegative_score']:.2f} | "
                  f"Evaluative: {row['g_evaluative_score']:.2f} | "
                  f"Confidence: {row['g_confidence']:.2f}")
        md.append(f"- Evidence: {row['g_primary_evidence']}\n")

        md.append("---\n")

    # ── Unanimous Agreement Examples ──
    md.append("## Unanimous Agreement Examples\n")

    # Counts by category
    md.append("### Unanimous Agreement by Category\n")
    md.append("| Category | Count |")
    md.append("|----------|-------|")
    for cat in CATEGORIES:
        count = (agree['h_classification'] == cat).sum()
        md.append(f"| {cat} | {count} |")
    md.append("")

    # 5 unanimous DELEGATIVE
    unan_deleg = agree[agree['h_classification'] == 'DELEGATIVE']
    n_deleg = min(5, len(unan_deleg))
    if n_deleg > 0:
        md.append(f"### Unanimous DELEGATIVE ({n_deleg} of {len(unan_deleg)} available)\n")
        for _, row in unan_deleg.head(5).iterrows():
            md.append(f"#### Narrative #{int(row['narrative_number'])} — "
                      f"Complaint {int(row['complaint_id'])}\n")
            md.append(f"**Product:** {row['product_type']} | "
                      f"**Company:** {row['company']} | "
                      f"**Date:** {row['date']}\n")
            narrative = str(row['narrative_text']).strip()
            for line in narrative.split('\n'):
                md.append(f"> {line}")
            md.append("")
            md.append("**Human (Chris):**")
            md.append(f"- Classification: **{row['h_classification']}**")
            md.append(f"- Delegative: {row['h_delegative_score']:.1f} | "
                      f"Evaluative: {row['h_evaluative_score']:.1f}")
            md.append(f"- Justification: {row['h_justification']}\n")
            md.append("**Claude Sonnet:**")
            md.append(f"- Classification: **{row['s_classification']}**")
            md.append(f"- Delegative: {row['s_delegative_score']:.2f} | "
                      f"Evaluative: {row['s_evaluative_score']:.2f} | "
                      f"Confidence: {row['s_confidence']:.2f}")
            md.append(f"- Evidence: {row['s_primary_evidence']}\n")
            md.append("**GPT-4o:**")
            md.append(f"- Classification: **{row['g_classification']}**")
            md.append(f"- Delegative: {row['g_delegative_score']:.2f} | "
                      f"Evaluative: {row['g_evaluative_score']:.2f} | "
                      f"Confidence: {row['g_confidence']:.2f}")
            md.append(f"- Evidence: {row['g_primary_evidence']}\n")
            md.append("---\n")
    else:
        md.append("### Unanimous DELEGATIVE\n")
        md.append("No cases of unanimous DELEGATIVE agreement found.\n")

    # 5 unanimous EVALUATIVE
    unan_eval = agree[agree['h_classification'] == 'EVALUATIVE']
    n_eval = min(5, len(unan_eval))
    if n_eval > 0:
        md.append(f"### Unanimous EVALUATIVE ({n_eval} of {len(unan_eval)} available)\n")
        for _, row in unan_eval.head(5).iterrows():
            md.append(f"#### Narrative #{int(row['narrative_number'])} — "
                      f"Complaint {int(row['complaint_id'])}\n")
            md.append(f"**Product:** {row['product_type']} | "
                      f"**Company:** {row['company']} | "
                      f"**Date:** {row['date']}\n")
            narrative = str(row['narrative_text']).strip()
            for line in narrative.split('\n'):
                md.append(f"> {line}")
            md.append("")
            md.append("**Human (Chris):**")
            md.append(f"- Classification: **{row['h_classification']}**")
            md.append(f"- Delegative: {row['h_delegative_score']:.1f} | "
                      f"Evaluative: {row['h_evaluative_score']:.1f}")
            md.append(f"- Justification: {row['h_justification']}\n")
            md.append("**Claude Sonnet:**")
            md.append(f"- Classification: **{row['s_classification']}**")
            md.append(f"- Delegative: {row['s_delegative_score']:.2f} | "
                      f"Evaluative: {row['s_evaluative_score']:.2f} | "
                      f"Confidence: {row['s_confidence']:.2f}")
            md.append(f"- Evidence: {row['s_primary_evidence']}\n")
            md.append("**GPT-4o:**")
            md.append(f"- Classification: **{row['g_classification']}**")
            md.append(f"- Delegative: {row['g_delegative_score']:.2f} | "
                      f"Evaluative: {row['g_evaluative_score']:.2f} | "
                      f"Confidence: {row['g_confidence']:.2f}")
            md.append(f"- Evidence: {row['g_primary_evidence']}\n")
            md.append("---\n")
    else:
        md.append("### Unanimous EVALUATIVE\n")
        md.append("No cases of unanimous EVALUATIVE agreement found.\n")

    return "\n".join(md), len(disagree), len(agree)


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    df = load_data()
    print(f"Merged dataset: {len(df)} narratives\n")

    # Verify all 100 present
    assert len(df) == 100, f"Expected 100, got {len(df)}"

    # Build report
    report = []
    report.append("# Inter-Rater Reliability Report")
    report.append("## Human (Chris) vs. Claude Sonnet vs. GPT-4o")
    report.append(f"**100 CFPB Narratives — Confidence-Stratified Sample**\n")
    report.append("---\n")

    print("Analysis 1: Cohen's Kappa...")
    report.append(analysis_1(df))

    print("Analysis 2: Pairwise Correlations...")
    report.append(analysis_2(df))

    print("Analysis 3: Confusion Matrices...")
    report.append(analysis_3(df))

    print("Analysis 4: Agreement by Confidence Level...")
    report.append(analysis_4(df))

    print("Analysis 5: Distribution Comparison...")
    report.append(analysis_5(df))

    # Save main report
    with open(OUT_REPORT, 'w') as f:
        f.write("\n".join(report))
    print(f"Saved: {OUT_REPORT}")

    # Analysis 6: Disagreement cases
    print("Analysis 6: Disagreement Cases...")
    disagree_md, n_disagree, n_agree = analysis_6(df)
    with open(OUT_DISAGREE_MD, 'w') as f:
        f.write(disagree_md)
    print(f"Saved: {OUT_DISAGREE_MD}")
    print(f"Saved: {OUT_DISAGREE_CSV}")
    print(f"Saved: {OUT_CORR_CSV}")

    # Summary
    print(f"\n{'=' * 70}")
    print(f"INTER-RATER ANALYSIS COMPLETE")
    print(f"{'=' * 70}")
    print(f"Unanimous agreement: {n_agree}/100 ({n_agree}%)")
    print(f"Any disagreement:    {n_disagree}/100 ({n_disagree}%)")


if __name__ == '__main__':
    main()
