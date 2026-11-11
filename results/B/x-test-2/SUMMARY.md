# Results: results\B\x-test-2

900 of 900 instances answered.

## Status accuracy by gold answer

| Group | Correct status |
|---|---|
| plan | 99.5% (597/600) |
| no plan | 99.6% (239/240) |
| missing info | 100.0% (30/30) |
| out of scope | 100.0% (30/30) |
| **all** | 99.6% (896/900) |

## Agreed metrics

- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 98.9% (890/900)
- valid-answer accuracy, gold PLAN instances: 98.5% (591/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 98.3% (590/600)
- valid plans that are not optimal: 0.2% (1/591)
- over-refusal (gold PLAN answered NO_PLAN): 0.3% (2/600)
- correct refusal, gold NO_PLAN instances: 99.6% (239/240)
- invented plan, gold NO_PLAN instances: 0.0% (0/240)

## Feasible plan requests (gold = PLAN)

| Class | Count |
|---|---|
| optimal | 98.3% (590/600) |
| invalid | 1.0% (6/600) |
| over-refusal | 0.3% (2/600) |
| wrong status | 0.2% (1/600) |
| preference gap | 0.2% (1/600) |

Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):

- R1: 4
- R10: 3
- R9: 3

## Impossible requests (gold = NO_PLAN)

| Kind | Correct refusal | Invented plan |
|---|---|---|
| q2_infeasible/capacity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/chain | 97.5% (39/40) | 0.0% (0/40) |
| q2_infeasible/exclusion | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/hidden | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/parity | 100.0% (40/40) | 0.0% (0/40) |
| q2_infeasible/rule_conflict | 100.0% (40/40) | 0.0% (0/40) |

## Format

- unparseable replies: 0
- replies that needed repair before parsing: 0
- repair kinds (clean = none needed): {'clean': 898, 'none': 2}
- replies cut off at max_tokens: 2
- accuracy counting repaired replies by their answer: 99.6% (896/900)
- strict accuracy (clean replies only count): 99.6% (896/900)
- clean replies right: 99.6% (896/900); repaired replies right: -
- valid-answer accuracy, clean replies: 98.9% (890/900); repaired replies: -
- valid-answer accuracy counting only clean replies as right (strict): 98.9% (890/900)
- optimal-plan accuracy, clean replies: 98.3% (590/600); repaired replies: -
- optimal-plan accuracy counting only clean replies as right (strict): 98.3% (590/600)

## Q2 factors

Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the level's gold PLAN instances divided by its optimal plans.

**By set**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| S1 | 171 | 99.4% (170/171) | 99.4% (170/171) | 745 | 3571 | 3708 |
| S2 | 63 | 98.4% (62/63) | 98.4% (62/63) | 952 | 3792 | 4149 |
| S3 | 273 | 98.5% (269/273) | 98.5% (269/273) | 708 | 3542 | 3833 |
| S4 | 312 | 98.7% (308/312) | 95.8% (69/72) | 709.5 | 3540 | 3822 |
| S5 | 21 | 100.0% (21/21) | 95.2% (20/21) | 858 | 3709 | 3914 |
| S6 | 60 | 100.0% (60/60) | - | 621.5 | 3415 | - |

**By answer type (gold status)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| MISSING_INFO | 30 | 100.0% (30/30) | - | 566 | 3322 | - |
| NO_PLAN | 240 | 99.6% (239/240) | - | 713 | 3551.5 | - |
| OUT_OF_SCOPE | 30 | 100.0% (30/30) | - | 689 | 3490 | - |
| PLAN | 600 | 98.5% (591/600) | 98.3% (590/600) | 740 | 3572.5 | 3832 |

**Current semester band (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 1-2 | 149 | 100.0% (149/149) | 100.0% (99/99) | 555 | 3348 | 3464 |
| 3-4 | 318 | 99.1% (315/318) | 98.8% (243/246) | 722 | 3547.5 | 3779 |
| 5-6 | 296 | 98.3% (291/296) | 97.5% (197/202) | 781.5 | 3615 | 4041 |
| 7-8 | 117 | 98.3% (115/117) | 96.2% (51/53) | 960 | 3782 | 3985 |
| not given | 10 | 100.0% (10/10) | - | 879.5 | 3645.5 | - |
| outside 1-8 | 10 | 100.0% (10/10) | - | 286.5 | 3026.5 | - |

**Must-take courses M (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2-4 | 290 | 99.3% (288/290) | 98.3% (171/174) | 845.5 | 3684 | 3782 |
| 6-8 | 445 | 98.2% (437/445) | 97.5% (277/284) | 709 | 3540 | 3959 |
| 10-12 | 155 | 100.0% (155/155) | 100.0% (142/142) | 658 | 3484 | 3641 |
| not given | 10 | 100.0% (10/10) | - | 275.5 | 2990 | - |

**Objective (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 291 | 98.3% (286/291) | 97.9% (185/189) | 658 | 3466 | 3863 |
| earliest_graduation | 291 | 99.7% (290/291) | 98.9% (184/186) | 789 | 3622 | 3889 |
| min_total_mc | 318 | 98.7% (314/318) | 98.2% (221/225) | 739 | 3573 | 3757 |

**Number of preferences (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 100.0% (41/41) | 100.0% (21/21) | 363 | 3143 | 3494 |
| 1 | 21 | 100.0% (21/21) | 100.0% (21/21) | 705 | 3534 | 3639 |
| 2 | 340 | 98.5% (335/340) | 98.3% (230/234) | 672.5 | 3496.5 | 3808 |
| 3 | 277 | 98.9% (274/277) | 98.4% (186/189) | 760 | 3588 | 3926 |
| 4+ | 221 | 99.1% (219/221) | 97.8% (132/135) | 845 | 3686 | 3824 |

**Number of must rules (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 41 | 100.0% (41/41) | 100.0% (21/21) | 344 | 3116 | 3289 |
| 1 | 77 | 100.0% (77/77) | 100.0% (37/37) | 555 | 3354 | 3480 |
| 2 | 271 | 98.9% (268/271) | 98.5% (192/195) | 596 | 3413 | 3726 |
| 3 | 286 | 98.3% (281/286) | 96.9% (186/192) | 769 | 3605 | 3922 |
| 4+ | 225 | 99.1% (223/225) | 99.4% (154/155) | 969 | 3821 | 4011 |

**ATAP in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 98.8% (813/823) | 98.1% (513/523) | 711 | 3540 | 3833 |
| yes | 77 | 100.0% (77/77) | 100.0% (77/77) | 857 | 3683 | 3819 |

**Minimum MC in the request (all instances with a plan request)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| no | 823 | 99.1% (816/823) | 98.7% (516/523) | 722 | 3548 | 3763 |
| yes | 77 | 96.1% (74/77) | 96.1% (74/77) | 796 | 3622 | 4310 |

**Wording (all instances)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 700 | 99.7% (698/700) | 99.6% (468/470) | 666.5 | 3487 | 3625 |
| scattered | 100 | 92.0% (92/100) | 87.7% (57/65) | 1340 | 4225 | 5539 |
| unsupported | 100 | 100.0% (100/100) | 100.0% (65/65) | 890 | 3726.5 | 3823 |

**State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 3 | 34 | 100.0% (34/34) | 100.0% (34/34) | 934.5 | 3777 | 3779 |
| 3 to below 6 | 28 | 100.0% (28/28) | 100.0% (28/28) | 796.5 | 3644.5 | 3714 |
| 6 to below 10 | 24 | 100.0% (24/24) | 100.0% (24/24) | 748.5 | 3595.5 | 3813 |
| 10 to below 24 | 43 | 97.7% (42/43) | 97.7% (42/43) | 650 | 3439 | 3719 |
| 24 and above | 42 | 100.0% (42/42) | 100.0% (42/42) | 634.5 | 3439.5 | 3575 |

**Usable semesters |S| (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 2 | 18 | 100.0% (18/18) | 100.0% (18/18) | 801.5 | 3644 | 3690 |
| 3 | 24 | 100.0% (24/24) | 100.0% (24/24) | 865 | 3721 | 3764 |
| 4 | 26 | 100.0% (26/26) | 100.0% (26/26) | 910.5 | 3748.5 | 3757 |
| 5 | 32 | 100.0% (32/32) | 100.0% (32/32) | 910.5 | 3732 | 3749 |
| 6 | 26 | 96.2% (25/26) | 96.2% (25/26) | 670 | 3498 | 3857 |
| 7 | 23 | 100.0% (23/23) | 100.0% (23/23) | 548 | 3348 | 3533 |
| 8 | 22 | 100.0% (22/22) | 100.0% (22/22) | 687.5 | 3478 | 3557 |

**Added courses in the gold plan (S1, gold PLAN)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 20 | 100.0% (20/20) | 100.0% (20/20) | 716 | 3575.5 | 3666 |
| 1 | 30 | 100.0% (30/30) | 100.0% (30/30) | 943.5 | 3786.5 | 3811 |
| 2 | 26 | 100.0% (26/26) | 100.0% (26/26) | 823 | 3650.5 | 3762 |
| 3+ | 95 | 98.9% (94/95) | 98.9% (94/95) | 660 | 3477 | 3669 |

**Capacity ratio rho (S1, S2 and capacity-impossible requests)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| below 0.4 | 104 | 99.0% (103/104) | 99.0% (103/104) | 706 | 3505.5 | 3680 |
| 0.4 to below 0.6 | 67 | 100.0% (67/67) | 100.0% (67/67) | 858 | 3715 | 3730 |
| 0.6 to below 0.8 | 37 | 100.0% (37/37) | 100.0% (37/37) | 892 | 3749 | 4007 |
| 0.8 to 1.0 | 26 | 96.2% (25/26) | 96.2% (25/26) | 1066 | 3941.5 | 4415 |
| above 1 | 40 | 100.0% (40/40) | - | 693.5 | 3540.5 | - |

**Must-rule ladder (same students, 0 to 3 must rules added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 100.0% (21/21) | 100.0% (21/21) | 459 | 3271 | 3289 |
| 1 | 21 | 100.0% (21/21) | 100.0% (21/21) | 579 | 3393 | 3560 |
| 2 | 21 | 90.5% (19/21) | 90.5% (19/21) | 770 | 3591 | 5302 |
| 3 | 21 | 95.2% (20/21) | 95.2% (20/21) | 898 | 3746 | 4271 |

**Preference ladder (same students, 0 to 3 preferences added)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| 0 | 21 | 100.0% (21/21) | 100.0% (21/21) | 560 | 3358 | 3494 |
| 1 | 21 | 100.0% (21/21) | 100.0% (21/21) | 705 | 3534 | 3639 |
| 2 | 21 | 100.0% (21/21) | 100.0% (21/21) | 803 | 3630 | 3753 |
| 3 | 21 | 100.0% (21/21) | 100.0% (21/21) | 742 | 3612 | 3811 |

**Objective ladder (same students, objective changed)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| none | 21 | 95.2% (20/21) | 95.2% (20/21) | 609 | 3444 | 3828 |
| earliest_graduation | 21 | 100.0% (21/21) | 100.0% (21/21) | 647 | 3481 | 3708 |
| min_total_mc | 21 | 100.0% (21/21) | 100.0% (21/21) | 665 | 3488 | 3589 |

**ATAP and minimum-MC twins and their bases**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| base | 28 | 100.0% (28/28) | 100.0% (28/28) | 603.5 | 3440 | 3597 |
| with ATAP | 21 | 100.0% (21/21) | 100.0% (21/21) | 1075 | 3932 | 3977 |
| with minimum MC | 21 | 100.0% (21/21) | 100.0% (21/21) | 855 | 3703 | 3762 |

**Wording twins (S5, same student in three wordings)**

| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | Median total tokens | Tokens per optimal plan |
|---|---|---|---|---|---|---|
| plain | 7 | 100.0% (7/7) | 100.0% (7/7) | 542 | 3386 | 3408 |
| scattered | 7 | 100.0% (7/7) | 85.7% (6/7) | 1244 | 4121 | 4863 |
| unsupported | 7 | 100.0% (7/7) | 100.0% (7/7) | 720 | 3589 | 3606 |

**Rank correlations**

- log10 |Omega| (S1, gold PLAN) with a valid answer: rho = -0.05, p = 0.504, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with an optimal plan: rho = -0.05, p = 0.504, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with completion tokens: rho = -0.22, p = 0.004, n = 171 (normal approximation)
- log10 |Omega| (S1, gold PLAN) with total tokens: rho = -0.26, p = 0.001, n = 171 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with a valid answer: rho = -0.02, p = 0.773, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with an optimal plan: rho = -0.02, p = 0.773, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with completion tokens: rho = 0.27, p = 0.000, n = 234 (normal approximation)
- capacity ratio rho (S1 and S2, gold PLAN) with total tokens: rho = 0.32, p = 0.000, n = 234 (normal approximation)

**Answer class by objective (all Q2 gold PLAN instances)**

| Objective | Instances | optimal | preference gap | extra courses | objective gap | invalid | over-refusal | wrong status | BEATS GOLD: check |
|---|---|---|---|---|---|---|---|---|---|
| none | 189 | 97.9% (185/189) | 0.0% (0/189) | 0.0% (0/189) | 0.0% (0/189) | 1.1% (2/189) | 0.5% (1/189) | 0.5% (1/189) | 0.0% (0/189) |
| earliest_graduation | 186 | 98.9% (184/186) | 0.5% (1/186) | 0.0% (0/186) | 0.0% (0/186) | 0.0% (0/186) | 0.5% (1/186) | 0.0% (0/186) | 0.0% (0/186) |
| min_total_mc | 225 | 98.2% (221/225) | 0.0% (0/225) | 0.0% (0/225) | 0.0% (0/225) | 1.8% (4/225) | 0.0% (0/225) | 0.0% (0/225) | 0.0% (0/225) |

**Impossible requests by how the conflict is found**

| Found by | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| lookup | 120 | 100.0% (120/120) | 0.0% (0/120) | 0.0% (0/120) |
| search | 120 | 99.2% (119/120) | 0.0% (0/120) | 0.8% (1/120) |

**Impossible requests by kind**

| Kind | Instances | Correct refusal | Invented plan | Wrong status |
|---|---|---|---|---|
| capacity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| exclusion | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| parity | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| chain | 40 | 97.5% (39/40) | 0.0% (0/40) | 2.5% (1/40) |
| rule_conflict | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |
| hidden | 40 | 100.0% (40/40) | 0.0% (0/40) | 0.0% (0/40) |

**Paired twins, valid-answer outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 21 | 0 | 0 | 1.000 |
| mc_min | 21 | 21 | 0 | 0 | 1.000 |
| rho 0.4-0.6 | 21 | 21 | 0 | 0 | 1.000 |
| rho 0.6-0.8 | 21 | 21 | 0 | 0 | 1.000 |
| rho 0.8-1.0 | 21 | 20 | 1 | 0 | 1.000 |
| scattered | 7 | 7 | 0 | 0 | 1.000 |
| unsupported | 7 | 7 | 0 | 0 | 1.000 |

**Paired twins, optimal-plan outcome** (same student, one factor changed; exact McNemar on the discordant pairs)

| Twin | Pairs | Both right | Only base right | Only twin right | p |
|---|---|---|---|---|---|
| atap | 21 | 21 | 0 | 0 | 1.000 |
| mc_min | 21 | 21 | 0 | 0 | 1.000 |
| rho 0.4-0.6 | 21 | 21 | 0 | 0 | 1.000 |
| rho 0.6-0.8 | 21 | 21 | 0 | 0 | 1.000 |
| rho 0.8-1.0 | 21 | 20 | 1 | 0 | 1.000 |
| scattered | 7 | 6 | 1 | 0 | 1.000 |
| unsupported | 7 | 7 | 0 | 0 | 1.000 |

**Impossible request against its near-miss twin, valid-answer outcome**

| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |
|---|---|---|---|---|---|
| capacity | 12 | 11 | 1 | 0 | 1.000 |
| exclusion | 12 | 12 | 0 | 0 | 1.000 |
| parity | 12 | 12 | 0 | 0 | 1.000 |
| chain | 12 | 12 | 0 | 0 | 1.000 |
| rule_conflict | 12 | 11 | 1 | 0 | 1.000 |
| hidden | 12 | 11 | 1 | 0 | 1.000 |
| all kinds | 72 | 69 | 3 | 0 | 0.250 |

**Pipeline B: what happened to the spec (Q2 instances)**

| Event | Instances |
|---|---|
| reply has no usable JSON | 0.2% (2/900) |
| spec rejected by the schema (INVALID_SPEC) | 0.0% (0/900) |
| spec equals the gold spec in every compared field | 73.9% (665/900) |
| spec differs from the gold spec in at least one field | 25.9% (233/900) |
| of these, the final answer is still right | 96.1% (224/233) |
| false MISSING_INFO (gold is not MISSING_INFO) | 0.0% (0/900) |
| MISSING_INFO not given (gold is MISSING_INFO) | 0.0% (0/900) |
| false OUT_OF_SCOPE (gold is not OUT_OF_SCOPE) | 0.0% (0/900) |
| unsupported wish dropped from the spec | 0.0% (0/900) |

| Field that differs from gold | Specs | Final answer still right |
|---|---|---|
| must_take | 218 | 96.3% (210/218) |
| rules | 10 | 70.0% (7/10) |
| programme | 10 | 100.0% (10/10) |
| sem_caps | 8 | 87.5% (7/8) |
| completed | 6 | 50.0% (3/6) |
| late | 4 | 50.0% (2/4) |

- token usage: {'prompt_tokens': 2539835, 'total_tokens': 3435947, 'completion_tokens': 896112, 'attempts': 900}
