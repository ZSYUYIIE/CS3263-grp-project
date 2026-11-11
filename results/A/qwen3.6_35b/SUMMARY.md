# Results: results\A\qwen3.6_35b

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 63.5% (381/600) |
| no plan | 71.3% (171/240) |
| missing info | 6.7% (2/30) |
| out of scope | 56.7% (17/30) |
| **all** | 63.4% (571/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 26.6% (239/900)
- valid-answer accuracy, gold PLAN instances: 8.2% (49/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 6.2% (37/600)
- valid plans that are not optimal: 24.5% (12/49)
- over-refusal (gold PLAN answered NO_PLAN): 36.5% (219/600)
- correct refusal, gold NO_PLAN instances: 71.3% (171/240)
- invented plan, gold NO_PLAN instances: 28.8% (69/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| invalid | 55.3% (332/600) |
| over-refusal | 36.5% (219/600) |
| optimal | 6.2% (37/600) |
| preference gap | 1.2% (7/600) |
| objective gap | 0.5% (3/600) |
| extra courses | 0.3% (2/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R4: 418
- R3: 293
- R9: 210
- R1: 84
- R8: 38
- R11: 30
- R10: 21
- R7: 18
- R6: 11
- R2: 9

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/chain | 67.5% (27/40) | 32.5% (13/40) |
| q2_infeasible/exclusion | 47.5% (19/40) | 52.5% (21/40) |
| q2_infeasible/hidden | 55.0% (22/40) | 45.0% (18/40) |
| q2_infeasible/parity | 70.0% (28/40) | 30.0% (12/40) |
| q2_infeasible/rule_conflict | 90.0% (36/40) | 10.0% (4/40) |

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 240
- repair kinds (clean = none needed): {'last_of_several': 26, 'clean': 660, 'extra_text': 128, 'cut_reasons': 86}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 63.4% (571/900)
- strict accuracy (clean replies only count): 45.6% (410/900)
- clean replies right: 62.1% (410/660); repaired replies right: 67.1% (161/240); Fisher exact p = 0.184
- valid-answer accuracy, clean replies: 25.9% (171/660); repaired replies: 28.3% (68/240); Fisher exact p = 0.495
- valid-answer accuracy counting only clean replies as right (strict): 19.0% (171/900)
- optimal-plan accuracy, clean replies: 1.9% (8/429); repaired replies: 17.0% (29/171); Fisher exact p = 0.000
- optimal-plan accuracy counting only clean replies as right (strict): 1.3% (8/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 6.4% (11/171) | 5.3% (9/171) | 261 | 11422 | 222823 |
| S2 | 63 | 7.9% (5/63) | 6.3% (4/63) | 584 | 11628 | 186390 |
| S3 | 273 | 9.2% (25/273) | 7.0% (19/273) | 281 | 11927 | 181741 |
| S4 | 312 | 56.1% (175/312) | 5.6% (4/72) | 270 | 11517.5 | 217707 |
| S5 | 21 | 19.0% (4/21) | 4.8% (1/21) | 1304 | 12919 | 272288 |
| S6 | 60 | 31.7% (19/60) | - | 125.5 | 9887.5 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 6.7% (2/30) | - | 227 | 9257 | - |
| NO_PLAN | 240 | 71.3% (171/240) | - | 244 | 11439.5 | - |
| OUT_OF_SCOPE | 30 | 56.7% (17/30) | - | 49.5 | 10222.5 | - |
| PLAN | 600 | 8.2% (49/600) | 6.2% (37/600) | 291 | 11793 | 198572 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 26.8% (40/149) | 4.0% (4/99) | 256 | 10290 | 272449 |
| 3-4 | 318 | 20.1% (64/318) | 3.3% (8/246) | 311.5 | 12085 | 393944 |
| 5-6 | 296 | 22.3% (66/296) | 5.4% (11/202) | 251 | 11810 | 226432 |
| 7-8 | 117 | 54.7% (64/117) | 26.4% (14/53) | 280 | 11339 | 43932 |
| not given | 10 | 10.0% (1/10) | - | 357.5 | 10875 | - |
| outside 1-8 | 10 | 40.0% (4/10) | - | 85 | 10222.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 36.2% (105/290) | 11.5% (20/174) | 239 | 10642.5 | 94898 |
| 6-8 | 445 | 27.0% (120/445) | 4.2% (12/284) | 275 | 11895 | 296562 |
| 10-12 | 155 | 8.4% (13/155) | 3.5% (5/142) | 291 | 12438 | 378092 |
| not given | 10 | 10.0% (1/10) | - | 87.5 | 3587.5 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 29.2% (85/291) | 6.9% (13/189) | 255 | 11321 | 165192 |
| earliest_graduation | 291 | 26.8% (78/291) | 4.8% (9/186) | 273 | 11649 | 265702 |
| min_total_mc | 318 | 23.9% (76/318) | 6.7% (15/225) | 282.5 | 11826 | 187223 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 17.1% (7/41) | 4.8% (1/21) | 190 | 10587 | 266888 |
| 1 | 21 | 4.8% (1/21) | 0.0% (0/21) | 194 | 11721 | - |
| 2 | 340 | 25.6% (87/340) | 6.4% (15/234) | 334 | 11810.5 | 194767 |
| 3 | 277 | 24.5% (68/277) | 3.7% (7/189) | 267 | 11554 | 324070 |
| 4+ | 221 | 34.4% (76/221) | 10.4% (14/135) | 245 | 11520 | 115981 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 19.5% (8/41) | 9.5% (2/21) | 196 | 10198 | 133204 |
| 1 | 77 | 36.4% (28/77) | 5.4% (2/37) | 262 | 11344 | 226142 |
| 2 | 271 | 22.5% (61/271) | 6.7% (13/195) | 247 | 11110 | 169451 |
| 3 | 286 | 26.6% (76/286) | 5.2% (10/192) | 274 | 11708 | 245916 |
| 4+ | 225 | 29.3% (66/225) | 6.5% (10/155) | 338 | 11910 | 196644 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 28.6% (235/823) | 6.5% (34/523) | 265 | 11364 | 179093 |
| yes | 77 | 5.2% (4/77) | 3.9% (3/77) | 328 | 15457 | 419332 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 28.6% (235/823) | 6.3% (33/523) | 273 | 11574 | 195197 |
| yes | 77 | 5.2% (4/77) | 5.2% (4/77) | 256 | 11583 | 226416 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 25.3% (177/700) | 4.9% (23/470) | 255 | 11444.5 | 247058 |
| scattered | 100 | 26.0% (26/100) | 4.6% (3/65) | 517 | 12210.5 | 281556 |
| unsupported | 100 | 36.0% (36/100) | 16.9% (11/65) | 349.5 | 11561 | 74559 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 14.7% (5/34) | 14.7% (5/34) | 209.5 | 10643 | 73560 |
| 3 to below 6 | 28 | 7.1% (2/28) | 3.6% (1/28) | 265.5 | 11929.5 | 345045 |
| 6 to below 10 | 24 | 4.2% (1/24) | 4.2% (1/24) | 279.5 | 11896 | 293237 |
| 10 to below 24 | 43 | 2.3% (1/43) | 2.3% (1/43) | 283 | 10847 | 492902 |
| 24 and above | 42 | 4.8% (2/42) | 2.4% (1/42) | 280.5 | 11663 | 506424 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 11.1% (2/18) | 11.1% (2/18) | 194.5 | 10643 | 97848 |
| 3 | 24 | 8.3% (2/24) | 8.3% (2/24) | 208.5 | 12295 | 151520 |
| 4 | 26 | 7.7% (2/26) | 7.7% (2/26) | 268 | 11846 | 155246 |
| 5 | 32 | 6.3% (2/32) | 3.1% (1/32) | 515 | 11910 | 399865 |
| 6 | 26 | 3.8% (1/26) | 3.8% (1/26) | 285.5 | 10609 | 293242 |
| 7 | 23 | 4.3% (1/23) | 4.3% (1/23) | 228 | 11292 | 277142 |
| 8 | 22 | 4.5% (1/22) | 0.0% (0/22) | 269.5 | 9730 | - |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 20.0% (4/20) | 15.0% (3/20) | 256 | 11374 | 73614 |
| 1 | 30 | 13.3% (4/30) | 13.3% (4/30) | 236.5 | 11080.5 | 85580 |
| 2 | 26 | 7.7% (2/26) | 7.7% (2/26) | 329.5 | 11125 | 160038 |
| 3+ | 95 | 1.1% (1/95) | 0.0% (0/95) | 283 | 11586 | - |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 7.7% (8/104) | 5.8% (6/104) | 262 | 10410.5 | 189710 |
| 0.4 to below 0.6 | 67 | 4.5% (3/67) | 4.5% (3/67) | 273 | 11867 | 269770 |
| 0.6 to below 0.8 | 37 | 8.1% (3/37) | 5.4% (2/37) | 699 | 13018 | 242848 |
| 0.8 to 1.0 | 26 | 7.7% (2/26) | 7.7% (2/26) | 609.5 | 11464.5 | 158851 |
| above 1 | 40 | 97.5% (39/40) | - | 226.5 | 11502.5 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 14.3% (3/21) | 9.5% (2/21) | 293 | 12630 | 133204 |
| 1 | 21 | 14.3% (3/21) | 9.5% (2/21) | 273 | 11818 | 136466 |
| 2 | 21 | 0.0% (0/21) | 0.0% (0/21) | 270 | 11447 | - |
| 3 | 21 | 4.8% (1/21) | 4.8% (1/21) | 337 | 12522 | 281104 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 9.5% (2/21) | 4.8% (1/21) | 281 | 12110 | 266888 |
| 1 | 21 | 4.8% (1/21) | 0.0% (0/21) | 194 | 11721 | - |
| 2 | 21 | 19.0% (4/21) | 14.3% (3/21) | 219 | 12564 | 88495 |
| 3 | 21 | 0.0% (0/21) | 0.0% (0/21) | 323 | 11754 | - |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 14.3% (3/21) | 14.3% (3/21) | 227 | 10583 | 77386 |
| earliest_graduation | 21 | 9.5% (2/21) | 4.8% (1/21) | 347 | 11649 | 244855 |
| min_total_mc | 21 | 9.5% (2/21) | 9.5% (2/21) | 282 | 11570 | 119715 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 21.4% (6/28) | 10.7% (3/28) | 1909.5 | 12542 | 120606 |
| with ATAP | 21 | 9.5% (2/21) | 9.5% (2/21) | 515 | 16303 | 172732 |
| with minimum MC | 21 | 9.5% (2/21) | 9.5% (2/21) | 275 | 11333 | 121570 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 28.6% (2/7) | 0.0% (0/7) | 3221 | 13584 | - |
| scattered | 7 | 28.6% (2/7) | 14.3% (1/7) | 795 | 12455 | 88821 |
| unsupported | 7 | 0.0% (0/7) | 0.0% (0/7) | 1027 | 12919 | - |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.15, p = 0.051, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.18, p = 0.019, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = 0.07, p = 0.330, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = 0.07, p = 0.343, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.00, p = 0.968, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = 0.02, p = 0.761, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = 0.13, p = 0.040, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.30, p = 0.000, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 6.9% (13/189) | 3.2% (6/189) | 1.1% (2/189) | 0.0% (0/189) | 57.1% (108/189) | 31.7% (60/189) | 0.0% (0/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 4.8% (9/186) | 0.5% (1/186) | 0.0% (0/186) | 1.1% (2/186) | 55.9% (104/186) | 37.6% (70/186) | 0.0% (0/186) | 0.0% (0/186) |
| min_total_mc | 225 | 6.7% (15/225) | 0.0% (0/225) | 0.0% (0/225) | 0.4% (1/225) | 53.3% (120/225) | 39.6% (89/225) | 0.0% (0/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 71.7% (86/120) | 28.3% (34/120) | 0.0% (0/120) |
| search | 120 | 70.8% (85/120) | 29.2% (35/120) | 0.0% (0/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| exclusion | 40 | 47.5% (19/40) | 52.5% (21/40) | 0.0% (0/40) |
| parity | 40 | 70.0% (28/40) | 30.0% (12/40) | 0.0% (0/40) |
| chain | 40 | 67.5% (27/40) | 32.5% (13/40) | 0.0% (0/40) |
| rule_conflict | 40 | 90.0% (36/40) | 10.0% (4/40) | 0.0% (0/40) |
| hidden | 40 | 55.0% (22/40) | 45.0% (18/40) | 0.0% (0/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 3 | 1 | 0.625 |
| mc_min | 21 | 2 | 2 | 0 | 0.500 |
| rho 0.4-0.6 | 21 | 1 | 3 | 1 | 0.625 |
| rho 0.6-0.8 | 21 | 2 | 2 | 0 | 0.500 |
| rho 0.8-1.0 | 21 | 0 | 4 | 1 | 0.375 |
| scattered | 7 | 1 | 1 | 1 | 1.000 |
| unsupported | 7 | 0 | 2 | 0 | 0.500 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 1 | 2 | 1 | 1.000 |
| mc_min | 21 | 1 | 2 | 1 | 1.000 |
| rho 0.4-0.6 | 21 | 1 | 2 | 1 | 1.000 |
| rho 0.6-0.8 | 21 | 1 | 2 | 0 | 0.500 |
| rho 0.8-1.0 | 21 | 0 | 3 | 1 | 0.625 |
| scattered | 7 | 0 | 0 | 1 | 1.000 |
| unsupported | 7 | 0 | 0 | 0 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 3 | 9 | 0 | 0.004 |
| exclusion | 12 | 0 | 7 | 0 | 0.016 |
| parity | 12 | 0 | 9 | 0 | 0.004 |
| chain | 12 | 0 | 7 | 0 | 0.016 |
| rule_conflict | 12 | 0 | 12 | 0 | 0.000 |
| hidden | 12 | 0 | 6 | 1 | 0.125 |
| all kinds | 72 | 3 | 50 | 1 | 0.000 |

- token usage: {'prompt_tokens': 9705516, 'total_tokens': 10715034, 'completion_tokens': 1009518, 'attempts': 908}
