# Results: results\B\qwen3.6_35b

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 85.5% (513/600) |
| no plan | 86.7% (208/240) |
| missing info | 76.7% (23/30) |
| out of scope | 93.3% (28/30) |
| **all** | 85.8% (772/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 84.3% (759/900)
- valid-answer accuracy, gold PLAN instances: 83.3% (500/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 81.2% (487/600)
- valid plans that are not optimal: 2.6% (13/500)
- over-refusal (gold PLAN answered NO_PLAN): 4.3% (26/600)
- correct refusal, gold NO_PLAN instances: 86.7% (208/240)
- invented plan, gold NO_PLAN instances: 0.8% (2/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| optimal | 81.2% (487/600) |
| wrong status | 10.2% (61/600) |
| over-refusal | 4.3% (26/600) |
| invalid | 2.2% (13/600) |
| preference gap | 2.0% (12/600) |
| objective gap | 0.2% (1/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R9: 5
- R11: 5
- R8: 2
- R1: 1
- R10: 1

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 87.5% (35/40) | 0.0% (0/40) |
| q2_infeasible/chain | 82.5% (33/40) | 2.5% (1/40) |
| q2_infeasible/exclusion | 87.5% (35/40) | 0.0% (0/40) |
| q2_infeasible/hidden | 92.5% (37/40) | 0.0% (0/40) |
| q2_infeasible/parity | 82.5% (33/40) | 0.0% (0/40) |
| q2_infeasible/rule_conflict | 87.5% (35/40) | 2.5% (1/40) |

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 0
- repair kinds (clean = none needed): {'clean': 900}
- replies cut off at max_tokens: 0
- accuracy counting repaired replies by their answer: 85.8% (772/900)
- strict accuracy (clean replies only count): 85.8% (772/900)
- clean replies right: 85.8% (772/900); repaired replies right: -
- valid-answer accuracy, clean replies: 84.3% (759/900); repaired replies: -
- valid-answer accuracy counting only clean replies as right (strict): 84.3% (759/900)
- optimal-plan accuracy, clean replies: 81.2% (487/600); repaired replies: -
- optimal-plan accuracy counting only clean replies as right (strict): 81.2% (487/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 87.1% (149/171) | 84.2% (144/171) | 416 | 3546 | 4194 |
| S2 | 63 | 81.0% (51/63) | 79.4% (50/63) | 436 | 3592 | 4523 |
| S3 | 273 | 78.8% (215/273) | 76.6% (209/273) | 405 | 3537 | 4614 |
| S4 | 312 | 87.5% (273/312) | 90.3% (65/72) | 413 | 3549.5 | 3903 |
| S5 | 21 | 95.2% (20/21) | 90.5% (19/21) | 395 | 3551 | 3916 |
| S6 | 60 | 85.0% (51/60) | - | 302.5 | 3356 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 76.7% (23/30) | - | 252 | 3280.5 | - |
| NO_PLAN | 240 | 86.7% (208/240) | - | 413 | 3551 | - |
| OUT_OF_SCOPE | 30 | 93.3% (28/30) | - | 342.5 | 3433 | - |
| PLAN | 600 | 83.3% (500/600) | 81.2% (487/600) | 412 | 3553.5 | 4359 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 91.3% (136/149) | 86.9% (86/99) | 316 | 3393 | 3911 |
| 3-4 | 318 | 82.4% (262/318) | 79.7% (196/246) | 409 | 3538 | 4434 |
| 5-6 | 296 | 83.8% (248/296) | 79.7% (161/202) | 435 | 3592 | 4498 |
| 7-8 | 117 | 85.5% (100/117) | 83.0% (44/53) | 468 | 3636 | 4389 |
| not given | 10 | 30.0% (3/10) | - | 393.5 | 3496.5 | - |
| outside 1-8 | 10 | 100.0% (10/10) | - | 172.5 | 3192.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 83.8% (243/290) | 80.5% (140/174) | 416.5 | 3550 | 4407 |
| 6-8 | 445 | 83.8% (373/445) | 82.0% (233/284) | 411 | 3549 | 4317 |
| 10-12 | 155 | 85.8% (133/155) | 80.3% (114/142) | 400 | 3532 | 4385 |
| not given | 10 | 100.0% (10/10) | - | 132 | 3125 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 85.2% (248/291) | 82.0% (155/189) | 375 | 3498 | 4250 |
| earliest_graduation | 291 | 82.5% (240/291) | 79.0% (147/186) | 424 | 3566 | 4509 |
| min_total_mc | 318 | 85.2% (271/318) | 82.2% (185/225) | 423.5 | 3563.5 | 4330 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 95.1% (39/41) | 90.5% (19/21) | 240 | 3313 | 3806 |
| 1 | 21 | 85.7% (18/21) | 85.7% (18/21) | 394 | 3516 | 4103 |
| 2 | 340 | 85.9% (292/340) | 82.5% (193/234) | 389.5 | 3509.5 | 4247 |
| 3 | 277 | 77.6% (215/277) | 72.5% (137/189) | 417 | 3562 | 4902 |
| 4+ | 221 | 88.2% (195/221) | 88.9% (120/135) | 449 | 3600 | 4044 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 97.6% (40/41) | 90.5% (19/21) | 236 | 3295 | 3756 |
| 1 | 77 | 87.0% (67/77) | 83.8% (31/37) | 361 | 3470 | 4124 |
| 2 | 271 | 89.7% (243/271) | 84.1% (164/195) | 375 | 3503 | 4147 |
| 3 | 286 | 86.7% (248/286) | 83.9% (161/192) | 426.5 | 3575.5 | 4249 |
| 4+ | 225 | 71.6% (161/225) | 72.3% (112/155) | 464 | 3623 | 4993 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 86.3% (710/823) | 84.3% (441/523) | 409 | 3543 | 4192 |
| yes | 77 | 63.6% (49/77) | 59.7% (46/77) | 415 | 3552 | 5955 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 84.0% (691/823) | 80.1% (419/523) | 411 | 3546 | 4418 |
| yes | 77 | 88.3% (68/77) | 88.3% (68/77) | 396 | 3534 | 3993 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 84.7% (593/700) | 82.3% (387/470) | 401 | 3525 | 4274 |
| scattered | 100 | 81.0% (81/100) | 72.3% (47/65) | 428 | 3596.5 | 4968 |
| unsupported | 100 | 85.0% (85/100) | 81.5% (53/65) | 459.5 | 3623 | 4435 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 82.4% (28/34) | 82.4% (28/34) | 452 | 3592 | 4366 |
| 3 to below 6 | 28 | 89.3% (25/28) | 89.3% (25/28) | 462 | 3626.5 | 4022 |
| 6 to below 10 | 24 | 95.8% (23/24) | 91.7% (22/24) | 430 | 3572.5 | 3898 |
| 10 to below 24 | 43 | 81.4% (35/43) | 79.1% (34/43) | 405 | 3530 | 4436 |
| 24 and above | 42 | 90.5% (38/42) | 83.3% (35/42) | 353 | 3436 | 4131 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 83.3% (15/18) | 83.3% (15/18) | 473.5 | 3609 | 4343 |
| 3 | 24 | 91.7% (22/24) | 91.7% (22/24) | 450.5 | 3632 | 3947 |
| 4 | 26 | 80.8% (21/26) | 80.8% (21/26) | 463.5 | 3622 | 4457 |
| 5 | 32 | 93.8% (30/32) | 90.6% (29/32) | 414 | 3556.5 | 3916 |
| 6 | 26 | 76.9% (20/26) | 73.1% (19/26) | 362 | 3453.5 | 4770 |
| 7 | 23 | 91.3% (21/23) | 91.3% (21/23) | 354 | 3439 | 3772 |
| 8 | 22 | 90.9% (20/22) | 77.3% (17/22) | 333.5 | 3425 | 4411 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 90.0% (18/20) | 90.0% (18/20) | 445 | 3587 | 4005 |
| 1 | 30 | 80.0% (24/30) | 80.0% (24/30) | 457.5 | 3597.5 | 4491 |
| 2 | 26 | 88.5% (23/26) | 80.8% (21/26) | 440 | 3594.5 | 4408 |
| 3+ | 95 | 88.4% (84/95) | 85.3% (81/95) | 374 | 3477 | 4093 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 85.6% (89/104) | 81.7% (85/104) | 376 | 3483.5 | 4264 |
| 0.4 to below 0.6 | 67 | 89.6% (60/67) | 88.1% (59/67) | 436 | 3587 | 4064 |
| 0.6 to below 0.8 | 37 | 81.1% (30/37) | 78.4% (29/37) | 470 | 3630 | 4630 |
| 0.8 to 1.0 | 26 | 80.8% (21/26) | 80.8% (21/26) | 446.5 | 3596.5 | 4456 |
| above 1 | 40 | 87.5% (35/40) | - | 416.5 | 3566.5 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 95.2% (20/21) | 90.5% (19/21) | 313 | 3414 | 3756 |
| 1 | 21 | 76.2% (16/21) | 76.2% (16/21) | 354 | 3467 | 4552 |
| 2 | 21 | 81.0% (17/21) | 81.0% (17/21) | 393 | 3520 | 4346 |
| 3 | 21 | 81.0% (17/21) | 81.0% (17/21) | 435 | 3602 | 4433 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 90.5% (19/21) | 90.5% (19/21) | 354 | 3472 | 3806 |
| 1 | 21 | 85.7% (18/21) | 85.7% (18/21) | 394 | 3516 | 4103 |
| 2 | 21 | 85.7% (18/21) | 81.0% (17/21) | 430 | 3558 | 4399 |
| 3 | 21 | 71.4% (15/21) | 66.7% (14/21) | 447 | 3607 | 5389 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 71.4% (15/21) | 61.9% (13/21) | 411 | 3556 | 5716 |
| earliest_graduation | 21 | 81.0% (17/21) | 81.0% (17/21) | 421 | 3566 | 4388 |
| min_total_mc | 21 | 85.7% (18/21) | 81.0% (17/21) | 426 | 3564 | 4404 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 92.9% (26/28) | 89.3% (25/28) | 444.5 | 3589 | 3985 |
| with ATAP | 21 | 38.1% (8/21) | 38.1% (8/21) | 454 | 3606 | 9449 |
| with minimum MC | 21 | 81.0% (17/21) | 81.0% (17/21) | 421 | 3581 | 4426 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 100.0% (7/7) | 100.0% (7/7) | 417 | 3567 | 3528 |
| scattered | 7 | 85.7% (6/7) | 71.4% (5/7) | 378 | 3535 | 4970 |
| unsupported | 7 | 100.0% (7/7) | 100.0% (7/7) | 395 | 3551 | 3551 |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = 0.03, p = 0.703, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.04, p = 0.604, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = -0.47, p = 0.000, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = -0.50, p = 0.000, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.01, p = 0.917, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = 0.02, p = 0.770, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = 0.41, p = 0.000, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.50, p = 0.000, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 82.0% (155/189) | 2.6% (5/189) | 0.0% (0/189) | 0.0% (0/189) | 2.6% (5/189) | 5.8% (11/189) | 6.9% (13/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 79.0% (147/186) | 0.5% (1/186) | 0.0% (0/186) | 0.5% (1/186) | 3.8% (7/186) | 4.3% (8/186) | 11.8% (22/186) | 0.0% (0/186) |
| min_total_mc | 225 | 82.2% (185/225) | 2.7% (6/225) | 0.0% (0/225) | 0.0% (0/225) | 0.4% (1/225) | 3.1% (7/225) | 11.6% (26/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 85.8% (103/120) | 0.0% (0/120) | 14.2% (17/120) |
| search | 120 | 87.5% (105/120) | 1.7% (2/120) | 10.8% (13/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 87.5% (35/40) | 0.0% (0/40) | 12.5% (5/40) |
| exclusion | 40 | 87.5% (35/40) | 0.0% (0/40) | 12.5% (5/40) |
| parity | 40 | 82.5% (33/40) | 0.0% (0/40) | 17.5% (7/40) |
| chain | 40 | 82.5% (33/40) | 2.5% (1/40) | 15.0% (6/40) |
| rule_conflict | 40 | 87.5% (35/40) | 2.5% (1/40) | 10.0% (4/40) |
| hidden | 40 | 92.5% (37/40) | 0.0% (0/40) | 7.5% (3/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 7 | 12 | 1 | 0.003 |
| mc_min | 21 | 16 | 3 | 1 | 0.625 |
| rho 0.4-0.6 | 21 | 19 | 0 | 1 | 1.000 |
| rho 0.6-0.8 | 21 | 15 | 4 | 0 | 0.125 |
| rho 0.8-1.0 | 21 | 16 | 3 | 0 | 0.250 |
| scattered | 7 | 6 | 1 | 0 | 1.000 |
| unsupported | 7 | 7 | 0 | 0 | 1.000 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 7 | 11 | 1 | 0.006 |
| mc_min | 21 | 15 | 3 | 2 | 1.000 |
| rho 0.4-0.6 | 21 | 18 | 0 | 2 | 0.500 |
| rho 0.6-0.8 | 21 | 13 | 5 | 1 | 0.219 |
| rho 0.8-1.0 | 21 | 15 | 3 | 1 | 0.625 |
| scattered | 7 | 5 | 2 | 0 | 0.500 |
| unsupported | 7 | 7 | 0 | 0 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 10 | 1 | 0 | 1.000 |
| exclusion | 12 | 10 | 0 | 1 | 1.000 |
| parity | 12 | 9 | 0 | 3 | 0.250 |
| chain | 12 | 9 | 1 | 2 | 1.000 |
| rule_conflict | 12 | 8 | 2 | 2 | 1.000 |
| hidden | 12 | 11 | 1 | 0 | 1.000 |
| all kinds | 72 | 57 | 5 | 8 | 0.581 |

**Pipeline B: what happened to the spec (Q2 instances)**

| Event | Instances |
|---|---|
| reply has no usable JSON | 0.0% (0/900) |
| spec rejected by the schema (INVALID_SPEC) | 10.4% (94/900) |
| spec equals the gold spec in every compared field | 54.2% (488/900) |
| spec differs from the gold spec in at least one field | 45.8% (412/900) |
| of these, the final answer is still right | 62.6% (258/412) |
| false MISSING_INFO (gold is not MISSING_INFO) | 0.0% (0/900) |
| MISSING_INFO not given (gold is MISSING_INFO) | 0.8% (7/900) |
| false OUT_OF_SCOPE (gold is not OUT_OF_SCOPE) | 0.0% (0/900) |
| unsupported wish dropped from the spec | 0.1% (1/900) |

| Field that differs from gold | Specs | Final answer still right |
|---|---|---|
| must_take | 199 | 83.9% (167/199) |
| rules | 157 | 30.6% (48/157) |
| late | 113 | 25.7% (29/113) |
| sem_caps | 42 | 26.2% (11/42) |
| mc_min | 36 | 83.3% (30/36) |
| early | 18 | 88.9% (16/18) |
| current_sem | 16 | 25.0% (4/16) |
| programme | 15 | 86.7% (13/15) |
| atap_sems | 15 | 13.3% (2/15) |
| completed | 9 | 66.7% (6/9) |
| unsupported | 5 | 80.0% (4/5) |
| mc_max | 1 | 100.0% (1/1) |
| objective | 1 | 100.0% (1/1) |

- token usage: {'prompt_tokens': 2812593, 'total_tokens': 3174690, 'completion_tokens': 362097, 'attempts': 900}
