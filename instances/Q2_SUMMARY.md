# Q2 instance set (seed 3263)

900 instances in `q2_900.json`. Regenerate with `python -m instances.generate_q2 --seed 3263`.

### Set

| Value | Count |
|---|---|
| S1 | 171 |
| S2 | 63 |
| S3 | 273 |
| S4 | 312 |
| S5 | 21 |
| S6 | 60 |
| total | 900 |

### Kind

| Value | Count |
|---|---|
| missing_info/completed | 10 |
| missing_info/current_sem | 10 |
| missing_info/must_take | 10 |
| out_of_scope/course not in catalogue | 5 |
| out_of_scope/minor | 5 |
| out_of_scope/other programme | 5 |
| out_of_scope/second major | 5 |
| out_of_scope/semester 0 | 5 |
| out_of_scope/semester above 8 | 5 |
| q2/S1 | 171 |
| q2/S2 | 63 |
| q2/S3 | 273 |
| q2/S5 | 21 |
| q2/near_miss_capacity | 12 |
| q2/near_miss_chain | 12 |
| q2/near_miss_exclusion | 12 |
| q2/near_miss_hidden | 12 |
| q2/near_miss_parity | 12 |
| q2/near_miss_rule_conflict | 12 |
| q2_infeasible/capacity | 40 |
| q2_infeasible/chain | 40 |
| q2_infeasible/exclusion | 40 |
| q2_infeasible/hidden | 40 |
| q2_infeasible/parity | 40 |
| q2_infeasible/rule_conflict | 40 |
| total | 900 |

### Answer type

| Value | Count |
|---|---|
| MISSING_INFO | 30 |
| NO_PLAN | 240 |
| OUT_OF_SCOPE | 30 |
| PLAN | 600 |
| total | 900 |

### Current semester band

| Value | Count |
|---|---|
| 1-2 | 149 |
| 3-4 | 318 |
| 5-6 | 296 |
| 7-8 | 117 |
| not given | 10 |
| outside 1-8 | 10 |
| total | 900 |

### Must-take count M

| Value | Count |
|---|---|
| 10-12 | 155 |
| 2-4 | 290 |
| 6-8 | 445 |
| not given | 10 |
| total | 900 |

### Objective

| Value | Count |
|---|---|
| earliest_graduation | 291 |
| min_total_mc | 318 |
| none | 291 |
| total | 900 |

### Number of preferences

| Value | Count |
|---|---|
| 0 | 41 |
| 1 | 21 |
| 2 | 340 |
| 3 | 277 |
| 4 | 221 |
| total | 900 |

### Number of must rules

| Value | Count |
|---|---|
| 0 | 41 |
| 1 | 77 |
| 2 | 271 |
| 3 | 286 |
| 4 | 225 |
| total | 900 |

### ATAP

| Value | Count |
|---|---|
| False | 823 |
| True | 77 |
| total | 900 |

### Minimum MC

| Value | Count |
|---|---|
| False | 823 |
| True | 77 |
| total | 900 |

### Wording

| Value | Count |
|---|---|
| plain | 700 |
| scattered | 100 |
| unsupported | 100 |
| total | 900 |

### NO_PLAN kind

| Value | Count |
|---|---|
| - | 660 |
| capacity | 40 |
| chain | 40 |
| exclusion | 40 |
| hidden | 40 |
| parity | 40 |
| rule_conflict | 40 |
| total | 900 |

### NO_PLAN found by

| Value | Count |
|---|---|
| - | 660 |
| lookup | 120 |
| search | 120 |
| total | 900 |

### log10 |Omega| on S1

| Bin | Count |
|---|---|
| below 3 | 34 |
| 3 to below 6 | 28 |
| 6 to below 10 | 24 |
| 10 to below 24 | 43 |
| 24 and above | 42 |

### Added courses in the gold plan on S1

| Value | Count |
|---|---|
| 0 | 20 |
| 1 | 30 |
| 2 | 26 |
| 3+ | 95 |

### Capacity ratio rho (S1, S2, capacity impossible)

| Bin | Count |
|---|---|
| below 0.4 | 104 |
| 0.4 to below 0.6 | 67 |
| 0.6 to below 0.8 | 37 |
| 0.8 to 1.0 | 26 |
| above 1 | 40 |

## Examples

- **q2-S1-001** (q2/S1, plain, gold `PLAN`): I am a Computer Science (BComp CS Hons) student. I have not completed any module yet. I am in Y1S1 now. I must take ES2660 and CS3230. CS3230 and ES2660 must not be in the same semester. I must take CS4430 in Y4S2. Ideally I'd take CS4430 before ES2660. I would like CS3230 as early as possible. Please plan my remaining semesters.
- **q2-S1-005** (q2/S1, scattered, gold `PLAN`): I have not completed any module yet. I'd rather do CS2109S before CS3213. At most 4 modules per semester. CS3230 has to be in semester 7. CS2109S and CS2030S must be in the same semester. If possible, I would like CS2030S in semester 6. If possible, keep CS3213 and CS2030S apart. Please use the fewest semesters. If possible, keep CS2030S and CS3230 apart. I must take CS3213 in Y3S2. I am currently in year 1 semester 1. I'm a BComp Computer Science Honours student. I need to take CS2109S and CS4220. I almost forgot CS2030S, I need that as well. Actually, scratch CS4220, I've decided not to take it. Please plan my remaining semesters.
- **q2-S1-028** (q2/S1, unsupported, gold `PLAN`): I have not completed any module yet. This semester is semester 1 for me. I still have to take CS2030S, IS1108, CS2106, CS3241, CS3219, MA1522, CS3268 and CS3233. There's a chance I fail one module this semester and have to retake it. I can take at most 16 MC per semester. CS3241 must come before IS1108. I must take CS3103 in Y4S1. I would like CS3233 as late as possible. I would like CS2106 as late as possible. I'd like modules taught by my favourite lecturer when possible. Can you plan the rest of my degree?
- **q2-S2-001** (q2/S2, scattered, gold `PLAN`): I've done CS2100, CS2105, CS3263, ES2660, MA1522, CS2101, CS2103T, CS2030S, ST2334, CS2109S, CS1101S, CS3219, CS2106, CS2040S and IS1108. CS3227 must come before CS3103. In semester 6 I can only take 3 modules. CS2102 and CS4218 must be in the same semester. I want to graduate as early as possible. At most 4 modules per semester. Modules I still need: CS2102, CS3227, CS3103 and CS4218. I'd rather do CS4218 before CS3282. I'm in Y3S1 now. Wait, sorry, I'm actually in semester 6. If you can, put CS3210 as late as possible. I almost forgot CS3210 and CS3282, I need those as well. I must take CS2102 in year 4 semester 1. Also already done: CS1231S, MA1521 and CS3230. CS2102 and CS3210 must not be in the same semester. Please plan my remaining semesters.
- **q2-S3-001** (q2/S3, scattered, gold `PLAN`): I've done CS3219, CS3263, IS1108, MA1521, CS2106, CS2101, MA1522 and ST2334. Oh, I forgot to say I also completed CS2103T, CS1231S, CS2109S, CS2100, CS2105, CS2030S, CS2040S, CS1101S, ES2660 and CS3230. If you can, put CS3210 as late as possible. Ideally I'd take CS4218 before CS3282. I'm in Y4S1 now. Wait, sorry, I'm actually in Y3S2. I plan to do ATAP at some point, no particular semester. I need to take CS4218, CS3227, CS2102, CS3103 and CS3282. I want to graduate as early as possible. Oh, and CS3210 too. What should my plan look like?
- **q2-S2-004** (q2/S2, plain, gold `PLAN`): My completed modules are MA1521, CS2100, MA1522, CS1101S, CS2101, ES2660, IS1108, CS1231S, ST2334, CS2103T, CS2030S and CS2040S. I am currently in Y2S2. I must take CS2109S, CS2102, CS3231, CS3230, CS3264 and CS3219. At most 3 modules per semester. In semester 8 I can only take 1 module. I have to take CS2102 and CS3264 together in one semester. I have to take CS3231 and CS2102 together in one semester. CS3230 and CS2109S must not be in the same semester. If possible, keep CS3231 and CS3264 apart. Ideally I'd take CS2102 before CS3219. If you can, put CS3230 as late as possible. Please plan my remaining semesters.
- **q2-S3-014** (q2/S3, plain, gold `PLAN`): So far I have passed ES2660, CS1231S, CS2100, CS2101, CS1101S, ST2334, CS2040S, CS2030S, MA1522, MA1521, IS1108 and CS2103T. I'm starting semester 4. I still have to take CS2109S, CS3231, CS2102, CS3230, CS3219 and CS3264. My ATAP internship is in Y3S2. If possible, keep CS3231 and CS3264 apart. I'd rather do CS2102 before CS3219. If you can, put CS3230 as late as possible. Please plan my remaining semesters.
- **q2-S2-016** (q2/S2, unsupported, gold `PLAN`): I have completed MA1521, CS1231S, ES2660, CS1101S, MA1522, IS1108, CS2040S, CS2030S, CS2101, ST2334, CS2103T and CS2100. I'm starting Y2S2. I must take CS2106, CS2109S, CS2105, CS4231, CS3219 and CS4226. I can take at most 12 MC per semester. In semester 6 I can only take 3 modules. There's a chance I fail one module this semester and have to retake it. Please use the fewest semesters. I need to finish CS3219 before I start CS4226. CS4231 must come before CS2109S. CS4226 and CS4231 must not be in the same semester. CS2106 must come before CS4231. Ideally CS4226 and CS2109S go in the same semester. I would like CS2109S as late as possible. Can you plan the rest of my degree?
- **q2-S3-066** (q2/S3, unsupported, gold `PLAN`): My completed modules are CS1231S, CS2103T, CS1101S, CS2040S, MA1521, IS1108, ES2660, MA1522, ST2334, CS2030S, CS2101 and CS2100. I am currently in year 2 semester 2. I still have to take CS2106, CS4231, CS2105, CS2109S, CS3219 and CS4226. I will do ATAP in semester 7. Finishing as soon as possible matters most to me. I would like CS4226 and CS2109S together in one semester. There's a chance I fail one module this semester and have to retake it. If you can, put CS2109S as late as possible. What should my plan look like?
- **q2-S4-001** (q2_infeasible/capacity, unsupported, gold `NO_PLAN`): My completed modules are MA1522, CS2040S, CS1101S, MA1521, IS1108, CS2030S and CS1231S. I am in year 2 semester 1 now. I still have to take CS3237, CS4221, CS2103T, CS3230, CS4247, CS2105 and CS3241. I can take at most 4 MC per semester. I need to finish CS2103T before I start CS3241. I want at most two modules with final exams in a semester. I'd like to avoid modules with heavy group projects. I'd rather do CS3237 before CS3241. Ideally I'd take CS2103T before CS2105. What should my plan look like?
- **q2-S4-002** (q2/near_miss_capacity, unsupported, gold `PLAN`): So far I have passed MA1521, MA1522, IS1108, CS1231S, CS2030S, CS2040S and CS1101S. I am in year 2 semester 1 now. I need to take CS3237, CS3241, CS4247, CS3230, CS4221, CS2103T and CS2105. I want at most two modules with final exams in a semester. I can take at most 8 MC per semester. I'd like to avoid modules with heavy group projects. CS2103T must come before CS3241. Ideally I'd take CS3237 before CS3241. I'd rather do CS2103T before CS2105. What should my plan look like?
- **q2-S4-004** (q2_infeasible/capacity, plain, gold `NO_PLAN`): I am a Computer Science (BComp CS Hons) student. My completed modules are CS2106, ST2334, CS2101, MA1521, ES2660, CS2109S, CS1101S, IS1108, CS2030S, CS3230, CS2040S, CS2100, CS1231S, CS2103T and MA1522. I am currently in Y3S1. I need to take CS2105, CS3219, CS4278, CS3264, CS4239 and CS2102. At most 1 module per semester. Please keep my total MC as low as possible. I need to finish CS2102 before I start CS4278. CS2105 must come before CS4278. CS4239 must come before CS3264. I would like CS4278 and CS4239 together in one semester. Ideally I'd take CS3264 before CS2105. How should I arrange my remaining semesters?
- **q2-S4-006** (q2/near_miss_capacity, plain, gold `PLAN`): My completed modules are ST2334, CS1231S, CS2103T, CS2030S, CS2100, CS2101, CS2106, CS2109S, CS1101S, CS2040S, CS3219, ES2660, MA1522, MA1521 and CS3230. This semester is year 3 semester 2 for me. My remaining required modules are CS4277, CS3235, CS2105, CS4247, IS1108 and CS2102. My limit is 12 MC each semester. Finishing as soon as possible matters most to me. I have to take CS2105 and CS2102 together in one semester. CS4277 and CS2102 must not be in the same semester. I must take CS4247 in year 4 semester 2. I have to take CS2102 and IS1108 together in one semester. Ideally CS2105 and CS4247 go in the same semester. I would like IS1108 as late as possible. Can you plan the rest of my degree?
- **q2-S4-008** (q2_infeasible/capacity, scattered, gold `NO_PLAN`): I've done ES2660 and CS2105. I'm in Y4S1 now. Wait, sorry, I'm actually in year 4 semester 2. If you can, put CS3233 as late as possible. I am a Computer Science (BComp CS Hons) student. If possible, keep CS3230 and CS3233 apart. I must take CS3223 in Y4S2. I'd prefer CS3223 and CS3230 in different semesters. At most 2 modules per semester. I need to take CS3233 and CS3223. Oh, and CS3230 too. Oh, I forgot to say I also completed ST2334, MA1522, CS2101, CS2100, CS3210, CS1231S, CS2106, IS1108, MA1521, CS3268, CS2040S, CS2109S, CS2030S, CS1101S, CS2102, CS3219 and CS2103T. I have to take CS3233 and CS3223 together in one semester. Please plan my remaining semesters.
- **q2-S4-028** (q2/near_miss_capacity, scattered, gold `PLAN`): I've done MA1521, CS1231S, CS2103T and IS1108. Ideally I'd take CS3281 before CS3240. If possible, keep CS3219 and CS2102 apart. I'd rather do CS3281 before CS2102. I can take at most 12 MC per semester. I'm in Y3S2 now. Wait, sorry, I'm actually in semester 5. I want the fewest total credits. I must take CS3268 in Y4S1. I would like CS3240 and CS2102 together in one semester. Also already done: CS2101, CS2100, MA1522, ST2334, CS2106, CS1101S, ES2660, CS2040S, CS2109S, CS2030S and CS3230. I need to take CS3268 and CS2102. Oh, and CS3240, CS3103, CS3219, CS4246 and CS3281 too. What should my plan look like?
- **q2-S4-053** (q2_infeasible/exclusion, scattered, gold `NO_PLAN`): I have not completed any module yet. I would like CS1101S as late as possible. I'm in year 1 semester 2 now. Wait, sorry, I'm actually in semester 1. CS3230 has to be in semester 5. Modules I still need: CS3230, CS3263, CS2102, CS1101S, CS2040S, CS4263, CS2030S and CS4223. If you can, put CS2040S as late as possible. I almost forgot CS1231S, I need that as well. I will be away on exchange in Y2S1, so no modules then. How should I arrange my remaining semesters?
- **q2-S4-054** (q2/near_miss_exclusion, scattered, gold `PLAN`): I have not completed any module yet. CS3230 has to be in semester 5. I need to take CS1101S, CS2030S, CS1231S, CS2102 and CS2040S. I would like CS2040S as late as possible. If you can, put CS1101S as late as possible. Oh, and CS3230, CS4223 and CS4263 too. I'm in year 1 semester 2 now. Wait, sorry, I'm actually in Y1S1. I will be away on exchange in Y2S1, so no modules then. Can you plan the rest of my degree?
- **q2-S4-055** (q2_infeasible/exclusion, plain, gold `NO_PLAN`): My completed modules are MA1521, CS1101S, ES2660 and CS1231S. I am currently in year 1 semester 2. I still have to take MA1522, CS4263, CS2105, CS3230, CS3243, ST2334 and CS4261. Please use the fewest semesters. I must take CS4261 in semester 3. CS2105 has to be in semester 5. Ideally I'd take MA1522 before CS4261. ST2334 as early as possible, please. How should I arrange my remaining semesters?
- **q2-S4-058** (q2/near_miss_exclusion, plain, gold `PLAN`): I've finished CS1231S, CS2100, CS2040S, CS2030S, MA1521, ST2334, CS2101, CS2103T, ES2660, CS1101S and MA1522. I am in Y2S2 now. My remaining required modules are CS2106, CS3242, IS1108 and CS4263. Finishing as soon as possible matters most to me. I must take CS4249 in semester 6. CS2106 has to be in semester 6. CS4236 has to be in semester 7. CS3223 has to be in semester 6. Ideally IS1108 and CS3242 go in the same semester. I would like CS3242 as early as possible. Please plan my remaining semesters.
- **q2-S4-061** (q2_infeasible/exclusion, unsupported, gold `NO_PLAN`): I've finished ES2660, CS2101, CS2100, CS1231S, CS3230, CS2106, ST2334, CS1101S, CS2109S, MA1521, CS2040S, CS2103T, MA1522, CS2102, IS1108, CS2030S and CS3219. I am currently in Y4S1. I need to take CS3243, CS4212, CS3210 and CS3263. My limit is 16 MC each semester. I want the fewest total credits. CS3210 and CS4212 must not be in the same semester. CS3264 has to be in semester 8. There's a chance I fail one module this semester and have to retake it. CS3210 has to be in semester 7. Ideally I'd take CS3264 before CS4212. Ideally CS3210 and CS3264 go in the same semester. If you can, put CS4212 as late as possible. How should I arrange my remaining semesters?
- **q2-S4-062** (q2/near_miss_exclusion, unsupported, gold `PLAN`): So far I have passed MA1521, CS2100, IS1108, CS2109S, MA1522, CS2101, CS2102, CS3230, CS1101S, CS2030S, CS2040S, CS2103T, CS2106, ES2660, CS1231S, CS3219 and ST2334. I'm starting semester 7. I need to take CS3263, CS3210 and CS4212. At most 4 modules per semester. I want the fewest total credits. CS3210 and CS4212 must not be in the same semester. I must take CS3264 in semester 8. CS3210 has to be in semester 7. There's a chance I fail one module this semester and have to retake it. I'd rather do CS3264 before CS4212. Ideally CS3210 and CS3264 go in the same semester. I would like CS4212 as late as possible. Please plan my remaining semesters.
- **q2-S4-105** (q2_infeasible/parity, plain, gold `NO_PLAN`): So far I have passed CS2106, CS1101S, CS2030S, CS2109S, CS2040S, CS3236, MA1522, ST2334, CS2100, CS1231S, CS2103T, CS2101, ES2660 and MA1521. I'm starting semester 5. I still have to take IS1108, CS3230, CS3281, CS2102, CS2105 and CS3219. I will be away on exchange in year 3 semester 2, so no modules then. I will do NOC in semester 8. I must take CS2102 in year 3 semester 1. Ideally CS2102 and CS3230 go in the same semester. I would like CS3230 as late as possible. Can you plan the rest of my degree?
- **q2-S4-106** (q2/near_miss_parity, plain, gold `PLAN`): I've finished CS3236, CS2103T, MA1521, ES2660, ST2334, CS2106, CS1231S, CS2040S, CS2101, CS2109S, CS2030S, CS1101S, MA1522 and CS2100. I'm starting semester 5. I still have to take CS3219, CS3281, IS1108, CS2102, CS3230 and CS2105. I will do NOC in semester 6. I must take CS2102 in semester 5. Ideally CS2102 and CS3230 go in the same semester. I would like CS3230 as late as possible. What should my plan look like?
- **q2-S4-109** (q2_infeasible/parity, unsupported, gold `NO_PLAN`): My completed modules are CS3230, CS1231S, CS2106, CS2040S, ST2334, CS2100, CS2103T, CS1101S, MA1522, CS2109S, CS2030S, IS1108, MA1521 and ES2660. I'm starting year 3 semester 1. I must take CS2105, CS3281, CS3242 and CS2101. I'd like to avoid modules with heavy group projects. I can take at most 12 MC per semester. I'm taking a leave of absence in semester 6. I will do NOC in semester 8. I'm also applying to have one module waived. I want to graduate as early as possible. I definitely can't have CS3242 and CS2105 together. I need to finish CS2105 before I start CS2101. I must take CS2105 in year 3 semester 1. I must take CS4211 in semester 5. Ideally CS3242 and CS2101 go in the same semester. I'd rather do CS4211 before CS3242. How should I arrange my remaining semesters?
- **q2-S4-110** (q2/near_miss_parity, unsupported, gold `PLAN`): So far I have passed CS2103T, ES2660, CS2040S, CS1231S, ST2334, CS2030S, IS1108, CS1101S, MA1521, MA1522, CS2106, CS3230, CS2109S and CS2100. I'm starting year 3 semester 1. My remaining required modules are CS2105, CS2101, CS3242 and CS3281. My limit is 12 MC each semester. I will do NOC in semester 6. Finishing as soon as possible matters most to me. I'm also applying to have one module waived. I'd like to avoid modules with heavy group projects. CS3242 and CS2105 must not be in the same semester. CS2105 must come before CS2101. I must take CS2105 in year 3 semester 1. CS4211 has to be in semester 5. Ideally CS3242 and CS2101 go in the same semester. Ideally I'd take CS4211 before CS3242. Can you plan the rest of my degree?
- **q2-S4-115** (q2_infeasible/parity, scattered, gold `NO_PLAN`): I've done CS2103T, CS2030S, MA1522, MA1521, ES2660, ST2334, CS2105, CS2106, CS2109S, CS2101, IS1108, CS3219, CS3231, CS1231S and CS2100. I'd prefer CS3230 and CS3236 in different semesters. I am a Computer Science (BComp CS Hons) student. I'm starting Y4S2. CS2102 as early as possible, please. CS3230 and CS2102 must be in the same semester. I'd rather do CS2102 before CS3227. I must take CS3227 in Y4S2. Modules I still need: CS3230 and CS3241. CS3230 has to be in semester 8. Oh, I forgot to say I also completed CS4243, CS2040S, CS4277 and CS1101S. Oh, and CS3268 and CS2102 too. I must take CS3236 in semester 8. Actually, scratch CS3241, I've decided not to take it. Please plan my remaining semesters.
- **q2-S4-145** (q2/near_miss_parity, scattered, gold `PLAN`): I've done CS2101, CS2102, ES2660, CS3219, CS2106, CS4226, MA1522, CS2105, ST2334, MA1521, CS2100, CS3230, CS2103T and CS2030S. Modules I still need: CS3241 and CS3235. Oh, I forgot to say I also completed CS2040S, CS2109S, CS1101S, IS1108 and CS1231S. If possible, keep CS3263 and CS4330 apart. I am in year 4 semester 1 now. Actually, scratch CS3235, I've decided not to take it. I almost forgot CS4212 and CS4261, I need those as well. I'd rather do CS3263 before CS3241. Please use the fewest semesters. I must take CS4330 in Y4S2. I must take CS3263 in semester 8. CS4212 as early as possible, please. I definitely can't have CS4212 and CS3241 together. Can you plan the rest of my degree?
- **q2-S4-157** (q2_infeasible/chain, plain, gold `NO_PLAN`): I've finished CS2100, CS1231S, ST2334, CS2103T, CS2101, CS1101S, CS2040S, MA1522, MA1521, CS2030S and ES2660. I'm starting year 2 semester 2. I must take CS4240, CS3230, CS4243, CS4249 and CS3247. I'm taking a leave of absence in semester 4. I will be away on exchange in Y4S2, so no modules then. I definitely can't have CS3247 and CS4243 together. Ideally CS4249 would be in semester 8. I would like CS4243 as late as possible. Can you plan the rest of my degree?
- **q2-S4-158** (q2/near_miss_chain, plain, gold `PLAN`): My completed modules are MA1522, ES2660, ST2334, CS1101S, CS2100, CS1231S, CS2101, MA1521, CS2103T, CS2030S and CS2040S. I am currently in year 2 semester 2. I still have to take CS3247, CS4243, CS3230, CS4240 and CS4249. I will be away on exchange in year 2 semester 2, so no modules then. I definitely can't have CS3247 and CS4243 together. Ideally CS4249 would be in Y4S2. If you can, put CS4243 as late as possible. What should my plan look like?
- **q2-S4-159** (q2_infeasible/chain, unsupported, gold `NO_PLAN`): I have completed CS2109S, ST2334, MA1521, MA1522, CS2103T, CS1101S, CS2101, CS1231S, CS2040S, CS2106, CS2030S, CS2100 and ES2660. This semester is semester 5 for me. I need to take CS4330, IS1108, CS3247, CS2105, CS4249, CS3230 and CS4222. I will be away on exchange in year 3 semester 2, so no modules then. Please use the fewest semesters. I have to take CS4330 and CS2105 together in one semester. I may S/U one of my modules. I have to take CS2105 and CS3230 together in one semester. Ideally CS4249 would be in Y4S2. Ideally IS1108 and CS4249 go in the same semester. What should my plan look like?
- **q2-S4-164** (q2_infeasible/chain, scattered, gold `NO_PLAN`): I've done CS2100. This semester is semester 4 for me. I would like CS3230 as early as possible. Also already done: CS2101, CS1101S, CS2030S, MA1521, CS2040S, IS1108, CS2103T, MA1522, CS1231S, ST2334 and ES2660. I need to take CS3230, CS2105, CS2102, CS4238 and CS4330. I almost forgot CS3219, I need that as well. CS2105 as early as possible, please. CS2102 has to be in semester 4. I will be away on exchange in year 3 semester 1, so no modules then. I am a Computer Science (BComp CS Hons) student. I will do NOC in semester 6. I will do NOC in semester 7. I would like CS3219 as early as possible. Actually, scratch CS4330, I've decided not to take it. I need to finish CS3219 before I start CS3230. How should I arrange my remaining semesters?
- **q2-S4-166** (q2/near_miss_chain, unsupported, gold `PLAN`): I'm a BComp Computer Science Honours student. I have completed CS2106, MA1521, CS2101, CS2103T, MA1522, ES2660, CS3230, CS2109S, CS1101S, CS2030S, CS2100, CS1231S, CS4277 and CS2040S. I am currently in year 3 semester 1. My remaining required modules are CS3242, CS2102, CS4224, CS4223, CS4231 and CS4240. I can take at most 16 MC per semester. Please keep my total MC as low as possible. I want at most two modules with final exams in a semester. I need to finish CS2102 before I start CS4240. I must take CS4430 in year 4 semester 2. I must take CS3242 in semester 8. If possible, I would like CS2102 in semester 7. Ideally CS4240 and CS4231 go in the same semester. Ideally I'd take CS4231 before CS2102. What should my plan look like?
- **q2-S4-197** (q2/near_miss_chain, scattered, gold `PLAN`): I've done MA1521, CS2040S, IS1108, CS1101S, ST2334, ES2660 and CS2030S. Modules I still need: CS4220, CS2106, CS3219 and CS2105. If you can, put CS3219 as late as possible. I almost forgot CS4350, CS2102 and CS3230, I need those as well. I have to take CS3219 and CS2102 together in one semester. I would like CS2105 as late as possible. At most 4 modules per semester. Also already done: CS1231S, CS2100, CS2101, MA1522 and CS2103T. Finishing as soon as possible matters most to me. CS2105 must come before CS3230. I'd prefer CS2102 and CS4220 in different semesters. I'm in year 3 semester 1 now. Wait, sorry, I'm actually in Y2S2. I definitely can't have CS2106 and CS3230 together. How should I arrange my remaining semesters?
- **q2-S4-209** (q2_infeasible/rule_conflict, plain, gold `NO_PLAN`): I'm a BComp Computer Science Honours student. I have not completed any module yet. This semester is Y1S1 for me. I must take ST2334, CS3243, CS4222, CS4268, CS3242 and MA1521. My limit is 16 MC each semester. CS3243 has to be in semester 6. CS4268 must come before CS3242. I need to finish CS3242 before I start CS4268. I'd prefer CS3243 and CS3242 in different semesters. If you can, put ST2334 as late as possible. How should I arrange my remaining semesters?
- **q2-S4-210** (q2/near_miss_rule_conflict, plain, gold `PLAN`): I'm a BComp Computer Science Honours student. I have not completed any module yet. This semester is semester 1 for me. I still have to take CS4268, ST2334, CS3243, CS4222, MA1521 and CS3242. My limit is 16 MC each semester. I must take CS3243 in semester 6. I need to finish CS4268 before I start CS3242. If possible, keep CS3243 and CS3242 apart. If you can, put ST2334 as late as possible. Can you plan the rest of my degree?
- **q2-S4-213** (q2_infeasible/rule_conflict, scattered, gold `NO_PLAN`): I've done CS2040S, ES2660, CS1231S, CS2101, CS1101S, IS1108, MA1521 and CS2100. I'm in semester 5 now. Wait, sorry, I'm actually in semester 4. Also already done: CS2030S, CS2103T, MA1522 and ST2334. I need to take CS3247, CS4234 and CS4247. I need to finish CS4234 before I start CS3247. Finishing as soon as possible matters most to me. I'd prefer CS4234 and CS4230 in different semesters. CS3230 must come before CS2105. Oh, and CS3230, CS4230 and CS2105 too. If possible, I would like CS4234 in semester 7. My limit is 16 MC each semester. CS3230 has to be in semester 6. I need to finish CS2105 before I start CS3230. How should I arrange my remaining semesters?
- **q2-S4-214** (q2/near_miss_rule_conflict, scattered, gold `PLAN`): I've done CS2040S, CS2030S, MA1522, CS2100, ES2660, CS2103T and CS2101. CS3230 must come before CS2105. If possible, keep CS4234 and CS4230 apart. Modules I still need: CS3230 and CS4247. Please use the fewest semesters. Ideally CS4234 would be in Y4S1. CS3247 must come before CS4234. Sorry, other way round: CS4234 must come before CS3247. CS3230 has to be in semester 6. Oh, and CS4230, CS3247, CS2105 and CS4234 too. This semester is year 2 semester 2 for me. Also already done: CS1101S, ST2334, MA1521, IS1108 and CS1231S. I can take at most 16 MC per semester. Please plan my remaining semesters.
- **q2-S4-220** (q2_infeasible/rule_conflict, unsupported, gold `NO_PLAN`): I'm a BComp Computer Science Honours student. So far I have passed CS1101S, ES2660, CS1231S and MA1521. I am in semester 2 now. I still have to take CS2102, CS3282, CS2030S and CS3247. Please use the fewest semesters. CS3247 must come before CS2102. I have to take CS3282 and CS2102 together in one semester. CS3282 and CS2102 must not be in the same semester. I'd rather do CS3282 before CS2030S. If possible, I would like CS2030S in semester 6. Ideally I'd take CS3247 before CS2102. I'd like my final semester to be lighter than the others. I would like CS2030S and CS2102 together in one semester. Please plan my remaining semesters.
- **q2-S4-236** (q2/near_miss_rule_conflict, unsupported, gold `PLAN`): I'm a BComp Computer Science Honours student. I have completed CS4225, CS2100, CS3210, CS1231S, CS1101S, CS2103T, MA1521, CS3230, CS2101, CS2030S, ES2660, CS2109S, CS2102, CS2105, CS3219, CS2106, IS1108, CS2040S and MA1522. I'm starting year 4 semester 1. I must take CS3235, CS4243, CS3281 and ST2334. I can take at most 16 MC per semester. I want the fewest total credits. I don't want one semester much heavier than another. CS4243 has to be in semester 8. I have to take CS3235 and ST2334 together in one semester. If possible, I would like CS3235 in semester 7. I'd prefer CS3281 and CS3235 in different semesters. I would like CS3281 as late as possible. If you can, put CS3235 as late as possible. How should I arrange my remaining semesters?
- **q2-S4-261** (q2_infeasible/hidden, plain, gold `NO_PLAN`): I have not completed any module yet. I am in Y1S1 now. My remaining required modules are CS3268, CS2040S and CS4277. CS4277 must come before CS3268. I must take CS2040S in Y1S1. If possible, I would like CS3268 in semester 7. I would like CS4277 as late as possible. What should my plan look like?
- **q2-S4-262** (q2/near_miss_hidden, plain, gold `PLAN`): I have not completed any module yet. I'm starting Y1S1. I still have to take CS2040S, CS3268 and CS4277. CS4277 must come before CS3268. I must take CS2040S in year 1 semester 2. If possible, I would like CS3268 in semester 7. I would like CS4277 as late as possible. Please plan my remaining semesters.
- **q2-S4-276** (q2_infeasible/hidden, unsupported, gold `NO_PLAN`): My completed modules are CS2106, ST2334, CS2040S, ES2660, MA1521, CS2109S, CS3264, CS1231S, IS1108, MA1522, CS2101, CS2030S, CS2100, CS1101S, CS3230 and CS2103T. I am currently in Y3S1. I still have to take CS3234, CS4224, CS3281, CS4211, CS3219, CS2102 and CS2105. I can take at most 12 MC per semester. I will do NOC in semester 8. I want the fewest total credits. CS3219 has to be in semester 7. I need to finish CS2102 before I start CS4211. CS4224 has to be in semester 5. Ideally I'd take CS3281 before CS2105. I'd rather do CS2105 before CS3219. Ideally CS4224 would be in Y4S1. I'm also applying to have one module waived. If you can, put CS4224 as late as possible. Please plan my remaining semesters.
- **q2-S4-287** (q2_infeasible/hidden, scattered, gold `NO_PLAN`): I've done MA1521, CS1231S, CS1101S, MA1522, CS3219, ES2660, CS2030S, CS2040S, ST2334, CS4243, CS2109S and CS2102. Please keep my total MC as low as possible. Modules I still need: CS3210. I almost forgot CS3235, I need that as well. I would like CS3210 as early as possible. Oh, I forgot to say I also completed CS3213, CS2103T, CS3230, CS2100, IS1108, CS2106, CS2105 and CS2101. I can take at most 16 MC per semester. CS4211 has to be in semester 7. I must take CS3235 in year 4 semester 1. I would like CS3235 as late as possible. If possible, I would like CS3210 in semester 7. Ideally I'd take CS4211 before CS4247. I'm in year 3 semester 2 now. Wait, sorry, I'm actually in semester 7. Can you plan the rest of my degree?
- **q2-S4-288** (q2/near_miss_hidden, scattered, gold `PLAN`): I've done CS2103T, CS1231S, CS2101 and CS3230. CS4211 has to be in semester 7. I'm starting year 4 semester 1. I can take at most 20 MC per semester. No wait, make that 16 MC. I would like CS3210 as early as possible. I would like CS3235 as late as possible. I want the fewest total credits. If possible, I would like CS3210 in semester 7. Oh, I forgot to say I also completed CS2030S, ST2334, CS2109S, CS2105, CS2040S, ES2660, CS2100, CS1101S, CS3219, MA1521, MA1522, CS3213, CS2102, CS4243, CS2106 and IS1108. I must take CS3235 in Y4S2. I need to take CS3210. Ideally I'd take CS4211 before CS4247. Oh, and CS3235 too. How should I arrange my remaining semesters?
- **q2-S4-296** (q2/near_miss_hidden, unsupported, gold `PLAN`): I've finished CS2103T, CS2030S, CS2100, CS2040S, CS1231S, ST2334, CS2101, CS3230, MA1521, CS1101S, IS1108, CS4226, MA1522, ES2660, CS2109S, CS2106, CS2105 and CS3219. I'm starting Y3S2. I need to take CS4261, CS3281, CS4225, CS4221 and CS2102. Finishing as soon as possible matters most to me. CS2102 has to be in semester 6. CS4221 has to be in semester 8. Ideally CS4261 and CS4221 go in the same semester. There's a chance I fail one module this semester and have to retake it. If you can, put CS4225 as late as possible. How should I arrange my remaining semesters?
- **q2-S5-001** (q2/S5, plain, gold `PLAN`): I'm a BComp Computer Science Honours student. I have not completed any module yet. I am in Y1S1 now. I need to take IS1108 and CS4262. At most 3 modules per semester. Semester 7 is my exchange semester. I must take CS3244 in year 3 semester 1. I need to finish CS4262 before I start IS1108. Ideally CS3244 and CS4262 go in the same semester. I would like IS1108 as early as possible. I would like CS4262 as late as possible. Please plan my remaining semesters.
- **q2-S5-002** (q2/S5, scattered, gold `PLAN`): I have not completed any module yet. I can take at most 16 MC per semester. No wait, make that 12 MC. Modules I still need: IS1108. Semester 7 is my exchange semester. I'm a BComp Computer Science Honours student. If you can, put CS4262 as late as possible. I would like CS3244 and CS4262 together in one semester. Oh, and CS4262 too. I need to finish CS4262 before I start IS1108. I would like IS1108 as early as possible. This semester is semester 1 for me. CS3244 has to be in semester 5. How should I arrange my remaining semesters?
- **q2-S5-003** (q2/S5, unsupported, gold `PLAN`): I am a Computer Science (BComp CS Hons) student. I have not completed any module yet. I am currently in semester 1. I must take IS1108 and CS4262. I can take at most 12 MC per semester. Semester 7 is my exchange semester. I don't want one semester much heavier than another. I must take CS3244 in year 3 semester 1. CS4262 must come before IS1108. I would like CS3244 and CS4262 together in one semester. My friend and I want to take our modules together where possible. I would like IS1108 as early as possible. If you can, put CS4262 as late as possible. Please plan my remaining semesters.
- **q2-S6-001** (missing_info/current_sem, plain, gold `MISSING_INFO`): I am a Computer Science (BComp CS Hons) student. I have not completed any module yet. My remaining required modules are CS3268 and ST2334. Semester 5 is my exchange semester. CS4220 has to be in semester 8. ST2334 and CS3268 must not be in the same semester. I'd rather do CS4220 before ST2334. ST2334 as early as possible, please. I would like CS3268 as early as possible. What should my plan look like?
- **q2-S6-002** (missing_info/current_sem, unsupported, gold `MISSING_INFO`): I'm a BComp Computer Science Honours student. My completed modules are CS1101S, MA1521, CS1231S and ES2660. I must take CS2101, CS2102, CS3247 and CS2106. Please use the fewest semesters. CS2106 must come before CS2101. CS3247 and CS2106 must not be in the same semester. I definitely can't have CS2101 and CS2102 together. Please keep my workload roughly the same every semester. If possible, I would like CS2106 in semester 6. Ideally CS2101 and CS3247 go in the same semester. I would like CS2102 as early as possible. I would like CS2106 as late as possible. How should I arrange my remaining semesters?
- **q2-S6-011** (missing_info/must_take, plain, gold `MISSING_INFO`): So far I have passed CS2109S, CS2106, MA1522, CS1101S, ES2660, CS3230, CS2040S, CS2101, CS4215, CS2103T, CS2030S, CS2100, ST2334, MA1521 and CS1231S. I am in year 3 semester 1 now. At most 4 modules per semester. Please plan my remaining semesters.
- **q2-S6-013** (missing_info/must_take, scattered, gold `MISSING_INFO`): I've done CS2100, CS2030S, CS2106, IS1108, MA1522, CS3237, CS1231S, ES2660, ST2334, CS2109S, CS1101S, CS3230, MA1521 and CS2105. Please keep my total MC as low as possible. My limit is 16 MC each semester. I'm in year 3 semester 2 now. Wait, sorry, I'm actually in year 4 semester 1. Also already done: CS3219, CS2102, CS2101, CS2040S and CS2103T. Can you plan the rest of my degree?
- **q2-S6-021** (missing_info/completed, plain, gold `MISSING_INFO`): I'm a BComp Computer Science Honours student. This semester is semester 3 for me. I must take CS2101, ST2334, CS4236, CS2109S, CS4240 and CS4212. I have to take CS4240 and CS2101 together in one semester. CS4212 and CS2101 must not be in the same semester. If possible, I would like CS4236 in semester 7. I would like CS4212 as early as possible. If you can, put CS4236 as late as possible. Can you plan the rest of my degree?
- **q2-S6-023** (missing_info/completed, scattered, gold `MISSING_INFO`): I must take CS3242 in year 4 semester 2. I must take CS4278 in year 3 semester 1. CS2102 and CS2105 must not be in the same semester. My limit is 16 MC each semester. If you can, put CS2105 as late as possible. I need to take CS2105 and CS4224. Actually, scratch CS4224, I've decided not to take it. I'd rather do CS4278 before CS2105. I want the fewest total credits. CS2102 has to be in semester 5. I am currently in semester 5. Oh, and CS2102 too. Please plan my remaining semesters.
- **q2-S6-031** (out_of_scope/other programme, plain, gold `OUT_OF_SCOPE`): I am a Business Analytics student. I have not completed any module yet. I'm starting Y1S1. My remaining required modules are CS4248 and CS3230. My limit is 16 MC each semester. I have to take CS4248 and CS3230 together in one semester. I must take CS3219 in semester 5. If possible, I would like CS3230 in semester 5. Ideally I'd take CS3230 before CS3219. I would like CS4248 as early as possible. What should my plan look like?
- **q2-S6-035** (out_of_scope/other programme, unsupported, gold `OUT_OF_SCOPE`): My programme is Data Science and Analytics. So far I have passed ES2660, CS2040S, CS1101S, CS2030S, MA1521, CS1231S and MA1522. This semester is Y2S1 for me. I still have to take CS3219 and CS4211. I want at most two modules with final exams in a semester. Please use the fewest semesters. I definitely can't have CS4211 and CS3219 together. I must take CS4211 in year 3 semester 1. CS4246 has to be in semester 5. Ideally CS3219 would be in Y2S2. Ideally I'd take CS4246 before CS3219. If possible, keep CS4211 and CS4246 apart. If you can, put CS3219 as late as possible. What should my plan look like?
- **q2-S6-036** (out_of_scope/second major, scattered, gold `OUT_OF_SCOPE`): I've done CS2040S, CS2030S, ES2660, CS1101S, IS1108, MA1521 and CS1231S. Also already done: MA1522. I'd rather do CS2105 before CS4236. I'm in year 2 semester 2 now. Wait, sorry, I'm actually in year 2 semester 1. Ideally I'd take CS4236 before CS3234. I must take CS3230 in semester 3. I'd prefer CS2105 and CS3234 in different semesters. I need to take CS3219. I will do NOC in semester 6. I almost forgot CS4236, CS2106 and CS2105, I need those as well. I study CS and I also have a second major in Mathematics. CS3234 has to be in semester 4. Please plan my remaining semesters.
- **q2-S6-037** (out_of_scope/second major, plain, gold `OUT_OF_SCOPE`): I'm a Computer Science student doing a second major in Statistics. So far I have passed CS2100, CS2030S, CS1101S, MA1522, CS1231S, MA1521, CS2040S, CS2103T, IS1108, ES2660, ST2334 and CS2101. I'm starting Y2S2. My remaining required modules are CS4222, CS3230, CS4240, CS2109S, CS3219 and CS2102. My limit is 16 MC each semester. Finishing as soon as possible matters most to me. CS4222 must come before CS3219. CS3219 must come before CS2109S. CS2102 and CS2109S must not be in the same semester. Ideally I'd take CS2102 before CS4240. Ideally I'd take CS4222 before CS4240. CS3230 as early as possible, please. I would like CS3219 as late as possible. How should I arrange my remaining semesters?
- **q2-S6-041** (out_of_scope/minor, plain, gold `OUT_OF_SCOPE`): I'm a CS student taking a minor in Economics. So far I have passed CS2040S, MA1521, CS2030S, CS4268, CS1231S, CS2101, CS2103T, IS1108, CS3230, CS2106, CS1101S, CS2100, MA1522, ST2334 and CS2109S. I am in semester 5 now. My remaining required modules are CS2105, CS2102, CS3282, ES2660, CS4224 and CS3219. My limit is 16 MC each semester. I have to take CS3282 and CS3219 together in one semester. CS2105 must come before CS4224. Ideally I'd take ES2660 before CS2105. I would like CS3219 as late as possible. I would like CS2102 as late as possible. Can you plan the rest of my degree?
- **q2-S6-042** (out_of_scope/minor, scattered, gold `OUT_OF_SCOPE`): I've done CS2105, CS1231S, ST2334, CS2040S, CS2030S and CS3230. I definitely can't have CS4223 and CS2102 together. Ideally CS2101 and CS3211 go in the same semester. Finishing as soon as possible matters most to me. Ideally I'd take CS4218 before CS3211. I must take CS3211 in semester 8. I need to take CS4278, CS2102, CS2101 and CS4218. I'm in semester 5 now. Wait, sorry, I'm actually in year 3 semester 2. I would like CS4218 and CS4223 together in one semester. I'm a CS student taking a minor in Mathematics. I'd prefer CS3231 and CS3211 in different semesters. I definitely can't have CS2102 and CS2101 together. Oh, I forgot to say I also completed ES2660, MA1522, CS2100, CS2109S, CS1101S, IS1108, MA1521, CS2103T, CS2106 and CS3219. Oh, and CS4248, CS3231, CS4223 and CS4268 too. Can you plan the rest of my degree?
- **q2-S6-045** (out_of_scope/minor, unsupported, gold `OUT_OF_SCOPE`): I'm a CS student taking a minor in Statistics. I have not completed any module yet. I am in year 1 semester 1 now. My remaining required modules are ES2660 and CS4246. At most 3 modules per semester. Finishing as soon as possible matters most to me. I definitely can't have ES2660 and CS4246 together. I must take ES2660 in year 3 semester 1. CS4262 has to be in semester 4. I'd rather do CS4262 before ES2660. I'd rather do CS4262 before CS4246. If possible, I would like CS4246 in semester 8. I want at most two modules with final exams in a semester. CS4246 as early as possible, please. Please plan my remaining semesters.
- **q2-S6-046** (out_of_scope/course not in catalogue, plain, gold `OUT_OF_SCOPE`): I'm a BComp Computer Science Honours student. I have not completed any module yet. This semester is semester 1 for me. I must take IS1108, MA1521, CS5340, CS4215 and CS3219. I can take at most 16 MC per semester. I need to finish IS1108 before I start MA1521. I have to take MA1521 and CS3219 together in one semester. If possible, I would like CS3219 in semester 4. I would like MA1521 as early as possible. I would like CS4215 as late as possible. How should I arrange my remaining semesters?
- **q2-S6-050** (out_of_scope/course not in catalogue, unsupported, gold `OUT_OF_SCOPE`): I'm a BComp Computer Science Honours student. So far I have passed MA1522, CS1231S, CS1101S, IS1108, ES2660, MA1521, CS2040S and CS2030S. This semester is semester 3 for me. My remaining required modules are CS4223, CS2109S, LAJ1201, CS2106 and CS4240. I want to graduate as early as possible. CS2106 and CS4240 must not be in the same semester. I must take CS4240 in semester 6. I must take CS2106 in semester 5. If possible, I would like CS2109S in semester 4. Ideally I'd take CS4240 before CS4223. I'd rather not have classes on Fridays. If you can, put CS2109S as late as possible. I would like CS4223 as late as possible. What should my plan look like?
- **q2-S6-051** (out_of_scope/semester above 8, plain, gold `OUT_OF_SCOPE`): I'm a BComp Computer Science Honours student. My completed modules are CS2100, IS1108, CS2040S, CS3230, ES2660, CS2102, CS1101S, ST2334, CS3227, CS2030S, CS2105, CS1231S, CS3219, CS4226, CS4231, CS2103T, MA1522, CS3213, CS2109S, MA1521 and CS2106. I'm currently in semester 9. I need to take CS2101, CS4225, CS4248 and CS4215. My limit is 16 MC each semester. Can you plan the rest of my degree?
- **q2-S6-056** (out_of_scope/semester 0, unsupported, gold `OUT_OF_SCOPE`): I have not completed any module yet. I am in semester 0 right now, before my first semester. My remaining required modules are CS4236, CS3230, CS3242, CS2101, ST2334, CS2106, CS2105 and CS3235. I'm also applying to have one module waived. At most 4 modules per semester. Can the last semester be a lighter one? Can you plan the rest of my degree?
- **q2-S6-057** (out_of_scope/semester 0, plain, gold `OUT_OF_SCOPE`): I have not completed any module yet. I am in semester 0 right now, before my first semester. I need to take CS4262 and CS2040S. I can take at most 12 MC per semester. Finishing as soon as possible matters most to me. Can you plan the rest of my degree?
- **q2-S6-059** (out_of_scope/semester 0, scattered, gold `OUT_OF_SCOPE`): I have not completed any module yet. I am in semester 0 right now, before my first semester. I need to take CS4246 and CS4239. Actually, scratch CS4239, I've decided not to take it. Oh, and IS1108 too. Please plan my remaining semesters.
