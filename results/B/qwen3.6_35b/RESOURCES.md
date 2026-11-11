# Resources: results\B\qwen3.6_35b

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 3132 | 3191 | 3234 |
| completion tokens | 409.5 | 538 | 624 |
| total tokens | 3545 | 3721 | 3824 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 8.105 | 26.05 | 62.22 |
| seconds of the successful request | 7.93 | 24.43 | 41.52 |
| solver seconds (pipeline B) | 0.031 | 0.351 | 37.071 |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 3174690
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 84.3% (759/900)
- valid-answer accuracy, gold PLAN instances: 83.3% (500/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 81.2% (487/600)
- valid plans that are not optimal: 2.6% (13/500)
- over-refusal (gold PLAN answered NO_PLAN): 4.3% (26/600)
- correct refusal, gold NO_PLAN instances: 86.7% (208/240)
- invented plan, gold NO_PLAN instances: 0.8% (2/240)
- tokens per valid answer (all instances): 4183
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 4359
