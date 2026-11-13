# Resources: results\alternative\a_plus\qwen3.6_35b\round_3

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 13388.5 | 41024 | 73067 |
| completion tokens | 529 | 5968 | 10104 |
| total tokens | 14936.5 | 45357 | 77851 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 10.97 | 116.15 | 301.87 |
| seconds of the successful request | 10.815 | 107.49 | 216.02 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 9
- total tokens over all instances: 17956363
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 41.0% (369/900)
- valid-answer accuracy, gold PLAN instances: 18.7% (112/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 11.8% (71/600)
- valid plans that are not optimal: 36.6% (41/112)
- over-refusal (gold PLAN answered NO_PLAN): 76.7% (460/600)
- correct refusal, gold NO_PLAN instances: 98.3% (236/240)
- invented plan, gold NO_PLAN instances: 1.7% (4/240)
- tokens per valid answer (all instances): 48662
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 187333
