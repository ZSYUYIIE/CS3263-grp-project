# Instance set (seed 3263)

115 instances. Regenerate with `python -m instances.generate --seed 3263`.

| Kind | Count |
|---|---|
| q1/eligible | 12 |
| q1/missing_prereq | 8 |
| q1/wrong_term | 4 |
| q1/precluded | 3 |
| q1/already_done | 2 |
| q1/closed | 1 |
| q2/loose | 25 |
| q2/tight | 20 |
| q2_infeasible/exclusion | 4 |
| q2_infeasible/chain | 4 |
| q2_infeasible/capacity | 4 |
| q2_infeasible/parity | 4 |
| q2_infeasible/rule_conflict | 4 |
| q2_infeasible/hidden | 4 |
| missing_info/q1 | 3 |
| missing_info/q2 | 4 |
| out_of_scope/programme | 6 |
| out_of_scope/course | 3 |

| Group | Gold status | Count |
|---|---|---|
| missing_info | MISSING_INFO | 7 |
| out_of_scope | OUT_OF_SCOPE | 9 |
| q1 | ELIGIBLE | 12 |
| q1 | NOT_ELIGIBLE | 18 |
| q2 | PLAN | 45 |
| q2_infeasible | NO_PLAN | 24 |

## Examples

- **q1-eligible-01** (gold status `ELIGIBLE`): I've finished CS2030S, MA1522, ST2334, CS2101, CS2103T, MA1521, CS1231S, CS1101S, CS2100 and CS2040S. I am in year 2 semester 1 now. Can I take CS2102 next semester?
- **q1-missing_prereq-01** (gold status `NOT_ELIGIBLE`): I've finished ES2660, CS1231S, ST2334, MA1521, MA1522, CS2030S, CS2100, CS1101S, CS2101, IS1108, CS2040S and CS2103T. Can I take CS3264 in year 2 semester 2?
- **q1-wrong_term-01** (gold status `NOT_ELIGIBLE`): So far I have passed IS1108, CS3230, MA1522, CS2030S, CS2100, MA1521, CS2106, CS2101, CS1101S, ST2334, CS1231S, CS2109S, CS2103T and CS2040S. I am in year 2 semester 2 now. Can I take CS3236 next semester?
- **q1-precluded-01** (gold status `NOT_ELIGIBLE`): I have completed CS2103T, CS2101, CS2030S, CS2102, CS1231S, ES2660, MA1521, ST2334, CS3264, CS2106, CS2100, CS3219, CS1101S, CS2109S, CS2040S, MA1522 and IS1108. I am in semester 7 now. Can I take CS3244 next semester?
- **q1-already_done-01** (gold status `NOT_ELIGIBLE`): I've finished MA1521, CS2030S, CS2100, CS2106, CS2040S, IS1108, CS3219, CS2102, ST2334, CS2103T, CS3230, ES2660, CS2109S, CS1231S, CS2101, CS2105, CS1101S and MA1522. I am in year 3 semester 2 now. Can I take CS2030S next semester?
- **q1-closed-01** (gold status `NOT_ELIGIBLE`): I have completed CS2040S, CS2100, CS1101S, CS2030S, CS1231S, CS2103T, MA1521, ST2334, ES2660, IS1108, CS2101 and MA1522. I am in semester 3 now. Can I take CS2109HS next semester?
- **q2-loose-01** (gold status `PLAN`): So far I have passed CS2103T, CS2030S, MA1521, CS2101, IS1108, ES2660, CS1101S, CS2040S, CS2100, MA1522, CS1231S and ST2334. I am currently in year 2 semester 2. I need to take CS3230, CS3236, CS2109S, CS3219 and CS2105. At most 5 modules per semester. I want the fewest total credits. Can you plan the rest of my degree?
- **q2-tight-01** (gold status `PLAN`): So far I have passed MA1521, CS2101, CS2030S, MA1522, CS2106, CS2100, CS2109S, IS1108, CS3219, CS3230, CS1101S, CS1231S, CS2105, CS2103T, CS2040S, ST2334 and ES2660. I am currently in semester 6. I need to take CS2102, CS4430, CS4243, CS4223 and CS4222. I can take at most 12 MC per semester. I would like CS4222 as early as possible. Ideally I'd take CS4243 before CS4222. What should my plan look like?
- **q2_infeasible-exclusion-01** (gold status `NO_PLAN`): So far I have passed ES2660, CS2101, CS2040S, CS1101S, MA1521, CS1231S, MA1522, CS3243, CS2100, ST2334, IS1108, CS2030S and CS2103T. I am currently in Y2S2. I must take CS2106, CS3263, CS3219, CS4278, CS3103 and CS2109S. Please use the fewest semesters. What should my plan look like?
- **q2_infeasible-chain-01** (gold status `NO_PLAN`): So far I have passed IS1108, MA1522, CS2101, CS1101S, ES2660, ST2334, CS2105, CS3230, CS2040S, CS3219, CS1231S, CS2102, MA1521, CS2100, CS2103T and CS2030S. I am currently in semester 8. I still have to take CS4243 and CS3264. Please use the fewest semesters. Please plan my remaining semesters.
- **q2_infeasible-capacity-01** (gold status `NO_PLAN`): I have completed CS2101, CS1231S, CS1101S, ES2660, CS3230, IS1108, MA1521, CS2105, CS2109S, CS2103T, ST2334, CS3219, MA1522, CS2040S, CS2106, CS2100 and CS2030S. I am currently in year 3 semester 2. I still have to take CS4330, CS4262, CS4238, CS4240 and CS2102. I can take at most 4 MC per semester. Please use the fewest semesters. Can you plan the rest of my degree?
- **q2_infeasible-parity-01** (gold status `NO_PLAN`): I've finished CS1101S, MA1521, CS2100, CS3219, CS2102, ST2334, CS2103T, CS2106, CS2040S, CS2109S, CS1231S, CS2105, CS3230, MA1522, CS2101, IS1108, CS2030S and ES2660. I'm starting year 4 semester 2. I need to take CS4330 and CS3237. Can you plan the rest of my degree?
- **q2_infeasible-rule_conflict-01** (gold status `NO_PLAN`): I have completed IS1108, MA1521, ST2334, CS2103T, CS2109S, CS1231S, CS2040S, CS2101, CS1101S, CS2106, ES2660, MA1522, CS2100, CS2030S and CS3230. I am in year 3 semester 1 now. I still have to take CS4330, CS4262 and CS3219. At most 2 modules per semester. CS4330 must come before CS3219. CS3219 must come before CS4330. What should my plan look like?
- **q2_infeasible-hidden-01** (gold status `NO_PLAN`): I have completed CS1231S, ES2660, IS1108, MA1522, CS2100, ST2334, MA1521, CS2101, CS2030S, CS1101S, CS2103T and CS2040S. I am currently in semester 4. I need to take CS2102, CS3230, CS4212, CS4248, CS2106, CS2109S, CS3219 and CS2105. CS4248 has to be in semester 4. What should my plan look like?
- **missing_info-q1-01** (gold status `MISSING_INFO`): I am in year 1 semester 2 now. Can I take CS3210 next semester?
- **missing_info-q2-01** (gold status `MISSING_INFO`): I am in Y2S2 now. I need to take CS3219, CS4226, CS2102, CS3235, CS4263 and CS3230. I can take at most 16 MC per semester. I want the fewest total credits. I would like CS3230 as late as possible. Can you plan the rest of my degree? I'd prefer modules with no final exam.
- **out_of_scope-programme-01** (gold status `OUT_OF_SCOPE`): I am doing BComp CS Hons with a second major in Mathematics. I have completed CS3230, CS2101, CS2106, CS2040S, MA1522, ST2334, MA1521, CS2103T, CS2100, CS2109S, IS1108, CS2030S, CS1231S, ES2660 and CS1101S. I am in semester 4 now. Can I take CS2105 next semester?
- **out_of_scope-course-01** (gold status `OUT_OF_SCOPE`): I have completed CS2100, CS1101S, MA1522, CS1231S, CS2101, ST2334, MA1521, CS2040S, CS2103T, CS2030S and ES2660. I am currently in year 2 semester 2. I still have to take CS3231, CS2106, CS4222, CS3219, CS2105, CS4261, CS3230, IS1108, CS2109S and LAJ1201. I would like CS2105 as early as possible. Please plan my remaining semesters.