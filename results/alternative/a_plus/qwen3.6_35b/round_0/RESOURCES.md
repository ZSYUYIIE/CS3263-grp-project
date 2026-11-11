# Resources: results\alternative\a_plus\qwen3.6_35b\round_0

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 10706.5 | 14391 | 17102 |
| completion tokens | 272.5 | 4932 | 9744 |
| total tokens | 11575.5 | 17272 | 23817 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 5.78 | 98.86 | 273.69 |
| seconds of the successful request | 5.76 | 94.97 | 167.78 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 8
- total tokens over all instances: 10715034
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 26.6% (239/900)
- valid-answer accuracy, gold PLAN instances: 8.2% (49/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 6.2% (37/600)
- valid plans that are not optimal: 24.5% (12/49)
- over-refusal (gold PLAN answered NO_PLAN): 36.5% (219/600)
- correct refusal, gold NO_PLAN instances: 71.3% (171/240)
- invented plan, gold NO_PLAN instances: 28.8% (69/240)
- tokens per valid answer (all instances): 44833
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 198572
