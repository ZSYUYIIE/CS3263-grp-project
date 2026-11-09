# Results: results\A\x-test-2

115 of 115 instances recorded.

## Status accuracy by group

| Group | Correct status |
|---|---|
| missing_info | 57% (4/7) |
| out_of_scope | 89% (8/9) |
| q1 | 90% (27/30) |
| q2 | 60% (27/45) |
| q2_infeasible | 92% (22/24) |
| **all** | 77% (88/115) |

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| optimal | 60% (27/45) |
| wrong status | 40% (18/45) |

q2/loose: valid 60% (15/25), optimal 60% (15/25)

q2/tight: valid 60% (12/20), optimal 60% (12/20)

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100% (4/4) | 0% (0/4) |
| q2_infeasible/chain | 100% (4/4) | 0% (0/4) |
| q2_infeasible/exclusion | 75% (3/4) | 0% (0/4) |
| q2_infeasible/hidden | 100% (4/4) | 0% (0/4) |
| q2_infeasible/parity | 100% (4/4) | 0% (0/4) |
| q2_infeasible/rule_conflict | 75% (3/4) | 0% (0/4) |

## Format

- unparseable replies: 26
- API/completion errors without an answer: 6
- replies wrapped in fences or extra text: 0
- token usage: {'prompt_tokens': 792853, 'total_tokens': 1067344, 'completion_tokens': 274491}
