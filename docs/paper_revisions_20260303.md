# Paper Revisions -- The Faithful Machine: Trust, Delegation, and Algorithm Aversion in Financial Advice

## Overall Feedback

- The 12pt font is larger than conventional for these drafts. Remove the 12pt parameter in main.tex.
- Look for an opportunity or two to work in the "faithful machine" framing in the introduction and/or theoretical framework to make the payoff in the conclusion.
- Spelling of "truster" / "trustor" is not consistent throughout. I prefer "trustor". Please make this consistent.
- Where we claim that this is the "first time" someone has applied philosophy of trust literature to finance, does that conflict with the fact that Carter et al. (2020) has investigated possible connections conceptually, if not experimentally?
- Everywhere we mention Claude Sonnet, we should report the version number as we do with GPT-4o.
- You refer to the "first author" several times, but there is only one author.

## 1. Introduction

- When we say "Second, we conduct a pre-registered between-subjects experiment (N = 354)" is that number correct? That reports the post-exclusion N rather than the number initially recruited. Don't change it if my question is off base.

## 2. Theoretical Framework: Evaluative and Delegative Trust

- In the sentence beginning "Consider two well-documented patterns ..." the word "well-documented" hangs into the margin.
- In 2.1.1, Evaluative Trust, the sentence beginning "Hardin (2002) models trust as ..." is a run-on after the em-dash.
- In the graf beginning "Holton (1994) provides the critical behavioral distinction ..." does it make sense to cite P. F. Strawson's "Freedom and Resentment," which is the source of the reactive attitudes concept?
- In the graf where we say "platforms that encourage frequent performance monitoring may inadvertently shift users from delegative to evaluative trust", cite Pettit, "The Cunning of Trust," _Philosophy & Public Affairs_, 24 (3), 1995, p. 224–25, where he says that surveillance makes (delegative) trust impossible. This is the text, no need to quote but useful to note this and cite Pettit: "The point is readily illustrated. Imagine the difference that can be made when an organization introduces various checks on when their nonmanagerial staff turn up for work and how they spend their time. Previously a manager in such an organization might have expressed trust in one of their staff by giving her some task to perform that would allow her, if she so wished, to exploit the trustor: to take an excessive amount of time over the job, to do the job sloppily, or whatever. Previously the expression of such trust, flattering as it is, might well have led to a relationship of trust between the manager and the member of staff, with all the attendant benefits that that can bring. But now that the checks have been put in place, the opportunity for the manager to manifest trusting reliance in the member of staff has been removed. The checks mean that the member of staff will have salient and unflattering reasons to comply, so that the manager's request cannot have the aspect of an expression of trust and cannot serve to establish a trusting relationship between the two."
- In the sentence beginning "No amount of performance can reopen it" (and in a couple of other spots through the paper), we suggest that learned distrust makes delegative trust impossible. It would be better to say: "No amoutn of performance is like to reopen it". 
- In 2.1.3, the phase "what has been violated is not a prediction but a grant of vulnerability" is awkward and unclear. It's the "grant of vulnerability" that doesn't make sense to me, maybe "grant of discretion"? Improve this sentence.
- Same section, where you say "This generates the betrayal premium prediction" -- is this our prediction, or Kormylo et al.'s? Cite appropriately.
- Claim 3 is rather strong when it says transparency or auditability eliminates discretionary space. *Auditability* is not the problem, frequent auditing does. The audit culture that O'Neill describes is a problem, but it's the feeling that you *are* being audited that causes the problems, not necessarily the *possibility* of being audited.
- In 2.1.4, we say "This failure has been interpreted as evidence that algorithms cannot receive trust beyond the competence-based dimension." By whom? We need to cite to the literature, please just flag if you can't reliably turn up these citations and we will add it later.
- In 2.2, you say that in the Trust Game, "The payoff matrix is known, the interaction is one-shot". Is the literature this one-dimensional, or are there citations we should make to improved Trust Game experiments, acknowledging them but arguing they still don't capture the full depth of delegative trust?
- You say "If the finance literature validates its trust measures against trust game behavior — and it does extensively (Johnson and Mislin, 2011) - then the empirical foundation may be systematically measuring evaluative trust while the advisory relationships it seeks to explain are substantially delegative." Please check that Johnson and Mislin say this.
- In 2.3, you say peace of mind "reduces the client's *perceived* variance of returns" in the Money Doctors account. Should this say "variance of expected returns"? Or is the idea that peace of mind reduces the perceived variance of actual returns? Check this.
- Also in 2.3, in the phrase "that the evaluative/delegative distinction reveals" the phrase "evaluative/delegative" hangs out into the margin.
- In 2.4, you say "The literature has treated these as context-dependent findings..." Where? Add appropriate citations or flag this for future work by another model.
- Same section, you say "Algorithm appreciation is evaluative trust operating as expected". But our argument leaves space for *delegative* trust in algorithms, too. Should this say "evaluative or delegative"? Or should it not, because we're talking about what others' models test, which is just evaluative? Flag if needed for future work.
- This sentence in the section needs added nuance, I don't think their account is this simple: "Bigman and Gray's finding reflects resistance to extending delegative trust to algorithms, not a generalized aversion."
- Is 2.5 repetitive given later discussion of these topics? In general this section should tie a little more to the trust in finance literature, possibly less to O'Neill. Flag if another model needs to add citations.

## 3. Data and Methods

- In 3.1.4, should we note how confident the models were, and the fact that we stratefied the low/medium/higher confidence sample at a relatively high level to account for this before human validation?
- In 3.2.1, the phrase "performance/analytics" hangs into the margin.
- In 3.2.2, the "preview" participants were all me testing the model. Do we leave this language as is?
- In 3.2.4, the word "Prior" in "Prior robo-advisor experience" is capitalized but should be lowercase.

## 6. Discussion

- In 6.1, is it true that "single-session vignette designs" are "the dominant paradigm in the algorithm aversion literature"? Has no one tried multi-session designs or other empirical means of testing algorithm aversion? Flag for another model if needed to address this.
- In 6.3, you discuss "resistance to algorithm aversion", which seems clunky. Can we not just say "appreciation" as Logg et al. do?

## 7. Conclusion

- The word "dilemma" in the phrase "poses a genuine dilemma" hangs out into the margin.
- Tables C.4, C.5, C.6, and D.1 are still stubs. Please flag these as TODOs.
