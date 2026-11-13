# Resources: results\alternative\a_plus\x-test-2\round_0

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 8626 | 11450 | 13582 |
| completion tokens | 3905 | 19604 | 24576 |
| total tokens | 12654.5 | 30362 | 38158 |
| reasoning tokens (when the API reports them) | 3772 | 19451 | 24576 |
| seconds per instance (whole) | 42.155 | 172.01 | 293.65 |
| seconds of the successful request | 42.155 | 172.01 | 293.64 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 43 (4.8%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 12899779
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 90.8% (817/900)
- valid-answer accuracy, gold PLAN instances: 89.2% (535/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 88.3% (530/600)
- valid plans that are not optimal: 0.9% (5/535)
- over-refusal (gold PLAN answered NO_PLAN): 2.8% (17/600)
- correct refusal, gold NO_PLAN instances: 96.7% (232/240)
- invented plan, gold NO_PLAN instances: 2.5% (6/240)
- tokens per valid answer (all instances): 15789
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 18292
