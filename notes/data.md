# The data: first inspection

Adds: what is in the downloaded SWE-smith files and what is wrong with them, for Part A and the walkthrough's
"problems in the data" section. Scripts are in `code/data/` (run as `uv run python -I code/data/<x>.py data/raw`);
the data is in `data/raw/`, which git ignores.

## Files

- Trajectories: `SWE-bench/SWE-smith-trajectories`, `data/tool-00000-of-00008.parquet` (249 MB), 3013 rows. Columns: `messages` (a JSON string), `instance_id`, `resolved` (bool), `model`, `traj_id`, `patch`.
- Tasks: `SWE-bench/SWE-smith`, all 11 `train-*.parquet` files (about 280 MB, 59,136 rows), because the file's ids are spread over all 11. Columns: `instance_id`, `patch`, `FAIL_TO_PASS`, `PASS_TO_PASS` (test-id arrays), `image_name`, `repo`, `problem_statement`.
- Join on `instance_id`: 2989 of 3013 rows (99.2%) match. The 24 that don't are all `iterative__dvc.1d6ea681.pr_*` (e.g. `iterative__dvc.1d6ea681.pr_8337`).
- `traj_id` is unique per row and is `instance_id` plus a suffix (e.g. `…func_pm_ctrl_shuffle__viqnyl9u.8qa84d2e`).
- Models: claude-3-7-sonnet-20250219 (2423 rows), claude-3-5-sonnet-20241022 (590).

## Format and how a run ends

- Each message has `role` (system/user/assistant/tool), `content` (a string or a list of `{type, text}` parts), plus `thought`, `action`, `agent`, `message_type`, `tool_calls` and `tool_call_ids`. Tools: `bash`, `str_replace_editor`, `submit`.
- There are two tool-call formats in this one "tool" file. 2052 runs use structured OpenAI-style `tool_calls` with `tool` replies (e.g. `django-money__django-money.835c1ab8.func_pm_ctrl_shuffle__viqnyl9u`). 961 runs have no `tool_calls` at all: the call is inline XML text in the assistant content (`<function=bash><parameter=command>…`), and the replies come back as `user` messages (e.g. `django__channels.a144b4b8.lm_rewrite__9vzepjtr`). A replay has to parse both.
- Submit usually happens twice. SWE-agent's first `submit` returns "Thank you for your work… please review your changes" with the diff, and asks the agent to remove its reproduction scripts and submit again. The final `submit` gets no reply; the run just ends. Structured runs: 2 submits in 1380, 1 in 519, and up to 13 in a few (e.g. `iterative__dvc.1d6ea681.pr_9044`). The "0 submits" count (1109) is the inline runs plus the runs that exited early.
- 157 runs end without a submit, on "Exit due to cost limit" (118), "total execution time exceeded" (33) or a litellm error (4). 14 of those still count as `resolved=True`, presumably because the working-tree diff was graded anyway.
- Every run's last message is from the assistant.

## Agent summary of its fix

- There is no summary field. About 39% of runs (1164) have a "## Summary" or a similar phrase in the last six assistant messages, usually one or two steps before the final submit, because the very last messages are "remove the test scripts" and an empty submit. Example with a summary: `facelessuser__soupsieve.a8080d97.func_pm_remove_cond__0nmyui1x`. Example without one: `bottlepy__bottle.a8dfef30.func_pm_ctrl_invert_if__rsfvwrzq` ("Now let's submit our fix:").
- The closest thing to a summary is the last assistant text over about 80 characters, ignoring a bare submit call. `thought` equals `content` in 65% of assistant messages, so it adds little.

## Confident claims vs `resolved` (Pim's question)

- I labelled a run "confident" when its last three assistant messages contain a success claim ("successfully fixed", "the fix works", "all tests pass", "issue is resolved" and similar; regex in `code/data/inspect_confidence.py`). 1886 of 3013 runs are confident.
- **The claims barely predict the outcome.** P(resolved | confident) = 0.53 against 0.37 when not confident: phi = 0.15, and 0.11 among the runs that ended by a submit. 891 confident runs are unresolved (e.g. `facelessuser__soupsieve.a8080d97.func_pm_remove_cond__0nmyui1x`, `Project-MONAI__MONAI.a09c1f08.func_pm_remove_assign__z47lyy02`). 417 resolved runs make no claim (e.g. `bottlepy__bottle.a8dfef30.func_pm_ctrl_invert_if__rsfvwrzq`). Leaving out runs with hedge words changes nothing (0.53).
- So a reviewer, or a hook, that trusts the agent's "it works" would wave through about 47% failures. This is an argument for checking the diff and the tests rather than the agent's words. Caveat: the label is a phrase match, checked by eye on two runs, not hand-labelled.

## Task description

- It is in both places. SWE-smith's `problem_statement` appears verbatim (whitespace normalised) inside `<pr_description>` in the first user message in 2331 of 2989 joined runs. In the other 658 it doesn't (e.g. `encode__starlette.db5063c2.pr_2711`): the run was probably made from an earlier version of the statement. Not checked further.
- `problem_statement` is empty for 18,033 of the 59,136 tasks, but for none of the 2989 tasks that have a trajectory here.

## The code change: a warning

- **SWE-smith's `patch` is the injected bug, not a fix.** Never show it to the reviewer as the agent's change. No trajectory `patch` equals any task `patch`.
- **The trajectory `patch` column looks misaligned with its rows.** It is empty in 649 rows (254 of them resolved, e.g. `django-money__django-money.835c1ab8.func_pm_ctrl_shuffle__viqnyl9u`, whose run clearly edited `djmoney/forms/widgets.py`). Of the 2364 non-empty patches, 2320 touch files the run never mentions: e.g. `marshmallow-code__apispec.8b421526.func_pm_remove_assign__kdkrbg6a` carries a diff of `flashtext/keyword.py`. In a sample of 150 non-empty patches, 142 touch files that appear in some *other* row's run. This is inferred (a file-path match, not an exact diff match), but it means the column can't be trusted as "this run's final diff".
- The reliable source for the agent's change is the run itself: rebuild it from the `str_replace_editor` create/str_replace/insert calls and `bash` file writes. Failing that, use the diff that the first `submit` reply prints.

## Test output

- The agent runs tests through `bash` (pytest, unittest, tox or runtests in 1430 commands, e.g. `mozillazg__python-pinyin.e42dede5.func_pm_remove_assign__vn346ybe`), plus its own `reproduce_issue.py` scripts, which most runs create and then delete before the final submit.
- Tool output is sometimes truncated: `<response clipped>` in 778 tool messages (mostly long file views, e.g. `marshmallow-code__marshmallow.9716fc62.func_pm_class_rm_funcs__e35a2bbx`), and "Observations should not exceed…" in 84 (e.g. `joke2k__faker.8b401a7d.func_pm_ctrl_invert_if__bompadwm`).
- The official grading tests (FAIL_TO_PASS, PASS_TO_PASS) are only in the task file; their output is not in the trajectory.

## Outcome label

- `resolved`: 1412 True against 1601 False (47% pass), a usable balance.

## Messy bits

- Repeated runs: 2692 instances have 1 run, 159 have 2, and 1 has 3 (`dask__dask.5f61e423.pr_7894`). In 10 instances the runs disagree on `resolved` (e.g. `andialbrecht__sqlparse.e57923b3.lm_rewrite__et9evoo0`). Split by instance, not by row.
- Run length: 9 to 303 messages, median 51. The longest is `conan-io__conan.86f29e13.func_pm_remove_cond__i9t0gz6m`. The JSON is up to 655k characters (median 94k), so a full run often won't fit a small reviewer context.
- Missing data: the 24 dvc ids that have no task row, the empty `patch` values above, and the 157 runs that ended early.
