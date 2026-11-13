"""Feedback prompt of pipeline A+ (pipelines/alternative/run_a_plus.py).

Round 0 uses the pipeline A prompt unchanged (pipelines/prompt_a.py). After a reply whose plan breaks hard rules,
the conversation continues with the model's own reply followed by this message. The violation lines are the
checker's own messages (eval/checker.py). The message names no answer status, no objective and no gold value.
"""
from __future__ import annotations

FEEDBACK = """Your previous answer contains a plan that breaks the following hard rules:

{violations}

Revise your answer. Return the complete answer again as a single JSON object in the same format as before."""


def feedback_message(violations: list[str]) -> dict:
    return {"role": "user", "content": FEEDBACK.format(violations="\n".join(f"- {v}" for v in violations))}
