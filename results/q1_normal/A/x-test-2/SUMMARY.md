# Results: results\A\x-test-2

400 of 400 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| eligible | 100.0% (141/141) |
| not eligible | 98.7% (222/225) |
| missing info | 100.0% (14/14) |
| out of scope | 100.0% (20/20) |
| **all** | 99.3% (397/400) |

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
- accuracy counting repaired replies by their answer: 99.3% (397/400)
- strict accuracy (clean replies only count): 99.3% (397/400)
- clean replies right: 99.3% (397/400); repaired replies right: -

## Q1 factors (instances/generate_q1.py)

Balanced accuracy (mean of the 4 per-class accuracies above): 99.7%

**By reason (base cases, plain wording)**

| Value | Correct |
|---|---|
| already_done | 100.0% (6/6) |
| closed | 100.0% (9/9) |
| eligible | 100.0% (54/54) |
| missing_prereq | 100.0% (54/54) |
| precluded | 93.3% (14/15) |
| wrong_term | 100.0% (12/12) |

**By formula complexity level (base cases, plain wording)**

| Value | Correct |
|---|---|
| 1 | 100.0% (50/50) |
| 2 | 98.0% (49/50) |
| 3 | 100.0% (50/50) |

**By wording style (all Q1 base-case renderings)**

| Value | Correct |
|---|---|
| correction | 98.7% (74/75) |
| plain | 99.3% (149/150) |
| scattered | 98.7% (74/75) |

Level 1 against level 3: Fisher exact p = 1.000

**Paired comparisons** (same base case, two versions; exact McNemar on the discordant pairs)

| Comparison | Pairs | Both right | Only first right | Only second right | p |
|---|---|---|---|---|---|
| plain vs scattered wording | 75 | 73 | 1 | 1 | 1.000 |
| plain vs correction wording | 75 | 74 | 1 | 0 | 1.000 |
| term absolute vs 'next semester' | 42 | 42 | 0 | 0 | 1.000 |
| ELIGIBLE base vs with excluding course | 18 | 18 | 0 | 0 | 1.000 |
| ELIGIBLE base vs its missing-prerequisite near-miss | 54 | 54 | 0 | 0 | 1.000 |

**By decision size k** (course codes in the target's prerequisite, preclusion and exclusion lists; state space 2^k; equal-size bins by rank of k, all Q1 instances whose target is in the catalogue)

| k | Instances | Correct |
|---|---|---|
| 1-6 | 95 | 100.0% (95/95) |
| 6-11 | 96 | 100.0% (96/96) |
| 11-16 | 96 | 97.9% (94/96) |
| 16-39 | 96 | 99.0% (95/96) |

Spearman correlation of k with a correct status: rho = -0.07, p = 0.168 (normal approximation)

Missing-prerequisite cases, missing course could be taken now: 100.0% (27/27); could not: 100.0% (27/27); Fisher exact p = 1.000

Correction wording where the retracted course would change the answer: 100.0% (22/22)

**Descriptive groups**

| Group | Correct |
|---|---|
| missing_info | 100.0% (14/14) |
| missing_info_decoy | 100.0% (6/6) |
| out_of_scope | 100.0% (20/20) |

- token usage: {'prompt_tokens': 2087191, 'total_tokens': 2251776, 'completion_tokens': 164585, 'attempts': 400}
