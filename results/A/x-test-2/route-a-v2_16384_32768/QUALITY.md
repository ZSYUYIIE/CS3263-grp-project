# Route A answer quality

| Check | Count |
|---|---:|
| recorded | 115 |
| status correct | 115 |
| format valid | 115 |
| api errors | 0 |
| budget exhausted | 0 |
| budget retried | 4 |
| eligibility cases | 30 |
| eligibility claims verified | 30 |
| quality errors | 1 |
| cases with unverified grade clauses | 5 |
| optimal plans | 44 |
| witness verified preference gaps | 1 |
| invalid plans | 0 |
| independently certified refusals | 24 |
| assistant review pass | 109 |
| assistant review issues | 5 |
| assistant review notes | 1 |
| explanations pending review | 0 |

Modelled plan constraints and Q1 boolean claims are checked from AY2026/27 catalogue data.
Optimality is measured against the saved gold reference; this audit does not call a solver.
A relative preference is not certified from a reference plan that itself missed that preference.
Independently valid offline witness plans can disprove a preference claim; they never enter generation.
Higher-than-pass grade clauses are reported as scope warnings: transcripts contain no grades,
and the benchmark's completion-only semantics do not establish real-world grade eligibility.
Correct refusal statuses do not by themselves prove that the written explanation is sound.
Free-text claims need separate review in explanation_review.csv. Existing review entries are preserved.

## Assisted review: issues needing attention

These notes preserve the original LLM replies. Status scores are not prose-correctness scores.

- **q1-missing_prereq-06**: ISSUE: correct NOT_ELIGIBLE under the completed-transcript-only benchmark, but the extra claim that CS3241 cannot be completed before next semester is unsupported. The request says current Y3S1; CS3241 is offered in Sem 1, its CS2030S/CS2040S prerequisites are completed, and it has no preclusion. It could be taken in the current term and completed before Y3S2. The answer should distinguish current transcript eligibility from conditional future completion.
- **q2-loose-25**: Valid plan, but the claimed earliest CS3219 placement is only earliest within the unnecessarily late CS2103DE path. CS2103T is also offered in Sem 1 and can be added in semester 3; a valid equal-added-course counterplan schedules CS3219 in semester 4 and has peak 8 MC instead of 12. See preference_witnesses.json. Do not certify the generated plan as preference-optimal.
- **q2-tight-11**: The plan is valid and minimum-credit, but the reason incorrectly claims that leaving calendar semesters 7-8 empty satisfies light-last-semester preference. The benchmark defines the last used semester: semester 6 has 4 MC and its average load is also 4 MC, so it is not lighter than average. The reference correctly marks this preference unmet.
- **q2-tight-14**: Plan is valid under the actual two-module (8 MC) cap, but the prose incorrectly refers to a 20 MC limit. The explanation should state the requested 8 MC cap. Other stated chains and exclusions agree with the catalogue.
- **q2_infeasible-chain-04**: NO_PLAN is correct, but the phrase that both CS3264 and CS3263 require CS2109S (or CS2109HS) conflates their alternatives. CS2109HS is an alternative only for CS3263; CS3264 specifically requires CS2109S. The final-semester missing-prerequisite contradiction remains valid.

## Optional wording notes

These are not incorrect decisions or scope-recognition failures.

- **out_of_scope-programme-05**: Correct OUT_OF_SCOPE decision and advisor referral. The response did not declare the student eligible and did not produce a plan. Its extra conditional course commentary is an optional wording note, not a wrong decision or scope-recognition failure. It may be omitted for stricter wording without changing any correctness score.

## Completion-only modelling limit

Higher-than-pass grade clauses remain unverified in: q2-loose-03, q2-loose-20, q2-loose-22, q2-tight-07, q2-tight-08.
These cases involve CS3233's A- prerequisites. Validity here is conditional on the benchmark's
completion-only simplification; it does not certify those grades for a real student.
