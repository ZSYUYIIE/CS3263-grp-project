# Resources: results\q1_ablation1\A\x-test-2

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 5118.5 | 8249 | 10974 |
| completion tokens | 361.5 | 728 | 1320 |
| total tokens | 5474.5 | 8620 | 11437 |
| reasoning tokens (when the API reports them) | 292.5 | 630 | 1249 |
| seconds per instance (whole) | 5.02 | 9.45 | 17.37 |
| seconds of the successful request | 5.02 | 9.45 | 17.37 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 2231843
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 400 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 400 of 400
- tokens per solution-correct answer: 5580
- tokens per optimal answer: 5580

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 4925 | 296 | 5329 | 4.21 |
| 6-11 | 96 | 4821 | 342 | 5181 | 5.07 |
| 11-16 | 96 | 4634 | 382 | 5122 | 4.93 |
| 16-39 | 96 | 6276 | 498.5 | 6838 | 5.955 |

Spearman correlation of k with total tokens: rho = 0.26, p = 0.000 (normal approximation)
