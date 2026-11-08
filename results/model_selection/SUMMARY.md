# Route A model-selection pilot

Same 8 cases, prompts, catalogue records and token cap; provider-default reasoning effort.
One response per case. This small, exploratory sample does not establish general superiority.
Latency includes shared-service queueing and retries; costs use the discovery API's listed rates.

Strict scores use the untouched response. Diagnostic scores remove only an extra `plan` or
`eligibility` wrapper to distinguish format errors from reasoning errors; the task type comes
from the gold spec for this offline diagnostic only. Stored responses and official grades are unchanged.
Recorded-reply cost excludes failed calls without final text, which may also be charged.

| Exact model ID | Answered | Strict status | Wrappers | Diagnostic status | Diagnostic valid plans | Diagnostic optimal plans | Median seconds | Recorded-reply USD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:27b` | 5/8 | 5/8 | 0 | 5/8 | 0/2 | 0/2 | 125.5 | $0.0415 |
| `x-test-1` | 6/8 | 0/8 | 6 | 6/8 | 2/2 | 2/2 | 94.3 | $0.0156 |
| `x-test-2` | 8/8 | 6/8 | 2 | 8/8 | 2/2 | 2/2 | 54.9 | $0.0325 |
| `x-test-4` | 3/8 | 0/8 | 3 | 3/8 | 0/2 | 0/2 | 24.0 | $0.0064 |

Pilot stopped after approximately 10 minutes with Qwen requests still unfinished. All eight requests finished for the other three models, including responses without final text.
Missing responses are coverage gaps, not evidence that the model reasoned incorrectly.
