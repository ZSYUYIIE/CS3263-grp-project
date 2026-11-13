# Results: results\A\x-test-2

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 90.5% (543/600) |
| no plan | 96.7% (232/240) |
| missing info | 76.7% (23/30) |
| out of scope | 90.0% (27/30) |
| **all** | 91.7% (825/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 90.8% (817/900)
- valid-answer accuracy, gold PLAN instances: 89.2% (535/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 88.3% (530/600)
- valid plans that are not optimal: 0.9% (5/535)
- over-refusal (gold PLAN answered NO_PLAN): 2.8% (17/600)
- correct refusal, gold NO_PLAN instances: 96.7% (232/240)
- invented plan, gold NO_PLAN instances: 2.5% (6/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| optimal | 88.3% (530/600) |
| wrong status | 6.7% (40/600) |
| over-refusal | 2.8% (17/600) |
| invalid | 1.3% (8/600) |
| extra courses | 0.5% (3/600) |
| preference gap | 0.2% (1/600) |
| objective gap | 0.2% (1/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R1: 8
- R9: 6
- R4: 4

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/chain | 97.5% (39/40) | 2.5% (1/40) |
| q2_infeasible/exclusion | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/hidden | 85.0% (34/40) | 12.5% (5/40) |
| q2_infeasible/parity | 97.5% (39/40) | 0.0% (0/40) |
| q2_infeasible/rule_conflict | 100.0% (40/40) | 0.0% (0/40) |

## Format

- unparseable replies: 43
- replies that needed repair before parsing: 0
- repair kinds (clean = none needed): {'clean': 857, 'unparseable': 43}
- replies cut off at max_tokens: 43
- accuracy counting repaired replies by their answer: 91.7% (825/900)
- strict accuracy (clean replies only count): 91.7% (825/900)
- clean replies right: 96.3% (825/857); repaired replies right: -
- valid-answer accuracy, clean replies: 95.3% (817/857); repaired replies: -
- valid-answer accuracy counting only clean replies as right (strict): 90.8% (817/900)
- optimal-plan accuracy, clean replies: 94.6% (530/560); repaired replies: -
- optimal-plan accuracy counting only clean replies as right (strict): 88.3% (530/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 91.8% (157/171) | 88.9% (152/171) | 6351 | 15088 | 17979 |
| S2 | 63 | 82.5% (52/63) | 82.5% (52/63) | 4804 | 13154 | 17556 |
| S3 | 273 | 91.6% (250/273) | 91.6% (250/273) | 5360 | 15232 | 17775 |
| S4 | 312 | 92.9% (290/312) | 80.6% (58/72) | 1766 | 10940.5 | 21301 |
| S5 | 21 | 85.7% (18/21) | 85.7% (18/21) | 7185 | 16779 | 20536 |
| S6 | 60 | 83.3% (50/60) | - | 678 | 8874 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 76.7% (23/30) | - | 1418.5 | 8779 | - |
| NO_PLAN | 240 | 96.7% (232/240) | - | 1440.5 | 10559 | - |
| OUT_OF_SCOPE | 30 | 90.0% (27/30) | - | 302 | 8972 | - |
| PLAN | 600 | 89.2% (535/600) | 88.3% (530/600) | 5691 | 15000 | 18292 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 85.9% (128/149) | 81.8% (81/99) | 7506 | 15118 | 22383 |
| 3-4 | 318 | 90.6% (288/318) | 88.2% (217/246) | 5396 | 14961.5 | 20006 |
| 5-6 | 296 | 92.9% (275/296) | 92.1% (186/202) | 3125 | 12092.5 | 15653 |
| 7-8 | 117 | 92.3% (108/117) | 86.8% (46/53) | 1442 | 10084 | 13673 |
| not given | 10 | 100.0% (10/10) | - | 2021.5 | 10279.5 | - |
| outside 1-8 | 10 | 80.0% (8/10) | - | 1072.5 | 9612.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 93.1% (270/290) | 90.2% (157/174) | 2090.5 | 10376.5 | 14606 |
| 6-8 | 445 | 89.4% (398/445) | 86.3% (245/284) | 3919 | 13154 | 19063 |
| 10-12 | 155 | 92.3% (143/155) | 90.1% (128/142) | 7699 | 16940 | 21335 |
| not given | 10 | 60.0% (6/10) | - | 1374.5 | 4792 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 87.3% (254/291) | 85.7% (162/189) | 3547 | 11927 | 18203 |
| earliest_graduation | 291 | 93.5% (272/291) | 90.3% (168/186) | 3874 | 12700 | 18333 |
| min_total_mc | 318 | 91.5% (291/318) | 88.9% (200/225) | 4301 | 13610.5 | 18328 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 82.9% (34/41) | 95.2% (20/21) | 3005 | 9698 | 16165 |
| 1 | 21 | 85.7% (18/21) | 85.7% (18/21) | 4386 | 14576 | 19340 |
| 2 | 340 | 92.4% (314/340) | 90.2% (211/234) | 4490 | 13213.5 | 18179 |
| 3 | 277 | 91.7% (254/277) | 88.4% (167/189) | 3633 | 12109 | 17703 |
| 4+ | 221 | 89.1% (197/221) | 84.4% (114/135) | 3785 | 12428 | 19570 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 78.0% (32/41) | 85.7% (18/21) | 3438 | 10326 | 20701 |
| 1 | 77 | 96.1% (74/77) | 94.6% (35/37) | 3093 | 12131 | 16764 |
| 2 | 271 | 90.0% (244/271) | 88.7% (173/195) | 3686 | 12070 | 16579 |
| 3 | 286 | 90.6% (259/286) | 87.0% (167/192) | 4476 | 13714.5 | 19862 |
| 4+ | 225 | 92.4% (208/225) | 88.4% (137/155) | 4000 | 12965 | 18614 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 90.6% (746/823) | 87.8% (459/523) | 3624 | 12081 | 17819 |
| yes | 77 | 92.2% (71/77) | 92.2% (71/77) | 6390 | 17819 | 21345 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 90.4% (744/823) | 87.4% (457/523) | 3732 | 12368 | 18665 |
| yes | 77 | 94.8% (73/77) | 94.8% (73/77) | 5775 | 14486 | 15954 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 92.0% (644/700) | 89.1% (419/470) | 3931.5 | 12484 | 18096 |
| scattered | 100 | 81.0% (81/100) | 78.5% (51/65) | 3958.5 | 13156.5 | 21394 |
| unsupported | 100 | 92.0% (92/100) | 92.3% (60/65) | 2922 | 12528.5 | 17020 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 97.1% (33/34) | 97.1% (33/34) | 2783 | 10829.5 | 11894 |
| 3 to below 6 | 28 | 92.9% (26/28) | 92.9% (26/28) | 4871.5 | 13362 | 15278 |
| 6 to below 10 | 24 | 100.0% (24/24) | 100.0% (24/24) | 6254.5 | 15335.5 | 15340 |
| 10 to below 24 | 43 | 88.4% (38/43) | 83.7% (36/43) | 7348 | 16824 | 21536 |
| 24 and above | 42 | 85.7% (36/42) | 78.6% (33/42) | 9562 | 17285.5 | 24230 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 88.9% (16/18) | 88.9% (16/18) | 2049.5 | 10720 | 13495 |
| 3 | 24 | 95.8% (23/24) | 95.8% (23/24) | 3882 | 13213.5 | 14320 |
| 4 | 26 | 100.0% (26/26) | 100.0% (26/26) | 4708 | 13199 | 13931 |
| 5 | 32 | 93.8% (30/32) | 93.8% (30/32) | 7136.5 | 15998 | 18246 |
| 6 | 26 | 92.3% (24/26) | 80.8% (21/26) | 7294.5 | 15353.5 | 20832 |
| 7 | 23 | 87.0% (20/23) | 82.6% (19/23) | 11462 | 19479 | 25316 |
| 8 | 22 | 81.8% (18/22) | 77.3% (17/22) | 8394.5 | 15547.5 | 21142 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 95.0% (19/20) | 95.0% (19/20) | 2285.5 | 10829.5 | 12914 |
| 1 | 30 | 90.0% (27/30) | 90.0% (27/30) | 3956.5 | 12295 | 14546 |
| 2 | 26 | 100.0% (26/26) | 96.2% (25/26) | 5012.5 | 13949 | 15221 |
| 3+ | 95 | 89.5% (85/95) | 85.3% (81/95) | 8341 | 16398 | 21162 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 90.4% (94/104) | 86.5% (90/104) | 6444 | 14758 | 18048 |
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
| 2 | 21 | 95.2% (20/21) | 95.2% (20/21) | 4891 | 14943 | 15477 |
| 3 | 21 | 95.2% (20/21) | 95.2% (20/21) | 5152 | 16076 | 17063 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 85.7% (18/21) | 85.7% (18/21) | 4649 | 12109 | 17792 |
| earliest_graduation | 21 | 85.7% (18/21) | 85.7% (18/21) | 5947 | 14053 | 19391 |
| min_total_mc | 21 | 90.5% (19/21) | 90.5% (19/21) | 6515 | 14918 | 17757 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 92.9% (26/28) | 89.3% (25/28) | 4474.5 | 13025 | 15722 |
| with ATAP | 21 | 90.5% (19/21) | 90.5% (19/21) | 6938 | 19145 | 22254 |
| with minimum MC | 21 | 100.0% (21/21) | 100.0% (21/21) | 5775 | 14669 | 14133 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 85.7% (6/7) | 85.7% (6/7) | 6916 | 15736 | 17700 |
| scattered | 7 | 71.4% (5/7) | 71.4% (5/7) | 10579 | 19082 | 29854 |
| unsupported | 7 | 100.0% (7/7) | 100.0% (7/7) | 5627 | 13759 | 16312 |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.18, p = 0.019, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.25, p = 0.001, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = 0.69, p = 0.000, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = 0.59, p = 0.000, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.13, p = 0.055, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = -0.06, p = 0.331, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = -0.13, p = 0.040, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.00, p = 0.969, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 85.7% (162/189) | 0.0% (0/189) | 0.0% (0/189) | 0.0% (0/189) | 1.6% (3/189) | 4.2% (8/189) | 8.5% (16/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 90.3% (168/186) | 0.0% (0/186) | 1.6% (3/186) | 0.5% (1/186) | 0.5% (1/186) | 1.1% (2/186) | 5.9% (11/186) | 0.0% (0/186) |
| min_total_mc | 225 | 88.9% (200/225) | 0.4% (1/225) | 0.0% (0/225) | 0.0% (0/225) | 1.8% (4/225) | 3.1% (7/225) | 5.8% (13/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 99.2% (119/120) | 0.0% (0/120) | 0.8% (1/120) |
| search | 120 | 94.2% (113/120) | 5.0% (6/120) | 0.8% (1/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| exclusion | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| parity | 40 | 97.5% (39/40) | 0.0% (0/40) | 2.5% (1/40) |
| chain | 40 | 97.5% (39/40) | 2.5% (1/40) | 0.0% (0/40) |
| rule_conflict | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| hidden | 40 | 85.0% (34/40) | 12.5% (5/40) | 2.5% (1/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 18 | 2 | 1 | 1.000 |
| mc_min | 21 | 20 | 0 | 1 | 1.000 |
| rho 0.4-0.6 | 21 | 19 | 1 | 1 | 1.000 |
| rho 0.6-0.8 | 21 | 17 | 3 | 1 | 0.625 |
| rho 0.8-1.0 | 21 | 14 | 6 | 0 | 0.031 |
| scattered | 7 | 4 | 2 | 1 | 1.000 |
| unsupported | 7 | 6 | 0 | 1 | 1.000 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 17 | 2 | 2 | 1.000 |
| mc_min | 21 | 19 | 0 | 2 | 0.500 |
| rho 0.4-0.6 | 21 | 18 | 1 | 2 | 1.000 |
| rho 0.6-0.8 | 21 | 16 | 3 | 2 | 1.000 |
| rho 0.8-1.0 | 21 | 13 | 6 | 1 | 0.125 |
| scattered | 7 | 4 | 2 | 1 | 1.000 |
| unsupported | 7 | 6 | 0 | 1 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 10 | 2 | 0 | 0.500 |
| exclusion | 12 | 11 | 1 | 0 | 1.000 |
| parity | 12 | 11 | 1 | 0 | 1.000 |
| chain | 12 | 12 | 0 | 0 | 1.000 |
| rule_conflict | 12 | 7 | 5 | 0 | 0.062 |
| hidden | 12 | 7 | 4 | 0 | 0.125 |
| all kinds | 72 | 58 | 13 | 0 | 0.000 |

- token usage: {'prompt_tokens': 7798639, 'total_tokens': 12899779, 'completion_tokens': 5101140, 'attempts': 900}
