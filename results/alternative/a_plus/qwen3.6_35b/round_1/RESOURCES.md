# Resources: results\alternative\a_plus\qwen3.6_35b\round_1

900 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 13388.5 | 29801 | 41024 |
| completion tokens | 499 | 5738 | 9812 |
| total tokens | 14936.5 | 33990 | 50836 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 10.26 | 112.26 | 301.87 |
| seconds of the successful request | 10.185 | 105.33 | 191.6 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 8
- total tokens over all instances: 16187360
- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: 36.7% (330/900)
- valid-answer accuracy, gold PLAN instances: 14.2% (85/600)
- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: 9.5% (57/600)
- valid plans that are not optimal: 32.9% (28/85)
- over-refusal (gold PLAN answered NO_PLAN): 69.8% (419/600)
- correct refusal, gold NO_PLAN instances: 93.3% (224/240)
- invented plan, gold NO_PLAN instances: 6.7% (16/240)
- tokens per valid answer (all instances): 49053
- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): 206916
