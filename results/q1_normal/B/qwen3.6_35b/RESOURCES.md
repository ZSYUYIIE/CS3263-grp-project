# Resources: results\B\qwen3.6_35b

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 2932.5 | 2975 | 3002 |
| completion tokens | 117 | 154 | 190 |
| total tokens | 3054 | 3132 | 3178 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 2.685 | 5.96 | 18.7 |
| seconds of the successful request | 2.685 | 5.96 | 18.7 |
| solver seconds (pipeline B) | 0 | 0.001 | 0.007 |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 1219940
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 383 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 383 of 400
- tokens per solution-correct answer: 3185
- tokens per optimal answer: 3185

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 2931 | 116 | 3050 | 2.72 |
| 6-11 | 96 | 2929.5 | 116 | 3047.5 | 2.555 |
| 11-16 | 96 | 2932 | 114 | 3051 | 2.545 |
| 16-39 | 96 | 2944 | 124.5 | 3071.5 | 2.855 |

Spearman correlation of k with total tokens: rho = 0.18, p = 0.001 (normal approximation)
