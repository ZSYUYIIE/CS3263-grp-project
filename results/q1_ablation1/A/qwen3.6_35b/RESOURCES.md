# Resources: results\q1_ablation1\A\qwen3.6_35b

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 6287 | 10375 | 13712 |
| completion tokens | 85.5 | 734 | 2683 |
| total tokens | 6489.5 | 10666 | 14185 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 2.245 | 13.82 | 38.74 |
| seconds of the successful request | 2.245 | 13.82 | 38.74 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 2623768
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 248 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 248 of 400
- tokens per solution-correct answer: 10580
- tokens per optimal answer: 10580

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 6046 | 70 | 6351 | 1.79 |
| 6-11 | 96 | 5897 | 70 | 5978 | 1.91 |
| 11-16 | 96 | 5684 | 107 | 5889.5 | 2.49 |
| 16-39 | 96 | 7823 | 119.5 | 8143.5 | 2.915 |

Spearman correlation of k with total tokens: rho = 0.24, p = 0.000 (normal approximation)
