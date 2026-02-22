# CFPB Data Analysis — Stage 2 Task Prompt (Revised)
## For Claude Code session, February 22, 2026

Read `project_briefing_20260221.md` for full project context if you haven't already. This session builds on Stage 1 structural exploration (completed). The 50-narrative hand-reading confirmed the evaluative/delegative signal is present but noisy — many complaints don't map cleanly to either trust mode. That's expected and the analysis design accounts for it.

## Background (short version)

The paper argues financial trust is two-dimensional: **evaluative trust** (performance monitoring, verification, benchmark-checking — withdrawn when evidence disappoints) and **delegative trust** (grants discretionary authority, accepts opacity, tolerates uncertainty — experienced as betrayal when violated). Stage 2 tests whether this distinction is observable in CFPB consumer complaint narratives using Claude API classification, validated against hand-coding and eMFD moral foundations scores.

## Task Overview

This is a three-step process. **Stop after each step and wait for my input before proceeding.**

1. **Filter and count** — Identify classifiable narratives across the three target product categories. Report counts. Save the filtered corpus. I decide how many to classify.
2. **Classify** — Run Claude API classification on the number I choose. Score with eMFD. Produce analysis tables.
3. **Hand-validation sample** — Pull 100 narratives for me to code blind.

Plus a focused side analysis of the algorithmic trigger subsample from Stage 1.

---

## Step 1: Filter and Count

### Filtering Criteria

From the full CFPB database, pull narratives that meet ALL of these criteria:

- **Product type:** Mortgage, Checking or savings, OR Credit card
- **Has narrative:** Non-null consumer narrative text
- **Minimum length:** 200+ characters (shorter narratives are too thin to classify reliably)
- **Not a template:** Exclude narratives that appear to be form letters or templates. Heuristics: (a) narratives that appear verbatim or near-verbatim more than 5 times in the database, (b) narratives that begin with common credit repair template openings like "I am writing to dispute," "This letter is to inform you," "Under the Fair Credit Reporting Act," "I am a victim of identity theft." Use your judgment on additional template indicators — the goal is to keep organic, voice-of-consumer narratives and exclude formulaic filings.
- **Date range:** 2015-06-01 onward (when CFPB started publishing narratives)

### Output for Step 1

Report:
- Total narratives passing all filters, by product type
- Examples of excluded templates (so I can verify the filter isn't too aggressive)
- Character length distribution of the filtered corpus (median, quartiles)
- A random sample of 10 narratives from the filtered set (for a quick sanity check)

Save the full filtered corpus to a file (CSV with complaint_id, product, sub_product, company, date, state, narrative_text).

**STOP HERE. Tell me the counts and show me the samples. I will tell you how many to classify and whether the filters need adjustment.**

---

## Step 2: Classify and Analyze

Once I give you a number N and confirm the filters are good:

### Sampling

Pull N narratives from the filtered corpus, stratified across product types. Unless I specify otherwise, stratify equally (N/3 per category). Random sample within each category. Save with complaint IDs for reproducibility.

### Classification via Claude API

Use the Anthropic API (Claude Sonnet — `claude-sonnet-4-5-20250929` or current equivalent). For each narrative, send this prompt:

---

**System prompt:**

```
You are a research assistant classifying consumer financial complaints for an academic study on trust in financial relationships.

The study distinguishes two modes of trust failure:

EVALUATIVE TRUST FAILURE: The consumer's complaint is primarily about unmet performance expectations, functional problems, or verification failures. The consumer treats the financial institution as a service provider that failed to deliver. Language focuses on: incorrect charges, broken processes, unmet promises, poor service quality, failure to perform as advertised. The emotional register is frustration, dissatisfaction, or anger at incompetence. The consumer's implicit stance is: "You didn't do what you were supposed to do."

DELEGATIVE TRUST FAILURE: The consumer's complaint reflects betrayal of a relationship in which they had granted the institution discretionary authority or relied on it as a fiduciary. Language focuses on: betrayal, abandonment, broken loyalty, abuse of the relationship, violation of good faith, taking advantage of vulnerability. The emotional register is moral outrage, a sense of personal violation, or grief at a relationship destroyed. The consumer's implicit stance is: "I trusted you and you betrayed me."

UNCLASSIFIABLE: The complaint does not clearly reflect either trust mode. This includes: template/form letters, pure factual disputes with no emotional content, identity theft reports where the consumer has no relationship with the institution, complaints too brief or unclear to assess, or complaints that mix both modes without a dominant one.

Important: Many complaints will be unclassifiable. That is expected. Do not force a classification. Only assign EVALUATIVE or DELEGATIVE when the language clearly reflects one mode.
```

**User prompt (per narrative):**

```
Classify this consumer financial complaint. Respond in exactly this JSON format:

{
  "classification": "EVALUATIVE" | "DELEGATIVE" | "UNCLASSIFIABLE",
  "confidence": <float 0.0 to 1.0>,
  "primary_evidence": "<one sentence quoting or paraphrasing the specific language that drove your classification>",
  "secondary_signals": "<one sentence noting any additional signals, or 'none'>",
  "delegative_score": <float 0.0 to 1.0>,
  "evaluative_score": <float 0.0 to 1.0>
}

The delegative_score and evaluative_score are independent dimensions, not a zero-sum scale. A complaint can score high on both (mixed), low on both (unclassifiable), or high on one and low on the other (clean classification).

COMPLAINT:
"""
{narrative_text}
"""
```

---

### Classification Implementation Notes

- Set `max_tokens` to 300. These responses are short.
- Set `temperature` to 0.0 for reproducibility.
- Parse the JSON response. If parsing fails, log the raw response and flag for manual review.
- Use the batch API if classifying more than 500 narratives.
- Save results as CSV: complaint_id, product, sub_product, company, date, state, narrative_text, classification, confidence, primary_evidence, secondary_signals, delegative_score, evaluative_score.

### eMFD Validation

Install the Extended Moral Foundations Dictionary library:
```
pip install emfdscore
```

If `emfdscore` isn't directly pip-installable or has dependency issues, the eMFD wordlists may be available as CSV/JSON from the original Hopp et al. repository (https://github.com/medianeuroscience/emfd). In that case, implement dictionary-based scoring manually — count hits per moral foundation per narrative, normalized by narrative length.

Score ALL classified narratives on the five moral foundations:
- Care/Harm
- Fairness/Cheating
- Loyalty/Betrayal
- Authority/Subversion
- Purity/Degradation

### Analysis Output

Produce these tables/statistics:

1. **Classification distribution by product type:** Count and percentage of EVALUATIVE / DELEGATIVE / UNCLASSIFIABLE per product category.
2. **Mean continuous scores by product type:** Mean delegative_score and evaluative_score per product category, with standard deviations.
3. **eMFD scores by classification:** Mean moral foundation scores for each classification category (EVALUATIVE / DELEGATIVE / UNCLASSIFIABLE).
4. **eMFD scores by product type:** Mean moral foundation scores per product category.
5. **Correlation matrix:** Correlations between delegative_score, evaluative_score, and the five eMFD foundation scores.
6. **Confidence distribution:** Distribution of confidence scores by classification category. Are DELEGATIVE classifications less confident than EVALUATIVE? (This would suggest delegative trust language is subtler.)
7. **Cross-tabulation:** Product type × classification × confidence level (high >0.7 / medium 0.4–0.7 / low <0.4).

**Prediction (for reference — do not use this to adjust results):** Mortgage complaints show the highest proportion of DELEGATIVE classifications. Credit card complaints show the highest proportion of EVALUATIVE classifications. Checking/savings falls in between. Narratives classified DELEGATIVE score higher on Care/Harm, Fairness/Cheating, and Loyalty/Betrayal moral foundations. The delegative_score correlates positively with these three foundations; the evaluative_score shows weak or no moral foundation correlation.

Save all tables and statistics to a summary file.

**STOP HERE. Show me the results. I will review before proceeding to Step 3.**

---

## Step 3: Hand-Validation Sample

After I've reviewed the classification results:

Pull 100 narratives for me to hand-code, stratified as follows:
- ~34 mortgage, ~33 checking/savings, ~33 credit card
- Within each product type, oversample from medium-confidence classifications (0.3–0.7). These are the borderline cases where human judgment matters most. Suggested split per product type: ~40% medium-confidence, ~30% high-confidence, ~30% low-confidence.

Produce two files:

**Blind coding file** (`cfpb_handcode_100_blind.md`): Markdown file with each narrative numbered, showing: complaint ID, product type, company, date, and full narrative text. NO classification, NO scores, NO evidence fields. Just the raw complaint for me to read and code.

**Answer key** (`cfpb_handcode_100_key.csv`): CSV with complaint_id and all Claude classification fields. I will not open this until I've finished my own coding.

---

## Side Analysis: Algorithmic Trigger Subsample

This runs alongside Steps 2–3, not gated by them.

### Sampling

From the ~42K algorithmic trigger narratives identified in Stage 1, pull a focused subsample of narratives involving **consequential automated decisions** (not just "I couldn't reach a human"). Search for:
- "automatically closed"
- "automatically denied"
- "auto-rejected"
- "algorithm"
- "automated system" + ("decision" OR "denied" OR "rejected" OR "closed" OR "blocked" OR "flagged")
- "computer decided"
- "no human" OR "no one can override" OR "can't override"

From the results, pull 500 narratives (or all of them if fewer than 500 match). These should be cases where an automated system made a decision that affected the consumer.

### Classification

Run the same Claude API classification prompt on this subsample.

### Analysis Question

When consumers complain about consequential automated decisions, do they use delegative trust language (betrayal, moral violation — suggesting they projected trust onto the system) or evaluative trust language (it didn't work right, the process was broken)? Or do they generate a third pattern — frustration at the absence of anyone to trust at all?

This subsample directly tests the O'Neill argument: automated systems that eliminate human discretion may destroy the conditions for delegative trust entirely, leaving consumers with no trust relationship to fall back on when things go wrong.

Report: classification distribution, mean continuous scores, comparison to the main corpus distributions, and 10 representative examples (pick narratives that best illustrate whatever pattern emerges).

Save results separately from the main analysis.

---

## Output Files

- `cfpb_filtered_corpus.csv` — Full filtered corpus from Step 1
- `cfpb_classified_N.csv` — Full classification results (N = whatever I choose)
- `cfpb_emfd_scores.csv` — eMFD scores for all classified narratives
- `cfpb_analysis_summary.md` — All tables, statistics, correlations from Step 2
- `cfpb_handcode_100_blind.md` — 100 narratives for blind hand-coding
- `cfpb_handcode_100_key.csv` — Answer key (Claude's classifications)
- `cfpb_algo_subsample_classified.csv` — Algorithmic trigger subsample results
- `cfpb_algo_subsample_analysis.md` — Algorithmic subsample summary and examples

## What NOT to Do

- Do not proceed past a STOP point without my explicit go-ahead
- Do not modify the classification prompt without discussing it with me first
- Do not editorialize about whether the results "support" or "fail to support" the theory — give me the data and let me interpret it
- Do not skip the eMFD validation — it's a separate method triangulating the same construct, which is important for the paper's credibility
