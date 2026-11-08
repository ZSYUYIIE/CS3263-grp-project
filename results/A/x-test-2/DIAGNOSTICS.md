# Secondary diagnostic analysis

The official scores in SUMMARY.md use untouched model outputs. This secondary analysis removes only extra plan/eligibility wrappers, using the gold task type offline. Original replies and official grades are unchanged. API errors remain failures.

| Metric | Official | Diagnostic after wrapper removal |
|---|---:|---:|
| Correct status | 88/115 | 107/115 |
| Valid feasible plans | 27/45 | 37/45 |
| Optimal feasible plans | 27/45 | 37/45 |

- Recorded outcomes: 115; final-text responses: 109.
- Extra JSON wrappers: 19.
- API completions without final text: 6; all 6 used the 8192-token output cap.

The batch was resumed after the initial client stopped on a no-final-text response. Existing replies were retained. See RUN_CONFIG.json for the resume note and input hashes; usage from the initial failed calls is unavailable.

Only this selected model was run over all 115 cases. The four-model pilot is exploratory, uses eight of these cases, and does not establish a general model ranking.
