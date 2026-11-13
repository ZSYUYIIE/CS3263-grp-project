"""Terminal interaction around pipeline B. Existing batch runners are unchanged."""
from __future__ import annotations

import argparse
import os
import re
from collections.abc import Callable

from m1_data.catalog import Catalog
from pipelines.config import load_env
from pipelines.run_a import DEFAULT_MAX_TOKENS, call_api, parse_reply_how
from pipelines.run_b import build_messages
from planner.formatting import HIGH, LOW, format_answer, format_bidding, heading, summary, wrap
from solver.admission import Admission
from solver.mdp import solve as bidding_policy
from solver.mdp import unsupported_reasons
from solver.run import MISSING_PROMPTS, prepare, run

QUERY_NAMES = {"eligible": "check whether I can take a course", "plan": "plan my remaining courses"}
EXAMPLES = {
    "eligible": "I have completed CS1101S and CS1231S and I am in Y1S2. Can I take CS2040S?",
    "plan": "I have completed no courses and I am in Y1S1. Plan CS1101S and CS1231S, at most 20 MC.",
}
MENU = ("\n\nWhat would you like to do?\n"
        "  1. Check whether I can take a course\n  2. Plan my remaining courses\n  3. Exit")


class BackToMenu(Exception):
    """The user explicitly left the current request."""


class QuitSession(Exception):
    """The user explicitly ended the session."""


def translate_request(request, *, model, base_url, key, max_tokens=DEFAULT_MAX_TOKENS, timeout=60, retries=1):
    """Use the unchanged pipeline B prompt and shared API/JSON helpers."""
    try:
        text, usage = call_api(build_messages({"request": request}), model, base_url, key, max_tokens,
                               timeout=timeout, retries=retries)
    except RuntimeError:
        raise
    except Exception as error:  # e.g. a base URL without http://, or a malformed reply
        raise RuntimeError(f"API error: {type(error).__name__}: {error}") from error
    if usage.get("finish_reason") == "length":
        raise RuntimeError("The translation was cut short. Shorten the request or increase --max-tokens.")
    spec, how, error = parse_reply_how(text, "query")
    if error:
        raise RuntimeError(f"Could not read the translated request: {error}.")
    if how == "last_of_several":
        raise RuntimeError("The model returned several possible requests. Please retry or clarify your request.")
    return spec


def or_list(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " or " + items[-1]


def choice(prompt, options, read, write, default=None):
    """The error names the keys the prompt shows (e.g. "Enter, R or B"), not internal option values."""
    shown = re.findall(r"\[([^\]]+)\]", prompt) or list(options)
    while True:
        value = read(prompt).strip().lower()
        if not value and default is not None:
            return default
        if value in options:
            return value
        write(f"Please choose {or_list(shown)}.")


def nonempty(prompt, read, write):
    while True:
        value = read(prompt).strip()
        if value:
            return value
        write("Please enter a value, or use /back to return to the menu.")


def unknown_codes(codes, catalog):
    return [code for code in codes if code not in catalog]


def missing_value(field, catalog, read, write):
    """Parse only the requested field; blanks never imply an empty transcript.

    Courses to take or check must be in the catalogue, so a typo is asked again here instead of
    becoming an out-of-scope refusal. Completed courses are not checked: the solver warns about and
    ignores unknown ones, and old codes from earlier years may be missing."""
    ay = str(catalog.data["acad_year"]).replace("-", "/")
    while True:
        asked = MISSING_PROMPTS[field]
        if field in ("completed", "must_take"):   # replace the solver's own bracketed hint, not add a second one
            asked = re.sub(r"\s*\([^)]*\)$", "", asked) + ' (comma-separated codes, or "none")'
        value = nonempty(f"Please give {asked}: ", read, write)
        if field in ("completed", "must_take"):
            if value.lower() == "none":
                return []
            if value.lower() in ("no", "n/a", "unknown"):
                write('Enter course codes, or explicitly enter "none".')
                continue
            codes = [item.strip().upper() for item in re.split(r"[,\s]+", value) if item.strip()]
            if not (codes and all(re.fullmatch(r"[A-Z]{2,}\d{4}[A-Z]*", code) for code in codes)):
                write('Use course codes such as CS1101S, or enter "none".')
            elif field == "must_take" and unknown_codes(codes, catalog):
                unknown = ", ".join(unknown_codes(codes, catalog))
                write(f"Not in the AY{ay} catalogue: {unknown}. Please check the codes.")
            else:
                return codes
        elif field == "target":
            if not re.fullmatch(r"[A-Za-z]{2,}\d{4}[A-Za-z]*", value):
                write("Enter one course code.")
            elif value.upper() not in catalog:
                write(f"{value.upper()} is not in the AY{ay} catalogue. Please check the code.")
            else:
                return value.upper()
        else:
            match = re.fullmatch(r"(?:[Yy]([1-9]\d*)[Ss]([12])|([1-9]\d*))", value)
            if match:
                return (int(match[1]) - 1) * 2 + int(match[2]) if match[1] else int(match[3])
            write("Enter a semester number (1 to 8) or a year/semester such as Y2S1.")


def get_translation(request, translate, read, write):
    while True:
        write("\nTranslating your request...")
        try:
            return translate(request), None
        except RuntimeError as error:
            write(f"\n  Problem: {error}")
            action = choice("\n[T] Retry translation  [R] Replace request  [B] Back: ", ("t", "r", "b"), read, write)
            if action != "t":
                return None, action


def review_request(query, spec, catalog, read, write):
    while True:
        early, cleaned, warnings = prepare(spec, catalog)
        if early and early["status"] != "MISSING_INFO":
            write(format_answer({**early, "warnings": warnings} if warnings else early, catalog))
            return choice("\n[R] Replace request  [B] Back: ", ("r", "b"), read, write)
        if spec["query"] != query:
            write(f"\nYour request was interpreted as: {QUERY_NAMES[spec['query']]}.")
            action = choice("[S] Switch to that query  [R] Replace request  [B] Back: ",
                            ("s", "r", "b"), read, write)
            if action != "s":
                return action
            query = spec["query"]
        if early:
            write("\nI need a little more information to answer this.")
            for field in early["missing"]:
                spec = {**spec, field: missing_value(field, catalog, read, write)}
            continue
        write(summary(spec, cleaned, warnings))
        action = choice("\n[Enter] Solve  [R] Replace request  [B] Back: ", ("s", "r", "b"), read, write, default="s")
        if action != "s":
            return action
        write("\nWorking out the answer...")
        answer = run(spec, catalog)
        write(format_answer(answer, catalog, completed=cleaned["completed"]))
        if answer["status"] == "PLAN" and any(answer["plan"].values()):
            offer_bidding(spec, cleaned, catalog, read, write)
        return "done"


def bidding_answers(spec, catalog):
    """The bidding policy (solver/mdp.py) under both probability scenarios."""
    return {estimator: bidding_policy(spec, catalog, Admission.load(estimator)) for estimator in (LOW, HIGH)}


def offer_bidding(spec, cleaned, catalog, read, write):
    """After a plan: offer the chance of getting its courses, and what to bid for if a bid fails."""
    reasons = unsupported_reasons(cleaned)
    if reasons:
        write("\n" + wrap("A check of your chances of getting these courses is not available for this request: "
                          + "; ".join(reasons) + "."))
        return
    action = choice("\n[C] Check my chances of getting these courses  [Enter] Back to menu: ", ("c", "m"),
                    read, write, default="m")
    if action == "c":
        write("\nWorking out your chances (this can take a few seconds)...")
        write(format_bidding(bidding_answers(spec, catalog), catalog))


def handle_request(query, translate, catalog, read, write):
    """A revision replaces the whole request; no transcript or spec leaks between requests."""
    while True:
        request = nonempty(f"\nDescribe your request in one line. For example:\n  {EXAMPLES[query]}\n> ",
                           read, write)
        request = f"Selected task: {QUERY_NAMES[query]}.\nStudent request: {request}"
        spec, action = get_translation(request, translate, read, write)
        if action is None:
            action = review_request(query, spec, catalog, read, write)
        if action != "r":
            return


def run_session(translate: Callable, catalog, read=input, write=print):
    """Inject input/output and translation so the full session can be tested offline."""
    def ask(prompt):
        value = read(prompt)
        if value.strip().lower() == "/back":
            raise BackToMenu
        if value.strip().lower() == "/quit":
            raise QuitSession
        return value

    ay = str(catalog.data["acad_year"]).replace("-", "/")   # same form as the solver's refusal message
    write(heading(f"NUS course planner for BComp (CS) Hons AY{ay}").lstrip("\n"))
    write("  Type /back to return to the menu or /quit to exit at any prompt.")
    try:
        while True:
            try:
                write(MENU)
                selected = choice("> ", ("1", "2", "3"), ask, write)
                if selected == "3":
                    break
                handle_request("eligible" if selected == "1" else "plan", translate, catalog, ask, write)
            except BackToMenu:
                continue
    except (EOFError, KeyboardInterrupt, QuitSession):
        write("\nSession ended.")
    write("Goodbye.")


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check course eligibility or plan remaining courses in natural language.")
    parser.add_argument("--timeout", type=positive_int, default=60,
                        help="API timeout in seconds per attempt (default: 60)")
    parser.add_argument("--retries", type=int, choices=range(3), default=1, help="API retries, 0 to 2 (default: 1)")
    parser.add_argument("--max-tokens", type=positive_int, default=DEFAULT_MAX_TOKENS,
                        help="Maximum translation reply tokens")
    args = parser.parse_args(argv)
    load_env()
    model, base, key = (os.environ.get(name) for name in ("LLM_MODEL", "LLM_BASE_URL", "LLM_API_KEY"))
    if not (model and base and key):
        print("Set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL in the project-root .env (see .env.example).")
        return 2

    def translate(request):
        return translate_request(request, model=model, base_url=base, key=key, max_tokens=args.max_tokens,
                                 timeout=args.timeout, retries=args.retries)

    enable_line_editing()
    run_session(translate, Catalog.load())
    return 0


def enable_line_editing():
    """Importing readline gives input() cursor movement and in-session history; not available on Windows."""
    try:
        import readline  # noqa: F401
    except ImportError:
        pass
