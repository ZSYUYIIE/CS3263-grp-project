# Q1 instance set (seed 3263)

400 instances. Regenerate with `python -m instances.generate_q1 --seed 3263`.

## By gold status

| Status | Instances |
|---|---|
| ELIGIBLE | 141 |
| MISSING_INFO | 14 |
| NOT_ELIGIBLE | 225 |
| OUT_OF_SCOPE | 20 |

## Base cases by reason and level

| Reason | L1 | L2 | L3 | Base cases | Instances |
|---|---|---|---|---|---|
| eligible | 18 | 18 | 18 | 54 | 138 |
| missing_prereq | 18 | 18 | 18 | 54 | 108 |
| precluded | 5 | 5 | 5 | 15 | 48 |
| wrong_term | 4 | 4 | 4 | 12 | 36 |
| closed | 3 | 3 | 3 | 9 | 18 |
| already_done | 2 | 2 | 2 | 6 | 12 |

## Roles

| Role | Instances |
|---|---|
| base_harder | 150 |
| base_plain | 150 |
| exclusion_twin | 18 |
| info | 40 |
| term_twin | 42 |

## Wording style

| Style | Instances |
|---|---|
| correction | 75 |
| plain | 250 |
| scattered | 75 |

## Complexity level of all instances

| Level | Instances |
|---|---|
| 1 | 120 |
| 2 | 120 |
| 3 | 120 |
| None | 40 |

Target use among base cases: max 4, distinct targets 85; CS3233 base cases: 2.

Completed-set reuse among non-missing base cases: max 1.

Sentence openings (first two words), top 5: i am 12%, i have 10%, excuse me. 7%, thanks for 6%, small query: 6%

Correction renderings: 75; retracted course would change the answer in 22 of 27 'drop' cases.

## Examples

- **q1-el-001-p** (ELIGIBLE, base_plain, plain): Planning ahead: I've finished MA1521, CS2040S, CS1231S, ES2660, CS2030S, CS2104, CS1101S and CS2103T. Do I qualify to take CS4211 in semester 5?
- **q1-el-001-h** (ELIGIBLE, base_harder, scattered): I am wondering about CS4211. Could I take it in Y3S1? I have completed CS2103T, ES2660, CS2104 and CS1101S. On top of that I cleared CS2030S. Done as well: CS2040S, MA1521 and CS1231S.
- **q1-el-001-t** (ELIGIBLE, term_twin, plain): I have credit for CS2030S, CS2040S, CS1231S, CS1101S, CS2104, CS2103T, MA1521 and ES2660. I am in Year 2, Semester 2 now. May I take CS4211 next semester?
- **q1-mp-001-p** (NOT_ELIGIBLE, base_plain, plain): Finished modules: CS2109S, CS1101S, MA1521, ES2660, CS2107, CS1231S, CS3234 and CS2040S. I want to take CS4211 in year 3 semester 1. Am I eligible?
- **q1-mp-001-h** (NOT_ELIGIBLE, base_harder, scattered): I have completed CS1101S, ES2660 and CS1231S. Besides those, I passed CS2040S, CS3234, MA1521, CS2107 and CS2109S. I am wondering about CS4211. Could I register for it in year 3 semester 1?
- **q1-el-003-h** (ELIGIBLE, base_harder, correction): Am I allowed to take CS3240 in year 3 semester 1? I have completed MA1301, ES2660, CS3230, CS2111, CS2101, CS4243, CS1231, CS2100HS and CS1101S. Sorry, not CS4243, I meant CS2040DE. I have not taken CS4215.
- **q1-mp-003-h** (NOT_ELIGIBLE, base_harder, correction): Is it possible for me to take CS3240 in Y3 Sem 1? I have completed CS2040DE, CS2101, CS4215, CS1101S, CS1231, CS3230, ES2660 and MA1301. Correction: I never took CS4215; it was CS2100HS. I haven't done MA3236 yet.
- **q1-el-011-x** (NOT_ELIGIBLE, exclusion_twin, plain): Planning ahead: Courses behind me: IE2110, ST2334, CS1010X, MA2104, MA1521, CS1231 and MA1522. Could I take MA3252 in Year 2, Semester 2?
- **q1-ex-001-p** (NOT_ELIGIBLE, base_plain, plain): These are done: CS1231S, CG2028, MA1521, CS1101S, CS2040, ES1000, IS1108 and MA2311. Am I allowed to take CS2100DE in Y2 Sem 2?
- **q1-ex-001-h** (NOT_ELIGIBLE, base_harder, scattered): I have completed ES1000, MA1521, CS1231S, IS1108, CG2028, CS2040 and MA2311. Besides those, I passed CS1101S. Is CS2100DE something I can enrol in in year 2 semester 2?
- **q1-ex-002-h** (NOT_ELIGIBLE, base_harder, correction): Hi! I am looking at Y4 Sem 1. Sorry, I mean Year 3, Semester 2. May I take EE4204? I have completed CS2100, CS1010, MA1508E, IS1108, CS3268, CS2040S, ES2660, CS1231S, ST2334, CS1010X, CS2105, ST3248, MA1521, CS2101, CS2106 and CS2109S. Sorry, not CS1010X, I meant CS3230. I have not taken CS5422. I haven't done CS1010HS yet.
- **q1-wt-001-p** (NOT_ELIGIBLE, base_plain, plain): Good day. May I take CS3216 in Y2 Sem 2? I already took CS2101, CS1231S, CS1010S, CS2030S, IS1108, ESP2111, CS2103T, CS2040S and CS2220.
- **q1-wt-001-h** (NOT_ELIGIBLE, base_harder, scattered): Hi! I have completed IS1108, CS2220, CS2101 and ESP2111. Also completed: CS2030S, CS1010S and CS2040S. Besides those, I passed CS1231S and CS2103T. I am wondering about CS3216. Could I enrol in it in year 2 semester 2?
- **q1-wt-001-t** (NOT_ELIGIBLE, term_twin, plain): My record shows ESP2111, CS1231S, CS2220, CS2040S, CS1010S, CS2101, CS2030S, IS1108 and CS2103T as completed. I am in Y2 Sem 1 now. Could I take CS3216 next semester?
- **q1-cl-001-p** (NOT_ELIGIBLE, base_plain, plain): Hi there. For year 2 semester 1, am I eligible to take LSM2241? I have completed MA1513, IS1108, MA1512, ES2660, CS1231S and LSM1301.
- **q1-cl-001-h** (NOT_ELIGIBLE, base_harder, scattered): I am wondering about LSM2241. Could I take it in semester 3? I have completed LSM1301, IS1108, ES2660 and MA1513. Done as well: MA1512 and CS1231S.
- **q1-cl-002-h** (NOT_ELIGIBLE, base_harder, correction): Hello! I have completed MA1521, ES1000, CS1101S, MA2311, CS1231S, MA1508E and ST2334. Wait, MA2311 is wrong. I actually finished MA2104. I haven't done CS5424 yet. I am looking at year 2 semester 1. Sorry, I mean Y2 Sem 2. Am I allowed to take EE5310?
- **q1-ad-001-p** (NOT_ELIGIBLE, base_plain, plain): I am planning my modules for Year 3, Semester 1. I have completed ST1131, CS2030S, CS2040S, CS3210, CS2106, CS2101, CS2100DE, IS2108, CS3227, CS3213, CS1101S, CS2103T, MA1522, CS1231S, MA1512 and ES2660. Am I allowed to take CS3227?
- **q1-ad-001-h** (NOT_ELIGIBLE, base_harder, correction): Hi there. I am looking at Y3S2. Sorry, I mean Y3S1. Can I take CS3227? I have completed MA1512, CS3227, CS2040S, MA1522, CS2030S, CS1101S, ST1131, CS1231S, IS2108, CS2106, CS2100DE, CS1010HS, ES2660, CS2103T, CS3210 and CS2101. Wait, CS1010HS is wrong. I actually finished CS3213. CS4238 is not on my record. CS2105 is not on my record.
- **q1-ad-002-h** (NOT_ELIGIBLE, base_harder, scattered): Thanks for helping. Does my record allow me to register for CS4247 in year 4 semester 2? I have completed MA1511, CS2105, CS2040S, CS1101S, CS2113, CS1231S, CS3241 and CS3234. Done as well: CS4247, CS3230, MA1522, CS2030S, CS3219, IS2101 and CS2100.
- **q1-wt-005-h** (NOT_ELIGIBLE, base_harder, correction): Hi there. I have completed CS2101, CS2103T, CS1101S, CS3230, IS1108, MA1522, CS1231S, CS5462, CS3281, MA1505, CS3219, CS2040S and CS2105. Correction: I never took CS5462; it was CS2030S. CS1010E is not on my record. I haven't done CS2113 yet. I am looking at year 4 semester 1. Sorry, I mean Y4 Sem 2. Is it possible for me to take CS3241?
- **q1-mi-01** (MISSING_INFO, info, plain): Is it possible for me to take CS2030 in Y4S2?
- **q1-dc-01** (ELIGIBLE, info, plain): Here is what I have finished: IS1108, CS2030S, MA2104, ES2660, MA3252, CS2100, CS1010HS, MA1513, CS3210, CS2101, MA1511 and ES1000. I want to take EE2211. Am I eligible?
- **q1-os-01** (OUT_OF_SCOPE, info, plain): I am a Business Analytics student. Finished modules: MA1508E, CS2030S, MA1521, MA3270, ESP2111, EE2211, IS2101, MA1511, ST2334, ST3248, CS2107 and CS1010X. Could I take EE4211 in semester 5?
- **q1-os-06** (OUT_OF_SCOPE, info, plain): Excuse me. Could I take CS5340 in Year 4, Semester 1? Here is what I have finished: MA1301X, CS1231S, ESP1111, ES1000, CS3210, IS2101, CS2106, IS2108, ESP2107, CS1101S, CS2100 and CS2030DE.
- **q1-os-16** (OUT_OF_SCOPE, info, plain): Planning ahead: On my transcript: CS2101, MA1505, CS2040S, CS2030, CS1231S, MA2104 and CS1101S. Am I eligible to take CS4215 in year 5 semester 1?