# Resources: results\B\x-test-2

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 2654 | 2688 | 2709 |
| completion tokens | 242 | 490 | 2286 |
| total tokens | 2896.5 | 3161 | 4963 |
| reasoning tokens (when the API reports them) | 158 | 393 | 2205 |
| seconds per instance (whole) | 3.83 | 8.46 | 28.78 |
| seconds of the successful request | 3.83 | 8.46 | 28.78 |
| solver seconds (pipeline B) | 0 | 0.001 | 0.008 |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 1172488
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 398 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 398 of 400
- tokens per solution-correct answer: 2946
- tokens per optimal answer: 2946

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 2653 | 232 | 2881 | 3.45 |
| 6-11 | 96 | 2652.5 | 238.5 | 2890.5 | 3.855 |
| 11-16 | 96 | 2653.5 | 245 | 2904.5 | 4.025 |
| 16-39 | 96 | 2661 | 252 | 2913 | 4.155 |

Spearman correlation of k with total tokens: rho = 0.14, p = 0.005 (normal approximation)
