# Part B: a study of commit-first review on SWE-smith runs

**Hypothesis.** Agent summaries are persuasive and not always faithful to the diff. A reviewer who commits to a verdict on the raw evidence (task, diff, test output) before seeing the summary approves fewer failed fixes than a reviewer who sees the summary from the start. The ability to tell good fixes from bad ones goes up, without a large cost in time or in wrongly denied good fixes.

**Material.** Recorded runs from the SWE-smith-trajectories `tool` split, which give a ground-truth label per run (`resolved`: whether the hidden tests pass). The sample is balanced 50/50 resolved and unresolved, stratified by repo and by the type of injected bug (the `func_pm_*` part of the instance id). It is limited to runs with a final submit and a diff under about 150 lines, so one review fits in a few minutes. The diff is rebuilt from the run itself, because the published `patch` column doesn't match its runs in this file.

**Comparison.** Two arms, each reviewer doing both, with runs assigned at random and no run seen twice by the same reviewer:
- **Control (summary-first):** the same evidence plus the agent's summary on one screen, and one verdict. This is today's approval button.
- **Commit-first:** the hook as built. Verdict 1 on the evidence alone, then the summary is revealed and verdict 2 is given.

The order of arms is counterbalanced. Comparing control with the final commit-first verdict measures the mechanism as a whole. Comparing verdict 1 with verdict 2 inside commit-first shows what the summary adds or takes away once the reviewer has committed.

**Measures.**
- **Primary:** the false-approval rate, i.e. the share of unresolved runs approved.
- **Secondary:**
  - the true-approval rate on resolved runs, and balanced accuracy or d′
  - time per review
  - switch rate from verdict 1 to verdict 2, split into helpful switches (towards the label) and harmful ones
- All analysed with a mixed model with random effects for reviewer and run. Each run's diff size and test-run count are logged, to check whether the effect depends on how much evidence there is.

**Size.** About 20 reviewers (Python developers) × 30 runs each gives about 300 unresolved-run judgements per arm. That is enough to detect a 10-point drop in false approvals from an assumed 40% base rate.

**What would prove me wrong.** These are fixed before the study:
- Commit-first's final false-approval rate is not lower than control's, with the confidence interval ruling out a 10-point drop.
- Or false approvals do drop, but true approvals drop by as much. That would mean reviewers just got stricter, not better at telling fixes apart.
- Or within commit-first, helpful switches after the summary clearly outnumber harmful ones while the arms don't differ. That would mean the summary is informative, and hiding it buys nothing.

**Limits.**
- **`resolved` is not "a reviewer should approve".** A fix can pass the hidden tests and still be bad, or be sound but fail on an unrelated test. Some "errors" will be correct human judgements, so a subset needs expert relabelling.
- **The summary is reconstructed.** SWE-agent writes no formal summary, so the "summary" is the agent's longest closing thought. A real coding assistant's final message may be more polished and more persuasive, so the effect may be larger in practice.
- **The bugs are synthetic.** They were injected on purpose into well-known Python repos, and the agents are older Claude models. Real bugs and real agents may differ.
- **Replay is not live oversight.** Reviewers can't run tests, ask the agent anything, or send it back for another try. The test output is the agent's own choice of scripts, not the real test suite. Denying a run has no cost here, unlike in a real workflow.
- **Committing has its own bias.** Having said verdict 1, people tend to keep it. So verdict 2 is not the same as an informed single verdict; this is why the control arm is needed rather than verdict 1 vs verdict 2 alone.
- **Expertise, fatigue and the knowledge of being studied all apply.** Results from developers unfamiliar with the repo may not carry over to a repo's own maintainers.
