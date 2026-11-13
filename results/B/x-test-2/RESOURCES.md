# Resources: results\B\x-test-2

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 2826 | 2874 | 2912 |
| completion tokens | 728 | 2249 | 24576 |
| total tokens | 3560.5 | 5081 | 27436 |
| reasoning tokens (when the API reports them) | 500.5 | 2035 | 24576 |
| seconds per instance (whole) | 6.595 | 20.9 | 195.55 |
| seconds of the successful request | 6.46 | 19.41 | 195.55 |
| solver seconds (pipeline B) | 0.0275 | 0.204 | 17.229 |

- instances with a reply cut off at max_tokens: 2 (0.2%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 3435947
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 98.9% (890/900)
- valid-answer accuracy, gold PLAN instances: 98.5% (591/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 98.3% (590/600)
- valid plans that are not optimal: 0.2% (1/591)
- over-refusal (gold PLAN answered NO_PLAN): 0.3% (2/600)
- correct refusal, gold NO_PLAN instances: 99.6% (239/240)
- invented plan, gold NO_PLAN instances: 0.0% (0/240)
- tokens per valid answer (all instances): 3861
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 3832
