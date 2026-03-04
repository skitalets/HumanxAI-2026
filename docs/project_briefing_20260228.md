# Project Briefing: UCLA Anderson "Human × AI Finance" Competition Paper
## Updated February 28, 2026 (end of Day 10)

## Title

**The Faithful Machine: Trust, Delegation, and Algorithm Aversion in Financial Advice**

## Context

Competing in UCLA Anderson's "Human × AI Finance" competition (deadline: March 18, 2026). Philosopher specializing in trust theory and working CFO. Research bridges philosophical trust theory with behavioral finance to explain algorithm aversion in financial advisory contexts. **Complete first draft achieved.** Targeting revision, Refine.ink pass, and finalization in the coming week.

Working with AI research assistant "Sage" (Claude-based, Telegram), Claude Code for data analysis and LaTeX compilation, Claude (this chat) for strategic thinking, writing, and project coordination, and Gemini for additional validation.

Preference: direct critical feedback over reassurance.

## Core Theoretical Contribution

Two independent dimensions of trust that the finance literature currently conflates:

- **Evaluative trust** E(i, j, D) ∈ [0,1]: Evidence-conditional performance assessment. Updates monotonically with performance signals. Exit when E_t falls below threshold. Reactive attitude: disappointment proportional to shortfall.
- **Delegative trust** δ(i, j, D) ∈ [0,1]: Granting discretionary authority with acceptance of opacity. Insensitive to ordinary performance signals (∂δ/∂s_t ≈ 0). Updates via relational signals (fiduciary breach, commitment violation). Reactive attitude: betrayal.

Three formal claims:
1. **Dimensional Separability** — E and δ respond to different signal classes
2. **Asymmetric Post-Shock Response** — High-E investors exit proportional to shortfall; high-δ investors are insensitive to performance shocks but show intense betrayal when relational trust is violated
3. **Transparency Paradox** — Increasing transparency raises evaluative trust (∂E/∂τ > 0) but undermines delegative trust (∂δ/∂τ < 0), formalizing O'Neill (2002)

**New concept (Day 10):** **Delegative foreclosure** — the structural closure of an entire trust mode toward a category of trustee, derived from Hardin (1993). Distinct from algorithm aversion as performance skepticism. Explains persistence of algorithm aversion in the face of superior performance evidence, and the Prolific manipulation failure.

## Current Status: COMPLETE FIRST DRAFT

**Paper metrics:** ~14,400 words core text, 49 pages title-to-conclusion, 71 pages total with bibliography and appendices. Font size is large — reformatting to standard journal conventions (11pt or 10pt) would reduce to ~30–35 pages core text without cuts.

### All Sections Drafted

| Section | Status | Source File |
|---|---|---|
| Introduction | ✅ Drafted | `intro_methods_prose_draft.md` → `sections/introduction.tex` |
| Theoretical Framework | ✅ Drafted + Hardin revision | `theoretical_framework_moves_1_2.md`, `moves_3_6.md`, `theory_revisions_hardin.md` |
| Data and Methods | ✅ Drafted | `intro_methods_prose_draft.md` → `sections/methods.tex` |
| CFPB Results | ✅ Drafted | `results_cfpb_prose_draft.md` → `sections/results_cfpb.tex` |
| Prolific Results | ✅ Drafted | `prolific_results_prose_draft.md` → `sections/results_prolific.tex` |
| Discussion | ✅ Drafted | `discussion_conclusion_prose_draft.md` → `sections/discussion.tex` |
| Conclusion | ✅ Drafted | `discussion_conclusion_prose_draft.md` → `sections/conclusion.tex` |
| Appendix A (CFPB Prompt) | ⚠️ Stub — needs prompt text from Claude Code | `sections/appendices.tex` |
| Appendix B (Instrument) | ✅ Drafted | `appendices_abc_draft.md` |
| Appendix C (Inter-Rater) | ✅ Drafted | `appendices_abc_draft.md` |
| Appendix D (Supp. Tables) | ⚠️ Being built by Claude Code | 10 tables specified, all source data exists |

### Theoretical Framework — Hardin Integration (Day 10)
Three insertions drafted and sent to Claude Code:
- **Move 1:** Hardin's street-level epistemology — trust as learned Bayesian prior, reframes measurement critique
- **Move 2:** Delegative foreclosure defined — closure of trust mode, not revision of trust estimate. Distinguished from Dietvorst-style aversion
- **Move 5:** Foreclosure explains persistence of algorithm aversion despite superior performance evidence

### Discussion Structure (Day 10)
Four substantive subsections plus limitations:
1. **Manipulation failure** — Hardin explains it, robo-experience predictor supports it, implications for experimental design and practice
2. **Dimensional separability across methods** — CFPB gradient + Prolific predictive structure as convergent evidence
3. **Reconciling the literature** — Dietvorst–Logg–Kormylo triangulation: all three findings decompose within two-dimensional framework
4. **Delegative foreclosure and design implications** — Inverts transparency-as-solution assumption, specific robo-advisor design implications, regulatory transparency paradox
5. **Limitations** — Six reported honestly: evaluative trust α, single human coder, censored CFPB sample, correlational robo-experience, manipulation failure for causal claims, no real financial consequences

## Completed Empirical Components

### CFPB Complaint Database Analysis
- 9,000 narratives classified across mortgage, checking/savings, credit card
- Dual-model AI classification (Claude Sonnet + GPT-4o)
- **Key findings:**
  - Cross-product delegative gradient: mortgage (21.1%) > checking/savings (16.4%) > credit card (12.3%), monotonic across all analysis variants
  - Evaluative scores flat (d = 0.030 mortgage vs. credit card) — dimensional separability signature
  - Confidence-stratified concordance: 68.8% → 87.7% → 99.2% (low/medium/high)
  - eMFD validation: delegative complaints higher on all five moral foundations, strongest on loyalty (d = 0.267)
  - Gradient retains 74.3% after narrative length control
  - Company-level variation: 3.6% to 37.8% delegative proportion across mortgage companies
- **Censored sample reframe:** CFPB = conservative test where even small variations are meaningful
- **Dimensional relationship:** Negative correlation (r = −.59) in CFPB vs. positive (r = .246) in Prolific — interpreted as complaint-context censoring, not construct opposition

### Prolific Experiment
- **Sample:** N = 354 after pre-registered exclusions (A=115, B=127, C=112)
- **Pre-registration:** AsPredicted #275,531
- **Key results:**
  - H1 (manipulation): FAILED. All p > .22, all η² < .01.
  - H2 (betrayal premium): NOT SUPPORTED. p = .564.
  - H3 (algorithm aversion): SURPRISING RESULT. Delegative trust dominant predictor (B = −0.326, β = −0.304, p < .001). Evaluative trust n.s. (p = .614). Opposite of prediction but stronger separability evidence.
  - H4 (delegative resilience): CONFIRMED. B = −0.206, β = −0.179, p = .001. Evaluative trust n.s.
  - H5 (literacy × condition): NOT SUPPORTED. p = .87. But robo-advisor experience strongly predicts delegative trust (B = 0.729, p = .001).
- **Measurement limitation:** Evaluative trust α = .429 (2 items). Delegative trust α = .807 (3 items).
- **Robustness:** Strict attention (N=342) and strict comprehension (N=289) produce identical patterns.

## Key Papers Engaged

### Kormylo, Adjerid, Ball & Dogan (2025)
"Till Tech Do Us Part" — Management Science 72(1):343-367.
**Status:** Read by Chris and Sage. Positioning complete.
**Role in paper:** Their finding (no betrayal aversion for algorithms) is confirmatory evidence for our framework. Our explanation (delegative trust requires attribution of discretionary authority, which doesn't form under default experimental conditions) is more fundamental than "people don't feel betrayed by machines." Tone: building on, not correcting.

### Dietvorst–Logg–Kormylo Triangulation
- Logg = evaluative trust with positive signals
- Dietvorst = evaluative trust with negative signals
- Kormylo = delegative trust not forming under default conditions
- **Our contribution:** The literature has been studying variation within evaluative trust without recognizing a second dimension exists

### Hardin (1993) "Street-Level Epistemology of Trust"
**Status:** Integrated into theory section (Day 10).
- Trust postures are learned Bayesian priors, relatively trustee-independent
- Learned extreme distrust forecloses opportunities → delegative foreclosure concept
- Explains manipulation failure and robo-experience predictor

## Sage Status

Sage has read Kormylo et al. and understands the framework's positioning. Initial mapping error (delegative = humans, evaluative = algorithms) corrected. Sage now correctly understands that delegative trust *can* form toward algorithms — the claim is that the literature has only studied algorithms under evaluative trust conditions. Key Sage insight worth keeping: "you can't betray evaluative trust, you just perform poorly."

**Overclaim to watch:** Sage described "Prolific data showing people *can* extend delegative trust to algorithms" — slightly overstated. Prolific shows pre-existing individual differences in delegative trust predict behavioral outcomes. The robo-experience predictor is correlational evidence about formation, not causal demonstration.

## Dissertation Connection (noted Day 10)

Chris noted a developmental ordering of trust modes with potential dissertation implications: delegative trust as primitive (infants have no choice but to delegate), evaluative trust as epistemic achievement, technological trust as further refinement that can be applied back to human trustees. Too large an argument for this paper — at most a footnote or future-directions sentence. Save for dissertation.

## What's Next (Priority Order)

### This weekend:
1. ✅ Print and take home the 71-page draft
2. Read the full paper start-to-finish with a pen — first time anyone has read it as a single document
3. Note tonal inconsistencies, repeated explanations, disconnects between sections written at different times
4. Identify trimming candidates (prose, not reformatting — reformatting is separate)

### Early next week:
5. Reformat to standard journal conventions (11pt or 10pt) — will reduce to ~30–35 pages core
6. Check UCLA Anderson competition for page limits — binding constraint if one exists
7. Defensive citations: ask Sage to identify 10–15 conspicuous bibliography gaps a Management Science reviewer would flag (algorithmic decision-making trust, robo-advisor behavior, fintech adoption, recent philosophy of trust)
8. Populate Appendix A with CFPB classification prompt from Claude Code
9. Verify comprehension check pass rate flag in methods section against actual data
10. Verify Dietvorst et al. (2018) citation (VERIFY WITH SAGE tag still in theory section)
11. Verify Kormylo first author's first name for .bib entry

### Mid-week:
12. Self-review and revision based on weekend read
13. Refine.ink Pass 1 — send core paper (no appendices), flag appendices as available
14. Revise based on Refine.ink feedback
15. Consider NotebookLM or similar for bibliography gap analysis / "reviewer #2" perspective

### Final push (~March 7–10):
16. Final compilation, proofread
17. Post to SSRN
18. Submit to competition (deadline: March 18)

### Post-competition:
19. Refine.ink Passes 2–3
20. Revise for Management Science submission

## Target Structure & Length
- Core text: ~14,400 words (~30–35 formatted pages after reformatting)
- With appendices: ~71 pages current (will compress with reformatting)
- Citation format: natbib/apalike
- ~30 references in .bib plus Kormylo (added) and Lusardi/Mitchell (added). Bibliography remains short — defensive citations needed.

## LaTeX Project Files

| File | Status |
|---|---|
| `main.tex` | ✅ Compiles clean |
| `sections/introduction.tex` | ✅ Built by Claude Code |
| `sections/theoretical_framework.tex` | ✅ With Hardin revisions |
| `sections/methods.tex` | ✅ Built with 3-item change order pending |
| `sections/results_cfpb.tex` | ✅ Built |
| `sections/results_prolific.tex` | ✅ Built |
| `sections/discussion.tex` | ✅ Built |
| `sections/conclusion.tex` | ✅ Built |
| `sections/appendices.tex` | ⚠️ A stub (needs prompt), B+C built, D in progress |
| `references.bib` | ✅ Hardin 1993, Kormylo 2025, Lusardi 2014 added |
| `figures/delegative_evaluative_scatter.png` | ✅ Generated |
| 7 Prolific tables (.tex) | ✅ Verified |
| 3 CFPB tables (.tex) | ✅ In main text |

## Review Workflow
- Self-review of printed draft (this weekend)
- Refine.ink academic AI review: 3-pass option purchased ($120). Pass 1 after self-review. Passes 2-3 held.

## Publication Strategy
- **Preprint:** SSRN Financial Economics Network (Behavioral Finance)
- **Primary target:** Management Science (Kormylo special issue fit, multi-method approach)
- **Secondary:** JBEF, JEBO, JBDM
- **AI disclosure:** Full transparency in methods section about multi-agent AI workflow
