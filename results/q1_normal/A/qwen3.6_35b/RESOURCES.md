# Resources: results\A\qwen3.6_35b

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 6382 | 10470 | 13807 |
| completion tokens | 86 | 699 | 1426 |
| total tokens | 6561.5 | 10601 | 13929 |
| reasoning tokens (when the API reports them) | 0 | 0 | 0 |
| seconds per instance (whole) | 2.03 | 12.23 | 26.89 |
| seconds of the successful request | 2.03 | 12.23 | 26.89 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 2656368
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 265 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 265 of 400
- tokens per solution-correct answer: 10024
- tokens per optimal answer: 10024

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 6141 | 69 | 6219 | 1.87 |
| 6-11 | 96 | 5992 | 76 | 6441 | 1.795 |
| 11-16 | 96 | 5779 | 96.5 | 5885 | 2.13 |
| 16-39 | 96 | 7918 | 118 | 8260.5 | 2.705 |

Spearman correlation of k with total tokens: rho = 0.24, p = 0.000 (normal approximation)
