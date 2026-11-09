# Results: results\A\x-test-2\route-a-v2_16384_32768

115 of 115 instances recorded.

## Status accuracy by group

| Group | Correct status |
|---|---|
| missing_info | 100% (7/7) |
| out_of_scope | 100% (9/9) |
| q1 | 100% (30/30) |
| q2 | 100% (45/45) |
| q2_infeasible | 100% (24/24) |
| **all** | 100% (115/115) |

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| optimal | 98% (44/45) |
| preference unverified | 2% (1/45) |

q2/loose: valid 100% (25/25), optimal 96% (24/25)

q2/tight: valid 100% (20/20), optimal 100% (20/20)

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100% (4/4) | 0% (0/4) |
| q2_infeasible/chain | 100% (4/4) | 0% (0/4) |
| q2_infeasible/exclusion | 100% (4/4) | 0% (0/4) |
| q2_infeasible/hidden | 100% (4/4) | 0% (0/4) |
| q2_infeasible/parity | 100% (4/4) | 0% (0/4) |
| q2_infeasible/rule_conflict | 100% (4/4) | 0% (0/4) |

## Format

- unparseable replies: 0
- API/completion errors without an answer: 0
- replies wrapped in fences or extra text: 0
- token usage: {'prompt_tokens': 871468, 'total_tokens': 1248813, 'completion_tokens': 377345}
