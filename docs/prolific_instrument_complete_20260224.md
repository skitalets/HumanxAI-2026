# Prolific Survey Instrument — Complete Draft
## February 24, 2026

### Revision History

- **February 24, 2026:** Added demographics, financial literacy (Lusardi-Mitchell Big 3), investment experience, and attention checks. Instrument is now complete and ready for pre-registration.
- **February 21, 2026:** Condition A rewritten (removed human/AI confound). Item 6 split into 6a/6b. Item 7 split into 7a/7b. Comprehension check added.

---

## Design Overview

- **Design:** Between-subjects, 3 conditions (A/B/C), 2 stages
- **Platform:** Prolific
- **Target N:** 300–500 respondents (~100–170 per condition)
- **Estimated completion time:** 6–8 minutes
- **Scale:** 7-point Likert (1 = Strongly Disagree to 7 = Strongly Agree) for all attitude/trust items

### Instrument Flow

1. Demographics and financial literacy (FL1–FL3, D1–D6)
2. Random assignment to Condition A, B, or C
3. Vignette presentation
4. Stage 1 items (Items 1–5: evaluative and delegative trust)
5. Adverse event presentation
6. Comprehension check
7. Stage 2 items (Items 6a–7b: reactive attitudes and behavioral response)

---

## Part 1: Demographics and Financial Literacy

*Administered before condition assignment to prevent priming effects.*

### Financial Knowledge

Please answer the following questions to the best of your ability:

**FL1.** Suppose you had $100 in a savings account and the interest rate was 2% per year. After 5 years, how much do you think you would have in the account if you left the money to grow?
1. More than $102
2. Exactly $102
3. Less than $102
4. Don't know

**FL2.** Imagine that the interest rate on your savings account was 1% per year and inflation was 2% per year. After 1 year, how much would you be able to buy with the money in this account?
1. More than today
2. Exactly the same
3. Less than today
4. Don't know

**FL3.** Please tell me whether this statement is true or false: "Buying a single company's stock usually provides a safer return than a stock mutual fund."
1. True
2. False
3. Don't know

*Scoring: FL1 = (1), FL2 = (3), FL3 = (2). Sum correct answers for literacy score (0–3). Split at median for high/low moderator analysis.*

### Background Information

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
- ☐ Used a robo-advisor (e.g., Betterment, Wealthfront)
- ☐ Worked with a human financial advisor
- ☐ Self-directed investing through a brokerage account
- ☐ Employer retirement plan (401k, 403b)
- ☐ No investment experience

**D6.** How much do you agree that attention to detail is important in financial decisions?
*(This question is checking if you are reading carefully. Please select "Somewhat disagree" for this item.)*

1. Strongly disagree
2. Moderately disagree
3. **Somewhat disagree** ← instructed response
4. Neither agree nor disagree
5. Somewhat agree
6. Moderately agree
7. Strongly agree

*Screening: Respondents who fail D6 are flagged. Recommend: retain all respondents but code D6 pass/fail as a covariate. Run primary analyses on full sample and robustness check excluding failures.*

---

## Part 2: Condition Assignment and Vignette

Each respondent is randomly assigned to ONE condition.

### Condition A — Relationship/Fiduciary

"WealthPath is your dedicated digital investment partner, designed to serve as a steward for your long-term financial goals. The platform's algorithms are built to act in your best interest, with full discretionary authority to adjust your portfolio as market conditions change. WealthPath is committed to building a lasting relationship with you through clear communication about its investment approach and personalized service aligned with your financial future. The platform is designed to guide you through market volatility with steady, disciplined investing on your behalf. WealthPath charges a 0.25% annual management fee and requires a $1,000 minimum investment. Account assets are held at a major custodian bank with SIPC protection up to $500,000."

*Delegative cues: steward, best interest, discretionary authority, lasting relationship, guide through volatility, on your behalf. Algorithm is the agent throughout — no humans introduced.*

### Condition B — Performance/Analytics

"WealthPath is a digital investment platform that uses systematic strategies to manage your portfolio efficiently. Our algorithms continuously analyze market data and economic indicators to make disciplined investment decisions based on quantitative analysis rather than emotion. WealthPath follows consistent rebalancing schedules and maintains proper diversification across different types of investments. The platform provides detailed reports showing exactly how your money is allocated and how your investments are performing compared to market benchmarks. You can track your portfolio's progress with clear analytics that show which decisions are working and why. WealthPath charges a 0.25% annual management fee and requires a $1,000 minimum investment. Account assets are held at a major custodian bank with SIPC protection up to $500,000."

*Evaluative cues: systematic, quantitative analysis, detailed reports, benchmark comparison, analytics, "which decisions are working and why." Emphasis on verifiability and performance monitoring.*

### Condition C — Neutral (Control)

"WealthPath is a digital investment platform that automatically manages your portfolio using algorithmic trading strategies. The platform creates diversified portfolios across stocks, bonds, and ETFs based on your risk tolerance and investment timeline. WealthPath charges a 0.25% annual management fee and requires a $1,000 minimum investment. The platform rebalances your portfolio quarterly and provides monthly performance reports through their mobile app. WealthPath has been operating since 2018 and currently manages portfolios for individual investors across all 50 states. Account assets are held at a major custodian bank with SIPC protection up to $500,000."

*Bare product description. No emphasis in either direction.*

---

## Part 3: Stage 1 Items

*Administered immediately after vignette.*

All items: 7-point Likert scale (1 = Strongly Disagree to 7 = Strongly Agree)

**Evaluative Trust Items:**

1. "I would want to regularly check WealthPath's performance against market benchmarks."
2. "I would trust WealthPath primarily because I can verify how it's performing."

**Delegative Trust Items:**

3. "I would be comfortable giving WealthPath full discretion to adjust my portfolio as it sees fit."
4. "I would be willing to let WealthPath make investment decisions without needing to understand each one."
5. "Even if I could review every decision WealthPath makes, I probably wouldn't bother."

---

## Part 4: Adverse Event

*Identical across all conditions.*

"Three months after opening your WealthPath account, you receive this notification:

> *'Your portfolio declined 8.7% this quarter during a broad market downturn. The S&P 500 declined 8.0% over the same period. Our models have adjusted positions to reflect current market conditions. No action is required on your part.'*

Your account balance shows a loss of $870 on your $10,000 investment."

*Underperformance: 70 basis points. Tight enough to be attributionally ambiguous — not obviously incompetent, but enough to create meaningful choice between exit and patience.*

---

## Part 5: Comprehension Check

*Administered immediately after adverse event.*

"Based on the notification you just read, how did WealthPath's performance compare to the overall stock market (S&P 500) during this period?"

1. WealthPath performed better than the market
2. WealthPath performed about the same as the market
3. **WealthPath performed worse than the market** ← correct
4. I'm not sure

*Respondents who select "about the same" or "not sure" may be operating in delegative mode (not attending to relative performance). Retain all respondents; code comprehension as a covariate. Run analyses with and without the comprehension-failure subset.*

---

## Part 6: Stage 2 Items

*Administered after comprehension check.*

All items: 7-point Likert scale (1 = Strongly Disagree to 7 = Strongly Agree)

**Reactive Attitude Items:**

6a. "After receiving WealthPath's notification about the decline, I feel a sense of betrayal."
6b. "After receiving WealthPath's notification about the decline, I feel disappointed by the results."

*Betrayal premium = 6a minus 6b. Prediction: delegative trusters score elevated on both, with betrayal exceeding or matching disappointment. Evaluative trusters score high on disappointment, low on betrayal.*

**Behavioral Response Items:**

7a. "My first reaction is to research alternative investment platforms rather than wait for WealthPath's strategy to recover."
7b. "After this experience, I would prefer to manage my own investments or work with a human financial advisor rather than continue using an algorithm."

*7a = general exit/platform churn. 7b = Dietvorst-style algorithm aversion (algorithm-to-human switch). Related but distinct constructs.*

---

## Scale Reference

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

## Pre-Registration: Key Hypotheses and Analysis Plan

### Primary Hypotheses

**H1 (Trust Mode Separation):** Condition A (fiduciary) produces higher scores on delegative trust items (3–5) than Condition B (performance). Condition B produces higher scores on evaluative trust items (1–2) than Condition A.

**H2 (Betrayal Premium):** The betrayal premium (6a minus 6b) is higher in Condition A than in Condition B. Delegative framing produces betrayal responses; evaluative framing produces disappointment responses.

**H3 (Algorithm Aversion Mechanism):** Item 7b (algorithm-to-human switch) is predicted by evaluative trust scores (Items 1–2) but not delegative trust scores (Items 3–5). Algorithm aversion is an evaluative trust failure, not a delegative trust betrayal.

**H4 (Delegative Resilience):** High delegative trust scores (Items 3–5) predict lower exit-seeking (7a) after the adverse event, controlling for evaluative trust scores.

### Pre-Registered Interaction

**H5 (Financial Literacy × Condition):** The difference between Condition A and Condition B on delegative trust items (3–5) is larger for high-literacy respondents (FL score 2–3) than for low-literacy respondents (FL score 0–1). Low-literacy respondents show elevated delegative scores across all conditions.

*Rationale: Low-sophistication respondents may default to delegative trust because they lack evaluative capacity. The fiduciary framing operates specifically on respondents with the evaluative capacity to be shifted.*

### Exploratory Analyses

**E1 (Variance Prediction):** Condition A produces higher variance on delegative trust items (3–5) than Conditions B or C (Levene's test). The fiduciary framing polarizes respondents into those who can and cannot extend delegative trust to algorithms.

**E2 (Comprehension Check as Signal):** Respondents who fail the comprehension check show higher delegative trust scores and lower evaluative trust scores than respondents who pass, regardless of condition.

**E3 (Robo-Advisor Experience):** Prior robo-advisor experience (D5) moderates the treatment effect, with experienced users showing attenuated framing effects.

### Analysis Approach

- Primary: Between-subjects ANOVA/regression on Items 1–5 by condition
- Secondary: Regression of Stage 2 items (6a, 6b, 7a, 7b) on Stage 1 trust scores with condition and covariates
- Covariates: Financial literacy (FL score), age, investment experience, comprehension check pass/fail, attention check pass/fail
- Moderator: Financial literacy × Condition interaction on Items 3–5
- Robustness: Exclude attention check failures; exclude comprehension check failures

---

## Remaining Steps Before Deployment

- [ ] Pre-register hypotheses and analysis plan (AsPredicted or OSF)
- [ ] Build survey in Prolific/Qualtrics
- [ ] Set randomization weights (equal allocation across 3 conditions)
- [ ] Set Prolific screening criteria (U.S. adults, approval rate >95%)
- [ ] Pilot test with 10–20 respondents to check timing and comprehension
- [ ] Set final sample size and budget ($500–750 target)
