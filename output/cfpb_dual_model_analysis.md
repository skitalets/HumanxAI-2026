# Dual-Model Classification Analysis: Sonnet & GPT-4o (N=9,000)

---

## Table 1: GPT-4o Classification Distribution by Product Type

| Product | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---------|----------:|----------:|---------------:|------:|
| mortgage | 2,191 (73.7%) | 589 (19.8%) | 194 (6.5%) | 2,974 |
| checking_savings | 2,127 (71.3%) | 395 (13.2%) | 463 (15.5%) | 2,985 |
| credit_card | 2,268 (76.0%) | 262 (8.8%) | 454 (15.2%) | 2,984 |
| **Total** | **6,586 (73.6%)** | **1,246 (13.9%)** | **1,111 (12.4%)** | **8,943** |

## Table 2: GPT-4o Continuous Scores by Product Type

| Product | Delegative Score | Evaluative Score |
|---------|---------------:|----------------:|
| mortgage | 0.411 (SD=0.219) | 0.724 (SD=0.195) |
| checking_savings | 0.371 (SD=0.194) | 0.705 (SD=0.207) |
| credit_card | 0.329 (SD=0.169) | 0.731 (SD=0.212) |
| **Overall** | 0.370 (SD=0.198) | 0.720 (SD=0.205) |

### Cross-Product Comparisons

**mortgage vs credit_card:**
- Delegative: mortgage mean=0.411, credit_card mean=0.329, U=5,545,242, p=8.95e-70 ***, Cohen's d=0.419
- Evaluative: mortgage mean=0.724, credit_card mean=0.731, U=4,209,198, p=3.25e-04 ***, Cohen's d=-0.031

**mortgage vs checking_savings:**
- Delegative: mortgage mean=0.411, checking_savings mean=0.371, U=4,879,004, p=2.59e-12 ***, Cohen's d=0.194
- Evaluative: mortgage mean=0.724, checking_savings mean=0.705, U=4,681,022, p=1.41e-04 ***, Cohen's d=0.097

## Table 3: Dual-Model Concordance Table (Sonnet × GPT-4o)

| Sonnet \ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Sonnet Total |
|-----------------|----------:|----------:|---------------:|------------:|
| EVALUATIVE | 6,037 | 351 | 575 | 6,963 |
| DELEGATIVE | 519 | 877 | 81 | 1,477 |
| UNCLASSIFIABLE | 30 | 18 | 455 | 503 |
| **GPT-4o Total** | 6,586 | 1,246 | 1,111 | 8,943 |

**Overall agreement:** 7,369/8,943 (82.4%)
**Cohen's Kappa:** 0.556

## Table 4: Concordant-Only Classification Distribution by Product Type

**Concordant narratives:** 7,369 (82.4%)
**Discordant narratives:** 1,574 (17.6%)

**Concordance by product type:**

| Product | Concordant | Discordant | Agreement Rate |
|---------|----------:|----------:|--------------:|
| mortgage | 2,472 | 502 | 83.1% |
| checking_savings | 2,405 | 580 | 80.6% |
| credit_card | 2,492 | 492 | 83.5% |

**Classification distribution (concordant cases only):**

| Product | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---------|----------:|----------:|---------------:|------:|
| mortgage | 1,996 (80.7%) | 414 (16.7%) | 62 (2.5%) | 2,472 |
| checking_savings | 1,958 (81.4%) | 286 (11.9%) | 161 (6.7%) | 2,405 |
| credit_card | 2,083 (83.6%) | 177 (7.1%) | 232 (9.3%) | 2,492 |
| **Total** | **6,037 (81.9%)** | **877 (11.9%)** | **455 (6.2%)** | **7,369** |

## Table 5: Concordant-Only Continuous Scores by Product Type (Averaged)

| Product | Avg Delegative Score | Avg Evaluative Score |
|---------|--------------------:|--------------------:|
| mortgage | 0.347 (SD=0.220) | 0.749 (SD=0.188) |
| checking_savings | 0.310 (SD=0.196) | 0.736 (SD=0.204) |
| credit_card | 0.269 (SD=0.163) | 0.749 (SD=0.212) |
| **Overall** | 0.309 (SD=0.197) | 0.745 (SD=0.202) |

### Cross-Product Comparisons (concordant, averaged scores)

**mortgage vs credit_card:**
- Delegative: mortgage mean=0.347, credit_card mean=0.269, U=3,882,984, p=1.01e-57 ***, Cohen's d=0.399
- Evaluative: mortgage mean=0.749, credit_card mean=0.749, U=3,008,090, p=0.145 , Cohen's d=0.001

**mortgage vs checking_savings:**
- Delegative: mortgage mean=0.347, checking_savings mean=0.310, U=3,297,194, p=3.00e-11 ***, Cohen's d=0.174
- Evaluative: mortgage mean=0.749, checking_savings mean=0.736, U=3,183,428, p=1.28e-05 ***, Cohen's d=0.065

## Table 6: Cross-Product Pattern Comparison — DELEGATIVE Proportion

| Product | Sonnet | GPT-4o | Concordant | Predicted Order |
|---------|-------:|-------:|----------:|:--------------:|
| mortgage | 21.0% | 19.8% | 16.7% | |
| checking_savings | 16.2% | 13.2% | 11.9% | |
| credit_card | 12.3% | 8.8% | 7.1% | |

**Monotonic ordering (mort > check > cc) holds?**
- Sonnet: Yes (21.0% > 16.2% > 12.3%)
- GPT-4o: Yes (19.8% > 13.2% > 8.8%)
- Concordant: Yes (16.7% > 11.9% > 7.1%)

## Table 7: Continuous Score Correlations Between Models (N=8,943)

| Score Pair | Pearson r | p-value | Spearman rho | p-value |
|------------|----------:|--------:|-------------:|--------:|
| Delegative (Sonnet vs GPT-4o) | 0.703 | 0.00e+00 *** | 0.738 | 0.00e+00 *** |
| Evaluative (Sonnet vs GPT-4o) | 0.680 | 0.00e+00 *** | 0.713 | 0.00e+00 *** |

## Table 8: eMFD Correlations with Classification Scores (Spearman)

| Foundation | Sonnet Deleg | GPT-4o Deleg | Sonnet Eval | GPT-4o Eval |
|------------|------------:|------------:|-----------:|-----------:|
| Care | 0.099 *** | 0.129 *** | -0.112 *** | -0.120 *** |
| Fairness | 0.069 *** | 0.106 *** | -0.086 *** | -0.103 *** |
| Loyalty | 0.118 *** | 0.158 *** | -0.108 *** | -0.128 *** |
| Authority | 0.035 ** | 0.074 *** | -0.062 *** | -0.078 *** |
| Sanctity | 0.108 *** | 0.155 *** | -0.119 *** | -0.139 *** |

*Significance: \*p<.05, \*\*p<.01, \*\*\*p<.001*

## Table 9: Confidence-Stratified Concordance

| Confidence Tercile | Range | N | Agreement Rate | Cohen's Kappa |
|-------------------|------:|--:|--------------:|--------------:|
| Low | 0.51–0.78 | 3,759 | 68.8% | 0.356 |
| Medium | 0.78–0.83 | 3,124 | 87.7% | 0.652 |
| High | 0.85–0.97 | 2,060 | 99.2% | 0.970 |
