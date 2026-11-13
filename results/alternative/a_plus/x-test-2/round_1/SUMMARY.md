# Results: results\alternative\a_plus\x-test-2\round_1

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 90.5% (543/600) |
| no plan | 99.2% (238/240) |
| missing info | 76.7% (23/30) |
| out of scope | 90.0% (27/30) |
| **all** | 92.3% (831/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 92.2% (830/900)
- valid-answer accuracy, gold PLAN instances: 90.3% (542/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 89.3% (536/600)
- valid plans that are not optimal: 1.1% (6/542)
- over-refusal (gold PLAN answered NO_PLAN): 2.8% (17/600)
- correct refusal, gold NO_PLAN instances: 99.2% (238/240)
- invented plan, gold NO_PLAN instances: 0.0% (0/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| optimal | 89.3% (536/600) |
| wrong status | 6.7% (40/600) |
| over-refusal | 2.8% (17/600) |
| extra courses | 0.7% (4/600) |
| preference gap | 0.2% (1/600) |
| objective gap | 0.2% (1/600) |
| invalid | 0.2% (1/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R1: 1
- R9: 1

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/chain | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/exclusion | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/hidden | 97.5% (39/40) | 0.0% (0/40) |
| q2_infeasible/parity | 97.5% (39/40) | 0.0% (0/40) |
| q2_infeasible/rule_conflict | 100.0% (40/40) | 0.0% (0/40) |

## Format

- unparseable replies: 43
- replies that needed repair before parsing: 0
- repair kinds (clean = none needed): {'clean': 857, 'unparseable': 43}
- replies cut off at max_tokens: 43
- accuracy counting repaired replies by their answer: 92.3% (831/900)
- strict accuracy (clean replies only count): 92.3% (831/900)
- clean replies right: 97.0% (831/857); repaired replies right: -
- valid-answer accuracy, clean replies: 96.8% (830/857); repaired replies: -
- valid-answer accuracy counting only clean replies as right (strict): 92.2% (830/900)
- optimal-plan accuracy, clean replies: 95.7% (536/560); repaired replies: -
- optimal-plan accuracy counting only clean replies as right (strict): 89.3% (536/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 93.6% (160/171) | 90.1% (154/171) | 6424 | 15099 | 18045 |
| S2 | 63 | 82.5% (52/63) | 82.5% (52/63) | 4804 | 13154 | 17556 |
| S3 | 273 | 91.9% (251/273) | 91.9% (251/273) | 5522 | 15251 | 17805 |
| S4 | 312 | 95.5% (298/312) | 83.3% (60/72) | 1766 | 10940.5 | 20949 |
| S5 | 21 | 90.5% (19/21) | 90.5% (19/21) | 7185 | 16844 | 20064 |
| S6 | 60 | 83.3% (50/60) | - | 678 | 8874 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 76.7% (23/30) | - | 1418.5 | 8779 | - |
| NO_PLAN | 240 | 99.2% (238/240) | - | 1440.5 | 10559 | - |
| OUT_OF_SCOPE | 30 | 90.0% (27/30) | - | 302 | 8972 | - |
| PLAN | 600 | 90.3% (542/600) | 89.3% (536/600) | 5724.5 | 15106 | 18282 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 90.6% (135/149) | 82.8% (82/99) | 7660 | 15370 | 22511 |
| 3-4 | 318 | 90.9% (289/318) | 88.6% (218/246) | 5396 | 14961.5 | 19975 |
| 5-6 | 296 | 93.6% (277/296) | 93.1% (188/202) | 3125 | 12092.5 | 15675 |
| 7-8 | 117 | 94.9% (111/117) | 90.6% (48/53) | 1467 | 10084 | 13579 |
| not given | 10 | 100.0% (10/10) | - | 2021.5 | 10279.5 | - |
| outside 1-8 | 10 | 80.0% (8/10) | - | 1072.5 | 9612.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 94.5% (274/290) | 92.0% (160/174) | 2104.5 | 10376.5 | 14541 |
| 6-8 | 445 | 91.5% (407/445) | 87.3% (248/284) | 3936 | 13345 | 19119 |
| 10-12 | 155 | 92.3% (143/155) | 90.1% (128/142) | 7699 | 16940 | 21335 |
| not given | 10 | 60.0% (6/10) | - | 1374.5 | 4792 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 89.0% (259/291) | 87.3% (165/189) | 3547 | 11928 | 18095 |
| earliest_graduation | 291 | 94.8% (276/291) | 90.9% (169/186) | 3874 | 12700 | 18285 |
| min_total_mc | 318 | 92.8% (295/318) | 89.8% (202/225) | 4455 | 13661.5 | 18432 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 82.9% (34/41) | 95.2% (20/21) | 3005 | 9698 | 16165 |
| 1 | 21 | 85.7% (18/21) | 85.7% (18/21) | 4386 | 14576 | 19340 |
| 2 | 340 | 93.5% (318/340) | 91.0% (213/234) | 4553 | 13412.5 | 18172 |
| 3 | 277 | 93.1% (258/277) | 89.9% (170/189) | 3659 | 12131 | 17591 |
| 4+ | 221 | 91.4% (202/221) | 85.2% (115/135) | 3785 | 12428 | 19709 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 78.0% (32/41) | 85.7% (18/21) | 3438 | 10326 | 20701 |
| 1 | 77 | 97.4% (75/77) | 94.6% (35/37) | 3215 | 12131 | 16764 |
| 2 | 271 | 92.3% (250/271) | 89.2% (174/195) | 3686 | 12081 | 16678 |
| 3 | 286 | 92.0% (263/286) | 88.5% (170/192) | 4528.5 | 13749.5 | 19708 |
| 4+ | 225 | 93.3% (210/225) | 89.7% (139/155) | 4041 | 13144 | 18614 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 92.2% (759/823) | 88.9% (465/523) | 3659 | 12131 | 17814 |
| yes | 77 | 92.2% (71/77) | 92.2% (71/77) | 6390 | 17819 | 21345 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 92.0% (757/823) | 88.5% (463/523) | 3785 | 12428 | 18620 |
| yes | 77 | 94.8% (73/77) | 94.8% (73/77) | 5846 | 14576 | 16137 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 92.6% (648/700) | 89.6% (421/470) | 3940 | 12600 | 18095 |
| scattered | 100 | 88.0% (88/100) | 84.6% (55/65) | 4074 | 13548 | 21090 |
| unsupported | 100 | 94.0% (94/100) | 92.3% (60/65) | 3171.5 | 12584 | 17020 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 97.1% (33/34) | 97.1% (33/34) | 2783 | 10829.5 | 11894 |
| 3 to below 6 | 28 | 92.9% (26/28) | 92.9% (26/28) | 4871.5 | 13362 | 15278 |
| 6 to below 10 | 24 | 100.0% (24/24) | 100.0% (24/24) | 6254.5 | 15335.5 | 15340 |
| 10 to below 24 | 43 | 90.7% (39/43) | 86.0% (37/43) | 7348 | 16824 | 21311 |
| 24 and above | 42 | 90.5% (38/42) | 81.0% (34/42) | 9562 | 17671.5 | 24486 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 88.9% (16/18) | 88.9% (16/18) | 2049.5 | 10720 | 13495 |
| 3 | 24 | 95.8% (23/24) | 95.8% (23/24) | 3882 | 13213.5 | 14320 |
| 4 | 26 | 100.0% (26/26) | 100.0% (26/26) | 4708 | 13199 | 13931 |
| 5 | 32 | 93.8% (30/32) | 93.8% (30/32) | 7136.5 | 15998 | 18246 |
| 6 | 26 | 96.2% (25/26) | 84.6% (22/26) | 7294.5 | 15353.5 | 20485 |
| 7 | 23 | 87.0% (20/23) | 82.6% (19/23) | 11462 | 19479 | 25316 |
| 8 | 22 | 90.9% (20/22) | 81.8% (18/22) | 8827 | 15684.5 | 21796 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 95.0% (19/20) | 95.0% (19/20) | 2285.5 | 10829.5 | 12914 |
| 1 | 30 | 90.0% (27/30) | 90.0% (27/30) | 3956.5 | 12295 | 14546 |
| 2 | 26 | 100.0% (26/26) | 96.2% (25/26) | 5012.5 | 13949 | 15221 |
| 3+ | 95 | 92.6% (88/95) | 87.4% (83/95) | 8499 | 16824 | 21208 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 93.3% (97/104) | 88.5% (92/104) | 6491 | 14789.5 | 18157 |
| 0.4 to below 0.6 | 67 | 94.0% (63/67) | 92.5% (62/67) | 5887 | 14809 | 17062 |
| 0.6 to below 0.8 | 37 | 91.9% (34/37) | 91.9% (34/37) | 5556 | 15113 | 16874 |
| 0.8 to 1.0 | 26 | 69.2% (18/26) | 69.2% (18/26) | 5148 | 13127.5 | 21658 |
| above 1 | 40 | 100.0% (40/40) | - | 1095.5 | 10104 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 85.7% (18/21) | 85.7% (18/21) | 5999 | 15669 | 20701 |
| 1 | 21 | 100.0% (21/21) | 100.0% (21/21) | 4028 | 14162 | 15150 |
| 2 | 21 | 100.0% (21/21) | 100.0% (21/21) | 5130 | 14994 | 15213 |
| 3 | 21 | 81.0% (17/21) | 81.0% (17/21) | 5749 | 16808 | 22651 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 95.2% (20/21) | 95.2% (20/21) | 4432 | 14229 | 16165 |
| 1 | 21 | 85.7% (18/21) | 85.7% (18/21) | 4386 | 14576 | 19340 |
| 2 | 21 | 95.2% (20/21) | 95.2% (20/21) | 5360 | 15408 | 16147 |
| 3 | 21 | 95.2% (20/21) | 95.2% (20/21) | 5152 | 16076 | 17063 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 90.5% (19/21) | 90.5% (19/21) | 4865 | 12109 | 17483 |
| earliest_graduation | 21 | 85.7% (18/21) | 85.7% (18/21) | 5947 | 14053 | 19391 |
| min_total_mc | 21 | 90.5% (19/21) | 90.5% (19/21) | 6515 | 14918 | 17757 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 96.4% (27/28) | 92.9% (26/28) | 4474.5 | 13650.5 | 15562 |
| with ATAP | 21 | 90.5% (19/21) | 90.5% (19/21) | 6938 | 19145 | 22254 |
| with minimum MC | 21 | 100.0% (21/21) | 100.0% (21/21) | 5775 | 14669 | 14133 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 100.0% (7/7) | 100.0% (7/7) | 6916 | 16844 | 16823 |
| scattered | 7 | 71.4% (5/7) | 71.4% (5/7) | 10579 | 19082 | 29854 |
| unsupported | 7 | 100.0% (7/7) | 100.0% (7/7) | 5627 | 13759 | 16312 |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.11, p = 0.136, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.23, p = 0.003, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = 0.70, p = 0.000, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = 0.61, p = 0.000, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.18, p = 0.005, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = -0.10, p = 0.129, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = -0.14, p = 0.029, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = -0.01, p = 0.843, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 87.3% (165/189) | 0.0% (0/189) | 0.0% (0/189) | 0.0% (0/189) | 0.0% (0/189) | 4.2% (8/189) | 8.5% (16/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 90.9% (169/186) | 0.0% (0/186) | 1.6% (3/186) | 0.5% (1/186) | 0.0% (0/186) | 1.1% (2/186) | 5.9% (11/186) | 0.0% (0/186) |
| min_total_mc | 225 | 89.8% (202/225) | 0.4% (1/225) | 0.4% (1/225) | 0.0% (0/225) | 0.4% (1/225) | 3.1% (7/225) | 5.8% (13/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 99.2% (119/120) | 0.0% (0/120) | 0.8% (1/120) |
| search | 120 | 99.2% (119/120) | 0.0% (0/120) | 0.8% (1/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| exclusion | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| parity | 40 | 97.5% (39/40) | 0.0% (0/40) | 2.5% (1/40) |
| chain | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| rule_conflict | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| hidden | 40 | 97.5% (39/40) | 0.0% (0/40) | 2.5% (1/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 18 | 2 | 1 | 1.000 |
| mc_min | 21 | 20 | 0 | 1 | 1.000 |
| rho 0.4-0.6 | 21 | 19 | 1 | 1 | 1.000 |
| rho 0.6-0.8 | 21 | 17 | 3 | 1 | 0.625 |
| rho 0.8-1.0 | 21 | 14 | 6 | 0 | 0.031 |
| scattered | 7 | 5 | 2 | 0 | 0.500 |
| unsupported | 7 | 7 | 0 | 0 | 1.000 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 17 | 2 | 2 | 1.000 |
| mc_min | 21 | 19 | 0 | 2 | 0.500 |
| rho 0.4-0.6 | 21 | 18 | 1 | 2 | 1.000 |
| rho 0.6-0.8 | 21 | 16 | 3 | 2 | 1.000 |
| rho 0.8-1.0 | 21 | 13 | 6 | 1 | 0.125 |
| scattered | 7 | 5 | 2 | 0 | 0.500 |
| unsupported | 7 | 7 | 0 | 0 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 11 | 1 | 0 | 1.000 |
| exclusion | 12 | 11 | 1 | 0 | 1.000 |
| parity | 12 | 11 | 1 | 0 | 1.000 |
| chain | 12 | 12 | 0 | 0 | 1.000 |
| rule_conflict | 12 | 8 | 4 | 0 | 0.125 |
| hidden | 12 | 7 | 5 | 0 | 0.062 |
| all kinds | 72 | 60 | 12 | 0 | 0.000 |

- token usage: {'prompt_tokens': 7916150, 'total_tokens': 13059370, 'completion_tokens': 5143220, 'attempts': 900}
