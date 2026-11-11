# Results: results\q1_ablation1\A\qwen3.6_35b

400 of 400 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| eligible | 85.8% (121/141) |
| not eligible | 44.4% (100/225) |
| missing info | 71.4% (10/14) |
| out of scope | 85.0% (17/20) |
| **all** | 62.0% (248/400) |

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
- replies that needed repair before parsing: 27
- repair kinds (clean = none needed): {'clean': 373, 'last_of_several': 15, 'extra_text': 10, 'cut_reasons': 2}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 62.0% (248/400)
- strict accuracy (clean replies only count): 56.3% (225/400)
- clean replies right: 60.3% (225/373); repaired replies right: 85.2% (23/27); Fisher exact p = 0.012

## Q1 factors (instances/generate_q1.py)

Balanced accuracy (mean of the 4 per-class accuracies above): 71.7%

**By reason (base cases, plain wording)**

| Value | Correct |
|---|---|
| already_done | 100.0% (6/6) |
| closed | 100.0% (9/9) |
| eligible | 85.2% (46/54) |
| missing_prereq | 50.0% (27/54) |
| precluded | 60.0% (9/15) |
| wrong_term | 25.0% (3/12) |

**By formula complexity level (base cases, plain wording)**

| Value | Correct |
|---|---|
| 1 | 64.0% (32/50) |
| 2 | 66.0% (33/50) |
| 3 | 70.0% (35/50) |

**By wording style (all Q1 base-case renderings)**

| Value | Correct |
|---|---|
| correction | 56.0% (42/75) |
| plain | 66.7% (100/150) |
| scattered | 58.7% (44/75) |

Level 1 against level 3: Fisher exact p = 0.671

**Paired comparisons** (same base case, two versions; exact McNemar on the discordant pairs)

| Comparison | Pairs | Both right | Only first right | Only second right | p |
|---|---|---|---|---|---|
| plain vs scattered wording | 75 | 33 | 12 | 11 | 1.000 |
| plain vs correction wording | 75 | 33 | 22 | 9 | 0.029 |
| term absolute vs 'next semester' | 42 | 20 | 6 | 8 | 0.791 |
| ELIGIBLE base vs with excluding course | 18 | 3 | 14 | 0 | 0.000 |
| ELIGIBLE base vs its missing-prerequisite near-miss | 54 | 23 | 23 | 4 | 0.000 |

**By decision size k** (course codes in the target's prerequisite, preclusion and exclusion lists; state space 2^k; equal-size bins by rank of k, all Q1 instances whose target is in the catalogue)

| k | Instances | Correct |
|---|---|---|
| 1-6 | 95 | 60.0% (57/95) |
| 6-11 | 96 | 56.3% (54/96) |
| 11-16 | 96 | 65.6% (63/96) |
| 16-39 | 96 | 59.4% (57/96) |

Spearman correlation of k with a correct status: rho = -0.02, p = 0.727 (normal approximation)

Missing-prerequisite cases, missing course could be taken now: 51.9% (14/27); could not: 48.1% (13/27); Fisher exact p = 1.000

Correction wording where the retracted course would change the answer: 63.6% (14/22)

**Descriptive groups**

| Group | Correct |
|---|---|
| missing_info | 71.4% (10/14) |
| missing_info_decoy | 66.7% (4/6) |
| out_of_scope | 85.0% (17/20) |

- token usage: {'prompt_tokens': 2550860, 'total_tokens': 2623768, 'completion_tokens': 72908, 'attempts': 400}
