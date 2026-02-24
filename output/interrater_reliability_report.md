# Inter-Rater Reliability Report
## Human (Chris) vs. Claude Sonnet vs. GPT-4o
**100 CFPB Narratives — Confidence-Stratified Sample**

---

## Analysis 1: Pairwise Cohen's Kappa (Categorical)

Three-way classification: EVALUATIVE / DELEGATIVE / UNCLASSIFIABLE

| Pair | Cohen's Kappa | 95% CI | % Agreement | Interpretation |
|------|---------------|--------|-------------|----------------|
| Human vs. Sonnet | 0.264 | [0.136, 0.397] | 54.0% | Fair |
| Human vs. GPT-4o | 0.361 | [0.207, 0.507] | 62.0% | Fair |
| Sonnet vs. GPT-4o | 0.590 | [0.442, 0.725] | 77.0% | Moderate |

**Interpretation benchmarks:** <0.20 poor, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect.

## Analysis 2: Pairwise Correlations (Continuous Scores)

**Note:** Human scores are rounded to 0.1 increments (slider input); LLM scores are
arbitrary floats. Correlations are computed on the raw values.

### Delegative Score Correlations

| Pair | Pearson r | p-value | Spearman rho | p-value |
|------|-----------|---------|--------------|---------|
| Human vs. Sonnet | 0.488 | 2.65e-07 | 0.377 | 1.11e-04 |
| Human vs. GPT-4o | 0.511 | 5.69e-08 | 0.372 | 1.40e-04 |
| Sonnet vs. GPT-4o | 0.776 | 2.50e-21 | 0.827 | 3.00e-26 |

### Evaluative Score Correlations

| Pair | Pearson r | p-value | Spearman rho | p-value |
|------|-----------|---------|--------------|---------|
| Human vs. Sonnet | 0.308 | 1.83e-03 | 0.400 | 3.68e-05 |
| Human vs. GPT-4o | 0.402 | 3.31e-05 | 0.458 | 1.62e-06 |
| Sonnet vs. GPT-4o | 0.779 | 1.33e-21 | 0.818 | 3.06e-25 |

## Analysis 3: Confusion Matrices

### Human vs. Sonnet

| Human \ Sonnet | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| **EVALUATIVE** | 29 | 10 | 0 | 39 |
| **DELEGATIVE** | 1 | 4 | 0 | 5 |
| **UNCLASSIFIABLE** | 34 | 1 | 21 | 56 |
| **Total** | 64 | 15 | 21 | 100 |

**Most common disagreement:** Sonnet says EVALUATIVE when Human says UNCLASSIFIABLE — N=34

### Human vs. GPT-4o

| Human \ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| **EVALUATIVE** | 30 | 4 | 5 | 39 |
| **DELEGATIVE** | 1 | 4 | 0 | 5 |
| **UNCLASSIFIABLE** | 24 | 4 | 28 | 56 |
| **Total** | 55 | 12 | 33 | 100 |

**Most common disagreement:** GPT-4o says EVALUATIVE when Human says UNCLASSIFIABLE — N=24

### Sonnet vs. GPT-4o

| Sonnet \ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| **EVALUATIVE** | 49 | 4 | 11 | 64 |
| **DELEGATIVE** | 5 | 8 | 2 | 15 |
| **UNCLASSIFIABLE** | 1 | 0 | 20 | 21 |
| **Total** | 55 | 12 | 33 | 100 |

**Most common disagreement:** GPT-4o says UNCLASSIFIABLE when Sonnet says EVALUATIVE — N=11

## Analysis 4: Agreement by Sonnet Confidence Bin

Confidence bins from Step 3 stratified sampling: low (<0.75), medium (0.75–0.85), high (>0.85).

**Note:** Human confidence was recorded as categorical (HIGH/MEDIUM/LOW), not float. Using Sonnet's confidence bins for stratification since those drove the sampling design.

| Confidence Bin | N | Human-Sonnet | Human-GPT-4o | Sonnet-GPT-4o |
|----------------|---|--------------|--------------|---------------|
| low | 30 | 30.0% | 50.0% | 50.0% |
| medium | 40 | 42.5% | 50.0% | 82.5% |
| high | 30 | 93.3% | 90.0% | 96.7% |

## Analysis 5: Distribution Comparison

### Classification Counts

| Category | Human | Sonnet | GPT-4o |
|----------|-------|--------|--------|
| EVALUATIVE | 39 (39%) | 64 (64%) | 55 (55%) |
| DELEGATIVE | 5 (5%) | 15 (15%) | 12 (12%) |
| UNCLASSIFIABLE | 56 (56%) | 21 (21%) | 33 (33%) |

### Systematic Biases

- **EVALUATIVE:** Sonnet classifies the most (64), Human the fewest (39). Spread: 25.
- **DELEGATIVE:** Sonnet classifies the most (15), Human the fewest (5). Spread: 10.
- **UNCLASSIFIABLE:** Human classifies the most (56), Sonnet the fewest (21). Spread: 35.

### Mean Continuous Scores

**Note:** Human scores use 0.1 increments (slider); LLM scores are continuous floats. Human tends to assign 0.0 for non-matching categories, producing lower means.

| Measure | Human | Sonnet | GPT-4o |
|---------|-------|--------|--------|
| delegative_score | 0.031 (SD=0.134) | 0.267 (SD=0.253) | 0.342 (SD=0.214) |
| evaluative_score | 0.178 (SD=0.233) | 0.583 (SD=0.326) | 0.599 (SD=0.264) |
