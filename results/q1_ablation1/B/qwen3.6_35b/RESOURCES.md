# Resources: results\q1_ablation1\B\qwen3.6_35b

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 2827.5 | 2870 | 2897 |
| completion tokens | 117 | 150 | 191 |
| total tokens | 2947 | 3017 | 3073 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 2.06 | 3.08 | 9.82 |
| seconds of the successful request | 2.06 | 3.08 | 9.82 |
| solver seconds (pipeline B) | 0 | 0.002 | 0.008 |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 1177533
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 346 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 346 of 400
- tokens per solution-correct answer: 3403
- tokens per optimal answer: 3403

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 2826 | 116 | 2944 | 2.1 |
| 6-11 | 96 | 2824.5 | 116 | 2938.5 | 1.95 |
| 11-16 | 96 | 2827 | 114 | 2944 | 2.065 |
| 16-39 | 96 | 2839 | 123.5 | 2967.5 | 2.095 |

Spearman correlation of k with total tokens: rho = 0.18, p = 0.000 (normal approximation)
