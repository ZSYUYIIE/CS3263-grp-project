# Resources: results\q1_ablation1\B\x-test-2

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 2550 | 2584 | 2605 |
| completion tokens | 253 | 510 | 3762 |
| total tokens | 2804 | 3071 | 6345 |
| reasoning tokens (when the API reports them) | 172 | 423 | 3670 |
| seconds per instance (whole) | 3.04 | 6 | 36.89 |
| seconds of the successful request | 3.04 | 6 | 36.89 |
| solver seconds (pipeline B) | 0 | 0.001 | 0.01 |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 1136002
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 400 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 400 of 400
- tokens per solution-correct answer: 2840
- tokens per optimal answer: 2840

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 2549 | 253 | 2803 | 3.36 |
| 6-11 | 96 | 2548.5 | 237.5 | 2782 | 2.745 |
| 11-16 | 96 | 2549.5 | 271 | 2824 | 2.955 |
| 16-39 | 96 | 2557 | 263.5 | 2816 | 3.06 |

Spearman correlation of k with total tokens: rho = 0.10, p = 0.058 (normal approximation)
