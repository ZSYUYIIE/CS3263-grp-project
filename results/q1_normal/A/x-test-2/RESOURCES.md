# Resources: results\A\x-test-2

400 instances. Token counts are as reported by the API. Seconds are wall-clock under the worker count saved in each record, on a shared server: indicative only.

| Quantity | Median | 95th percentile | Max |
|---|---|---|---|
| prompt tokens | 5159.5 | 8290 | 11015 |
| completion tokens | 344.5 | 776 | 4659 |
| total tokens | 5504 | 8687 | 11569 |
| reasoning tokens (when the API reports them) | 269.5 | 711 | 4582 |
| seconds per instance (whole) | 5.23 | 10.65 | 55.05 |
| seconds of the successful request | 5.23 | 10.65 | 55.05 |
| solver seconds (pipeline B) | - | - | - |

- instances with a reply cut off at max_tokens: 0 (0.0%)
- instances that needed more than one API attempt: 0
- total tokens over all instances: 2251776
- solution accuracy (right status, and for PLAN a plan meeting every hard rule): 397 of 400
- optimality accuracy (also optimal under the objective, then fewest added courses, then most preferences): 397 of 400
- tokens per solution-correct answer: 5672
- tokens per optimal answer: 5672

## Tokens by size (Q2 requests; size = number of must-take courses in the gold spec)

| Size bin | Instances | Median completion tokens | Median total tokens |
|---|---|---|---|

## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)

Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).

| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |
|---|---|---|---|---|---|
| 1-6 | 95 | 4966 | 279 | 5398 | 4.81 |
| 6-11 | 96 | 4862 | 332.5 | 5191.5 | 5.195 |
| 11-16 | 96 | 4675 | 365 | 5106 | 5.22 |
| 16-39 | 96 | 6317 | 461.5 | 6854.5 | 6.305 |

Spearman correlation of k with total tokens: rho = 0.26, p = 0.000 (normal approximation)
