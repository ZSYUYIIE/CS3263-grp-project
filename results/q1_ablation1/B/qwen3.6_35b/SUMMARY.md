# Results: results\q1_ablation1\B\qwen3.6_35b

400 of 400 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| eligible | 75.9% (107/141) |
| not eligible | 92.4% (208/225) |
| missing info | 78.6% (11/14) |
| out of scope | 100.0% (20/20) |
| **all** | 86.5% (346/400) |

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
- replies that needed repair before parsing: 0
- repair kinds (clean = none needed): {'clean': 400}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 86.5% (346/400)
- strict accuracy (clean replies only count): 86.5% (346/400)
- clean replies right: 86.5% (346/400); repaired replies right: -

## Q1 factors (instances/generate_q1.py)

Balanced accuracy (mean of the 4 per-class accuracies above): 86.7%

**By reason (base cases, plain wording)**

| Value | Correct |
|---|---|
| already_done | 100.0% (6/6) |
| closed | 100.0% (9/9) |
| eligible | 81.5% (44/54) |
| missing_prereq | 100.0% (54/54) |
| precluded | 100.0% (15/15) |
| wrong_term | 66.7% (8/12) |

**By formula complexity level (base cases, plain wording)**

| Value | Correct |
|---|---|
| 1 | 92.0% (46/50) |
| 2 | 88.0% (44/50) |
| 3 | 92.0% (46/50) |

**By wording style (all Q1 base-case renderings)**

| Value | Correct |
|---|---|
| correction | 89.3% (67/75) |
| plain | 90.7% (136/150) |
| scattered | 89.3% (67/75) |

Level 1 against level 3: Fisher exact p = 1.000

**Paired comparisons** (same base case, two versions; exact McNemar on the discordant pairs)

| Comparison | Pairs | Both right | Only first right | Only second right | p |
|---|---|---|---|---|---|
| plain vs scattered wording | 75 | 66 | 3 | 1 | 0.625 |
| plain vs correction wording | 75 | 63 | 4 | 4 | 1.000 |
| term absolute vs 'next semester' | 42 | 18 | 10 | 3 | 0.092 |
| ELIGIBLE base vs with excluding course | 18 | 18 | 0 | 0 | 1.000 |
| ELIGIBLE base vs its missing-prerequisite near-miss | 54 | 44 | 0 | 10 | 0.002 |

**By decision size k** (course codes in the target's prerequisite, preclusion and exclusion lists; state space 2^k; equal-size bins by rank of k, all Q1 instances whose target is in the catalogue)

| k | Instances | Correct |
|---|---|---|
| 1-6 | 95 | 82.1% (78/95) |
| 6-11 | 96 | 90.6% (87/96) |
| 11-16 | 96 | 87.5% (84/96) |
| 16-39 | 96 | 86.5% (83/96) |

Spearman correlation of k with a correct status: rho = 0.05, p = 0.350 (normal approximation)

Missing-prerequisite cases, missing course could be taken now: 100.0% (27/27); could not: 100.0% (27/27); Fisher exact p = 1.000

Correction wording where the retracted course would change the answer: 81.8% (18/22)

**Descriptive groups**

| Group | Correct |
|---|---|
| missing_info | 78.6% (11/14) |
| missing_info_decoy | 100.0% (6/6) |
| out_of_scope | 100.0% (20/20) |

- token usage: {'prompt_tokens': 1131033, 'total_tokens': 1177533, 'completion_tokens': 46500, 'attempts': 400}
