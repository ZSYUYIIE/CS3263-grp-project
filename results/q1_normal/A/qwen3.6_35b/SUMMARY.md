# Results: results\A\qwen3.6_35b

400 of 400 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| eligible | 85.8% (121/141) |
| not eligible | 51.1% (115/225) |
| missing info | 78.6% (11/14) |
| out of scope | 90.0% (18/20) |
| **all** | 66.3% (265/400) |

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|

q2/loose: valid -, optimal -

q2/tight: valid -, optimal -

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 33
- repair kinds (clean = none needed): {'clean': 367, 'last_of_several': 20, 'extra_text': 10, 'cut_reasons': 3}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 66.3% (265/400)
- strict accuracy (clean replies only count): 58.8% (235/400)
- clean replies right: 64.0% (235/367); repaired replies right: 90.9% (30/33); Fisher exact p = 0.001

## Q1 factors (instances/generate_q1.py)

Balanced accuracy (mean of the 4 per-class accuracies above): 76.4%

**By reason (base cases, plain wording)**

| Value | Correct |
|---|---|
| already_done | 100.0% (6/6) |
| closed | 100.0% (9/9) |
| eligible | 87.0% (47/54) |
| missing_prereq | 57.4% (31/54) |
| precluded | 60.0% (9/15) |
| wrong_term | 41.7% (5/12) |

**By formula complexity level (base cases, plain wording)**

| Value | Correct |
|---|---|
| 1 | 68.0% (34/50) |
| 2 | 72.0% (36/50) |
| 3 | 74.0% (37/50) |

**By wording style (all Q1 base-case renderings)**

| Value | Correct |
|---|---|
| correction | 62.7% (47/75) |
| plain | 71.3% (107/150) |
| scattered | 61.3% (46/75) |

Level 1 against level 3: Fisher exact p = 0.660

**Paired comparisons** (same base case, two versions; exact McNemar on the discordant pairs)

| Comparison | Pairs | Both right | Only first right | Only second right | p |
|---|---|---|---|---|---|
| plain vs scattered wording | 75 | 35 | 15 | 11 | 0.557 |
| plain vs correction wording | 75 | 37 | 20 | 10 | 0.099 |
| term absolute vs 'next semester' | 42 | 25 | 5 | 4 | 1.000 |
| ELIGIBLE base vs with excluding course | 18 | 2 | 14 | 1 | 0.001 |
| ELIGIBLE base vs its missing-prerequisite near-miss | 54 | 25 | 22 | 6 | 0.004 |

**By decision size k** (course codes in the target's prerequisite, preclusion and exclusion lists; state space 2^k; equal-size bins by rank of k, all Q1 instances whose target is in the catalogue)

| k | Instances | Correct |
|---|---|---|
| 1-6 | 95 | 64.2% (61/95) |
| 6-11 | 96 | 62.5% (60/96) |
| 11-16 | 96 | 66.7% (64/96) |
| 16-39 | 96 | 65.6% (63/96) |

Spearman correlation of k with a correct status: rho = 0.00, p = 0.989 (normal approximation)

Missing-prerequisite cases, missing course could be taken now: 63.0% (17/27); could not: 51.9% (14/27); Fisher exact p = 0.583

Correction wording where the retracted course would change the answer: 81.8% (18/22)

**Descriptive groups**

| Group | Correct |
|---|---|
| missing_info | 78.6% (11/14) |
| missing_info_decoy | 66.7% (4/6) |
| out_of_scope | 90.0% (18/20) |

- token usage: {'prompt_tokens': 2588860, 'total_tokens': 2656368, 'completion_tokens': 67508, 'attempts': 400}
