# Resources: results\alternative\a_plus\qwen3.6_35b\round_2

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 13388.5 | 36317 | 59464 |
| completion tokens | 529 | 5874 | 10104 |
| total tokens | 14936.5 | 40373 | 67810 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 10.965 | 116.15 | 301.87 |
| seconds of the successful request | 10.815 | 107.49 | 206.81 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 9
- total tokens over all instances: 17531323
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 40.0% (360/900)
- valid-answer accuracy, gold PLAN instances: 17.7% (106/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 11.5% (69/600)
- valid plans that are not optimal: 34.9% (37/106)
- over-refusal (gold PLAN answered NO_PLAN): 75.2% (451/600)
- correct refusal, gold NO_PLAN instances: 97.1% (233/240)
- invented plan, gold NO_PLAN instances: 2.9% (7/240)
- tokens per valid answer (all instances): 48698
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 187660
