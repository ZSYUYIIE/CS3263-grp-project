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

**q1-eligible-01**: I've finished CS2030S, MA1522, ST2334, CS2101, CS2103T, MA1521, CS1231S, CS1101S, CS2100 and CS2040S. I am in year 2 semester 1 now. Can I take CS2102 next semester?

Gold status: `ELIGIBLE`

**q1-missing_prereq-01**: I've finished ES2660, CS1231S, ST2334, MA1521, MA1522, CS2030S, CS2100, CS1101S, CS2101, IS1108, CS2040S and CS2103T. Can I take CS3264 in year 2 semester 2?

Gold status: `NOT_ELIGIBLE`

**q1-wrong_term-01**: So far I have passed IS1108, CS3230, MA1522, CS2030S, CS2100, MA1521, CS2106, CS2101, CS1101S, ST2334, CS1231S, CS2109S, CS2103T and CS2040S. I am in year 2 semester 2 now. Can I take CS3236 next semester?

Gold status: `NOT_ELIGIBLE`

**q1-precluded-01**: I have completed CS2103T, CS2101, CS2030S, CS2102, CS1231S, ES2660, MA1521, ST2334, CS3264, CS2106, CS2100, CS3219, CS1101S, CS2109S, CS2040S, MA1522 and IS1108. I am in semester 7 now. Can I take CS3244 next semester?

Gold status: `NOT_ELIGIBLE`

**q1-already_done-01**: I've finished MA1521, CS2030S, CS2100, CS2106, CS2040S, IS1108, CS3219, CS2102, ST2334, CS2103T, CS3230, ES2660, CS2109S, CS1231S, CS2101, CS2105, CS1101S and MA1522. I am in year 3 semester 2 now. Can I take CS2030S next semester?

Gold status: `NOT_ELIGIBLE`

**q1-closed-01**: I have completed CS2040S, CS2100, CS1101S, CS2030S, CS1231S, CS2103T, MA1521, ST2334, ES2660, IS1108, CS2101 and MA1522. I am in semester 3 now. Can I take CS2109HS next semester?

Gold status: `NOT_ELIGIBLE`

**q2-loose-01**: I am a Computer Science (BComp CS Hons) student. I've finished MA1521, CS2103T, CS2101, ES2660, IS1108, CS2030S, CS1101S, ST2334, MA1522, CS1231S, CS2040S and CS2100. I am in year 2 semester 2 now. I need to take CS3219, CS2109S, CS2105, CS3236 and CS3230. At most 5 modules per semester. I want the fewest total credits. Please plan my remaining semesters.

Gold status: `PLAN`

**q2-tight-01**: So far I have passed IS1108, MA1522, CS1231S, MA1521, CS2030S, CS2040S and CS1101S. I am currently in year 2 semester 1. I still have to take CS3264, CS3230, CS2106, CS4224, ST2334, CS2109S, CS2102 and CS4330. I can take at most 8 MC per semester. I want the fewest total credits. I'd prefer CS2106 and CS4224 in different semesters. What should my plan look like?

Gold status: `PLAN`

**q2_infeasible-exclusion-01**: I have completed CS1231S, CS2109S, CS2030S, CS2040S, CS2103T, CS2101, ST2334, CS2100, CS1101S, IS1108, MA1521, CS2106, MA1522, CS3264 and ES2660. I'm starting Y3S1. I need to take CS3281, CS2105, CS3240, CS3231, CS2102, CS3244 and CS3219. Please plan my remaining semesters.

Gold status: `NO_PLAN`

**q2_infeasible-chain-01**: I've finished CS1101S, CS2100, MA1522, CS2030S, ES2660, CS2040S, CS3219, CS2101, CS2103T, MA1521, IS1108, CS2102, CS3230, CS2105, ST2334 and CS1231S. I'm starting year 4 semester 2. I must take CS3263 and CS3264. Please plan my remaining semesters.

Gold status: `NO_PLAN`

**q2_infeasible-capacity-01**: I've finished IS1108, CS2100, CS2101, ST2334, CS2030S, CS1231S, CS2106, CS3230, CS1101S, CS2109S, ES2660, MA1522, CS2103T, CS2040S and MA1521. I'm starting Y3S1. I must take CS4261, CS4278, CS2105, CS2102, CS3219 and CS4350. I can take at most 4 MC per semester. Please use the fewest semesters. Can you plan the rest of my degree?

Gold status: `NO_PLAN`

**q2_infeasible-parity-01**: So far I have passed CS2030S, CS2109S, IS1108, ST2334, CS1231S, CS2040S, CS2100, CS2103T, CS2101, CS2106, CS2102, ES2660, CS3230, CS2105, MA1522, CS3219, MA1521 and CS1101S. I am in year 4 semester 2 now. I still have to take CS4230 and CS4226. What should my plan look like?

Gold status: `NO_PLAN`

**q2_infeasible-rule_conflict-01**: I have completed CS2040S, ES2660, CS2106, CS3219, CS1101S, CS1231S, MA1521, CS2100, CS2101, CS2109S, CS2030S, CS2103T, CS3230, CS2105 and MA1522. I'm starting semester 6. I need to take CS3233, ST2334, CS3264, CS3268 and IS1108. At most 2 modules per semester. I want to graduate as early as possible. CS3264 must come before ST2334. ST2334 must come before CS3264. Please plan my remaining semesters.

Gold status: `NO_PLAN`

**q2_infeasible-hidden-01**: I've finished CS2040S, MA1521, CS2101, IS1108, CS1231S, CS2103T, MA1522, CS1101S, ST2334, CS2100, CS2030S and ES2660. I'm starting year 2 semester 2. I still have to take CS3247, CS4236, CS2102, CS4243, CS2106 and CS3230. CS4236 has to be in semester 4. Can you plan the rest of my degree?

Gold status: `NO_PLAN`

**missing_info-q1-01**: I am in semester 5 now. Can I take CS4246 next semester?

Gold status: `MISSING_INFO`

**missing_info-q2-01**: I have completed CS2030S, MA1522, CS2109S, CS3230, ST2334, CS2101, CS2103T, CS1231S, IS1108, ES2660, CS2040S, CS1101S, CS2100, MA1521 and CS2106. I still have to take CS3263 and CS2102. Semester 7 is my exchange semester. I want to graduate as early as possible. Please spread the workload evenly. I would like CS2102 as early as possible. Can you plan the rest of my degree? I might fail CS2106, so keep that in mind.

Gold status: `MISSING_INFO`

**out_of_scope-programme-01**: I am doing BComp CS Hons with a minor in Economics. I've finished CS2101, CS2109S, CS2105, CS3230, CS2100, CS2040S, CS2030S, CS3219, CS2106, ES2660, MA1522, ST2334, CS2103T, MA1521, CS1101S, CS1231S and IS1108. I am in year 3 semester 1 now. Can I take CS3233 next semester?

Gold status: `OUT_OF_SCOPE`

**out_of_scope-course-01**: I have completed ST2334, CS2103T, CS2100, MA1522, CS3230, CS2102, CS2040S, CS2109S, IS1108, CS1231S, CS2106, ES2660, CS2030S, MA1521, CS3219, CS1101S, CS2101 and CS2105. I am in Y4S1 now. Can I take CS5242 next semester?

Gold status: `OUT_OF_SCOPE`
