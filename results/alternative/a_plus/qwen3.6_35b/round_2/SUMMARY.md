# Results: results\alternative\a_plus\qwen3.6_35b\round_2

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 24.8% (149/600) |
| no plan | 97.1% (233/240) |
| missing info | 13.3% (4/30) |
| out of scope | 56.7% (17/30) |
| **all** | 44.8% (403/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 40.0% (360/900)
- valid-answer accuracy, gold PLAN instances: 17.7% (106/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 11.5% (69/600)
- valid plans that are not optimal: 34.9% (37/106)
- over-refusal (gold PLAN answered NO_PLAN): 75.2% (451/600)
- correct refusal, gold NO_PLAN instances: 97.1% (233/240)
- invented plan, gold NO_PLAN instances: 2.9% (7/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| over-refusal | 75.2% (451/600) |
| optimal | 11.5% (69/600) |
| invalid | 7.2% (43/600) |
| preference gap | 3.8% (23/600) |
| objective gap | 1.5% (9/600) |
| extra courses | 0.8% (5/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R3: 44
- R4: 29
- R9: 18
- R10: 6
- R8: 3
- R1: 2
- R11: 2
- R6: 2
- R7: 1
- R2: 1

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/chain | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/exclusion | 95.0% (38/40) | 5.0% (2/40) |
| q2_infeasible/hidden | 95.0% (38/40) | 5.0% (2/40) |
| q2_infeasible/parity | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/rule_conflict | 97.5% (39/40) | 2.5% (1/40) |

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 171
- repair kinds (clean = none needed): {'clean': 729, 'extra_text': 78, 'cut_reasons': 77, 'last_of_several': 15, 'control_chars': 1}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 44.8% (403/900)
- strict accuracy (clean replies only count): 34.8% (313/900)
- clean replies right: 42.9% (313/729); repaired replies right: 52.6% (90/171); Fisher exact p = 0.026
- valid-answer accuracy, clean replies: 38.1% (278/729); repaired replies: 48.0% (82/171); Fisher exact p = 0.019
- valid-answer accuracy counting only clean replies as right (strict): 30.9% (278/900)
- optimal-plan accuracy, clean replies: 7.4% (35/470); repaired replies: 26.2% (34/130); Fisher exact p = 0.000
- optimal-plan accuracy counting only clean replies as right (strict): 5.8% (35/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 12.9% (22/171) | 10.5% (18/171) | 508 | 16994 | 191629 |
| S2 | 63 | 12.7% (8/63) | 11.1% (7/63) | 872 | 13115 | 157238 |
| S3 | 273 | 20.5% (56/273) | 12.5% (34/273) | 765 | 21741 | 190674 |
| S4 | 312 | 79.2% (247/312) | 12.5% (9/72) | 409.5 | 12983.5 | 164998 |
| S5 | 21 | 28.6% (6/21) | 4.8% (1/21) | 1678 | 16162 | 430639 |
| S6 | 60 | 35.0% (21/60) | - | 134.5 | 10074.5 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 13.3% (4/30) | - | 321.5 | 9500 | - |
| NO_PLAN | 240 | 97.1% (233/240) | - | 331.5 | 12185.5 | - |
| OUT_OF_SCOPE | 30 | 56.7% (17/30) | - | 49.5 | 10222.5 | - |
| PLAN | 600 | 17.7% (106/600) | 11.5% (69/600) | 745.5 | 19364 | 187660 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 33.6% (50/149) | 6.1% (6/99) | 280 | 11128 | 268400 |
| 3-4 | 318 | 33.6% (107/318) | 7.3% (18/246) | 747 | 17691 | 314645 |
| 5-6 | 296 | 38.9% (115/296) | 11.4% (23/202) | 598.5 | 20526.5 | 205893 |
| 7-8 | 117 | 70.9% (83/117) | 41.5% (22/53) | 518 | 12712 | 42681 |
| not given | 10 | 10.0% (1/10) | - | 357.5 | 10875 | - |
| outside 1-8 | 10 | 40.0% (4/10) | - | 85 | 10222.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 50.0% (145/290) | 20.7% (36/174) | 430.5 | 12521 | 85713 |
| 6-8 | 445 | 42.5% (189/445) | 9.2% (26/284) | 614 | 17728 | 245810 |
| 10-12 | 155 | 16.1% (25/155) | 4.9% (7/142) | 659 | 19197 | 495969 |
| not given | 10 | 10.0% (1/10) | - | 123 | 3877 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 43.6% (127/291) | 12.7% (24/189) | 460 | 14607 | 158333 |
| earliest_graduation | 291 | 40.5% (118/291) | 9.7% (18/186) | 567 | 15366 | 237865 |
| min_total_mc | 318 | 36.2% (115/318) | 12.0% (27/225) | 597.5 | 15394 | 180258 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 22.0% (9/41) | 14.3% (3/21) | 309 | 11815 | 178593 |
| 1 | 21 | 9.5% (2/21) | 0.0% (0/21) | 356 | 20410 | - |
| 2 | 340 | 39.1% (133/340) | 10.7% (25/234) | 597 | 15271 | 201356 |
| 3 | 277 | 40.4% (112/277) | 9.5% (18/189) | 584 | 17767 | 229824 |
| 4+ | 221 | 47.1% (104/221) | 17.0% (23/135) | 429 | 13487 | 121183 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 24.4% (10/41) | 9.5% (2/21) | 328 | 11815 | 289042 |
| 1 | 77 | 62.3% (48/77) | 10.8% (4/37) | 554 | 17952 | 217284 |
| 2 | 271 | 41.7% (113/271) | 15.9% (31/195) | 579 | 18991 | 134233 |
| 3 | 286 | 37.4% (107/286) | 9.4% (18/192) | 526 | 14936.5 | 239402 |
| 4+ | 225 | 36.4% (82/225) | 9.0% (14/155) | 518 | 13077 | 216488 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 42.0% (346/823) | 11.7% (61/523) | 499 | 13767 | 172311 |
| yes | 77 | 18.2% (14/77) | 10.4% (8/77) | 1331 | 30794 | 304695 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 42.9% (353/823) | 12.0% (63/523) | 524 | 14652 | 180416 |
| yes | 77 | 9.1% (7/77) | 7.8% (6/77) | 601 | 19486 | 263722 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 39.7% (278/700) | 9.6% (45/470) | 508.5 | 16197.5 | 228537 |
| scattered | 100 | 33.0% (33/100) | 7.7% (5/65) | 829 | 14362 | 271035 |
| unsupported | 100 | 49.0% (49/100) | 29.2% (19/65) | 466 | 13633.5 | 68905 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 26.5% (9/34) | 26.5% (9/34) | 444.5 | 16626.5 | 63538 |
| 3 to below 6 | 28 | 17.9% (5/28) | 10.7% (3/28) | 1586.5 | 21662.5 | 221082 |
| 6 to below 10 | 24 | 12.5% (3/24) | 8.3% (2/24) | 1835.5 | 26222.5 | 307238 |
| 10 to below 24 | 43 | 7.0% (3/43) | 7.0% (3/43) | 645 | 16994 | 301082 |
| 24 and above | 42 | 4.8% (2/42) | 2.4% (1/42) | 299.5 | 12401 | 696516 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 16.7% (3/18) | 16.7% (3/18) | 355.5 | 16070 | 102419 |
| 3 | 24 | 20.8% (5/24) | 16.7% (4/24) | 827 | 24956.5 | 158900 |
| 4 | 26 | 15.4% (4/26) | 15.4% (4/26) | 656 | 20970.5 | 143824 |
| 5 | 32 | 12.5% (4/32) | 6.3% (2/32) | 2429 | 20194 | 379234 |
| 6 | 26 | 11.5% (3/26) | 11.5% (3/26) | 523.5 | 15552.5 | 166918 |
| 7 | 23 | 4.3% (1/23) | 4.3% (1/23) | 228 | 12378 | 374972 |
| 8 | 22 | 9.1% (2/22) | 4.5% (1/22) | 269.5 | 11580 | 296984 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 40.0% (8/20) | 35.0% (7/20) | 773 | 17326.5 | 56681 |
| 1 | 30 | 16.7% (5/30) | 16.7% (5/30) | 612.5 | 20465.5 | 118437 |
| 2 | 26 | 19.2% (5/26) | 19.2% (5/26) | 1143.5 | 19530 | 118244 |
| 3+ | 95 | 4.2% (4/95) | 1.1% (1/95) | 379 | 12713 | 1869153 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 14.4% (15/104) | 12.5% (13/104) | 471 | 12969 | 134918 |
| 0.4 to below 0.6 | 67 | 10.4% (7/67) | 9.0% (6/67) | 659 | 19884 | 253682 |
| 0.6 to below 0.8 | 37 | 13.5% (5/37) | 8.1% (3/37) | 1127 | 13871 | 263537 |
| 0.8 to 1.0 | 26 | 11.5% (3/26) | 11.5% (3/26) | 978 | 13854.5 | 161119 |
| above 1 | 40 | 100.0% (40/40) | - | 234 | 11502.5 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 23.8% (5/21) | 9.5% (2/21) | 1039 | 28591 | 289042 |
| 1 | 21 | 23.8% (5/21) | 9.5% (2/21) | 813 | 28351 | 262030 |
| 2 | 21 | 23.8% (5/21) | 19.0% (4/21) | 657 | 24307 | 142680 |
| 3 | 21 | 23.8% (5/21) | 14.3% (3/21) | 1596 | 24729 | 186468 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 19.0% (4/21) | 14.3% (3/21) | 1037 | 20306 | 178593 |
| 1 | 21 | 9.5% (2/21) | 0.0% (0/21) | 356 | 20410 | - |
| 2 | 21 | 19.0% (4/21) | 14.3% (3/21) | 407 | 19114 | 147070 |
| 3 | 21 | 9.5% (2/21) | 4.8% (1/21) | 614 | 20429 | 459208 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 19.0% (4/21) | 19.0% (4/21) | 746 | 21399 | 111821 |
| earliest_graduation | 21 | 23.8% (5/21) | 9.5% (2/21) | 1809 | 20320 | 239994 |
| min_total_mc | 21 | 28.6% (6/21) | 14.3% (3/21) | 1061 | 20500 | 149996 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 32.1% (9/28) | 17.9% (5/28) | 2933.5 | 23060.5 | 137280 |
| with ATAP | 21 | 23.8% (5/21) | 19.0% (4/21) | 2394 | 29362 | 145175 |
| with minimum MC | 21 | 19.0% (4/21) | 14.3% (3/21) | 600 | 17732 | 133892 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 42.9% (3/7) | 0.0% (0/7) | 3791 | 22098 | - |
| scattered | 7 | 28.6% (2/7) | 14.3% (1/7) | 795 | 12455 | 88821 |
| unsupported | 7 | 14.3% (1/7) | 0.0% (0/7) | 1450 | 26330 | - |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.24, p = 0.002, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.26, p = 0.001, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = -0.08, p = 0.277, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = -0.16, p = 0.040, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.03, p = 0.655, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = -0.03, p = 0.651, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = 0.14, p = 0.028, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.15, p = 0.021, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 12.7% (24/189) | 5.8% (11/189) | 2.6% (5/189) | 0.0% (0/189) | 6.3% (12/189) | 72.5% (137/189) | 0.0% (0/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 9.7% (18/186) | 1.6% (3/186) | 0.0% (0/186) | 4.3% (8/186) | 8.6% (16/186) | 75.8% (141/186) | 0.0% (0/186) | 0.0% (0/186) |
| min_total_mc | 225 | 12.0% (27/225) | 4.0% (9/225) | 0.0% (0/225) | 0.4% (1/225) | 6.7% (15/225) | 76.9% (173/225) | 0.0% (0/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 97.5% (117/120) | 2.5% (3/120) | 0.0% (0/120) |
| search | 120 | 96.7% (116/120) | 3.3% (4/120) | 0.0% (0/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| exclusion | 40 | 95.0% (38/40) | 5.0% (2/40) | 0.0% (0/40) |
| parity | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| chain | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| rule_conflict | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| hidden | 40 | 95.0% (38/40) | 5.0% (2/40) | 0.0% (0/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 5 | 4 | 1.000 |
| mc_min | 21 | 3 | 3 | 1 | 0.625 |
| rho 0.4-0.6 | 21 | 3 | 3 | 1 | 0.625 |
| rho 0.6-0.8 | 21 | 2 | 4 | 0 | 0.125 |
| rho 0.8-1.0 | 21 | 1 | 5 | 1 | 0.219 |
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
| exclusion | 12 | 0 | 11 | 1 | 0.006 |
| parity | 12 | 2 | 9 | 0 | 0.004 |
| chain | 12 | 1 | 10 | 1 | 0.012 |
| rule_conflict | 12 | 1 | 11 | 0 | 0.001 |
| hidden | 12 | 4 | 8 | 0 | 0.008 |
| all kinds | 72 | 12 | 57 | 2 | 0.000 |

- token usage: {'prompt_tokens': 16173026, 'total_tokens': 17531323, 'completion_tokens': 1358297, 'attempts': 909}
