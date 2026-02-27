# Appendices A–C — Prose Draft

**Last updated:** 2026-02-27

---

## Appendix A: CFPB Classification Prompt

The following prompt was used identically for both Claude Sonnet (Anthropic) and GPT-4o (OpenAI) classifications. Each model received the prompt once per narrative and returned a categorical classification, continuous scores on both dimensions, and a confidence rating.

**[INSERT FULL CLASSIFICATION PROMPT FROM CLAUDE CODE SESSION]**

*Note for Claude Code: The full prompt text should be inserted here verbatim, including the construct definitions, the output format specification (categorical classification, continuous delegative score 0–1, continuous evaluative score 0–1, confidence rating 0–1), and any examples or rubric language provided to the models. Format as a block quote or verbatim environment in LaTeX. Do not edit the prompt text — reproduce it exactly as it was used.*

---

## Appendix B: Prolific Survey Instrument

The following instrument was administered via Qualtrics to participants recruited through the Prolific platform. Demographics and financial literacy were administered before condition assignment. Items are reproduced exactly as presented to participants, with the exception of design notes (omitted) and correct answers (indicated in brackets for the financial literacy and comprehension items).

### Part 1: Demographics and Financial Literacy

#### Financial Literacy (Lusardi and Mitchell 2014)

**FL1.** Suppose you had $100 in a savings account and the interest rate was 2% per year. After 5 years, how much do you think you would have in the account if you left the money to grow?

1. More than $102 [correct]
2. Exactly $102
3. Less than $102
4. Don't know

**FL2.** Imagine that the interest rate on your savings account was 1% per year and inflation was 2% per year. After 1 year, how much would you be able to buy with the money in this account?

1. More than today
2. Exactly the same
3. Less than today [correct]
4. Don't know

**FL3.** Please tell me whether this statement is true or false: "Buying a single company's stock usually provides a safer return than a stock mutual fund."

1. True
2. False [correct]
3. Don't know

*Scoring: Sum of correct responses (0–3).*

#### Background Information

**D1.** What is your age? _____ years

**D2.** What is your gender?

1. Male
2. Female
3. Non-binary
4. Prefer not to say

**D3.** What is your annual household income before taxes?

1. Under $25,000
2. $25,000–$49,999
3. $50,000–$74,999
4. $75,000–$99,999
5. $100,000–$149,999
6. $150,000–$199,999
7. $200,000 or more

**D4.** What is your highest level of education?

1. Less than high school
2. High school diploma or GED
3. Some college
4. Bachelor's degree
5. Graduate degree

**D5.** Which of the following investment experiences have you had? (Check all that apply)

- Used a robo-advisor (e.g., Betterment, Wealthfront)
- Worked with a human financial advisor
- Self-directed investing through a brokerage account
- Employer retirement plan (401k, 403b)
- No investment experience

**D6.** [Attention Check] How much do you agree that attention to detail is important in financial decisions? *(This question is checking if you are reading carefully. Please select "Somewhat disagree" for this item.)*

1. Strongly Disagree
2. Moderately Disagree
3. Somewhat Disagree [instructed response]
4. Neither Agree nor Disagree
5. Somewhat Agree
6. Moderately Agree
7. Strongly Agree

### Part 2: Condition Vignettes

Participants were randomly assigned to one of three conditions. All vignettes describe the same technological agent (WealthPath) with matched structural features (0.25% annual fee, $1,000 minimum, SIPC protection, custodial banking). Only the trust framing varies.

#### Condition A — Relationship/Fiduciary

"WealthPath is your dedicated digital investment partner, designed to serve as a steward for your long-term financial goals. The platform's algorithms are built to act in your best interest, with full discretionary authority to adjust your portfolio as market conditions change. WealthPath is committed to building a lasting relationship with you through clear communication about its investment approach and personalized service aligned with your financial future. The platform is designed to guide you through market volatility with steady, disciplined investing on your behalf. WealthPath charges a 0.25% annual management fee and requires a $1,000 minimum investment. Account assets are held at a major custodian bank with SIPC protection up to $500,000."

#### Condition B — Performance/Analytics

"WealthPath is a digital investment platform that uses systematic strategies to manage your portfolio efficiently. Our algorithms continuously analyze market data and economic indicators to make disciplined investment decisions based on quantitative analysis rather than emotion. WealthPath follows consistent rebalancing schedules and maintains proper diversification across different types of investments. The platform provides detailed reports showing exactly how your money is allocated and how your investments are performing compared to market benchmarks. You can track your portfolio's progress with clear analytics that show which decisions are working and why. WealthPath charges a 0.25% annual management fee and requires a $1,000 minimum investment. Account assets are held at a major custodian bank with SIPC protection up to $500,000."

#### Condition C — Neutral Control

"WealthPath is a digital investment platform that automatically manages your portfolio using algorithmic trading strategies. The platform creates diversified portfolios across stocks, bonds, and ETFs based on your risk tolerance and investment timeline. WealthPath charges a 0.25% annual management fee and requires a $1,000 minimum investment. The platform rebalances your portfolio quarterly and provides monthly performance reports through their mobile app. WealthPath has been operating since 2018 and currently manages portfolios for individual investors across all 50 states. Account assets are held at a major custodian bank with SIPC protection up to $500,000."

### Part 3: Stage 1 Items (Evaluative and Delegative Trust)

Administered immediately after vignette. All items use a 7-point Likert scale (1 = Strongly Disagree to 7 = Strongly Agree).

**Evaluative Trust (α = .429):**

1. "I would want to regularly check WealthPath's performance against market benchmarks."
2. "I would trust WealthPath primarily because I can verify how it's performing."

**Delegative Trust (α = .807):**

3. "I would be comfortable giving WealthPath full discretion to adjust my portfolio as it sees fit."
4. "I would be willing to let WealthPath make investment decisions without needing to understand each one."
5. "Even if I could review every decision WealthPath makes, I probably wouldn't bother."

### Part 4: Adverse Event

Identical across all conditions.

"Three months after opening your WealthPath account, you receive this notification:

> *'Your portfolio declined 8.7% this quarter during a broad market downturn. The S&P 500 declined 8.0% over the same period. Our models have adjusted positions to reflect current market conditions. No action is required on your part.'*

Your account balance shows a loss of $870 on your $10,000 investment."

### Part 5: Comprehension Check

"Based on the notification you just read, how did WealthPath's performance compare to the overall stock market (S&P 500) during this period?"

1. WealthPath performed better than the market
2. WealthPath performed about the same as the market
3. WealthPath performed worse than the market [correct]
4. I'm not sure

### Part 6: Stage 2 Items (Reactive Attitudes and Behavioral Response)

Administered after comprehension check. All items use the same 7-point Likert scale.

**Reactive Attitudes:**

6a. "After receiving WealthPath's notification about the decline, I feel a sense of betrayal."
6b. "After receiving WealthPath's notification about the decline, I feel disappointed by the results."

*Betrayal premium = Item 6a minus Item 6b.*

**Behavioral Response:**

7a. "My first reaction is to research alternative investment platforms rather than wait for WealthPath's strategy to recover."
7b. "After this experience, I would prefer to manage my own investments or work with a human financial advisor rather than continue using an algorithm."

### Scale Reference

| Value | Label |
|-------|-------|
| 1 | Strongly Disagree |
| 2 | Moderately Disagree |
| 3 | Somewhat Disagree |
| 4 | Neither Agree nor Disagree |
| 5 | Somewhat Agree |
| 6 | Moderately Agree |
| 7 | Strongly Agree |

---

## Appendix C: Inter-Rater Reliability Details

This appendix reports the full inter-rater reliability analysis for the CFPB classification system. Three raters classified a confidence-stratified subsample of 100 narratives: one human coder (the first author) and two large language models (Claude Sonnet and GPT-4o). Additionally, full-sample concordance statistics are reported for the dual-model classification of all 8,943 narratives classified by both models.

### C.1 Human Validation Sample

The 100-narrative subsample was stratified by Sonnet confidence level to ensure representation across the classification difficulty spectrum: 30 low-confidence narratives (Sonnet confidence < 0.75), 40 medium-confidence narratives (0.75–0.85), and 30 high-confidence narratives (> 0.85). The human coder classified each narrative independently using the same construct definitions provided to the AI models, recording a categorical classification (evaluative, delegative, or unclassifiable), continuous delegative and evaluative scores (0–1, using a slider input rounded to 0.1 increments), and a categorical confidence rating (high, medium, or low).

### C.2 Pairwise Categorical Agreement

| Pair | Cohen's κ | 95% CI | % Agreement | Interpretation |
|---|---|---|---|---|
| Human vs. Sonnet | 0.264 | [0.136, 0.397] | 54.0% | Fair |
| Human vs. GPT-4o | 0.361 | [0.207, 0.507] | 62.0% | Fair |
| Sonnet vs. GPT-4o | 0.590 | [0.442, 0.725] | 77.0% | Moderate |

Interpretation benchmarks (Landis and Koch 1977): < 0.20 poor, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect.

### C.3 Pairwise Continuous Score Correlations

Human scores were recorded using 0.1-increment slider input; LLM scores are continuous floats. Correlations are computed on raw values.

**Delegative Score:**

| Pair | Pearson *r* | *p* | Spearman ρ | *p* |
|---|---|---|---|---|
| Human vs. Sonnet | .488 | 2.65e-07 | .377 | 1.11e-04 |
| Human vs. GPT-4o | .511 | 5.69e-08 | .372 | 1.40e-04 |
| Sonnet vs. GPT-4o | .776 | 2.50e-21 | .827 | 3.00e-26 |

**Evaluative Score:**

| Pair | Pearson *r* | *p* | Spearman ρ | *p* |
|---|---|---|---|---|
| Human vs. Sonnet | .308 | 1.83e-03 | .400 | 3.68e-05 |
| Human vs. GPT-4o | .402 | 3.31e-05 | .458 | 1.62e-06 |
| Sonnet vs. GPT-4o | .779 | 1.33e-21 | .818 | 3.06e-25 |

### C.4 Confusion Matrices

**Human vs. Sonnet:**

| Human \ Sonnet | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| EVALUATIVE | 29 | 10 | 0 | 39 |
| DELEGATIVE | 1 | 4 | 0 | 5 |
| UNCLASSIFIABLE | 34 | 1 | 21 | 56 |
| Total | 64 | 15 | 21 | 100 |

**Human vs. GPT-4o:**

| Human \ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| EVALUATIVE | 30 | 4 | 5 | 39 |
| DELEGATIVE | 1 | 4 | 0 | 5 |
| UNCLASSIFIABLE | 24 | 4 | 28 | 56 |
| Total | 55 | 12 | 33 | 100 |

**Sonnet vs. GPT-4o:**

| Sonnet \ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| EVALUATIVE | 49 | 4 | 11 | 64 |
| DELEGATIVE | 5 | 8 | 2 | 15 |
| UNCLASSIFIABLE | 1 | 0 | 20 | 21 |
| Total | 55 | 12 | 33 | 100 |

### C.5 Confidence-Stratified Agreement (100-Narrative Subsample)

| Confidence Bin | N | Human–Sonnet | Human–GPT-4o | Sonnet–GPT-4o |
|---|---|---|---|---|
| Low (< 0.75) | 30 | 30.0% | 50.0% | 50.0% |
| Medium (0.75–0.85) | 40 | 42.5% | 50.0% | 82.5% |
| High (> 0.85) | 30 | 93.3% | 90.0% | 96.7% |

### C.6 Classification Distribution Comparison

| Category | Human | Sonnet | GPT-4o |
|---|---|---|---|
| EVALUATIVE | 39 (39%) | 64 (64%) | 55 (55%) |
| DELEGATIVE | 5 (5%) | 15 (15%) | 12 (12%) |
| UNCLASSIFIABLE | 56 (56%) | 21 (21%) | 33 (33%) |

The human coder classified substantially more narratives as unclassifiable (56%) than either AI model (Sonnet: 21%, GPT-4o: 33%), reflecting a higher threshold for inferring trust-relevant language from factual complaint descriptions.

### C.7 Disagreement Pattern Analysis

Of the 100 narratives, 49 received unanimous agreement across all three raters. The remaining 51 disagreements followed systematic patterns:

| Human | Sonnet | GPT-4o | Count |
|---|---|---|---|
| UNCLASSIFIABLE | EVALUATIVE | EVALUATIVE | 23 |
| UNCLASSIFIABLE | EVALUATIVE | UNCLASSIFIABLE | 8 |
| EVALUATIVE | DELEGATIVE | EVALUATIVE | 4 |
| EVALUATIVE | DELEGATIVE | DELEGATIVE | 4 |
| UNCLASSIFIABLE | EVALUATIVE | DELEGATIVE | 3 |
| EVALUATIVE | EVALUATIVE | UNCLASSIFIABLE | 3 |
| EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | 2 |
| Other patterns | | | 4 |

The dominant disagreement pattern (23 of 51 cases, 45%) involves both AI models classifying a narrative as evaluative where the human coded it as unclassifiable. These cases typically involve factual complaints describing service failures (account holds, missing documents, disputed charges) without explicit evaluative language. The AI models inferred frustrated performance expectations from the complaint structure; the human coder required more explicit evaluative vocabulary to assign the classification.

### C.8 Illustrative Disagreement Cases

**Case 1 (Complaint #4121639, Checking/Savings, Chime Financial).** A consumer reports that Chime placed a hold on their account containing unemployment back pay and that they sent all requested documentation. The human coded this as UNCLASSIFIABLE ("factual"), while both Sonnet and GPT-4o coded it as EVALUATIVE, interpreting the account hold despite compliance with documentation requests as an implicit performance failure. This illustrates the threshold difference: the human required explicit evaluative language, while the models inferred it from the service failure structure.

**Case 2 (Complaint #10717654, Mortgage, Mr. Cooper).** A consumer reports missing loan documents, discrepancies in payoff quotes, and COVID deferral payments reported as delinquent. The human coded this as UNCLASSIFIABLE ("factual, no evaluative or delegative language"), while both models coded it as EVALUATIVE, interpreting the document failures and credit reporting errors as implicit performance complaints. Again, the complaint describes functional failures without using the language of frustrated expectations.

**Case 3 (Complaint #7441427, Credit Card, Wells Fargo).** A consumer reports disputed fraudulent charges that Wells Fargo repeatedly denied. The human coded this as EVALUATIVE (noting "frustrated expectations"), Sonnet coded it as DELEGATIVE (citing "I feel like I'm not being heard"), and GPT-4o coded it as EVALUATIVE (focusing on incorrect charges). This case illustrates genuine construct ambiguity: the complaint contains both evaluative elements (the fraud process failed) and delegative elements (the relationship feels unresponsive), and reasonable coders disagree about which mode dominates.

### C.9 Full-Sample Dual-Model Concordance (N = 8,943)

For reference, the full-sample concordance statistics for the complete CFPB dataset:

**Concordance Table:**

| Sonnet \ GPT-4o | EVALUATIVE | DELEGATIVE | UNCLASSIFIABLE | Total |
|---|---|---|---|---|
| EVALUATIVE | 6,037 | 351 | 575 | 6,963 |
| DELEGATIVE | 519 | 877 | 81 | 1,477 |
| UNCLASSIFIABLE | 30 | 18 | 455 | 503 |
| Total | 6,586 | 1,246 | 1,111 | 8,943 |

Overall agreement: 7,369/8,943 (82.4%), κ = 0.556.

Concordant cases by product:

| Product | Concordant | Discordant | Agreement |
|---|---|---|---|
| Mortgage | 2,472 | 502 | 83.1% |
| Checking/Savings | 2,405 | 580 | 80.6% |
| Credit Card | 2,492 | 492 | 83.5% |

Continuous score correlations between models (*N* = 8,943): delegative *r* = .703 (ρ = .738), evaluative *r* = .680 (ρ = .713), all *p* < .001.

---

## Notes for Claude Code

- **Appendix A** has a placeholder for the CFPB classification prompt. Chris will provide the prompt text from Claude Code session history. Insert it verbatim in a `\begin{quote}` or `\begin{verbatim}` environment.
- **Appendix B** reproduces the instrument exactly as administered. Use `\begin{enumerate}` for response options. Correct answers are indicated in brackets — these should be formatted as marginal notes or footnotes in LaTeX, not inline.
- **Appendix C** contains 8 tables and 3 illustrative cases. Tables should use standard `\begin{table}` environments. The illustrative cases should be formatted as indented block text with complaint ID, product, and company in bold.
- **Section labels:** `\label{app:cfpb_prompt}`, `\label{app:instrument}`, `\label{app:interrater}`
- **No new .bib entries needed** beyond what's already been added (Lusardi and Mitchell 2014 is the only citation, already in .bib from methods section).
