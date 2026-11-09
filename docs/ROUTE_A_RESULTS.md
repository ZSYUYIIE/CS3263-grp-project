# Route A results and review clarification

The revised direct-LLM run uses SoCLaaS model `x-test-2`, listed by the discovery API as
Test DeepSeek V4.1 Flash 1017, on the 115 saved AY2026/27 degree-planning instances.
The full records, manifest and review evidence are in
[`results/A/x-test-2/route-a-v2_16384_32768/`](../results/A/x-test-2/route-a-v2_16384_32768/).

## Final decisions versus answer quality

- All **115/115 final status decisions** match the reference.
- All **115/115 responses** follow the revised output contract.
- All **45/45 generated plans** satisfy the benchmark's modelled hard constraints.
- Forty-four plans meet the reference quality threshold. One has a preference gap demonstrated by an
  independently valid offline alternative plan; validity alone does not establish preference optimality.
- Five remaining review findings concern a preference choice or explanation accuracy. They are not five
  incorrect final status decisions.
- One additional observation is retained as an **optional wording note**, not an answer error.

The optional note is `out_of_scope-programme-05`. The model correctly returned `OUT_OF_SCOPE`, referred the
Information Systems student to an advisor, and did not give an eligibility decision or a plan. Its extra
conditional course commentary was originally flagged too strongly. That commentary may be omitted for a
stricter wording style, but it is not a wrong decision or a failure to recognise the scope boundary.

This review reclassification does not change any original response, final status score or plan-validity score.
Per-case annotations are in
[`explanation_review.csv`](../results/A/x-test-2/route-a-v2_16384_32768/explanation_review.csv),
and the current findings are in
[`QUALITY.md`](../results/A/x-test-2/route-a-v2_16384_32768/QUALITY.md).

## Token exhaustion versus response-content findings

Two different counts were previously described as six:

1. In the original 8,192-token run, six calls reached the output cap without final text. These were completion
   budget failures, not evidence of incorrect reasoning. They were not established to be HTTP 429 throttling.
2. Review of the revised completed responses originally flagged six content/policy observations. After the
   clarification above, five remain quality findings and one is an optional wording note.

The revised policy starts at 16,384 completion tokens and permits one exhaustion-only retry at 32,768 tokens,
using identical original messages and no grading feedback. Four cases used that retry. All 115 final attempts
ended with a normal stop, with no unfinished final responses. All 119 budget attempts and their usage are retained.

## Limits

Five generated plans involve CS3233's higher-than-pass grade requirements. The benchmark contains passed-course
lists rather than grades, so those requirements remain unverified. The results certify the completion-only
benchmark constraints, not unconditional real-world grade eligibility.

The prompt and budget were improved together; the before/after comparison does not isolate their individual
effects. The original run and the small historical model-selection pilot are preserved separately.
No review notes, reference answers or counterexample plans are fed into generation.
