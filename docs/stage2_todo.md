# CFPB Stage 2: Analysis Pipeline TODO

**Context:** Stage 1 (structural exploration) is complete. See `output/cfpb_structural_summary.md` for results. The data file is `data/complaints.csv.zip` (Git LFS, ~1.7GB compressed, ~7.7GB uncompressed CSV).

**Goal:** Determine whether the evaluative/delegative trust distinction is observable in how consumers describe financial relationship failures across product types.

**Key prediction:** Mortgage complaints (long-term, high-stakes, personal relationships) should show more delegative trust language (betrayal, broken promises, abuse of relationship) than credit card complaints (transactional, performance-based, easily switched). Checking/savings should fall in between.

---

## Step 1: Filter and Extract Target Narratives

**Input:** `data/complaints.csv.zip` (full CFPB database)
**Output:** `data/complaints_financial_filtered.csv.gz`

Filter to complaints that have narratives (`Consumer complaint narrative` is not null) AND belong to these product categories:

- **Mortgage:** `Product` contains "Mortgage" (expect ~139K narratives)
- **Checking/Savings:** `Product` contains "Checking or savings" OR "Bank account or service" (expect ~183K)
- **Credit Card:** `Product` contains "Credit card" (expect ~217K)

Add a normalized `product_group` column with values: `mortgage`, `checking_savings`, `credit_card`.

Columns to keep: `Complaint ID`, `Date received`, `Product`, `Sub-product`, `product_group`, `Company`, `Consumer complaint narrative`

Print summary stats: row counts per product_group, date range, narrative length distribution.

**Technical notes:**
- Use chunked reading (250K rows) — the full CSV won't fit in memory on small instances
- The CSV has duplicate product labels from CFPB taxonomy changes (e.g., "Credit card" and "Credit card or prepaid card" are separate strings — catch both)
- Use `on_bad_lines='skip'` and `low_memory=False`
- Stage 1 script (`cfpb_stage1_analysis.py`) has working chunked-read boilerplate

---

## Step 2: Stratified Sample of 200 Narratives for Classification

**Input:** `data/complaints_financial_filtered.csv.gz`
**Output:** `data/classification_sample_200.csv`

Draw a stratified random sample:
- 80 mortgage narratives
- 60 checking/savings narratives
- 60 credit card narratives

Stratification rationale: oversample mortgage (the strongest predicted delegative signal) to ensure adequate power for the key comparison.

Filter criteria for sample quality:
- Narrative length between 200 and 5,000 characters (exclude ultra-short complaints and copy-pasted legal letters)
- Exclude narratives that are mostly redacted (CFPB replaces PII with `XXXX` — skip if >30% of text is `X`)

Set random seed = 42 for reproducibility. Save with all columns from Step 1.

---

## Step 3: Claude API Classification (200 Narratives)

**Input:** `data/classification_sample_200.csv`
**Output:** `output/classification_results_200.csv`

For each narrative, call the Claude API (claude-sonnet-4-20250514 or latest available) with this structured prompt:

```
You are a research assistant analyzing consumer financial complaint narratives.

Read this consumer complaint and rate it on two dimensions:

1. EVALUATIVE TRUST FAILURE (1-7): The complaint reflects performance disappointment,
   unmet functional expectations, process failures, fee disputes, or service quality
   problems. The consumer treats the institution as a tool that didn't work properly.

2. DELEGATIVE TRUST BETRAYAL (1-7): The complaint reflects moral violation, betrayal
   of a relationship, abuse of granted authority, broken promises, or violation of
   vulnerability. The consumer treats the institution as having betrayed a personal
   commitment.

These are INDEPENDENT dimensions — a complaint can score high on both, low on both,
or high on one and low on the other.

Product type: {product_group}
Company: {company}

COMPLAINT NARRATIVE:
{narrative}

Respond in JSON format:
{
  "evaluative_score": <1-7>,
  "delegative_score": <1-7>,
  "evaluative_justification": "<one sentence>",
  "delegative_justification": "<one sentence>",
  "key_phrases_evaluative": ["<phrase1>", "<phrase2>"],
  "key_phrases_delegative": ["<phrase1>", "<phrase2>"],
  "dominant_mode": "evaluative" | "delegative" | "mixed" | "neither"
}
```

**Technical notes:**
- Use `temperature=0` for reproducibility
- Add exponential backoff for rate limits
- Save raw API responses alongside parsed scores
- Budget: ~200 calls at ~1K tokens each = ~200K tokens, well under $1
- If no Anthropic API key is available, save the prompts as a batch file that can be run later

---

## Step 4: eMFD Moral Foundations Scoring

**Input:** `data/classification_sample_200.csv`
**Output:** `output/emfd_scores_200.csv`

Score each narrative using the Extended Moral Foundations Dictionary (eMFD, Hopp et al. 2021).

Install: `pip install emfdscore`

Score on all five moral foundations:
- Care/Harm
- Fairness/Cheating
- Loyalty/Betrayal
- Authority/Subversion
- Purity/Degradation

**Prediction:** Narratives with high delegative trust betrayal scores (from Step 3) should score higher on Care/Harm, Fairness/Cheating, and Loyalty/Betrayal. Evaluative trust failures should score lower on moral foundations overall.

---

## Step 5: Analysis and Tables

**Input:** `output/classification_results_200.csv`, `output/emfd_scores_200.csv`
**Output:** `output/stage2_analysis_results.md`, `output/stage2_tables/` (individual table files)

### Table 1: Descriptive Statistics by Product Group
- Mean/SD of evaluative and delegative scores by product_group
- Mean/SD of narrative length by product_group
- Distribution of `dominant_mode` by product_group

### Table 2: Cross-Product Comparison (Key Test)
- t-tests or Mann-Whitney U: mortgage vs. credit card on delegative scores
- t-tests or Mann-Whitney U: mortgage vs. credit card on evaluative scores
- Effect sizes (Cohen's d)
- Prediction: mortgage > credit card on delegative; credit card >= mortgage on evaluative

### Table 3: eMFD Correlation Matrix
- Pearson/Spearman correlations between Claude's evaluative/delegative scores and eMFD foundation scores
- Prediction: delegative score correlates with Care/Harm, Fairness/Cheating, Loyalty/Betrayal

### Table 4: Example Narratives
- 3 highest-scoring delegative narratives (one per product)
- 3 highest-scoring evaluative narratives (one per product)
- 3 mixed narratives
- Include key phrases identified by Claude

### Figure 1: Score Distributions
- Scatter plot: evaluative score (x) vs. delegative score (y), colored by product_group
- Histograms of each score by product_group

---

## Step 6: Summary Report

**Output:** `output/stage2_summary.md`

Write a brief (1-2 page) summary answering:
1. Is the evaluative/delegative distinction visible in the data?
2. Does it vary by product type as predicted?
3. Does eMFD triangulation support the classification?
4. What are the limitations of the 200-narrative pilot?
5. Recommendation: should we scale up to full corpus, or pivot?

---

## Dependencies

```
pip install pandas numpy scipy matplotlib seaborn anthropic emfdscore
```

## File Structure After Completion

```
data/
  complaints.csv.zip          # Raw data (Git LFS)
  complaints_financial_filtered.csv.gz  # Step 1 output
  classification_sample_200.csv         # Step 2 output
output/
  cfpb_structural_summary.md           # Stage 1 (existing)
  cfpb_50_narrative_sample.md          # Stage 1 (existing)
  classification_results_200.csv        # Step 3 output
  emfd_scores_200.csv                   # Step 4 output
  stage2_analysis_results.md            # Step 5 output
  stage2_tables/                        # Step 5 tables
  stage2_summary.md                     # Step 6 output
```
