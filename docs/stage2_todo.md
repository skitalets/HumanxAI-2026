# CFPB Stage 2: Analysis Pipeline Status

**Authoritative spec:** `docs/cfpb_stage2_prompt_revised_20260222.md`
**Last updated:** 2026-02-22

---

## Step 1: Filter and Count — DONE

**Script:** `stage2_step1_filter.py`
**Output:** `data/cfpb_filtered_corpus.csv` (745 MB, not in git — rerun script to regenerate)

Filtered the full CFPB database (13.8M complaints) to classifiable narratives:
- Product: Mortgage, Checking/savings, Credit card
- Has narrative, 200+ chars, date >= 2015-06-01
- Excluded template openings (2,096 removed) and near-duplicates appearing 5+ times (11,996 removed)

**Result:** 483,525 narratives (131,921 mortgage, 163,171 checking/savings, 188,433 credit card)

---

## Step 2: Classify and Analyze — DONE

### Sampling — DONE
**Script:** `stage2_step2_sample.py`
**Output:** `data/classification_sample_9000.csv` (not in git)

9,000 narratives, 3,000 per product category, random seed = 42.

### Classification — DONE
**Script:** `stage2_step2_classify.py` (async, 20 concurrent requests)
**Output:** `output/cfpb_classified_9000.csv` (in git)

- Model: claude-sonnet-4-5-20250929, temperature=0.0, max_tokens=300
- Prompt: exact spec from `cfpb_stage2_prompt_revised_20260222.md`
- 0.0–1.0 float scores, three-way categorical (EVALUATIVE/DELEGATIVE/UNCLASSIFIABLE)
- NO product type or company passed to classifier (prevents hypothesis leakage)
- 8,991 valid, 9 parse errors

**Key results:**
- Mortgage: 21.1% DELEGATIVE, 76.4% EVALUATIVE, 2.5% UNCLASSIFIABLE
- Checking/savings: 16.4% DELEGATIVE, 77.9% EVALUATIVE, 5.7% UNCLASSIFIABLE
- Credit card: 12.3% DELEGATIVE, 79.2% EVALUATIVE, 8.5% UNCLASSIFIABLE
- Mortgage vs credit card delegative score: Cohen's d=0.313, p=2.4e-44
- Evaluative scores flat across products (d=0.030)

### eMFD Scoring — DONE
**Script:** `stage2_step2_emfd.py`
**Output:** `output/cfpb_emfd_scores.csv` (in git)

Dictionary-based scoring using eMFD (Hopp et al. 2021), downloaded from GitHub.
`emfdscore` pip package unavailable — implemented manual dictionary scoring.

**Key results:** DELEGATIVE complaints score higher than EVALUATIVE on all five moral foundations:
- Loyalty: d=0.267, p=4.1e-23
- Sanctity: d=0.263, p=3.4e-22
- Care: d=0.235, p=2.2e-19

### Analysis Tables — DONE
**Script:** `stage2_step2_analyze.py`
**Output:** `output/cfpb_analysis_summary.md`, `output/stage2_tables/`

All 7 tables from spec produced. See `cfpb_analysis_summary.md` for full results.

---

## Step 3: Hand-Validation Sample — DONE (files produced, coding in progress)

**Script:** `stage2_step3_handcode.py`
**Outputs:**
- `output/cfpb_handcode_100_blind.md` — blind coding markdown
- `output/cfpb_handcode_100_blind.csv` — blind coding spreadsheet (empty coding columns)
- `output/cfpb_handcode_100_key.csv` — answer key (Claude's classifications)

100 narratives, confidence-stratified:
- 34 mortgage, 33 checking/savings, 33 credit card
- 40 medium-confidence (0.75–0.85), 30 high (>0.85), 30 low (<0.75)
- Note: Sonnet's confidence floor was 0.65, so bins adapted from spec's 0.4/0.7 thresholds

**Hand-coding app:** `handcode_app.py` (Flask, run locally with `python handcode_app.py`)

**Status:** Chris coding blind. Answer key not yet opened.

---

## Side Analysis: Algorithmic Trigger Subsample — NOT STARTED

From ~42K algorithmic trigger narratives (Stage 1), pull focused subsample of consequential automated decisions. Classify with same Claude API prompt. Compare distributions to main corpus. See spec for search terms and analysis questions.

---

## Summary Report — NOT STARTED

1-2 page summary: Is the distinction visible? Does it vary by product? eMFD triangulation? Limitations? Scale up or pivot?

---

## File Inventory

### In git (`output/`)
- `cfpb_structural_summary.md` — Stage 1 structural stats
- `cfpb_50_narrative_sample.md` — Stage 1 hand-reading sample
- `cfpb_algorithmic_trigger_examples.md` — Stage 1 trigger word search
- `cfpb_fintech_search_results.md` — Stage 1 fintech company search
- `cfpb_classified_9000.csv` — Full classification results
- `cfpb_emfd_scores.csv` — eMFD moral foundations scores
- `cfpb_analysis_summary.md` — All analysis tables
- `cfpb_handcode_100_blind.md` — Blind coding (markdown)
- `cfpb_handcode_100_blind.csv` — Blind coding (spreadsheet)
- `cfpb_handcode_100_key.csv` — Answer key
- `stage2_tables/` — Individual table CSVs

### Not in git (regenerate from scripts)
- `data/complaints.csv` — 7.7GB raw CFPB CSV (download from consumerfinance.gov)
- `data/cfpb_filtered_corpus.csv` — 745MB filtered corpus (rerun `stage2_step1_filter.py`)
- `data/classification_sample_9000.csv` — 9K sample (rerun `stage2_step2_sample.py`)

### Scripts
- `cfpb_stage1_analysis.py` — Stage 1 structural exploration
- `cfpb_fix_bot_trigger.py` — Stage 1 bot trigger word fix
- `stage2_step1_filter.py` — Filter corpus
- `stage2_step2_sample.py` — Draw stratified sample
- `stage2_step2_classify.py` — Claude API classification (async)
- `stage2_step2_emfd.py` — eMFD dictionary scoring
- `stage2_step2_analyze.py` — Analysis tables
- `stage2_step3_handcode.py` — Hand-validation sample generation
- `handcode_app.py` — Flask hand-coding app
