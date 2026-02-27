# CFPB Complaint Database Analysis — Results Section Prose Draft

**Verified against:** cfpb_analysis_summary.md, cfpb_dual_model_analysis.md, interrater_reliability_report.md, within_product_analysis_results.md  
**Last updated:** 2026-02-27  
**Section label:** results_cfpb  
**Position in paper:** Section 5 (after Prolific results) or Section 4 (before Prolific results — TBD)

---

## 4.x CFPB Complaint Database Analysis

The CFPB analysis provides naturalistic evidence for dimensional separability. Where the Prolific experiment tests whether trust dimensions predict distinct post-shock responses in a controlled setting, the CFPB analysis asks whether evaluative and delegative trust are distinguishable in the language of real consumer complaints — filed by people with actual financial grievances, not experimental participants responding to vignettes. The two analyses are methodologically independent: different populations, different product domains, different measurement approaches, and different analytic strategies. Neither depends on the other. This is the triangulation.

### Sample and Classification Procedure

We sampled 9,000 consumer complaint narratives from the CFPB database, equally distributed across three product categories: mortgage (*n* = 3,000), checking and savings (*n* = 3,000), and credit card (*n* = 3,000). These categories were selected to vary in the degree to which the consumer–institution relationship involves delegation of discretionary authority. Mortgage relationships are long-duration, high-stakes, and involve ongoing servicing decisions that consumers cannot easily monitor — conditions that our theoretical framework identifies as conducive to delegative trust. Credit card relationships, by contrast, are largely transactional: the consumer evaluates terms, monitors statements, and assesses performance on observable metrics. Checking and savings accounts fall between these poles.

Each narrative was independently classified by two large language models — Claude Sonnet (Anthropic) and GPT-4o (OpenAI) — using identical prompts that defined the evaluative and delegative trust constructs and asked for (a) a categorical classification (evaluative, delegative, or unclassifiable), (b) continuous scores on each dimension (0–1), and (c) a confidence rating (0–1). Of the 9,000 narratives, Sonnet produced valid classifications for 8,991 (99.9%) and GPT-4o for 8,943 (99.4%). Dual-model analyses use the *N* = 8,943 narratives classified by both models.

### Cross-Product Delegative Gradient

The central prediction is that delegative trust indicators should vary across product categories in a theoretically predictable way: highest for mortgages (long-term, opaque servicing), intermediate for checking and savings (ongoing relationship, moderate complexity), and lowest for credit cards (transactional, transparent terms). Evaluative trust indicators, by contrast, should be relatively uniform, since all three product types involve assessable performance dimensions.

**[TABLE: Cross-Product Delegative Gradient]**

| | Mortgage | Checking/Savings | Credit Card |
|---|---|---|---|
| **Panel A: Delegative Classification Proportion** | | | |
| Sonnet | 21.1% | 16.4% | 12.3% |
| GPT-4o | 19.8% | 13.2% | 8.8% |
| Concordant only | 16.7% | 11.9% | 7.1% |
| **Panel B: Mean Delegative Score (SD)** | | | |
| Sonnet | 0.335 (0.249) | 0.300 (0.228) | 0.263 (0.210) |
| GPT-4o | 0.411 (0.219) | 0.371 (0.194) | 0.329 (0.169) |
| Concordant avg. | 0.347 (0.220) | 0.310 (0.196) | 0.269 (0.163) |
| **Panel C: Mean Evaluative Score (SD)** | | | |
| Sonnet | 0.718 (0.210) | 0.708 (0.220) | 0.711 (0.233) |
| GPT-4o | 0.724 (0.195) | 0.705 (0.207) | 0.731 (0.212) |
| Concordant avg. | 0.749 (0.188) | 0.736 (0.204) | 0.749 (0.212) |

The predicted monotonic ordering — mortgage > checking/savings > credit card — holds for delegative indicators across all three analysis variants: Sonnet-only, GPT-4o-only, and concordant cases. The gradient is robust. For mortgage versus credit card, the delegative score difference is statistically significant and of moderate size: Sonnet *d* = 0.313 (*U* = 5,413,026, *p* < .001); GPT-4o *d* = 0.419 (*U* = 5,545,242, *p* < .001); concordant averaged scores *d* = 0.399 (*U* = 3,882,984, *p* < .001).

Evaluative scores, by contrast, are essentially flat across products. The mortgage–credit card difference in evaluative scores is negligible: Sonnet *d* = 0.030; GPT-4o *d* = −0.031; concordant *d* = 0.001 (n.s., *p* = .145). This asymmetry is precisely what dimensional separability predicts. If the two trust modes were a single underlying construct — "complaint intensity" or "relationship quality" — we would expect both dimensions to co-vary across product types. Instead, only delegative trust tracks the theoretically relevant product dimension (relationship opacity and duration), while evaluative trust remains stable.

### Dual-Model Concordance

A classification scheme is only useful if it can be applied reliably.

**[TABLE: Confidence-Stratified Inter-Model Concordance (N = 8,943)]**

| Confidence Tercile | Range | N | Agreement | Cohen's κ |
|---|---|---|---|---|
| Low | 0.51–0.78 | 3,759 | 68.8% | 0.356 |
| Medium | 0.78–0.83 | 3,124 | 87.7% | 0.652 |
| High | 0.85–0.97 | 2,060 | 99.2% | 0.970 |
| Overall | — | 8,943 | 82.4% | 0.556 |

Overall categorical agreement is 82.4% (κ = 0.556, moderate). This headline figure, however, masks a sharp confidence–concordance gradient. When both models assign high confidence, agreement reaches 99.2% (κ = 0.970, almost perfect). When confidence is low, agreement drops to 68.8% (κ = 0.356). This pattern is theoretically informative: the narratives that are difficult for classifiers are the ambiguous cases where trust mode is genuinely unclear, not cases where the classification scheme is arbitrary.

Continuous scores show strong cross-model convergence. Sonnet and GPT-4o delegative scores correlate at *r* = .703 (Spearman ρ = .738, *p* < .001); evaluative scores at *r* = .680 (ρ = .713, *p* < .001). Both models independently recover the same latent structure in the complaint narratives.

### Moral Foundations Validation

As an independent check on construct validity, we scored all narratives using the extended Moral Foundations Dictionary (eMFD) and compared moral language across trust classifications. The theoretical prediction is specific: delegative trust violations should activate relational moral foundations — particularly loyalty (the foundation most closely associated with trust betrayal) — more than evaluative trust violations.

Narratives classified as delegative scored significantly higher than evaluative narratives on all five moral foundations, with the largest effects for loyalty (*d* = 0.267, *p* < .001) and sanctity (*d* = 0.263, *p* < .001), followed by care (*d* = 0.235, *p* < .001). The loyalty result is particularly important: in the Moral Foundations framework, the loyalty foundation tracks in-group betrayal and allegiance — precisely the relational vocabulary our theory associates with delegative trust violation.

Correlation patterns reinforce this interpretation. Delegative scores correlate positively with all foundations, most strongly with loyalty (ρ = .118, *p* < .001). Evaluative scores correlate *negatively* with all foundations, most strongly with sanctity (ρ = −.119, *p* < .001) and care (ρ = −.112, *p* < .001). These opposing sign patterns hold for both Sonnet and GPT-4o classifications, providing further evidence that the two models are recovering the same construct distinction.

**[TABLE: eMFD Correlations with Trust Scores: Dual-Model Comparison (Spearman ρ)]**

| Foundation | Delegative (Sonnet) | Delegative (GPT-4o) | Evaluative (Sonnet) | Evaluative (GPT-4o) |
|---|---|---|---|---|
| Care | .099*** | .129*** | −.112*** | −.120*** |
| Fairness | .069*** | .106*** | −.086*** | −.103*** |
| Loyalty | .118*** | .158*** | −.108*** | −.128*** |
| Authority | .035** | .074*** | −.062*** | −.078*** |
| Sanctity | .108*** | .155*** | −.119*** | −.139*** |

*\*p < .05, \*\*p < .01, \*\*\*p < .001*

### Human Validation

To assess whether the AI classifications capture distinctions recognizable to a human coder, one author (the first author) independently classified a confidence-stratified subsample of 100 narratives. Stratification ensured representation across confidence levels: 30 low-confidence, 40 medium, and 30 high-confidence narratives (based on Sonnet confidence bins).

Categorical agreement was fair by conventional benchmarks: κ = 0.264 for human–Sonnet and κ = 0.361 for human–GPT-4o. The two AI models agreed more with each other (κ = 0.590) than either did with the human coder. However, the confidence-stratified pattern is dramatic and informative. At high confidence, human–Sonnet agreement reaches 93.3% and human–GPT-4o reaches 90.0%. At low confidence, agreement drops to 30.0% and 50.0%, respectively.

The primary source of disagreement is systematic and interpretable: the human coder classified 56% of narratives as unclassifiable, compared to 21% (Sonnet) and 33% (GPT-4o). The most common disagreement pattern — 23 of 51 disagreement cases — was both AI models classifying a narrative as evaluative where the human coded it as unclassifiable. This reflects a higher threshold for inferring trust language in the human coding: factual complaints that describe service failures without explicit evaluative language (e.g., "they put a hold on my account and I can't access it") were coded unclassifiable by the human but evaluative by the models, which inferred frustration with performance from the complaint structure.

Continuous score correlations tell a more encouraging story. Human and model delegative scores correlate moderately (human–Sonnet *r* = .488, *p* < .001; human–GPT-4o *r* = .511, *p* < .001), and both are substantially lower than the inter-model correlation (*r* = .776). Evaluative score correlations follow the same hierarchy (human–Sonnet *r* = .308; human–GPT-4o *r* = .402; inter-model *r* = .779). The models agree with each other more than with the human, but the human–model agreement is significant and in the expected direction, particularly at high confidence.

We interpret this pattern as follows. The dual-model approach functions as an automated coding system with known biases (over-attribution of evaluative intent in factual narratives). The high-confidence subset, where all three raters converge, represents the clearest cases of each trust mode. The analyses reported above are robust to restricting to concordant cases (see Cross-Product Delegative Gradient), which partially addresses this concern.

### Dimensional Relationship

Our theoretical framework characterizes evaluative and delegative trust as independent dimensions. In the Prolific experiment, the two composites correlate at *r* = .246 (6% shared variance), consistent with dimensional separability. The CFPB data present a more complex picture.

Across the full sample, delegative and evaluative continuous scores are moderately negatively correlated (Sonnet *r* = −.592; GPT-4o *r* = −.574; concordant averaged *r* = −.561). This is substantially stronger than the Prolific correlation and in the opposite direction. Three features of the data suggest this reflects properties of the CFPB sample rather than the constructs themselves.

First, the correlation varies substantially across product types: mortgage *r* = −.807, checking/savings *r* = −.589, credit card *r* = −.400 (Sonnet). If the negative correlation reflected a true inverse relationship between the constructs, we would expect it to be stable across contexts. Instead, it tracks product complexity — strongest where the complaint space is most constrained (mortgages, where nearly every complaint involves either servicing failures or relationship violations) and weakest where complaints are more heterogeneous (credit cards).

Second, the scatter plot (Figure X) reveals that the correlation is partly driven by clustering at classification-typical regions rather than a smooth negative slope. Narratives cluster in a high-evaluative/low-delegative region and a high-delegative/moderate-evaluative region, with relatively sparse representation in the joint-high quadrant. This is consistent with the classification mechanics: when a narrative strongly expresses one trust mode, the classifier assigns lower scores to the other mode, producing a mechanical negative correlation within the classification system.

**[FIGURE: delegative_evaluative_scatter.png — Caption: Delegative versus evaluative trust scores (Sonnet classifications, N = 8,943). Points are colored by product type. The moderate negative correlation (r = −.592) is partly driven by clustering at classification-typical regions rather than a smooth inverse relationship.]**

Third, and most importantly, the CFPB sample is censored: it consists entirely of people who have filed formal complaints. These consumers have already experienced a breakdown in their relationship with the institution. In the language of our framework, the sample is heavily weighted toward cases where at least one trust mode has been violated. In a general population, individuals may hold high levels of both evaluative and delegative trust simultaneously (as the Prolific data suggest). In the CFPB sample, the complaint context compresses the joint distribution toward the violated region of the trust space.

We therefore treat the negative correlation as an informative feature of the complaint context — consistent with the theory's prediction that trust violations are mode-specific — rather than evidence against dimensional independence. The stronger test of independence comes from the Prolific general-population sample, where the weak positive correlation (*r* = .246, 6% shared variance) supports separability.

### Robustness: Narrative Length

Delegative narratives are longer than evaluative narratives across all product types (e.g., mortgage: delegative *M* = 2,144 characters vs. evaluative *M* = 1,590). This raises a potential confound: perhaps longer narratives simply provide more text for classifiers to identify relational cues, and the delegative classification is partly an artifact of narrative length.

To address this, we regressed Sonnet delegative scores on log-transformed character count and product category dummies. Length is a significant predictor (*b* = 0.079, *p* < .001). However, the cross-product delegative gradient retains 74.3% of its magnitude after controlling for length (raw gradient: 0.071; residualized gradient: 0.053).^[Gradient values computed from unrounded mean delegative scores.] The theoretically meaningful between-product variation in delegative trust cannot be explained by narrative length alone.

### Exploratory: Company-Level Variation

As an exploratory analysis, we examined whether specific mortgage companies generate disproportionately more delegative complaints. Among the 15 companies with 50 or more mortgage narratives, delegative classification proportions ranged from 3.6% to 37.8% — a spread of 34.2 percentage points. This variation suggests that institutional behavior may drive the trust mode activated in consumer complaints, a hypothesis consistent with our framework's claim that delegative trust responds to relational rather than performance signals. We return to this finding in the Discussion.

### Summary

The CFPB analysis provides naturalistic evidence for three aspects of our theoretical framework. First, the cross-product delegative gradient — consistent across two independent AI classifiers and robust to narrative length controls — demonstrates that trust modes are separable in real consumer behavior and track theoretically predicted product characteristics. Second, the eMFD analysis shows that delegative complaints activate relational moral vocabulary, particularly loyalty, at higher rates than evaluative complaints. Third, the dual-model approach, validated against human coding at high confidence levels, provides a reliable method for identifying trust modes in unstructured text at scale.

The CFPB database does not cover investment advisory services, which fall under SEC and FINRA jurisdiction rather than CFPB oversight. This means we cannot directly study robo-advisor complaints. We treat this jurisdictional boundary as a triangulation feature rather than a limitation: the CFPB analysis covers banking products using naturalistic complaint data, while the Prolific experiment covers algorithmic investment advice using controlled vignettes. The theoretical framework's predictions hold across both domains, different populations, and different measurement approaches.

---

## Notes for Claude Code

- **Tables needed:** 3 (cross-product gradient, confidence-stratified concordance, eMFD dual-model correlations)
- **Figure needed:** 1 (delegative_evaluative_scatter.png — already generated)
- **Section label:** `\label{sec:results_cfpb}`
- **Cross-references needed:** Will need to reference Prolific results section for the r = .246 comparison
- **Footnote:** One footnote on gradient computation from unrounded means
- **Significance notation:** Match Prolific section conventions (\*p < .05, \*\*p < .01, \*\*\*p < .001)
