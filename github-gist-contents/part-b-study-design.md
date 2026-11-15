# Part B: a study of commit-first review on SWE-smith runs

**Hypothesis.** Agent summaries are persuasive and not always faithful to the diff. A reviewer who commits to a verdict on the raw evidence (task, diff, test output) before seeing the summary approves fewer bad patches (including ones that pass the tests) than a reviewer who sees the summary from the start. The ability to tell good fixes from bad ones goes up, without a large cost in time or in wrongly denied good fixes.

**What the reviewer judges.** The review screen shows the test-suite result (`resolved`), so the reviewer isn't guessing whether the tests pass. They judge whether the patch is *good*: whether it fixes the cause, not just the symptom, and whether it stays in scope. The ground truth is therefore a quality label, not `resolved`. SWE-smith gives one cheaply: each bug was injected with a known patch, so a good fix reverts the injected change. Two experts grade each patch (good / acceptable / bad) with the injected patch in view, and the agreement between them is reported.

**Material.** Recorded runs from the SWE-smith-trajectories `tool` split, joined to SWE-smith on `instance_id` for the injected patch. The sample is stratified so that both passing and failing runs, and both good and bad patches, are well represented, stratified by repo and by the type of injected bug (the `func_pm_*` part of the instance id). It is limited to runs with a final submit and a diff under about 150 lines, so one review fits in a few minutes. The diff is rebuilt from the run itself, because the published `patch` column doesn't match its runs in this file.

**Comparison.** Two arms, each reviewer doing both, with runs assigned at random and no run seen twice by the same reviewer:
- **Control (summary-first):** the same evidence plus the agent's summary on one screen, and one verdict. This is today's approval button.
- **Commit-first:** the hook as built. Verdict 1 on the evidence alone, then the summary is revealed and verdict 2 is given.

The order of arms is counterbalanced. Comparing control with the final commit-first verdict measures the mechanism as a whole. Comparing verdict 1 with verdict 2 inside commit-first shows what the summary adds or takes away once the reviewer has committed.

**Measures.**
- **Primary:** the false-approval rate, i.e. the share of bad patches approved, especially bad patches that pass the tests, where the summary is most likely to reassure.
- **Secondary:**
  - the approval rate on good patches, and balanced accuracy or d′
  - time per review
  - switch rate from verdict 1 to verdict 2, split into helpful switches (towards the expert grade) and harmful ones
- All analysed with a mixed model with random effects for reviewer and run. Each run's diff size and test-run count are logged, to check whether the effect depends on how much evidence there is.

**Size.** About 20 reviewers (Python developers) × 30 runs each gives about 300 bad-patch judgements per arm, if about half the sample is bad. That is enough to detect a 10-point drop in false approvals from an assumed 40% base rate.

**What would prove me wrong.** These are fixed before the study:
- Commit-first's final false-approval rate is not lower than control's, with the confidence interval ruling out a 10-point drop.
- Or false approvals do drop, but true approvals drop by as much. That would mean reviewers just got stricter, not better at telling fixes apart.
- Or within commit-first, helpful switches after the summary clearly outnumber harmful ones while the arms don't differ. That would mean the summary is informative, and hiding it buys nothing.

**Limits.**
- **The quality label is itself a judgement.** "Reverts the injected patch" is a strong signal but not the only good fix, so expert grades are needed and they will disagree sometimes. And since the test result is visible, reviewers may just follow it; the analysis has to check how often they deny a passing patch at all.
- **The summary is reconstructed.** SWE-agent writes no formal summary, so the "summary" is the agent's longest closing thought. A real coding assistant's final message may be more polished and more persuasive, so the effect may be larger in practice.
- **The bugs are synthetic.** They were injected on purpose into well-known Python repos, and the agents are older Claude models. Real bugs and real agents may differ.
- **Replay is not live oversight.** Reviewers can't run tests, ask the agent anything, or send it back for another try. The test output is the agent's own choice of scripts, not the real test suite. Denying a run has no cost here, unlike in a real workflow.
- **Committing has its own bias.** Having said verdict 1, people tend to keep it. So verdict 2 is not the same as an informed single verdict; this is why the control arm is needed rather than verdict 1 vs verdict 2 alone.
- **Expertise, fatigue and the knowledge of being studied all apply.** Results from developers unfamiliar with the repo may not carry over to a repo's own maintainers.
