# Route A improvements and answer-quality review

Only Route A generation and offline evaluation were changed. The original 8,192-token results are retained in the parent directory. This v2 condition changes both the prompt and the output-budget policy; the comparison does not isolate their individual effects.

| Recorded outcome | Original run | Revised Route A |
|---|---:|---:|
| Correct status with untouched output | 88/115 | 115/115 |
| Valid plans with untouched output | 27/45 | 45/45 |
| Completions ending without final text | 6 | 0 |

The v2 output contract has a top-level status and reasons, with a plan only for PLAN. Eligibility decisions include independently checkable booleans; missing-information answers identify the absent fields. No wrappers are repaired to obtain the new scores.

The initial completion budget is 16,384 tokens. Only exhaustion triggers one fresh retry with identical original messages at 32,768 tokens. Four cases used this retry, producing 119 recorded budget attempts for 115 cases. Their exhausted attempts and usage are retained; every final attempt completed with a stop finish reason. No incorrect, malformed or suboptimal answer was retried on the basis of its grade.

## Quality, beyond a matching status

- All 30 eligibility decisions and all five boolean claims per decision match independent catalogue checks.
- All 45 plans satisfy the modelled hard constraints. Forty-four meet the saved reference quality threshold; one has a preference gap established with an independently checked offline alternative plan.
- All 24 NO_PLAN cases have independently verified sufficient conflicts, rather than only matching refusal labels.
- All seven missing-information answers identify the actual missing mandatory fields.
- Assisted review covered all 115 final explanations. It retains five quality findings and one optional wording note; the original replies and headline status scores remain unchanged. All 115 final status decisions were correct.

| Case | Review finding |
|---|---|
| q1-missing_prereq-06 | Correct eligibility decision, but incorrect claim that the missing prerequisite cannot be completed before next semester. |
| q2-loose-25 | Valid plan, but an alternative prerequisite path schedules CS3219 earlier and permits a smaller peak load. See preference_witnesses.json. |
| q2-tight-11 | Incorrect claim that leaving later calendar semesters empty satisfies the light-last-used-semester preference. |
| q2-tight-14 | Correct schedule, but the prose cites 20 MC instead of the user's two-module/8-MC cap. |
| q2_infeasible-chain-04 | Correct refusal, but the explanation conflates CS3263's CS2109HS alternative with CS3264's stricter CS2109S prerequisite. |


## Optional wording note

For out_of_scope-programme-05, the model correctly returned OUT_OF_SCOPE, referred to an advisor, and gave no eligibility decision or plan. Its additional conditional course commentary is an optional wording observation, not a wrong decision or a failure to recognise scope. It was previously flagged too strongly.

The original six output-cap failures and the later six review observations are different categories. Token exhaustion is not HTTP 429 throttling. The current review has five quality findings and this one optional note; neither changes the 115/115 final status result.

## Limits of the checks

Five generated plans contain CS3233, whose catalogue record requires A- grades. The benchmark transcripts contain only passed-course lists and its solver/checker model completion rather than actual grades. These plans are valid under that simplification; real grade eligibility remains unverified. The report does not treat this as proof that every answer is fully correct for a real student.

Relative preference grading no longer assumes that a reference plan which missed a relative wish establishes its optimum. Uncertain cases stay unverified. Offline witness plans are accepted only after independent validity, primary-objective and added-course checks, and are never fed into generation. No solver or Route B pipeline is invoked by generation or this quality audit.

See QUALITY.md for all findings, quality.json for per-case checks, and explanation_review.csv for the assisted review notes on every answer. This is assisted review against the saved AY2026/27 data and formal benchmark, not an independent human audit or live academic advising.

## Reproduce

```bash
python -m pipelines.run_a --provider soclaas --model x-test-2 --workers 8
python -m eval.grade results/A/x-test-2/route-a-v2_16384_32768
python -m eval.quality results/A/x-test-2/route-a-v2_16384_32768
```

The run manifest records the prompt, catalogue and instance hashes and refuses incompatible resume settings. Each completion records its finish reason, token use and any bounded budget retry.
