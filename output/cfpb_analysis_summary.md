# CFPB Stage 2: Classification & eMFD Analysis Results

Total narratives classified: 9,000
Valid classifications: 8,991
Parse errors: 9

## Table 1: Classification Distribution by Product Type

| Product | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---------|----------:|----------:|---------------:|------:|
| mortgage | 2,290 (76.4%) | 633 (21.1%) | 75 (2.5%) | 2,998 |
| checking_savings | 2,333 (77.9%) | 490 (16.4%) | 172 (5.7%) | 2,995 |
| credit_card | 2,373 (79.2%) | 369 (12.3%) | 256 (8.5%) | 2,998 |
| **Total** | 6,996 (77.8%) | 1,492 (16.6%) | 503 (5.6%) | 8,991 |

## Table 2: Mean Continuous Scores by Product Type

| Product | Delegative Score | Evaluative Score |
|---------|---------------:|----------------:|
| mortgage | 0.335 (SD=0.249) | 0.718 (SD=0.210) |
| checking_savings | 0.300 (SD=0.228) | 0.708 (SD=0.220) |
| credit_card | 0.263 (SD=0.210) | 0.711 (SD=0.233) |
| **Overall** | 0.299 (SD=0.231) | 0.712 (SD=0.221) |

### Cross-Product Comparisons (Mortgage vs Credit Card)

- Delegative score: mortgage mean=0.335, credit_card mean=0.263
  Mann-Whitney U=5,413,026, p=2.36e-44, Cohen's d=0.313

- Evaluative score: mortgage mean=0.718, credit_card mean=0.711
  Mann-Whitney U=4,622,994, p=4.30e-02, Cohen's d=0.030

### Mortgage vs Checking/Savings
- Delegative score: mortgage=0.335, checking_savings=0.300, p=1.10e-08, Cohen's d=0.150
- Evaluative score: mortgage=0.718, checking_savings=0.708, p=3.14e-08, Cohen's d=0.048

## Table 3: eMFD Scores by Classification Category

| Foundation | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE |
|------------|---------|---------|---------|
| Care | 0.02673 (0.00598) | 0.02806 (0.00537) | 0.02852 (0.00824) |
| Fairness | 0.03052 (0.00696) | 0.03156 (0.00607) | 0.03244 (0.00923) |
| Loyalty | 0.02311 (0.00489) | 0.02434 (0.00434) | 0.02420 (0.00695) |
| Authority | 0.02428 (0.00548) | 0.02478 (0.00463) | 0.02603 (0.00732) |
| Sanctity | 0.01999 (0.00461) | 0.02115 (0.00423) | 0.02185 (0.00716) |

### EVALUATIVE vs DELEGATIVE (Mann-Whitney U tests)

- Care: DELEG mean=0.02806, EVAL mean=0.02673, p=2.15e-19, Cohen's d=0.235 ***
- Fairness: DELEG mean=0.03156, EVAL mean=0.03052, p=4.99e-11, Cohen's d=0.159 ***
- Loyalty: DELEG mean=0.02434, EVAL mean=0.02311, p=4.13e-23, Cohen's d=0.267 ***
- Authority: DELEG mean=0.02478, EVAL mean=0.02428, p=1.42e-05, Cohen's d=0.097 ***
- Sanctity: DELEG mean=0.02115, EVAL mean=0.01999, p=3.35e-22, Cohen's d=0.263 ***

## Table 4: eMFD Scores by Product Type

| Foundation | mortgage | checking_savings | credit_card |
|------------|---------|---------|---------|
| Care | 0.02653 (0.00597) | 0.02720 (0.00618) | 0.02742 (0.00601) |
| Fairness | 0.03098 (0.00692) | 0.03088 (0.00716) | 0.03055 (0.00688) |
| Loyalty | 0.02320 (0.00469) | 0.02396 (0.00521) | 0.02296 (0.00493) |
| Authority | 0.02364 (0.00496) | 0.02463 (0.00578) | 0.02512 (0.00559) |
| Sanctity | 0.01995 (0.00449) | 0.02046 (0.00495) | 0.02044 (0.00481) |

## Table 5: Correlation Matrix

Spearman correlations between classification scores and eMFD foundations.

| | Deleg | Eval | Care | Fair | Loya | Auth | Sanc |
|---|---:|---:|---:|---:|---:|---:|---:|
| Deleg | 1.00 | -0.461 | 0.099 | 0.069 | 0.118 | 0.034 | 0.108 |
| Eval | -0.461 | 1.00 | -0.112 | -0.086 | -0.108 | -0.062 | -0.119 |
| Care | 0.099 | -0.112 | 1.00 | 0.862 | 0.853 | 0.806 | 0.861 |
| Fair | 0.069 | -0.086 | 0.862 | 1.00 | 0.837 | 0.814 | 0.851 |
| Loya | 0.118 | -0.108 | 0.853 | 0.837 | 1.00 | 0.859 | 0.837 |
| Auth | 0.034 | -0.062 | 0.806 | 0.814 | 0.859 | 1.00 | 0.790 |
| Sanc | 0.108 | -0.119 | 0.861 | 0.851 | 0.837 | 0.790 | 1.00 |

### Key correlations (with p-values)

- Delegative x Care: rho=0.099, p=7.14e-21 ***
- Delegative x Fairness: rho=0.069, p=4.27e-11 ***
- Delegative x Loyalty: rho=0.118, p=4.44e-29 ***
- Evaluative x Care: rho=-0.112, p=1.35e-26 ***
- Evaluative x Fairness: rho=-0.086, p=3.22e-16 ***
- Evaluative x Loyalty: rho=-0.108, p=1.09e-24 ***

## Table 6: Confidence Distribution by Classification

| Classification | Mean | Median | SD | Min | Max | N |
|----------------|-----:|-------:|---:|----:|----:|--:|
| EVALUATIVE | 0.796 | 0.820 | 0.048 | 0.65 | 0.95 | 6,996 |
| DELEGATIVE | 0.798 | 0.820 | 0.043 | 0.72 | 0.95 | 1,492 |
| UNCLASSIFIABLE | 0.836 | 0.850 | 0.065 | 0.65 | 1.00 | 503 |

One-sided test (DELEGATIVE confidence < EVALUATIVE confidence): U=5,257,165, p=6.81e-01

## Table 7: Product x Classification x Confidence Level

| Product | Classification | High (>0.7) | Medium (0.4-0.7) | Low (<0.4) |
|---------|----------------|----------:|----------------:|-----------:|
| mortgage | EVALUATIVE | 2286 (100%) | 4 (0%) | 0 (0%) |
| mortgage | DELEGATIVE | 633 (100%) | 0 (0%) | 0 (0%) |
| mortgage | UNCLASSIFIABLE | 67 (89%) | 8 (11%) | 0 (0%) |
| checking_savings | EVALUATIVE | 2329 (100%) | 4 (0%) | 0 (0%) |
| checking_savings | DELEGATIVE | 490 (100%) | 0 (0%) | 0 (0%) |
| checking_savings | UNCLASSIFIABLE | 158 (92%) | 14 (8%) | 0 (0%) |
| credit_card | EVALUATIVE | 2371 (100%) | 2 (0%) | 0 (0%) |
| credit_card | DELEGATIVE | 369 (100%) | 0 (0%) | 0 (0%) |
| credit_card | UNCLASSIFIABLE | 248 (97%) | 8 (3%) | 0 (0%) |
