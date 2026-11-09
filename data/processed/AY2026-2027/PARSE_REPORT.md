# Parse report, AY2026-2027

Generated 2026-11-09T16:35:46+00:00 from data fetched 2026-11-09T16:34:02+00:00.

## Summary

| Metric | Value |
|---|---|
| courses_total | 795 |
| courses_with_full_details | 393 |
| stubs_not_in_ay | 117 |
| stubs_outside_fetch_scope | 285 |
| available_to_student | 303 |
| with_prereq | 270 |
| with_preclusion | 227 |
| crosscheck_match | 255 |
| crosscheck_mismatch | 37 |
| parse_errors | 0 |
| courses_with_warnings | 20 |
| courses_with_overrides | 0 |

## Cross-check: prerequisiteRule vs NUSMods prereqTree

Both sources are parsed and resolved independently; they should give the same logic.
Matches: 255. Mismatches: 37. Rule but no tree: 13 (BT4101, CG4001, CP3208, CP3209, CP3209R, CP4106, CS2101, CS2101X, EG2401A, ES1000, ES2007D, IS2101, ST1232).

| Course | From prerequisiteRule | From prereqTree | Resolution |
|---|---|---|---|
| BT3017 | ((BT1101 or BT1101HS) and (CS1010J or CS1010E or CS1010S or CS1010X or CS1010 or CS1101S or CS1010A or CS1010HS or UTC2851) and ST2334) or (ST2131 and ST2132 and (MA2001 or MA1522 or MA1311)) | (BT1101 or BT1101HS) and (CS1010J or CS1010E or CS1010S or CS1010X or CS1010 or CS1101S or CS1010A or CS1010HS or UTC2851) and (ST2334 or (ST2131 and ST2132 and (MA2001 or MA1522 or MA1311))) | used prereqTree (ambiguous AND/OR) |
| CS1231 | none | MA1301X or MA1301 | rule has a pre-university-subject alternative that prereqTree drops |
| CS1231S | none | MA1301X or MA1301 | rule has a pre-university-subject alternative that prereqTree drops |
| CS2309 | ((CS1231 or CS1231S or MA1100 or MA1100T) and (CS2030 or CS2030S or CS2030DE or CS2030HS) and (CS2040 or CS2040S or CS2040HS or CS2040C or CS2040DE)) or CS2113 or CS2113T | (CS1231 or CS1231S or MA1100 or MA1100T) and (((CS2030 or CS2030S or CS2030DE or CS2030HS) and (CS2040 or CS2040S or CS2040HS or CS2040C or CS2040DE)) or CS2113 or CS2113T) | used prereqTree (ambiguous AND/OR) |
| CS4240 | CS3240 | CS3240 and (MA1301 or MA1301X) | rule has a pre-university-subject alternative that prereqTree drops |
| DAO1704 | impossible | none | rule has a programme/cohort gate that prereqTree drops |
| DAO2702 | impossible | DAO1704 or DAO1704X or RE1702 | rule has a programme/cohort gate that prereqTree drops |
| DBA4714 | impossible | DAO2702 or DAO2702X | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| DSA1101 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| DSA4213 | impossible | MA2001 and (MA2104 or MA2311) and (CS2040 or CS2040C or CS2040DE or CS2040HS or CS2040S or ST2137) | rule has a programme/cohort gate that prereqTree drops |
| DSE1101 | impossible | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| ES1531 | impossible | none | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| ES2002 | impossible | ES1000 | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| ES2531 | impossible | none | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| ES2631 | impossible | none | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| FAS1101 | impossible | none | rule has a pre-university-subject alternative that prereqTree drops; rule has a programme/cohort gate that prereqTree drops |
| ISE3550 | impossible | 6 of (SE1101E, SE2210, SE2214, SE2217, SE2218, SE2221, SE2224, SE2225, SE2660, SE3211, SE3214, SE3219, SE3220, SE3224, SE3550, SE3551, SE3660, SE3880C, SE4101, SE4218, SE4227, SE4401, SE4401HM, SE4660, SE4660HM, SE5660, SE6660, SE6770, SEA5101, SEA5102, SEA5201, SEA5203, SEA5212, SEA5213, SEA5214, SEA5223, SEA5224, SEA5231, SEA5233, SEA5234, SEA5237, SEA5238, SEA5301A, SEA5301B, SEA5302A, SEA5302B, SEA5401, SEA5660) | rule has a programme/cohort gate that prereqTree drops |
| MA1100 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1100T | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1311 | none | MA1301 or MA1301FC or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1312 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1505 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1508E | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1511 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1512 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1513 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1521 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1522 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA1531 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA2001 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA2002 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MA2301 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| MNO2706 | impossible | none | rule has a programme/cohort gate that prereqTree drops |
| PC1101 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| PC2174A | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |
| SE3550 | impossible | 6 of (SE1101E, SE2210, SE2214, SE2217, SE2218, SE2221, SE2224, SE2225, SE2660, SE3211, SE3214, SE3219, SE3220, SE3224, SE3551, SE3660, SE3880C, SE4101, SE4218, SE4227, SE4401, SE4401HM, SE4660, SE4660HM, SE5660, SE6660, SE6770, SEA5101, SEA5102, SEA5201, SEA5203, SEA5212, SEA5213, SEA5214, SEA5223, SEA5224, SEA5231, SEA5233, SEA5234, SEA5237, SEA5238, SEA5301A, SEA5301B, SEA5302A, SEA5302B, SEA5401, SEA5660) | rule has a programme/cohort gate that prereqTree drops |
| ST1131 | none | MA1301 or MA1301X | rule has a pre-university-subject alternative that prereqTree drops |

## Parse errors

None.

## Not available to this student

- AI5205 (Ethics, Governance, and Compliance in AI and Emerging Technologies): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- BN1111 (Biomedical Engineering Principles and Practice I): not offered in any semester in AY2026-2027
- BSP1703X (Managerial Economics): not offered in any semester in AY2026-2027
- CE2407 (Engineering & Uncertainty Analyses): not offered in any semester in AY2026-2027
- CG4001 (B. Eng. Dissertation): prerequisite can never be met by this student (programme/cohort gate)
- CG4003 (Advanced Project and Internship): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- CN3421 (Process Modeling And Numerical Simulation): not offered in any semester in AY2026-2027
- CS1010J (Programming Methodology): not offered in any semester in AY2026-2027
- CS1010XCP (Programming Methodology): not offered in any semester in AY2026-2027
- CS2030HS (Programming Methodology II): not open to PROGRAMS 0300CSHON
- CS2040HS (Data Structures and Algorithms): not open to PROGRAMS 0300CSHON
- CS2100R (Computer Organisation): not offered in any semester in AY2026-2027
- CS2101X (Effective Communication for Computing Professionals): prerequisite can never be met by this student (programme/cohort gate)
- CS2109HS (Introduction to AI and Machine Learning): not open to PROGRAMS 0300CSHON
- CS2113T (Software Engineering & Object-Oriented Programming): not offered in any semester in AY2026-2027
- CS3220 (Computer Architecture): not offered in any semester in AY2026-2027
- CS3225 (Combinatorial Methods in Bioinformatics): not offered in any semester in AY2026-2027
- CS3226 (Web Programming and Applications): not offered in any semester in AY2026-2027
- DAO1704 (Decision Analytics using Spreadsheets and AI): prerequisite can never be met by this student (programme/cohort gate)
- DAO1704X (Decision Analytics using Spreadsheets and AI): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- DAO2702 (Programming for Business Analytics and AI): prerequisite can never be met by this student (programme/cohort gate)
- DAO2702X (Programming for Business Analytics and AI): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- DBA3711 (Stochastic Models in Management): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- DBA4714 (Deep Learning and Generative AI in Business): prerequisite can never be met by this student (programme/cohort gate)
- DSA4213 (Natural Language Processing for Data Science): prerequisite can never be met by this student (programme/cohort gate)
- DSC3216 (Predictive Analytics in Business): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- DSE1101 (Introductory Data Science for Economics): prerequisite can never be met by this student (programme/cohort gate)
- EC1301 (Principles of Economics): not offered in any semester in AY2026-2027
- EC2101 (Microeconomic Analysis I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- EE1111 (Engineering Principles and Practice I): not offered in any semester in AY2026-2027
- EE2012A (Analytical Methods in Electrical and Computer Engineering): not offered in any semester in AY2026-2027
- EE2020 (Digital Fundamentals): not offered in any semester in AY2026-2027
- EE2024 (Programming for Computer Interfaces): not offered in any semester in AY2026-2027
- EE4001 (B.Eng. Dissertation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- EE4002D (Design Capstone): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- EE4002R (Research Capstone): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- EE4210 (Network Protocols and Applications): not offered in any semester in AY2026-2027
- EE4211 (Data Science for the Internet of Things): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- EE4214 (Real-Time Embedded Systems): not offered in any semester in AY2026-2027
- EE5310 (Communication Networking Fundamentals): not offered in any semester in AY2026-2027
- EE5731 (Visual Computing): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- EE6310 (Communication Networking Fundamentals (Advanced)): not offered in any semester in AY2026-2027
- ES1531 (Critical Thinking And Writing): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- ES2002 (Business Communication for Leaders (BBA)): prerequisite can never be met by this student (programme/cohort gate)
- ES2007D (Professional Communication): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- ES2531 (Critical Thinking And Writing): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- ES2631 (Critique and Communication of Thinking and Design): prerequisite can never be met by this student (programme/cohort gate)
- FAS1101 (Writing Academically: Arts and Social Sciences): prerequisite can never be met by this student (programme/cohort gate)
- GEK1549 (Critical Thinking And Writing): not offered in any semester in AY2026-2027
- GET1021 (Critical Thinking And Writing): not offered in any semester in AY2026-2027
- HS1502 (Conceptual Introduction to Machine Learning): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- HS1503 (Living with AI: Understanding the Technology that’s Changing Everything): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- HS1504 (Ex Machina? The Promises, Problems and Potentials of AI): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- IS1103 (Ethics in Computing): not offered in any semester in AY2026-2027
- IS2103 (Enterprise Systems Server-side Design and Development): not offered in any semester in AY2026-2027
- IS3106 (Enterprise Systems Interface Design and Development): not offered in any semester in AY2026-2027
- IS4240 (Business Intelligence Systems): not offered in any semester in AY2026-2027
- IS4242 (Intelligent Systems and Techniques): not offered in any semester in AY2026-2027
- IS5006 (Human-Centred Intelligent Systems): not offered in any semester in AY2026-2027
- IS5110 (Software Project Management): not offered in any semester in AY2026-2027
- ISE3550 (Extended Internship): prerequisite can never be met by this student (programme/cohort gate)
- ISY5005 (Intelligent Software Agents): not offered in any semester in AY2026-2027
- IT1007 (Introduction to Programming with Python and C): not offered in any semester in AY2026-2027
- IT2002 (Database Technology and Management): not open to PROGRAMS 0300CSHON
- IT3011 (Introduction to Machine Learning and Applications): not offered in any semester in AY2026-2027
- LSM2241 (Introductory Bioinformatics): not offered in any semester in AY2026-2027
- MA1311 (Matrix Algebra): not offered in any semester in AY2026-2027
- MA1312 (Calculus with Applications): not offered in any semester in AY2026-2027
- MA1531 (Calculus for Data Science): not open to PROGRAMS 0300CSHON
- MA2001 (Linear Algebra I): not open to PROGRAMS 0300CSHON
- MA2002 (Calculus): not open to PROGRAMS 0300CSHON
- MA2101 (Linear Algebra II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2101S (Linear Algebra II (S)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2202 (Algebra I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2202S (Algebra I (S)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2213 (Numerical Analysis I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2214 (Combinatorics and Graphs I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2288 (Basic UROPS in Mathematics I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2288R (Basic UROPS in Mathematics I (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2289 (Basic UROPS in Mathematics II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2289R (Basic UROPS in Mathematics II (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2301 (Basic Applied Mathematics): not offered in any semester in AY2026-2027
- MA2310 (FOS Undergraduate Professional Internship Programme 1ST): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2312U (FOS Undergraduate Professional Internship Programme 2S1): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2313 (FOS Undergraduate Professional Internship Programme 2S2): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA2401 (Mathematical Foundations of Data Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3201 (Algebra II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3205 (Set Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3209 (Metric and Topological Spaces): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3210 (Mathematical Analysis II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3211 (Complex Analysis I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3211S (Complex Analysis I (S)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3220 (Ordinary Differential Equations): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3233 (Combinatorics and Graphs II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3236 (Non-Linear Programming): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3238 (Stochastic Processes I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3238S (Stochastic Processes I (S)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3252 (Linear and Network Optimisation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3264 (Mathematical Modelling): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3265 (Introduction to Number Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3288 (Advanced UROPS in Mathematics I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3288R (Advanced UROPS in Mathematics I (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3289 (Advanced UROPS in Mathematics II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3310 (FOS Undergraduate Professional Internship Programme 2ST): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3312 (FOS Undergraduate Professional Internship Programme 3S1): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA3313 (FOS Undergraduate Professional Internship Programme 3S2): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4198 (Mathematics Capstone Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4203 (Galois Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4207 (Mathematical Logic): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4211 (Functional Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4221 (Partial Differential Equations): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4229 (Fourier Analysis and Approximation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4230 (Matrix Computation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4233 (Dynamical Systems): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4235 (Topics in Graph Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4251 (Stochastic Processes II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4254 (Discrete Optimization): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4255 (Numerical Methods in Differential Equations): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4261 (Information and Coding Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4262 (Measure and Integration): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4264 (Game Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4266 (Introduction to Algebraic Topology): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4270 (Data Modelling and Computation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4273 (Algebraic Geometry of Curves and Surfaces): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4275 (Mathematics of Reinforcement Learning): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4276 (Theory of Algebraic Numbers): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4288O (Undergraduate Project in Mathematics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4288P (Undergraduate Project in Mathematics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4310 (FOS Undergraduate Professional Internship Programme 3ST): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4312 (FOS Undergraduate Professional Internship Programme 4S1): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA4313 (FOS Undergraduate Professional Internship Programme 4S2): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5198 (Graduate Seminar Course in Mathematics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5202 (Number Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5204 (Commutative and Homological Algebra): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5205 (Graduate Analysis I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5206 (Graduate Analysis II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5210 (Differentiable Manifolds): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5213 (Advanced Partial Differential Equations): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5216 (Differential Geometry): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5217 (Graduate Complex Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5218 (Representation Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5219 (Logic and Foundation of Mathematics I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5222 (Ergodic Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5232 (Modeling and Numerical Simulations): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5233 (Computational Mathematics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5243 (Advanced Mathematical Programming): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5248 (Stochastic Analysis in Mathematical Finance): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5249 (Stochastic Processes and Algorithms): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5251 (Spectral Methods and Applications): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5252 (Methods of Applied Mathematics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5259 (Introductory Probability): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5260 (Advanced Probability): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5266 (Optimization): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5270 (Game Theory and applications): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5271 (Introduction to Computational Mathematics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5272 (Mathematical Underpinnings of Data Science): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5401 (Graduate Internship in Mathematics I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA5402 (Graduate Internship in Mathematics II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA6202 (Approximate Subgroups): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA6211 (Topics in Geometry and Topology I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA6225 (Topics in Machine Learning): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MA6291 (Topics in Mathematics I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ME1102 (Engineering Principles and Practice I): not offered in any semester in AY2026-2027
- ME2104 (Engineering Principles and Practice II): not offered in any semester in AY2026-2027
- ME2143 (Sensors and Actuators): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- MNO2706 (Business Communication for Leaders (ACC)): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- NM1101E (Communications, New Media and Society): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM1101X (Communications, New Media and Society): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2101 (Theories of Communications and New Media): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2103 (Quantitative Research Methods): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2104 (Qualitative Communication Research Methods): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2105 (Communicative Competence in Action): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2209 (Social Psychology of New Media): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2219 (Principles of Communication Management): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2220 (Introduction to Media Writing): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2223 (Media Law and Policy): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2226 (Introduction to Visual Cultural Analytics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2227 (Understanding Visual Culture): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM2228 (Data Intelligence for Social Applications): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3205 (Digital Media Cultures): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3217 (Principles of Visual Communication Design): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3219 (Writing for Communication Management): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3221 (Mobile Interaction Design): not offered in any semester in AY2026-2027
- NM3230 (Digital Storytelling): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3241 (Cultural Studies: Theory and Practice): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3244 (Consulting as a Communication & Career Skill): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3245 (Managing Arts and Cultural Events): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3246 (Mobile Storytelling for Social Impact): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3247 (Digital Economies): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3248 (Communications, Culture, and Sustainability): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3249 (Digital News Writing and Data Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3250 (Media, City and Public Culture): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3251 (Media Industries in the Global Age): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3252 (Communicating Risk and Crisis in the Digital Age): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3253 (Fandoms to Algorithms: K-Pop, Data and Culture): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3254 (Artificial Intelligence, Algorithms and Governance): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3255 (AI-Mediated Communication): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3550C (CNM Internship Programme): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3550Y (Communications & New Media Internship): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3551 (FASS Undergraduate Research Opportunity (UROP)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM3551R (FASS Undergraduate Research Opportunity (UROP)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4206 (Media Policy and Regulation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4207 (Managing Communication Campaigns): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4208 (Strategic Communication Design): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4212 (Race, Media, and Representation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4230 (Communications for Social Change): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4231 (Digital Media Storytelling Strategies): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4242 (Critical Perspectives on Technology): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4244 (Sex in the Media): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4245 (Political Communication): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4247 (Creative Writing in the Marketplace): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4249 (Media & Audiences): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4255 (Social Media and Computational Communication): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4257 (Multiplatform Advertising Strategies): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4258 (Health Communication): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4259HM (Mobile Interaction Design): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- NM4260HM (Game Design): prerequisite can never be met by this student (programme/cohort gate); not offered in any semester in AY2026-2027
- NM4401 (Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4401HM (Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4660 (Independent Study): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NM4660HM (Independent Study): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2006 (Human Trafficking and Labour Migration): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2008 (Power, Space and Pleasure): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2010 (Sites of Tourism): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2018 (Danger and Security): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2029 (Evolutionary Psychology and Art): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2032 (Identity, Death, and Immortality): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2034 (Wild and Simple: Living and Thinking Sustainably): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2035 (Art and the Attention Economy): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2036 (Space, Place and the Human Experience): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2037 (Absences: Beyond the Edges of the Material World): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2038 (Screening Historical Trauma): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2040 (The Limits of Money): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2041 (The Popularity of Korean Culture): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- NTW2042 (Illusions and Hallucinations: Appearance and Reality): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- PC2134 (Mathematical Mtds in Physics I): not offered in any semester in AY2026-2027
- RB1101 (Fundamentals of Robotics I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- RE1704 (Principles of Real Estate Economics): not offered in any semester in AY2026-2027
- RVX1000 (Citizen Speak: Persuasion and Polarization in Society): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- RVX1001 (Science Fiction and Society): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- RVX1003 (Print to Screen: Analysing Film Adaptation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- RVX1004 (Cultural Expressions of Science, Technology and Warfare): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- RVX1005 (Intersectionality, Identity and Inequality in Asia): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- RVX1006 (Storying Sustainability: Dodos, Condos & Tornadoes): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4101 (Software Analysis and Design): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4101C (Software Analysis and Design): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4104 (Digital Product Management): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4105 (Web Application Development): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4105C (Web Application Development): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4106 (AD Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4107 (Industrial Attachment Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4108 (Mobile Application Development): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4110 (Machine Learning Application Development): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4110C (Machine Learning Application Development): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SA4111 (Agile Software Delivery): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SE3550 (Southeast Asian Studies Internship): prerequisite can never be met by this student (programme/cohort gate)
- SP1541 (Communication Practices in Popular Science): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- SP1541X (Communication Practices in Popular Science): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST1232 (Statistics for Life Sciences): not offered in any semester in AY2026-2027
- ST2288 (Basic UROPS in Statistics and Applied Probability I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST2288R (Basic UROPS in Statistics and Applied Probability I (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST2289 (Basic UROPS in Statistics and Applied Probability II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST2289R (Basic UROPS in Statistics and Applied Probability II (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST2310 (FOS Undergraduate Professional Internship Programme 1ST): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST2312 (FOS Undergraduate Professional Internship Programme 2S1): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST2313 (FOS Undergraduate Professional Internship Programme 2S2): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3232 (Design & Analysis of Experiments): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3236 (Stochastic Processes I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3239 (Survey Methodology): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3244 (Demographic Methods): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3246 (Statistical Models for Actuarial Science): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3247 (Simulation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3288 (Advanced UROPS in Statistics & Applied Probability I): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3288R (Advanced UROPS in Statistics & Applied Probability I (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3289 (Advanced UROPS in Statistics & Applied Probability II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3289R (Advanced UROPS in Statistics & Applied Probability II (REx)): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3310 (FOS Undergraduate Professional Internship Programme 2ST): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3311 (Undergraduate Professional Internship Programme): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3312 (FOS Undergraduate Professional Internship Programme 3S1): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST3313 (FOS Undergraduate Professional Internship Programme 3S2): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4199 (Honours Project in Statistics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4231 (Computer Intensive Statistical Methods): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4233 (Linear Models): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4234 (Bayesian Statistics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4238 (Stochastic Processes II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4245 (Statistical Methods for Finance): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4250 (Multivariate Statistical Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4253 (Applied Time Series Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4288 (Honours Project in Statistics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4299 (Applied Project in Statistics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4310 (FOS Undergraduate Professional Internship Programme 3ST): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4312 (FOS Undergraduate Professional Internship Programme 4S1): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST4313 (FOS Undergraduate Professional Internship Programme 4S2): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5188 (Applied Data Science Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5199 (Coursework Track Ii Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5201 (Statistical Foundations of Data Science): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5201X (Statistical Foundations of Data Science): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5202 (Applied Regression Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5202X (Applied Regression Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5203 (Design of Experiments): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5207 (Nonparametric Regression): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5209X (Analysis Of Time Series Data): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5211X (Sampling from Finite Populations): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5212 (Survival Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5213 (Advanced Categorical Data Analysis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5218 (Advanced Statistical Methods in Finance): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5221 (Stochastic Processes and Applications): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5225 (Statistical Analysis of Networks): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5226 (Spatial Statistics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5227 (Applied Statistical Learning): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5229 (Deep Learning in Data Analytics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5230 (Applied Natural Language Processing): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST5290 (Data Science Industry Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6101 (Advanced Statistical Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6102 (Advanced Statistical Theory II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6103 (Advanced Probability Theory): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6104 (Statistical Models): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6105 (Computational Statistics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6120 (Graduate Seminar Course): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6242 (Topics II): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- ST6243 (Topics III): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- STR1000 (Career Compass Starter Workshops): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- STR2000 (Career Compass Starter Clinics): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- TCE2407 (Engineering & Uncertainty Analyses): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- TEE2002 (Engineering Mathematics II): not offered in any semester in AY2026-2027
- TEE2023 (Signals and Systems): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- TEE2101 (Programming Methodology): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- TEE3207 (Computer Architecture): not offered in any semester in AY2026-2027
- TG1401 (Engineering Mathematics I): not offered in any semester in AY2026-2027
- UTW1001A (Identities and Ideas in Modern Market-Driven Societies): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001AA (Amusing Ourselves to Death? Discerning the Digital Deluge): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001C (At the Edges of the Law: Ethics, Morality and Society): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001I (Science and popular narratives): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001J (How do we frame the Climate Crisis?): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001K (Meaning of Home and Identity in the Diaspora): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001P (Heroes): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001Q (English, Singlish and intercultural communication): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001T (How Rich Should Anyone Be?): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001V (Am I Who I Am? Knowledge, Language and Identity): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- UTW1001X (Ecospirituality: Religion, Nature, Culture): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4401 (Integrated Honours Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4402 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4403 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4405HM (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4406 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4408 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4413 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4417EC (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFA4417PL (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFB4001 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFB4002 (Integrated Honours Dissertation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFC4101 (Integrated Honours Thesis): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFC4102 (Integrated Honours Dissertation): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFE4401 (Integrated Honours Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFS4199M (Integrated Honours Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- XFS4199S (Integrated Honours Project): details not in dataset [data gap]: outside fetch scope, so this is a data limitation, not an academic rule
- YCC1122 (Quantitative Reasoning): not offered in any semester in AY2026-2027
- YSC1212 (Introduction to Computer Science): not offered in any semester in AY2026-2027
- YSC1213 (General Physics): not offered in any semester in AY2026-2027
- YSC1216 (Calculus): not offered in any semester in AY2026-2027
- YSC2203 (Classical Mechanics): not offered in any semester in AY2026-2027
- YSC2209 (Proof): not offered in any semester in AY2026-2027
- YSC2221 (Introduction to Python): not offered in any semester in AY2026-2027
- YSC2229 (Introductory Data Structures and Algorithms): not offered in any semester in AY2026-2027
- YSC2232 (Linear Algebra): not offered in any semester in AY2026-2027
- YSC2239 (Introduction to Data Science): not offered in any semester in AY2026-2027
- YSC2243 (Probability): not offered in any semester in AY2026-2027
- YSC2252 (Multivariable Calculus): not offered in any semester in AY2026-2027
- YSC3203 (Advanced Algorithms and Data Structures): not offered in any semester in AY2026-2027
- YSC3217 (Programming Operating Systems, Interfaces & eXtras): not offered in any semester in AY2026-2027
- YSC3232 (Software Engineering): not offered in any semester in AY2026-2027
- YSC4216 (Machine Learning): not offered in any semester in AY2026-2027
- YSS1203 (Principles of Economics): not offered in any semester in AY2026-2027
- YSS2203 (Intermediate Microeconomics): not offered in any semester in AY2026-2027
- YSS2211 (Econometrics): not offered in any semester in AY2026-2027

## Warnings (spot-check these first)

- BT3017: prerequisiteRule mixes AND/OR without brackets; using NUSMods prereqTree reading. Usual-precedence reading was: ((BT1101 or BT1101HS) and (CS1010J or CS1010E or CS1010S or CS1010X or CS1010 or CS1101S or CS1010A or CS1010HS or UTC2851) and ST2334) or (ST2131 and ST2132 and (MA2001 or MA1522 or MA1311))
- BT4103: pattern UWC2101% matches no known course
- CP3880: pattern UWC2101% matches no known course
- CS2040HS: preclusion rule uses OR; read as 'any clause blocks'
- CS2100: preclusion rule uses OR; read as 'any clause blocks'
- CS2100HS: preclusion rule uses OR; read as 'any clause blocks'
- CS2106: preclusion rule uses OR; read as 'any clause blocks'
- CS2309: prerequisiteRule mixes AND/OR without brackets; using NUSMods prereqTree reading. Usual-precedence reading was: ((CS1231 or CS1231S or MA1100 or MA1100T) and (CS2030 or CS2030S or CS2030DE or CS2030HS) and (CS2040 or CS2040S or CS2040HS or CS2040C or CS2040DE)) or CS2113 or CS2113T
- CS5446: preclusion rule uses OR; read as 'any clause blocks'
- CS5462: preclusion rule uses OR; read as 'any clause blocks'
- CS5477: preclusion rule uses OR; read as 'any clause blocks'
- EC1101E: preclusion rule uses OR; read as 'any clause blocks'
- EE4210: preclusion rule uses OR; read as 'any clause blocks'
- EE4212: preclusion rule uses OR; read as 'any clause blocks'
- EE4704: preclusion rule uses OR; read as 'any clause blocks'
- EE5310: preclusion rule uses OR; read as 'any clause blocks'
- FAS1101: pattern UTW2001% matches no known course
- IS3103: pattern UWC2101% matches no known course
- IS4403: preclusion rule uses OR; read as 'any clause blocks'
- YSC4216: preclusion rule uses OR; read as 'any clause blocks'

## Asymmetric preclusions

A lists B as a preclusion but B (in this AY) does not list A. Treated as mutual anyway.

BSP1703 → EC2101, BSP1703X → EC2101, BT1101 → DSA1101, BT1101 → DSE1101, BT1101 → ST1131, BT1101HS → BT1101, BT1101HS → DSA1101, BT1101HS → DSE1101, BT1101HS → EC2303, BT1101HS → ST1131, BT4240 → IS4240, CE2407 → TCE2407, CE2407A → CE2407, CE2407A → TCE2407, CE2407B → CE2407, CE2407B → TCE2407, CG1111A → BN2111, CG1111A → ESP2111, CG1111A → ME2104, CG1111A → ME2105, CG2023 → TEE2023, CG2028 → CS2100, CG3201 → BT4240, CG3201 → DMX1401AI, CG3201 → DMX1501AI, CG3207 → TEE3207, CG4001 → CG4003, CG4001 → CP4101, CG4001 → EE4001, CG4001 → EE4002D, CG4001 → EE4002R, CP2106 → CS2103, CP2106 → CS2103DE, CP2106 → CS2103T, CP2106 → CS2113, CP2106 → CS2113T, CP4106 → BT4101, CP4106 → CP4101, CP4106 → XFA4401, CP4106 → XFA4402, CP4106 → XFA4403, CP4106 → XFA4405HM, CP4106 → XFA4406, CP4106 → XFA4408, CP4106 → XFA4413, CP4106 → XFA4417EC, CP4106 → XFA4417PL, CP4106 → XFB4001, CP4106 → XFB4002, CP4106 → XFC4101, CP4106 → XFC4102, CP4106 → XFE4401, CP4106 → XFS4199M, CP4106 → XFS4199S, CS1010XCP → CS1010, CS1010XCP → CS1010A, CS1010XCP → CS1010E, CS1010XCP → CS1010HS, CS1010XCP → CS1010J, CS1010XCP → CS1010S, CS1010XCP → CS1010X, CS1010XCP → CS1101S, CS2030HS → CS2030DE, CS2040HS → CS2040DE, CS2100DE → CS2100R, CS2100HS → CG2028, CS2100HS → CS2100DE, CS2100HS → EE2028, CS2101 → CS2103, CS2101 → CS2113, CS2101X → CS2103, CS2101X → CS2103T, CS2101X → CS2113, CS2101X → CS2113T, CS2101X → ES2002, CS2101X → ES2007D, CS2101X → IS2101, CS2103DE → CS2103R, CS2103T → ES2002, CS2103T → ES2007D, CS2106 → EE4214, CS2109HS → CG3201, CS2109HS → DMX1401AI, CS2109HS → EE2211, CS2109S → DMX1401AI, CS2109S → EE2211, CS2113T → ES2002, CS2113T → ES2007D, CS2113T → IS2101, CS3244 → DMX1401AI, CS3244 → EE3703, CS4263 → CS2109S, CS4263 → CS3243, CS4263 → CS3263, CS4330 → CS3225, CS5246 → DSA4213, DAO1704 → DAO1704X, DAO2702 → DAO2702X, DSA3102 → MA3236, EC2303 → SA4101, EC2303 → SA4101C, EC2303 → SA4104, EC2303 → SA4105, EC2303 → SA4105C, EC2303 → SA4106, EC2303 → SA4107, EC2303 → SA4108, EC2303 → SA4110, EC2303 → SA4110C, EC2303 → SA4111, EC2303 → ST1131, EC2303 → ST2132, EC2303 → ST2137, EC2303 → ST2288, EC2303 → ST2288R, EC2303 → ST2289, EC2303 → ST2289R, EC2303 → ST2310, EC2303 → ST2312, EC2303 → ST2313, EC2303 → ST3131, EC2303 → ST3232, EC2303 → ST3236, EC2303 → ST3239, EC2303 → ST3244, EC2303 → ST3246, EC2303 → ST3247, EC2303 → ST3248, EC2303 → ST3288, EC2303 → ST3288R, EC2303 → ST3289, EC2303 → ST3289R, EC2303 → ST3310, EC2303 → ST3311, EC2303 → ST3312, EC2303 → ST3313, EC2303 → ST4199, EC2303 → ST4231, EC2303 → ST4233, EC2303 → ST4234, EC2303 → ST4238, EC2303 → ST4245, EC2303 → ST4248, EC2303 → ST4250, EC2303 → ST4253, EC2303 → ST4288, EC2303 → ST4299, EC2303 → ST4310, EC2303 → ST4312, EC2303 → ST4313, EE1111A → BN1111, EE1111A → EE1111, EE1111A → ESP1111, EE1111A → ME1102, EE1111A → ME2105, EE1111A → RB2101, EE2012 → CE2407A, EE2012 → ST2131, EE2012 → ST2334, EE2012A → ST2131, EE2012A → ST2334, EE2023 → TEE2023, EE2028 → EE2024, EE2111A → ESP2111, EE2111A → ME2104, EE2111A → ME2105, EE2213 → CS2109S, EE4204 → CEG5101, EE4204 → CS2105, EE4204 → EE5310, EE4204 → EE6310, EE4204 → TEE4204, EE4212 → EE5731, EE4802 → EE4211, EE4802 → IT3011, EE5310 → EE6310, ES1531 → GEK1549, ES1531 → GET1021, ES1531 → UTW1001A, ES1531 → UTW1001AA, ES1531 → UTW1001C, ES1531 → UTW1001I, ES1531 → UTW1001J, ES1531 → UTW1001K, ES1531 → UTW1001P, ES1531 → UTW1001Q, ES1531 → UTW1001T, ES1531 → UTW1001V, ES1531 → UTW1001X, ES2002 → NTW2006, ES2002 → NTW2008, ES2002 → NTW2010, ES2002 → NTW2018, ES2002 → NTW2029, ES2002 → NTW2032, ES2002 → NTW2034, ES2002 → NTW2035, ES2002 → NTW2036, ES2002 → NTW2037, ES2002 → NTW2038, ES2002 → NTW2040, ES2002 → NTW2041, ES2002 → NTW2042, ES2531 → GEK1549, ES2531 → GET1021, ES2531 → UTW1001A, ES2531 → UTW1001AA, ES2531 → UTW1001C, ES2531 → UTW1001I, ES2531 → UTW1001J, ES2531 → UTW1001K, ES2531 → UTW1001P, ES2531 → UTW1001Q, ES2531 → UTW1001T, ES2531 → UTW1001V, ES2531 → UTW1001X, ES2631 → ES1531, ES2631 → ES2531, ES2631 → GEK1549, ES2631 → GET1021, ES2631 → UTW1001A, ES2631 → UTW1001AA, ES2631 → UTW1001C, ES2631 → UTW1001I, ES2631 → UTW1001J, ES2631 → UTW1001K, ES2631 → UTW1001P, ES2631 → UTW1001Q, ES2631 → UTW1001T, ES2631 → UTW1001V, ES2631 → UTW1001X, ESP1111 → ME1102, FAS1101 → ES1531, FAS1101 → ES2631, FAS1101 → GEK1549, FAS1101 → GET1021, FAS1101 → RVX1000, FAS1101 → RVX1001, FAS1101 → RVX1003, FAS1101 → RVX1004, FAS1101 → RVX1005, FAS1101 → RVX1006, FAS1101 → SP1541, FAS1101 → SP1541X, FAS1101 → UTW1001A, FAS1101 → UTW1001AA, FAS1101 → UTW1001C, FAS1101 → UTW1001I, FAS1101 → UTW1001J, FAS1101 → UTW1001K, FAS1101 → UTW1001P, FAS1101 → UTW1001Q, FAS1101 → UTW1001T, FAS1101 → UTW1001V, FAS1101 → UTW1001X, FT5012 → AI5205, HS1501 → CS2109HS, HS1501 → CS2109S, HS1501 → HS1502, HS1501 → HS1503, HS1501 → HS1504, IE2100 → DBA3711, IE4213 → CS3244, IE4213 → EE4211, IE4213 → IT3011, IFS4201 → IFS4205, IFS4202 → IFS4201, IS2109 → CS2109S, IS2109 → IS4242, IS3106 → CS3226, IS3109 → CG3201, IS4010 → CP3880, IS4400 → IS5006, IS4401 → DBA4714, IS4401 → IE4280, IS4403 → DBA5114, IS4403 → ISY5005, IT1244 → CS2109S, IT1244 → CS3243, IT1244 → CS3244, IT1244 → CS3263, IT1244 → CS3264, IT1244 → IT3011, IT3010 → BT2102, IT3010 → CS2102, IT3011 → CS3264, IT3011 → DMX1401AI, IT3011 → EE2211, MA1100T → YSC2209, MA1301 → MA1100, MA1301 → MA1100T, MA1301 → MA1311, MA1301 → MA1312, MA1301 → MA1505, MA1301 → MA1508E, MA1301 → MA1511, MA1301 → MA1512, MA1301 → MA1513, MA1301 → MA1521, MA1301 → MA1522, MA1301 → MA1531, MA1301 → MA2001, MA1301 → MA2002, MA1301 → MA2101, MA1301 → MA2101S, MA1301 → MA2104, MA1301 → MA2108, MA1301 → MA2108S, MA1301 → MA2116, MA1301 → MA2116T, MA1301 → MA2202, MA1301 → MA2202S, MA1301 → MA2213, MA1301 → MA2214, MA1301 → MA2288, MA1301 → MA2288R, MA1301 → MA2289, MA1301 → MA2289R, MA1301 → MA2301, MA1301 → MA2310, MA1301 → MA2311, MA1301 → MA2312U, MA1301 → MA2313, MA1301 → MA2401, MA1301 → MA3201, MA1301 → MA3205, MA1301 → MA3209, MA1301 → MA3210, MA1301 → MA3211, MA1301 → MA3211S, MA1301 → MA3220, MA1301 → MA3233, MA1301 → MA3236, MA1301 → MA3238, MA1301 → MA3238S, MA1301 → MA3252, MA1301 → MA3264, MA1301 → MA3265, MA1301 → MA3270, MA1301 → MA3288, MA1301 → MA3288R, MA1301 → MA3289, MA1301 → MA3310, MA1301 → MA3312, MA1301 → MA3313, MA1301 → MA4198, MA1301 → MA4203, MA1301 → MA4207, MA1301 → MA4211, MA1301 → MA4221, MA1301 → MA4229, MA1301 → MA4230, MA1301 → MA4233, MA1301 → MA4235, MA1301 → MA4251, MA1301 → MA4254, MA1301 → MA4255, MA1301 → MA4261, MA1301 → MA4262, MA1301 → MA4264, MA1301 → MA4266, MA1301 → MA4270, MA1301 → MA4273, MA1301 → MA4275, MA1301 → MA4276, MA1301 → MA4288O, MA1301 → MA4288P, MA1301 → MA4310, MA1301 → MA4312, MA1301 → MA4313, MA1301 → MA5198, MA1301 → MA5202, MA1301 → MA5204, MA1301 → MA5205, MA1301 → MA5206, MA1301 → MA5210, MA1301 → MA5213, MA1301 → MA5216, MA1301 → MA5217, MA1301 → MA5218, MA1301 → MA5219, MA1301 → MA5222, MA1301 → MA5232, MA1301 → MA5233, MA1301 → MA5243, MA1301 → MA5248, MA1301 → MA5249, MA1301 → MA5251, MA1301 → MA5252, MA1301 → MA5259, MA1301 → MA5260, MA1301 → MA5266, MA1301 → MA5270, MA1301 → MA5271, MA1301 → MA5272, MA1301 → MA5401, MA1301 → MA5402, MA1301 → MA6202, MA1301 → MA6211, MA1301 → MA6225, MA1301 → MA6291, MA1301X → MA1100, MA1301X → MA1100T, MA1301X → MA1311, MA1301X → MA1312, MA1301X → MA1505, MA1301X → MA1508E, MA1301X → MA1511, MA1301X → MA1512, MA1301X → MA1513, MA1301X → MA1521, MA1301X → MA1522, MA1301X → MA1531, MA1301X → MA2001, MA1301X → MA2002, MA1301X → MA2101, MA1301X → MA2101S, MA1301X → MA2104, MA1301X → MA2108, MA1301X → MA2108S, MA1301X → MA2116, MA1301X → MA2116T, MA1301X → MA2202, MA1301X → MA2202S, MA1301X → MA2213, MA1301X → MA2214, MA1301X → MA2288, MA1301X → MA2288R, MA1301X → MA2289, MA1301X → MA2289R, MA1301X → MA2301, MA1301X → MA2310, MA1301X → MA2311, MA1301X → MA2312U, MA1301X → MA2313, MA1301X → MA2401, MA1301X → MA3201, MA1301X → MA3205, MA1301X → MA3209, MA1301X → MA3210, MA1301X → MA3211, MA1301X → MA3211S, MA1301X → MA3220, MA1301X → MA3233, MA1301X → MA3236, MA1301X → MA3238, MA1301X → MA3238S, MA1301X → MA3252, MA1301X → MA3264, MA1301X → MA3265, MA1301X → MA3270, MA1301X → MA3288, MA1301X → MA3288R, MA1301X → MA3289, MA1301X → MA3310, MA1301X → MA3312, MA1301X → MA3313, MA1301X → MA4198, MA1301X → MA4203, MA1301X → MA4207, MA1301X → MA4211, MA1301X → MA4221, MA1301X → MA4229, MA1301X → MA4230, MA1301X → MA4233, MA1301X → MA4235, MA1301X → MA4251, MA1301X → MA4254, MA1301X → MA4255, MA1301X → MA4261, MA1301X → MA4262, MA1301X → MA4264, MA1301X → MA4266, MA1301X → MA4270, MA1301X → MA4273, MA1301X → MA4275, MA1301X → MA4276, MA1301X → MA4288O, MA1301X → MA4288P, MA1301X → MA4310, MA1301X → MA4312, MA1301X → MA4313, MA1301X → MA5198, MA1301X → MA5202, MA1301X → MA5204, MA1301X → MA5205, MA1301X → MA5206, MA1301X → MA5210, MA1301X → MA5213, MA1301X → MA5216, MA1301X → MA5217, MA1301X → MA5218, MA1301X → MA5219, MA1301X → MA5222, MA1301X → MA5232, MA1301X → MA5233, MA1301X → MA5243, MA1301X → MA5248, MA1301X → MA5249, MA1301X → MA5251, MA1301X → MA5252, MA1301X → MA5259, MA1301X → MA5260, MA1301X → MA5266, MA1301X → MA5270, MA1301X → MA5271, MA1301X → MA5272, MA1301X → MA5401, MA1301X → MA5402, MA1301X → MA6202, MA1301X → MA6211, MA1301X → MA6225, MA1301X → MA6291, MA1508E → MA1311, MA1511 → MA2002, MA1513 → MA1311, MA1522 → MA1311, MA1522 → YSC2232, MA1531 → MA1312, MA1531 → MA1505, MA1531 → MA1511, MA1531 → MA1521, MA1531 → MA2002, MA1531 → MA2104, MA1531 → YSC1216, MA2001 → YSC2232, MA2002 → YSC1216, MA2116 → YSC2243, MA2116T → EC2303, MA2116T → MA2301, MA2116T → YSC2243, MA2301 → MA1312, MA2301 → MA1505, MA2301 → MA1508E, MA2301 → MA1511, MA2301 → MA1513, MA2301 → MA1521, MA2301 → MA2001, MA2301 → MA2002, MA2311 → MA2108, MA2311 → MA2108S, ME1102 → RB1101, ME2105 → ESP2111, ME2105 → ME2104, ME2105 → ME2143, MNO2706 → IS2101, MNO2706 → IS3103, NM2207 → CS1010, NM2207 → CS1010A, NM2207 → CS1010E, NM2207 → CS1010HS, NM2207 → CS1010J, NM2207 → CS1010R, NM2207 → CS1010S, NM2207 → CS1010X, NM2207 → CS1010XCP, NM2207 → CS1101S, NM4259 → NM3221, NM4259HM → NM3221, PC1201 → PC1101, PC2174A → PC2134, RB2101 → EE1111B, RB2101 → ME2104, RB2101 → ME2105, RE1702 → DAO1704X, ST1232 → CE2407, ST1232 → CN3421, ST1232 → ST1131, ST1232 → ST2334, ST2131 → CE2407, TEE4204 → CS2105, TEE4204 → CS3103, TTG2401 → TEE2002, UTC2851 → CS1010R, ZB2101 → LSM2241
