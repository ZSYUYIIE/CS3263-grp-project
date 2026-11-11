# Resources: results\alternative\a_plus\x-test-2\round_3

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 8664.5 | 11977 | 28541 |
| completion tokens | 3917.5 | 20241 | 24576 |
| total tokens | 12721 | 31273 | 43367 |
| reasoning tokens (when the API reports them) | 3789 | 20038 | 24576 |
| seconds per instance (whole) | 42.76 | 173.57 | 293.65 |
| seconds of the successful request | 42.76 | 173.57 | 293.64 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 43 (4.8%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 13071563
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 92.3% (831/900)
- valid-answer accuracy, gold PLAN instances: 90.5% (543/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 89.5% (537/600)
- valid plans that are not optimal: 1.1% (6/543)
- over-refusal (gold PLAN answered NO_PLAN): 2.8% (17/600)
- correct refusal, gold NO_PLAN instances: 99.2% (238/240)
- invented plan, gold NO_PLAN instances: 0.0% (0/240)
- tokens per valid answer (all instances): 15730
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 18271
