# Results: results\alternative\a_plus\qwen3.6_35b\round_1

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 30.2% (181/600) |
| no plan | 93.3% (224/240) |
| missing info | 13.3% (4/30) |
| out of scope | 56.7% (17/30) |
| **all** | 47.3% (426/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 36.7% (330/900)
- valid-answer accuracy, gold PLAN instances: 14.2% (85/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 9.5% (57/600)
- valid plans that are not optimal: 32.9% (28/85)
- over-refusal (gold PLAN answered NO_PLAN): 69.8% (419/600)
- correct refusal, gold NO_PLAN instances: 93.3% (224/240)
- invented plan, gold NO_PLAN instances: 6.7% (16/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| over-refusal | 69.8% (419/600) |
| invalid | 16.0% (96/600) |
| optimal | 9.5% (57/600) |
| preference gap | 3.0% (18/600) |
| objective gap | 1.2% (7/600) |
| extra courses | 0.5% (3/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R3: 92
- R4: 64
- R9: 42
- R10: 14
- R8: 12
- R1: 10
- R11: 7
- R7: 6
- R6: 4
- R2: 2

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/chain | 92.5% (37/40) | 7.5% (3/40) |
| q2_infeasible/exclusion | 87.5% (35/40) | 12.5% (5/40) |
| q2_infeasible/hidden | 90.0% (36/40) | 10.0% (4/40) |
| q2_infeasible/parity | 92.5% (37/40) | 7.5% (3/40) |
| q2_infeasible/rule_conflict | 97.5% (39/40) | 2.5% (1/40) |

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 178
- repair kinds (clean = none needed): {'clean': 722, 'extra_text': 86, 'cut_reasons': 76, 'last_of_several': 15, 'control_chars': 1}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 47.3% (426/900)
- strict accuracy (clean replies only count): 36.6% (329/900)
- clean replies right: 45.6% (329/722); repaired replies right: 54.5% (97/178); Fisher exact p = 0.036
- valid-answer accuracy, clean replies: 35.3% (255/722); repaired replies: 42.1% (75/178); Fisher exact p = 0.099
- valid-answer accuracy counting only clean replies as right (strict): 28.3% (255/900)
- optimal-plan accuracy, clean replies: 5.6% (26/467); repaired replies: 23.3% (31/133); Fisher exact p = 0.000
- optimal-plan accuracy counting only clean replies as right (strict): 4.3% (26/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 9.9% (17/171) | 8.8% (15/171) | 486 | 16728 | 206437 |
| S2 | 63 | 9.5% (6/63) | 7.9% (5/63) | 699 | 13115 | 204748 |
| S3 | 273 | 16.8% (46/273) | 10.3% (28/273) | 657 | 20655 | 208936 |
| S4 | 312 | 75.3% (235/312) | 11.1% (8/72) | 395 | 12983.5 | 175885 |
| S5 | 21 | 23.8% (5/21) | 4.8% (1/21) | 1678 | 16162 | 416649 |
| S6 | 60 | 35.0% (21/60) | - | 134.5 | 10074.5 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 13.3% (4/30) | - | 321.5 | 9500 | - |
| NO_PLAN | 240 | 93.3% (224/240) | - | 329.5 | 12185.5 | - |
| OUT_OF_SCOPE | 30 | 56.7% (17/30) | - | 49.5 | 10222.5 | - |
| PLAN | 600 | 14.2% (85/600) | 9.5% (57/600) | 616.5 | 18949 | 206916 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 32.9% (49/149) | 6.1% (6/99) | 280 | 11128 | 256527 |
| 3-4 | 318 | 30.8% (98/318) | 6.1% (15/246) | 593 | 17481.5 | 335843 |
| 5-6 | 296 | 33.4% (99/296) | 7.4% (15/202) | 521 | 20411.5 | 286789 |
| 7-8 | 117 | 67.5% (79/117) | 39.6% (21/53) | 518 | 12712 | 43599 |
| not given | 10 | 10.0% (1/10) | - | 357.5 | 10875 | - |
| outside 1-8 | 10 | 40.0% (4/10) | - | 85 | 10222.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 46.9% (136/290) | 18.4% (32/174) | 401.5 | 12521 | 91422 |
| 6-8 | 445 | 38.9% (173/445) | 6.7% (19/284) | 553 | 17728 | 308418 |
| 10-12 | 155 | 12.9% (20/155) | 4.2% (6/142) | 543 | 19114 | 501463 |
| not given | 10 | 10.0% (1/10) | - | 123 | 3877 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 39.5% (115/291) | 9.5% (18/189) | 434 | 14607 | 193208 |
| earliest_graduation | 291 | 37.5% (109/291) | 8.1% (15/186) | 509 | 15366 | 256893 |
| min_total_mc | 318 | 33.3% (106/318) | 10.7% (24/225) | 557.5 | 15394 | 185962 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 19.5% (8/41) | 9.5% (2/21) | 309 | 11815 | 222040 |
| 1 | 21 | 4.8% (1/21) | 0.0% (0/21) | 356 | 20264 | - |
| 2 | 340 | 35.9% (122/340) | 8.5% (20/234) | 556 | 15271 | 227193 |
| 3 | 277 | 36.5% (101/277) | 7.4% (14/189) | 520 | 17586 | 269444 |
| 4+ | 221 | 44.3% (98/221) | 15.6% (21/135) | 429 | 13487 | 123272 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 24.4% (10/41) | 9.5% (2/21) | 328 | 11815 | 243648 |
| 1 | 77 | 55.8% (43/77) | 8.1% (3/37) | 499 | 17785 | 261107 |
| 2 | 271 | 37.3% (101/271) | 12.8% (25/195) | 530 | 18763 | 151240 |
| 3 | 286 | 33.9% (97/286) | 7.8% (15/192) | 506.5 | 14936.5 | 262113 |
| 4+ | 225 | 35.1% (79/225) | 7.7% (12/155) | 500 | 13077 | 234243 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 38.6% (318/823) | 9.6% (50/523) | 477 | 13767 | 191215 |
| yes | 77 | 15.6% (12/77) | 9.1% (7/77) | 1060 | 29789 | 319070 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 39.4% (324/823) | 9.9% (52/523) | 499 | 14652 | 199350 |
| yes | 77 | 7.8% (6/77) | 6.5% (5/77) | 495 | 19085 | 285602 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 36.0% (252/700) | 7.2% (34/470) | 486 | 16090.5 | 272587 |
| scattered | 100 | 31.0% (31/100) | 7.7% (5/65) | 778.5 | 14362 | 259900 |
| unsupported | 100 | 47.0% (47/100) | 27.7% (18/65) | 466 | 13633.5 | 68154 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 23.5% (8/34) | 23.5% (8/34) | 408.5 | 16145 | 68951 |
| 3 to below 6 | 28 | 7.1% (2/28) | 3.6% (1/28) | 1068 | 20881.5 | 594272 |
| 6 to below 10 | 24 | 8.3% (2/24) | 8.3% (2/24) | 630.5 | 22119 | 254728 |
| 10 to below 24 | 43 | 7.0% (3/43) | 7.0% (3/43) | 566 | 16994 | 259746 |
| 24 and above | 42 | 4.8% (2/42) | 2.4% (1/42) | 299.5 | 12401 | 661990 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 11.1% (2/18) | 11.1% (2/18) | 355.5 | 16070 | 147522 |
| 3 | 24 | 12.5% (3/24) | 12.5% (3/24) | 727.5 | 23440.5 | 182765 |
| 4 | 26 | 15.4% (4/26) | 15.4% (4/26) | 486.5 | 19897 | 128075 |
| 5 | 32 | 9.4% (3/32) | 6.3% (2/32) | 2429 | 20194 | 323928 |
| 6 | 26 | 7.7% (2/26) | 7.7% (2/26) | 514 | 15552.5 | 218875 |
| 7 | 23 | 4.3% (1/23) | 4.3% (1/23) | 228 | 12378 | 358330 |
| 8 | 22 | 9.1% (2/22) | 4.5% (1/22) | 269.5 | 11580 | 296984 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 35.0% (7/20) | 30.0% (6/20) | 489 | 17326.5 | 57942 |
| 1 | 30 | 16.7% (5/30) | 16.7% (5/30) | 485.5 | 19833 | 114329 |
| 2 | 26 | 11.5% (3/26) | 11.5% (3/26) | 769.5 | 19530 | 174174 |
| 3+ | 95 | 2.1% (2/95) | 1.1% (1/95) | 379 | 12713 | 1654742 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 13.5% (14/104) | 11.5% (12/104) | 444.5 | 12969 | 140050 |
| 0.4 to below 0.6 | 67 | 4.5% (3/67) | 4.5% (3/67) | 510 | 19884 | 432664 |
| 0.6 to below 0.8 | 37 | 8.1% (3/37) | 5.4% (2/37) | 1127 | 13871 | 343786 |
| 0.8 to 1.0 | 26 | 11.5% (3/26) | 11.5% (3/26) | 785 | 13854.5 | 151379 |
| above 1 | 40 | 100.0% (40/40) | - | 234 | 11502.5 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 23.8% (5/21) | 9.5% (2/21) | 1014 | 25216 | 243648 |
| 1 | 21 | 19.0% (4/21) | 9.5% (2/21) | 745 | 20385 | 235356 |
| 2 | 21 | 19.0% (4/21) | 14.3% (3/21) | 657 | 23460 | 171089 |
| 3 | 21 | 14.3% (3/21) | 9.5% (2/21) | 1596 | 24678 | 257084 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 14.3% (3/21) | 9.5% (2/21) | 673 | 20306 | 222040 |
| 1 | 21 | 4.8% (1/21) | 0.0% (0/21) | 356 | 20264 | - |
| 2 | 21 | 19.0% (4/21) | 14.3% (3/21) | 407 | 18899 | 139200 |
| 3 | 21 | 9.5% (2/21) | 4.8% (1/21) | 495 | 19569 | 417585 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 14.3% (3/21) | 14.3% (3/21) | 587 | 20553 | 131541 |
| earliest_graduation | 21 | 19.0% (4/21) | 4.8% (1/21) | 692 | 20320 | 406518 |
| min_total_mc | 21 | 19.0% (4/21) | 9.5% (2/21) | 1061 | 20500 | 203824 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 32.1% (9/28) | 17.9% (5/28) | 2582 | 22172 | 124143 |
| with ATAP | 21 | 23.8% (5/21) | 19.0% (4/21) | 1701 | 29362 | 141063 |
| with minimum MC | 21 | 19.0% (4/21) | 14.3% (3/21) | 486 | 17579 | 122364 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 42.9% (3/7) | 0.0% (0/7) | 3791 | 22098 | - |
| scattered | 7 | 28.6% (2/7) | 14.3% (1/7) | 795 | 12455 | 88821 |
| unsupported | 7 | 0.0% (0/7) | 0.0% (0/7) | 1450 | 26330 | - |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.19, p = 0.014, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.21, p = 0.006, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = -0.07, p = 0.356, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = -0.15, p = 0.052, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.06, p = 0.362, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = -0.04, p = 0.492, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = 0.13, p = 0.051, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.15, p = 0.022, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 9.5% (18/189) | 5.8% (11/189) | 1.6% (3/189) | 0.0% (0/189) | 15.3% (29/189) | 67.7% (128/189) | 0.0% (0/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 8.1% (15/186) | 1.1% (2/186) | 0.0% (0/186) | 3.2% (6/186) | 17.2% (32/186) | 70.4% (131/186) | 0.0% (0/186) | 0.0% (0/186) |
| min_total_mc | 225 | 10.7% (24/225) | 2.2% (5/225) | 0.0% (0/225) | 0.4% (1/225) | 15.6% (35/225) | 71.1% (160/225) | 0.0% (0/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 93.3% (112/120) | 6.7% (8/120) | 0.0% (0/120) |
| search | 120 | 93.3% (112/120) | 6.7% (8/120) | 0.0% (0/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| exclusion | 40 | 87.5% (35/40) | 12.5% (5/40) | 0.0% (0/40) |
| parity | 40 | 92.5% (37/40) | 7.5% (3/40) | 0.0% (0/40) |
| chain | 40 | 92.5% (37/40) | 7.5% (3/40) | 0.0% (0/40) |
| rule_conflict | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| hidden | 40 | 90.0% (36/40) | 10.0% (4/40) | 0.0% (0/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 5 | 4 | 1.000 |
| mc_min | 21 | 3 | 3 | 1 | 0.625 |
| rho 0.4-0.6 | 21 | 1 | 5 | 1 | 0.219 |
| rho 0.6-0.8 | 21 | 2 | 4 | 0 | 0.125 |
| rho 0.8-1.0 | 21 | 1 | 5 | 1 | 0.219 |
| scattered | 7 | 2 | 1 | 0 | 1.000 |
| unsupported | 7 | 0 | 3 | 0 | 0.250 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 4 | 3 | 1.000 |
| mc_min | 21 | 2 | 3 | 1 | 0.625 |
| rho 0.4-0.6 | 21 | 1 | 4 | 1 | 0.375 |
| rho 0.6-0.8 | 21 | 1 | 4 | 0 | 0.125 |
| rho 0.8-1.0 | 21 | 1 | 4 | 1 | 0.375 |
| scattered | 7 | 0 | 0 | 1 | 1.000 |
| unsupported | 7 | 0 | 0 | 0 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 4 | 8 | 0 | 0.008 |
| exclusion | 12 | 0 | 9 | 0 | 0.004 |
| parity | 12 | 2 | 8 | 0 | 0.008 |
| chain | 12 | 0 | 10 | 1 | 0.012 |
| rule_conflict | 12 | 1 | 11 | 0 | 0.001 |
| hidden | 12 | 3 | 8 | 0 | 0.008 |
| all kinds | 72 | 10 | 54 | 1 | 0.000 |

- token usage: {'prompt_tokens': 14906005, 'total_tokens': 16187360, 'completion_tokens': 1281355, 'attempts': 908}
