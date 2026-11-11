# Results: results\alternative\a_plus\qwen3.6_35b\round_3

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 23.3% (140/600) |
| no plan | 98.3% (236/240) |
| missing info | 13.3% (4/30) |
| out of scope | 56.7% (17/30) |
| **all** | 44.1% (397/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 41.0% (369/900)
- valid-answer accuracy, gold PLAN instances: 18.7% (112/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 11.8% (71/600)
- valid plans that are not optimal: 36.6% (41/112)
- over-refusal (gold PLAN answered NO_PLAN): 76.7% (460/600)
- correct refusal, gold NO_PLAN instances: 98.3% (236/240)
- invented plan, gold NO_PLAN instances: 1.7% (4/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| over-refusal | 76.7% (460/600) |
| optimal | 11.8% (71/600) |
| invalid | 4.7% (28/600) |
| preference gap | 4.0% (24/600) |
| objective gap | 2.0% (12/600) |
| extra courses | 0.8% (5/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R3: 31
- R4: 17
- R9: 9
- R10: 3
- R11: 2
- R6: 2
- R1: 1
- R8: 1

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/chain | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/exclusion | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/hidden | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/parity | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/rule_conflict | 97.5% (39/40) | 2.5% (1/40) |

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 171
- repair kinds (clean = none needed): {'clean': 729, 'extra_text': 77, 'cut_reasons': 78, 'last_of_several': 15, 'control_chars': 1}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 44.1% (397/900)
- strict accuracy (clean replies only count): 34.3% (309/900)
- clean replies right: 42.4% (309/729); repaired replies right: 51.5% (88/171); Fisher exact p = 0.033
- valid-answer accuracy, clean replies: 39.2% (286/729); repaired replies: 48.5% (83/171); Fisher exact p = 0.031
- valid-answer accuracy counting only clean replies as right (strict): 31.8% (286/900)
- optimal-plan accuracy, clean replies: 7.9% (37/471); repaired replies: 26.4% (34/129); Fisher exact p = 0.000
- optimal-plan accuracy counting only clean replies as right (strict): 6.2% (37/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 14.0% (24/171) | 10.5% (18/171) | 508 | 16994 | 198374 |
| S2 | 63 | 12.7% (8/63) | 11.1% (7/63) | 880 | 13115 | 160965 |
| S3 | 273 | 21.6% (59/273) | 12.8% (35/273) | 782 | 21741 | 190478 |
| S4 | 312 | 80.4% (251/312) | 13.9% (10/72) | 409.5 | 12983.5 | 150576 |
| S5 | 21 | 28.6% (6/21) | 4.8% (1/21) | 1678 | 16162 | 430639 |
| S6 | 60 | 35.0% (21/60) | - | 134.5 | 10074.5 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 13.3% (4/30) | - | 321.5 | 9500 | - |
| NO_PLAN | 240 | 98.3% (236/240) | - | 331.5 | 12185.5 | - |
| OUT_OF_SCOPE | 30 | 56.7% (17/30) | - | 49.5 | 10222.5 | - |
| PLAN | 600 | 18.7% (112/600) | 11.8% (71/600) | 765.5 | 19364 | 187333 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 33.6% (50/149) | 6.1% (6/99) | 280 | 11128 | 273209 |
| 3-4 | 318 | 35.5% (113/318) | 7.3% (18/246) | 757 | 17691 | 326873 |
| 5-6 | 296 | 39.9% (118/296) | 12.4% (25/202) | 598.5 | 20526.5 | 193547 |
| 7-8 | 117 | 70.9% (83/117) | 41.5% (22/53) | 518 | 12712 | 42681 |
| not given | 10 | 10.0% (1/10) | - | 357.5 | 10875 | - |
| outside 1-8 | 10 | 40.0% (4/10) | - | 85 | 10222.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 50.7% (147/290) | 21.3% (37/174) | 430.5 | 12521 | 84147 |
| 6-8 | 445 | 43.6% (194/445) | 9.5% (27/284) | 614 | 17728 | 242481 |
| 10-12 | 155 | 17.4% (27/155) | 4.9% (7/142) | 659 | 19197 | 520029 |
| not given | 10 | 10.0% (1/10) | - | 123 | 3877 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 45.0% (131/291) | 13.8% (26/189) | 460 | 14607 | 150083 |
| earliest_graduation | 291 | 41.6% (121/291) | 9.7% (18/186) | 579 | 15366 | 245773 |
| min_total_mc | 318 | 36.8% (117/318) | 12.0% (27/225) | 597.5 | 15394 | 184244 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 22.0% (9/41) | 14.3% (3/21) | 309 | 11815 | 178593 |
| 1 | 21 | 9.5% (2/21) | 0.0% (0/21) | 356 | 20410 | - |
| 2 | 340 | 39.4% (134/340) | 10.7% (25/234) | 597 | 15271 | 207149 |
| 3 | 277 | 42.2% (117/277) | 10.6% (20/189) | 589 | 17767 | 213492 |
| 4+ | 221 | 48.4% (107/221) | 17.0% (23/135) | 429 | 13487 | 124413 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 24.4% (10/41) | 9.5% (2/21) | 328 | 11815 | 297919 |
| 1 | 77 | 66.2% (51/77) | 16.2% (6/37) | 554 | 17952 | 153394 |
| 2 | 271 | 42.1% (114/271) | 15.9% (31/195) | 597 | 18991 | 137114 |
| 3 | 286 | 38.5% (110/286) | 9.4% (18/192) | 526 | 14936.5 | 246185 |
| 4+ | 225 | 37.3% (84/225) | 9.0% (14/155) | 518 | 13077 | 221612 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 43.1% (355/823) | 12.0% (63/523) | 499 | 13767 | 171615 |
| yes | 77 | 18.2% (14/77) | 10.4% (8/77) | 1367 | 30794 | 311114 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 43.9% (361/823) | 12.2% (64/523) | 524 | 14652 | 182585 |
| yes | 77 | 10.4% (8/77) | 9.1% (7/77) | 631 | 19486 | 230745 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 41.0% (287/700) | 10.0% (47/470) | 508.5 | 16197.5 | 225946 |
| scattered | 100 | 33.0% (33/100) | 7.7% (5/65) | 829 | 14362 | 274396 |
| unsupported | 100 | 49.0% (49/100) | 29.2% (19/65) | 466 | 13633.5 | 68905 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 26.5% (9/34) | 26.5% (9/34) | 444.5 | 16626.5 | 64411 |
| 3 to below 6 | 28 | 17.9% (5/28) | 10.7% (3/28) | 1586.5 | 21662.5 | 221082 |
| 6 to below 10 | 24 | 12.5% (3/24) | 8.3% (2/24) | 2799.5 | 26222.5 | 321199 |
| 10 to below 24 | 43 | 11.6% (5/43) | 7.0% (3/43) | 645 | 16994 | 329625 |
| 24 and above | 42 | 4.8% (2/42) | 2.4% (1/42) | 299.5 | 12401 | 696516 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 16.7% (3/18) | 16.7% (3/18) | 355.5 | 16070 | 102419 |
| 3 | 24 | 20.8% (5/24) | 16.7% (4/24) | 1056.5 | 24956.5 | 165880 |
| 4 | 26 | 15.4% (4/26) | 15.4% (4/26) | 705 | 20970.5 | 149404 |
| 5 | 32 | 15.6% (5/32) | 6.3% (2/32) | 2429 | 20194 | 398026 |
| 6 | 26 | 15.4% (4/26) | 11.5% (3/26) | 523.5 | 15552.5 | 178113 |
| 7 | 23 | 4.3% (1/23) | 4.3% (1/23) | 228 | 12378 | 374972 |
| 8 | 22 | 9.1% (2/22) | 4.5% (1/22) | 269.5 | 11580 | 296984 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 45.0% (9/20) | 35.0% (7/20) | 866.5 | 17326.5 | 60153 |
| 1 | 30 | 16.7% (5/30) | 16.7% (5/30) | 760.5 | 20465.5 | 122870 |
| 2 | 26 | 23.1% (6/26) | 19.2% (5/26) | 1143.5 | 19530 | 120382 |
| 3+ | 95 | 4.2% (4/95) | 1.1% (1/95) | 379 | 12713 | 1933407 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 14.4% (15/104) | 12.5% (13/104) | 471 | 12969 | 136344 |
| 0.4 to below 0.6 | 67 | 13.4% (9/67) | 9.0% (6/67) | 659 | 19884 | 268559 |
| 0.6 to below 0.8 | 37 | 13.5% (5/37) | 8.1% (3/37) | 1154 | 13871 | 271658 |
| 0.8 to 1.0 | 26 | 11.5% (3/26) | 11.5% (3/26) | 978 | 13854.5 | 166234 |
| above 1 | 40 | 100.0% (40/40) | - | 234 | 11502.5 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 23.8% (5/21) | 9.5% (2/21) | 1039 | 28591 | 297919 |
| 1 | 21 | 33.3% (7/21) | 14.3% (3/21) | 933 | 28990 | 184835 |
| 2 | 21 | 23.8% (5/21) | 19.0% (4/21) | 657 | 24307 | 142680 |
| 3 | 21 | 23.8% (5/21) | 14.3% (3/21) | 1596 | 24729 | 190605 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 19.0% (4/21) | 14.3% (3/21) | 1037 | 20306 | 178593 |
| 1 | 21 | 9.5% (2/21) | 0.0% (0/21) | 356 | 20410 | - |
| 2 | 21 | 19.0% (4/21) | 14.3% (3/21) | 407 | 19114 | 152165 |
| 3 | 21 | 9.5% (2/21) | 4.8% (1/21) | 614 | 20429 | 485645 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 19.0% (4/21) | 19.0% (4/21) | 784 | 21399 | 116878 |
| earliest_graduation | 21 | 28.6% (6/21) | 9.5% (2/21) | 1809 | 20320 | 262236 |
| min_total_mc | 21 | 28.6% (6/21) | 14.3% (3/21) | 1061 | 20500 | 149996 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 35.7% (10/28) | 17.9% (5/28) | 2933.5 | 23060.5 | 142280 |
| with ATAP | 21 | 23.8% (5/21) | 19.0% (4/21) | 2394 | 29362 | 149372 |
| with minimum MC | 21 | 19.0% (4/21) | 14.3% (3/21) | 600 | 17732 | 133892 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 42.9% (3/7) | 0.0% (0/7) | 3791 | 22098 | - |
| scattered | 7 | 28.6% (2/7) | 14.3% (1/7) | 795 | 12455 | 88821 |
| unsupported | 7 | 14.3% (1/7) | 0.0% (0/7) | 1450 | 26330 | - |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.21, p = 0.006, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.26, p = 0.001, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = -0.08, p = 0.289, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = -0.16, p = 0.036, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.02, p = 0.792, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = -0.03, p = 0.651, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = 0.14, p = 0.028, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.15, p = 0.022, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 13.8% (26/189) | 6.3% (12/189) | 2.6% (5/189) | 0.0% (0/189) | 3.7% (7/189) | 73.5% (139/189) | 0.0% (0/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 9.7% (18/186) | 1.6% (3/186) | 0.0% (0/186) | 5.9% (11/186) | 4.8% (9/186) | 78.0% (145/186) | 0.0% (0/186) | 0.0% (0/186) |
| min_total_mc | 225 | 12.0% (27/225) | 4.0% (9/225) | 0.0% (0/225) | 0.4% (1/225) | 5.3% (12/225) | 78.2% (176/225) | 0.0% (0/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 98.3% (118/120) | 1.7% (2/120) | 0.0% (0/120) |
| search | 120 | 98.3% (118/120) | 1.7% (2/120) | 0.0% (0/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| exclusion | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| parity | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| chain | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| rule_conflict | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| hidden | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 6 | 4 | 0.754 |
| mc_min | 21 | 3 | 4 | 1 | 0.375 |
| rho 0.4-0.6 | 21 | 3 | 4 | 1 | 0.375 |
| rho 0.6-0.8 | 21 | 2 | 5 | 0 | 0.062 |
| rho 0.8-1.0 | 21 | 1 | 6 | 1 | 0.125 |
| scattered | 7 | 2 | 1 | 0 | 1.000 |
| unsupported | 7 | 1 | 2 | 0 | 0.500 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 4 | 3 | 1.000 |
| mc_min | 21 | 2 | 3 | 1 | 0.625 |
| rho 0.4-0.6 | 21 | 3 | 2 | 1 | 1.000 |
| rho 0.6-0.8 | 21 | 1 | 4 | 0 | 0.125 |
| rho 0.8-1.0 | 21 | 1 | 4 | 1 | 0.375 |
| scattered | 7 | 0 | 0 | 1 | 1.000 |
| unsupported | 7 | 0 | 0 | 0 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 4 | 8 | 0 | 0.008 |
| exclusion | 12 | 1 | 11 | 0 | 0.001 |
| parity | 12 | 3 | 8 | 0 | 0.008 |
| chain | 12 | 2 | 10 | 0 | 0.002 |
| rule_conflict | 12 | 1 | 11 | 0 | 0.001 |
| hidden | 12 | 4 | 8 | 0 | 0.008 |
| all kinds | 72 | 15 | 56 | 0 | 0.000 |

- token usage: {'prompt_tokens': 16579202, 'total_tokens': 17956363, 'completion_tokens': 1377161, 'attempts': 909}
