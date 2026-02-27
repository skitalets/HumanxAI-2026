# Introduction and Data & Methods — Prose Draft

**Verified against:** project_briefing_20260227.md, sidecar_memo_triangulation_hardin.md, prolific_instrument_revised_20260221.md, all results files, theory_revisions_hardin.md  
**Last updated:** 2026-02-27  
**Section labels:** introduction, data_methods

---

## Introduction

Why do some investors abandon algorithmic financial advisors after a single bad quarter while others remain patient through prolonged downturns? The behavioral finance literature offers two competing answers. Dietvorst, Simmons, and Massey (2015) document "algorithm aversion" — the tendency to abandon algorithms after observing errors, even when the algorithm outperforms human alternatives. Logg, Minson, and Moore (2019) document the opposite: "algorithm appreciation," a systematic preference for algorithmic over human judgment in predictive domains. These findings have been treated as context-dependent results requiring reconciliation through moderator variables — task type, outcome observability, individual differences — without a unifying theoretical account of why the same class of decision-aid produces opposite reactions.

We propose that the contradiction is an artifact of dimensional collapse. The finance literature treats trust as varying in degree but not in kind: investors trust more or less, along a single continuum. Drawing on philosophical accounts of trust that have not previously been applied to financial relationships — particularly the work of Baier (1986), Holton (1994), Nickel (2012), and Hawley (2014) — we distinguish two qualitatively different trust modes. *Evaluative trust* is evidence-conditional performance assessment: the investor monitors outcomes, compares them to benchmarks, and maintains the relationship insofar as the evidence supports it. Withdrawal takes the form of proportional disappointment. *Delegative trust* is the grant of discretionary authority with acceptance of opacity: the investor transfers judgment to the advisor and refrains from continuous verification. Violation produces not disappointment but betrayal — a reactive attitude whose intensity reflects the depth of the relationship rather than the magnitude of the performance shortfall.

This distinction resolves the algorithm aversion puzzle. Logg et al.'s appreciation and Dietvorst et al.'s aversion are both evaluative trust responding to performance signals — positive in one case, negative in the other. They are movements along the same dimension under different evidentiary conditions, not contradictory findings about human–algorithm interaction. Kormylo, Adjerid, Ball, and Dogan (2025) introduce a third finding that completes the picture: betrayal aversion reduces delegation to human experts but not to algorithmic experts. Our framework explains why — betrayal is the reactive attitude specific to delegative trust violation, and under default experimental conditions, delegative trust toward algorithms does not form. The literature has been studying variation within evaluative trust without recognizing that a second dimension exists.

We test the evaluative/delegative framework using two complementary empirical approaches. First, we analyze 9,000 consumer complaint narratives from the Consumer Financial Protection Bureau (CFPB) database, classifying them for trust mode using dual-model AI classification (Claude Sonnet and GPT-4o). The central finding is a cross-product delegative gradient: delegative trust indicators decline monotonically from mortgage to checking/savings to credit card complaints, tracking the theoretically predicted dimension of relationship opacity and duration, while evaluative trust indicators remain flat. This asymmetric pattern — one dimension varying while the other holds constant across product types — is the signature of dimensional separability.

Second, we conduct a pre-registered between-subjects experiment (N = 354) in which participants encounter a robo-advisory platform under fiduciary, performance, or neutral framing before experiencing an identical adverse performance event. The manipulation does not shift trust modes — a theoretically informative failure we explain through Hardin's (1993) street-level epistemology of trust, which holds that trust postures are learned through experience rather than installed by framing. However, the individual-differences analyses reveal the framework's predictive power: delegative trust is the dominant predictor of resistance to algorithm aversion (B = −0.326, *p* < .001) and resilience to exit (B = −0.206, *p* = .001), while evaluative trust predicts neither outcome.

The paper makes three contributions. First, it introduces the evaluative/delegative distinction to behavioral finance, grounding it in philosophical trust theory and operationalizing it for empirical measurement. Second, it provides convergent evidence from naturalistic and experimental methods that the two trust modes are separable, respond to different signal classes, and predict distinct post-shock behaviors. Third, it resolves the algorithm aversion/appreciation contradiction by showing that both phenomena operate within the evaluative dimension, while the delegative dimension — absent from the experimental literature because standard paradigms do not create conditions for its formation — predicts which investors resist the aversion response. We introduce the concept of *delegative foreclosure* — the structural closure of a trust mode toward a category of trustee, derived from Hardin's insight about self-reinforcing distrust — to explain both the persistence of algorithm aversion in the face of superior performance evidence and the failure of institutional framing to shift trust postures.

The remainder of the paper proceeds as follows. Section 2 develops the theoretical framework, distinguishing evaluative and delegative trust, connecting them to the principal–agent literature and the Money Doctors model, and deriving five pre-registered hypotheses. Section 3 describes the data and methods for both empirical analyses. Section 4 reports the CFPB results. Section 5 reports the Prolific experimental results. Section 6 discusses implications, including the reconciliation of the algorithm aversion literature and the design implications of delegative foreclosure. Section 7 concludes.

---

## Data and Methods

This study employs two complementary empirical approaches: a naturalistic analysis of consumer complaint narratives from the CFPB database and a pre-registered between-subjects experiment conducted on the Prolific platform. The two analyses are methodologically independent — different populations, product domains, measurement instruments, and analytic strategies — and are designed to provide convergent evidence for the evaluative/delegative trust framework through triangulation rather than mutual dependence.

### CFPB Complaint Database Analysis

#### Sample

We sampled 9,000 consumer complaint narratives from the CFPB database, equally distributed across three product categories: mortgage (*n* = 3,000), checking and savings (*n* = 3,000), and credit card (*n* = 3,000). These categories were selected to vary along the dimension our framework identifies as theoretically relevant: the degree to which the consumer–institution relationship involves delegation of discretionary authority. Mortgage relationships are long-duration, high-stakes, and involve ongoing servicing decisions (escrow management, modification processing, loss mitigation) that consumers cannot easily monitor. Credit card relationships are largely transactional, with observable terms and assessable performance on standard metrics (interest rates, fees, dispute resolution). Checking and savings accounts fall between these poles. The sample was drawn from narratives with sufficient text for classification (minimum 50 words) filed between 2018 and 2024.

#### Classification Procedure

Each narrative was independently classified by two large language models — Claude Sonnet (Anthropic) and GPT-4o (OpenAI) — using identical classification prompts. The prompts defined the evaluative and delegative trust constructs using language drawn from the theoretical framework and asked each model to provide three outputs for each narrative: (a) a categorical classification (evaluative, delegative, or unclassifiable), (b) continuous scores on each dimension (0–1 scale), and (c) a confidence rating (0–1 scale). The dual-model approach serves as an automated inter-rater reliability check: agreement between independently developed language models, trained on different data and using different architectures, provides stronger evidence for classification validity than either model alone.

Of the 9,000 narratives, Claude Sonnet produced valid classifications for 8,991 (99.9%) and GPT-4o for 8,943 (99.4%). All dual-model analyses use the *N* = 8,943 narratives successfully classified by both models.

#### Moral Foundations Validation

As an independent construct validity check, all narratives were scored using the extended Moral Foundations Dictionary (eMFD), which provides continuous scores on five moral foundations: care, fairness, loyalty, authority, and sanctity. The theoretical prediction is that delegative trust violations should activate relational moral foundations — particularly loyalty, the foundation most closely associated with betrayal and in-group allegiance — at higher rates than evaluative trust complaints.

#### Human Validation

One author (the first author) independently classified a confidence-stratified subsample of 100 narratives to assess whether AI classifications capture distinctions recognizable to a human coder. The subsample was stratified by Sonnet confidence level (30 low-confidence, 40 medium, 30 high-confidence) to ensure representation across the classification difficulty spectrum.

### Prolific Experiment

#### Design

The experiment employed a between-subjects design with three conditions. Participants were randomly assigned to encounter a hypothetical robo-advisory platform (WealthPath) under one of three framings: fiduciary/relationship (Condition A), performance/analytics (Condition B), or neutral control (Condition C). All participants then experienced an identical adverse performance event before completing dependent measures. The study was pre-registered at AsPredicted (#275,531).

#### Participants

We recruited 471 participants through the Prolific platform, targeting U.S.-based adults with balanced demographic representation. After pre-registered exclusions, the final sample comprised *N* = 354 participants (Condition A: *n* = 115; Condition B: *n* = 127; Condition C: *n* = 112). The exclusion funnel proceeded as follows: 471 initial completes → 468 (excluding survey previews) → 451 (excluding pilot responses) → 446 (Prolific platform matching) → 357 (minimum completion time) → 354 (dual attention/comprehension check). Robustness analyses using stricter exclusion criteria (attention-only: *N* = 342; comprehension-only: *N* = 289) produce identical patterns of significance.

#### Materials

**Condition vignettes.** Each vignette described WealthPath using matched structural features (0.25% annual fee, $1,000 minimum, SIPC protection, custodial banking) while varying the trust framing. Condition A emphasized fiduciary cues: the platform as a "dedicated digital investment partner" and "steward" with "full discretionary authority" and a commitment to "building a lasting relationship." Condition B emphasized evaluative cues: "systematic strategies," "quantitative analysis," "detailed reports," benchmark comparison, and analytics showing "which decisions are working and why." Condition C provided a bare product description with no emphasis in either direction.

Critically, all three vignettes described the same technological agent — no human advisors were introduced in any condition. This addresses a confound in earlier algorithm trust research where fiduciary framing was bundled with human agency.

**Adverse event.** All participants received an identical notification: their WealthPath portfolio declined 8.7% during a quarter in which the S&P 500 declined 8.0%, producing a loss of $870 on a $10,000 investment. The 70-basis-point underperformance was designed to be attributionally ambiguous — enough to register as underperformance for attentive evaluators, but close enough to the benchmark to be dismissible by delegative trusters.

#### Measures

All items used a 7-point Likert scale (1 = Strongly Disagree to 7 = Strongly Agree) unless otherwise noted.

**Evaluative trust** (2 items, α = .429). Items assessed performance-monitoring orientation: "I would want to regularly check WealthPath's performance against market benchmarks" and "I would trust WealthPath primarily because I can verify how it's performing." The low reliability of this composite is a recognized limitation; the scale captures benchmark-monitoring orientation but fails to cohere as a unitary construct. We report results using the composite but note the attenuation of evaluative trust effects throughout.

**Delegative trust** (3 items, α = .807). Items assessed willingness to grant discretionary authority: "I would be comfortable giving WealthPath full discretion to adjust my portfolio as it sees fit"; "I would be willing to let WealthPath make investment decisions without needing to understand each one"; and "Even if I could review every decision WealthPath makes, I probably wouldn't bother."

**Betrayal** (1 item). "After receiving WealthPath's notification about the decline, I feel a sense of betrayal."

**Disappointment** (1 item). "After receiving WealthPath's notification about the decline, I feel disappointed by the results."

**Betrayal premium.** Computed as the difference between betrayal and disappointment scores (Item 6a minus Item 6b), operationalizing Holton's (1994) reactive attitude distinction.

**Exit intent** (1 item). "My first reaction is to research alternative investment platforms rather than wait for WealthPath's strategy to recover."

**Algorithm aversion** (1 item). "After this experience, I would prefer to manage my own investments or work with a human financial advisor rather than continue using an algorithm." This item operationalizes Dietvorst et al.'s (2015) specific definition of algorithm aversion as the shift from algorithmic to human judgment, distinct from general exit-seeking behavior.

**Comprehension check** (1 item, administered immediately after the adverse event). Participants were asked how WealthPath's performance compared to the S&P 500, with four response options. The correct answer (WealthPath performed worse) was selected by 81.6% of the final sample [FLAG: VERIFY THIS PERCENTAGE AGAINST ACTUAL DATA]. Comprehension pass/fail was coded as a covariate in all analyses. Following pre-registered protocol, participants who failed the comprehension check were retained in the primary analyses, with robustness checks excluding them.

**Financial literacy** (3 items). The Lusardi and Mitchell (2014) "Big Three" financial literacy battery: compound interest, inflation, and diversification items. Responses were coded as correct/incorrect and summed to create a 0–3 financial literacy composite.

**Attention check** (1 item). A directed-choice item embedded in the demographic battery instructing participants to select a specific response option. Participants who failed were excluded per the pre-registered protocol.

**Demographics.** Age, income, investment experience, education, and prior robo-advisor experience (binary: have you ever used a robo-advisory platform?).

#### Analytic Strategy

The pre-registered analysis plan specified five hypothesis tests:

H1 (Trust Mode Separation) was tested via one-way ANOVA comparing evaluative and delegative trust composites across conditions, with planned contrasts between Conditions A and B.

H2 (Betrayal Premium) was tested via one-way ANOVA comparing the betrayal premium (6a minus 6b) across conditions, with the prediction that Condition A would produce the largest premium.

H3 (Algorithm Aversion Mechanism) was tested via hierarchical multiple regression predicting algorithm aversion (Item 7b) from evaluative trust, delegative trust, and condition dummies, with the pre-registered prediction that evaluative trust would be the significant predictor.

H4 (Delegative Resilience) was tested via hierarchical multiple regression predicting exit intent (Item 7a) from evaluative trust, delegative trust, and condition dummies.

H5 (Financial Literacy Interaction) was tested via moderated regression including a financial literacy × condition interaction term predicting delegative trust.

All analyses were conducted using the pre-registered exclusion criteria. Robustness analyses using stricter attention-only (*N* = 342) and comprehension-only (*N* = 289) exclusion thresholds are reported alongside primary results.

---

## Notes for Claude Code

- **Section labels:** `\label{sec:introduction}`, `\label{sec:methods}`
- **Subsection labels:** `\label{sec:methods_cfpb}`, `\label{sec:methods_prolific}`, `\label{sec:methods_design}`, `\label{sec:methods_participants}`, `\label{sec:methods_materials}`, `\label{sec:methods_measures}`, `\label{sec:methods_analysis}`
- **Citations to add to .bib if not present:**

```bibtex
@article{lusardi2014financial,
  author = {Lusardi, Annamaria and Mitchell, Olivia S.},
  title = {The Economic Importance of Financial Literacy: Theory and Evidence},
  journal = {Journal of Economic Literature},
  volume = {52},
  number = {1},
  pages = {5--44},
  year = {2014}
}
```

- **FLAG:** The comprehension check pass rate (81.6%) needs to be verified against actual Prolific data. I estimated from the exclusion funnel (289/354) but this is the comprehension-strict subsample, which may not be the same as the comprehension check pass rate. Chris to verify and replace.
- **Cross-references needed:** Hypotheses H1–H5 should reference the theory section where they are formally stated. The adverse event description should match exactly across methods and results sections — verify consistency.
- **The introduction references Section numbers (2–7) — these need to match the actual section numbering in main.tex.**
- **No tables or figures in these sections.**
