"""Bidding MDP (solver/mdp.py), its probabilities (solver/admission.py) and the report extraction.

The main guard is `test_certain_bids_reproduce_cpsat`: with every probability equal to 1 the MDP
must give the CP-SAT last semester on every committed request that has a plan, and the plan it
follows must pass the independent checker.
"""
import argparse
import copy
import json
from pathlib import Path

import pytest

import solver.mdp
from eval.checker import check_plan
from experiments.extract_demand import parse_report
from experiments.run_mdp import for_graduation, row_of
from m1_data.catalog import Catalog
from solver.admission import ESTIMATORS, Admission, estimate, failure_rates, read_rows
from solver.common import LAST_SEM
from solver.mdp import LATE, OVERRUN_SEMESTERS, build, expected_last, missing_value, on_time, solve
from solver.run import run

ROOT = Path(__file__).resolve().parent.parent
INSTANCES = json.loads((ROOT / "instances" / "instances.json").read_text())
PLANS = [r for r in INSTANCES if r["gold_answer"]["status"] == "PLAN"]
EXAMPLE = json.loads((ROOT / "examples" / "q2_bidding.json").read_text())
HAND = {"CS2109S": 0.88, "CS4248": 0.60, "CS2106": 0.81, "CS2105": 0.90}
START = frozenset()


@pytest.fixture(scope="module")
def cat():
    return Catalog.load()


def one_course(**changes):
    spec = {"query": "plan", "current_sem": 7, "completed": ["CS2100"], "must_take": ["CS2106"]}
    spec.update(changes)
    return spec


def row(code="CS9999", semester=1, round_no=1, year="2024-2025", klass="L1", main=0, reserve=0, quota=0):
    return {"acad_year": year, "semester": str(semester), "round": str(round_no), "code": code, "class": klass,
            "vacancy": "0", "demand": str(main + quota), "main": str(main), "reserve": str(reserve),
            "quota": str(quota), "timetable": "0", "workload": "0", "others": "0"}


# ---- probabilities --------------------------------------------------------------------------------

def test_overflow_of_one_class_is_absorbed_by_the_reserve_list_of_another():
    rows = [row(klass="L1", main=324, reserve=35), row(klass="L2", main=10, quota=37)]
    assert failure_rates(rows) == {("CS9999", 1): {1: (2, 371)}}


def test_reserve_places_never_make_the_failure_count_negative():
    rows = [row(klass="L1", main=50, reserve=9)]
    assert failure_rates(rows)[("CS9999", 1)][1] == (0, 50)


def test_years_are_pooled_but_overflow_is_netted_within_a_year():
    rows = [row(year="2024-2025", main=90, quota=10), row(year="2025-2026", main=100, reserve=8)]
    assert failure_rates(rows)[("CS9999", 1)][1] == (10, 200)


def test_the_two_estimators():
    rounds = {1: (40, 100), 2: (5, 10), 3: (0, 0)}
    assert estimate(rounds, "round1") == 0.6
    assert estimate(rounds, "all_rounds") == 0.8       # 1 - 0.4 * 0.5; round 3 has no bidders
    assert estimate({2: (1, 4)}, "round1") is None     # no round-1 evidence
    assert estimate({}, "all_rounds") is None


def test_committed_rows_are_consistent_and_complete(cat):
    rows = read_rows()
    reports = {(r["acad_year"], r["semester"], r["round"]) for r in rows}
    assert len(reports) == 12                          # two years, two semesters, three rounds
    for r in rows:
        counted = sum(int(r[k]) for k in ("main", "quota", "timetable", "workload", "others"))
        assert int(r["demand"]) == counted, r
        assert r["code"] in cat


def test_loaded_tables_are_probabilities_and_ordered():
    optimistic, pessimistic = Admission.load("all_rounds"), Admission.load("round1")
    assert optimistic.table and pessimistic.table
    for key, p in pessimistic.table.items():
        assert 0.0 <= p <= 1.0
        assert optimistic.table[key] >= p, key
    assert not optimistic.known("CS9999", 3)
    with pytest.raises(ValueError):
        Admission.load("made_up")


def test_a_course_term_without_rows_gets_the_stated_fallback_not_certainty():
    for estimator in ESTIMATORS:
        mean = Admission.load(estimator)
        expected = round(sum(mean.table.values()) / len(mean.table), 3)
        assert mean.missing == expected < 1.0 and mean.missing_rule == "mean"
        assert mean.p("CS9999", 3) == expected and not mean.known("CS9999", 3)
        assert Admission.load(estimator, missing="certain").p("CS9999", 3) == 1.0
        assert Admission.load(estimator, missing=0.7).p("CS9999", 3) == 0.7
        assert Admission.load(estimator, missing=0.7).table == mean.table
    assert Admission.load("round1").missing <= Admission.load("all_rounds").missing
    for bad in ("median", 1.5, -0.1):
        with pytest.raises(ValueError):
            Admission.load(missing=bad)
    assert Admission.from_dict({"CS4248": 0.6}).p("CS2106", 5) == 1.0     # a hand table names the uncertain ones
    assert Admission.certain().p("CS2106", 5) == 1.0
    assert missing_value("mean") == "mean" and missing_value("0.9") == 0.9
    with pytest.raises(argparse.ArgumentTypeError):
        missing_value("2")


def test_the_answer_says_the_probabilities_are_an_approximate_scenario(cat):
    for estimator in ESTIMATORS:
        answer = solve(EXAMPLE, cat, Admission.load(estimator))
        assert answer["scenario"].startswith(f"approximate scenario '{estimator}'")
        assert "AY2024/25 and AY2025/26" in answer["scenario"]
    certain = solve(EXAMPLE, cat, Admission.load(missing="certain"))
    assert "treated as certain" in certain["scenario"]
    assert solve(EXAMPLE, cat, Admission.certain())["scenario"] == "every bid succeeds"
    assert "set by hand" in solve(EXAMPLE, cat, Admission.from_dict(HAND))["scenario"]


def test_from_dict_by_course_or_by_term():
    table = Admission.from_dict({"cs4248": 0.6, "CS2106": {"1": 1.0, "2": 0.8}})
    assert table.p("CS4248", 5) == table.p("CS4248", 6) == 0.6
    assert (table.p("CS2106", 5), table.p("CS2106", 6)) == (1.0, 0.8)
    with pytest.raises(ValueError):
        Admission.from_dict({"CS4248": 1.2})


def test_report_rows_are_parsed_and_checked():
    head = ("  Undergraduate Courses, Select Courses (Round 2)\n  Semester 1, AY2025/2026\n")
    line = "   Computer Science   CS4248   Natural Language Processing   L1   22   32   22   0   10   0   0   0\n"
    assert parse_report(head + line) == [{
        "acad_year": "2025-2026", "semester": 1, "round": 2, "code": "CS4248", "class": "L1", "vacancy": "22",
        "demand": 32, "main": 22, "reserve": 0, "quota": 10, "timetable": 0, "workload": 0, "others": 0}]
    with pytest.raises(ValueError):
        parse_report(head + line.replace("   10   0   0   0", "   9   0   0   0"))
    with pytest.raises(ValueError):
        parse_report(line)


# ---- the MDP ------------------------------------------------------------------------------------

def test_certain_bids_reproduce_cpsat(cat):
    assert len(PLANS) == 45
    for r in PLANS:
        early, mdp, plan_answer, _ = build(r["gold_spec"], cat, Admission.certain())
        assert early is None, r["id"]
        cost = mdp.value(mdp.start, START)
        assert mdp.evaluate() == {mdp.start - 1 + int(cost): 1.0}, r["id"]
        gold = r["gold_answer"]["last_semester"]
        if r["gold_spec"].get("objective") == "earliest_graduation":
            assert mdp.start - 1 + cost == gold, r["id"]
        elif gold is not None:
            assert mdp.start - 1 + cost <= gold, r["id"]

        got, plan = START, {}
        for semester in range(mdp.start, LAST_SEM + 1):
            if mdp.finished(got):
                break
            plan[str(semester)] = list(mdp.policy(semester, got))
            got |= set(plan[str(semester)])
        assert mdp.finished(got), r["id"]
        assert check_plan(r["gold_spec"], plan) == [], r["id"]


def test_one_course_two_tries_matches_the_closed_form(cat):
    _, mdp, _, _ = build(one_course(), cat, Admission.from_dict({"CS2106": 0.5}))
    assert mdp.evaluate() == {7: 0.5, 8: 0.25, LATE: 0.25}
    assert mdp.value(7, START) == pytest.approx(0.5 * 1 + 0.25 * 2 + 0.25 * (2 + OVERRUN_SEMESTERS))
    answer = solve(one_course(), cat, Admission.from_dict({"CS2106": 0.5}))
    assert answer["status"] == "POLICY"
    assert answer["first_bid"] == {"semester": 7, "courses": ["CS2106"]}
    assert answer["on_time_probability"] == 0.75
    assert answer["deterministic"] == {"last_semester": 7, "plan": {"7": ["CS2106"]}, "success_probability": 0.5}


def test_worked_example_matches_an_independent_calculation(cat):
    """Numbers from a separate brute-force script written before this module (all bids, own rules)."""
    _, mdp, _, _ = build(EXAMPLE, cat, Admission.from_dict(HAND), overrun=10)
    assert mdp.value(5, START) == pytest.approx(4.171, abs=5e-4)
    assert set(mdp.policy(5, START)) == {"CS2109S", "CS2106", "CS2105"}
    finish = mdp.evaluate()
    assert finish[7] == pytest.approx(0.720, abs=5e-4)
    assert finish[8] == pytest.approx(0.191, abs=5e-4)
    assert on_time(finish) == pytest.approx(0.911, abs=5e-4)
    assert expected_last(finish) == pytest.approx((7 * finish[7] + 8 * finish[8]) / on_time(finish))


@pytest.mark.parametrize("estimator", ESTIMATORS)
def test_value_is_the_cost_of_the_optimal_policy(cat, estimator):
    _, mdp, _, _ = build(EXAMPLE, cat, Admission.load(estimator))
    finish = mdp.evaluate()
    assert sum(finish.values()) == pytest.approx(1.0)
    assert mdp.expected_cost(finish) == pytest.approx(mdp.value(mdp.start, START))


def test_keeping_only_the_largest_bids_does_not_change_the_value(cat):
    for spec in [EXAMPLE, *(r["gold_spec"] for r in PLANS[:12])]:
        admission = Admission.load("round1")
        _, pruned, _, _ = build(spec, cat, admission)
        _, full, _, _ = build(spec, cat, admission, all_bids=True)
        assert pruned.value(pruned.start, START) == pytest.approx(full.value(full.start, START))
        assert len(pruned.bids(pruned.start, START)) <= len(full.bids(full.start, START))


def test_a_lower_probability_or_a_higher_overrun_never_helps(cat):
    def cost(table, overrun=2):
        _, mdp, _, _ = build(EXAMPLE, cat, Admission.from_dict(table), overrun=overrun)
        return mdp.value(mdp.start, START)

    assert cost({}) == 3.0
    assert cost({}) <= cost(HAND) <= cost({**HAND, "CS4248": 0.3})
    assert cost(HAND, overrun=2) <= cost(HAND, overrun=10)


def test_the_chain_head_is_bid_for_first(cat):
    answer = solve(EXAMPLE, cat, Admission.from_dict(HAND))
    assert "CS2109S" in answer["first_bid"]["courses"]
    assert answer["alternatives"][0]["courses"] == answer["first_bid"]["courses"]
    costs = [a["expected_cost"] for a in answer["alternatives"]]
    assert costs == sorted(costs)
    without = [a for a in answer["alternatives"] if "CS2109S" not in a["courses"]]
    assert all(a["expected_cost"] > costs[0] for a in without)
    assert sum(row["probability"] for row in answer["if_then"]) == pytest.approx(1.0, abs=1e-3)
    assert answer["model"]["uncertain"] == sorted(HAND)


def test_a_policy_that_breaks_a_rule_is_rejected(cat):
    _, mdp, _, _ = build(EXAMPLE, cat, Admission.certain())
    with pytest.raises(ValueError, match="CS3263 cannot be taken"):
        mdp.evaluate(lambda semester, got: ("CS3263",))
    with pytest.raises(ValueError, match="more than 12 MC"):
        mdp.evaluate(lambda semester, got: ("CS2109S", "CS2106", "CS2105", "CS3230"))


# ---- answers that are not a policy -----------------------------------------------------------------

def test_answers_of_the_solver_pass_through(cat):
    assert solve({"query": "plan"}, cat)["status"] == "MISSING_INFO"
    assert solve({"query": "plan", "colour": "red"}, cat)["status"] == "INVALID_SPEC"
    assert solve(one_course(programme="BComp CS with a second major in Mathematics"), cat)["status"] == "OUT_OF_SCOPE"
    no_plan = one_course(current_sem=8, must_take=["CS2106", "CS3211"])
    assert solve(no_plan, cat) == run(no_plan, cat)
    assert solve(no_plan, cat)["status"] == "NO_PLAN"


def test_requests_outside_the_model_are_unsupported(cat):
    eligible = {"query": "eligible", "target": "CS2106", "completed": ["CS2100"]}
    assert solve(eligible, cat)["status"] == "UNSUPPORTED"
    must = one_course(rules=[{"type": "in_sem", "course": "CS2106", "sem": 8, "strength": "must"}])
    assert solve(must, cat) == {"status": "UNSUPPORTED", "reasons": ["must rules are not modelled under uncertainty"]}
    assert solve(one_course(atap_sems=[7]), cat)["status"] == "UNSUPPORTED"
    assert solve(one_course(mc_min=4), cat)["status"] == "UNSUPPORTED"


def test_preferences_are_reported_as_not_applied(cat):
    spec = one_course(objective="none", late=["CS2106"], unsupported=["no 8am classes"])
    answer = solve(spec, cat, Admission.certain())
    assert answer["not_applied"] == ["no 8am classes", "preference: CS2106 as late as possible"]
    assert any("objective 'none'" in note for note in answer["notes"])
    assert answer["first_bid"]["courses"] == ["CS2106"]


def test_nothing_left_to_take(cat):
    answer = solve(one_course(completed=["CS2100", "CS2106"]), cat, Admission.certain())
    assert answer["status"] == "POLICY"
    assert answer["first_bid"]["courses"] == [] and answer["on_time_probability"] == 1.0
    assert answer["expected_last_semester"] is None and answer["finish_distribution"] == {}
    assert answer["expected_cost"] == 0.0 and answer["alternatives"] == [] and answer["if_then"] == []


def test_a_search_past_the_state_limit_is_reported(cat, monkeypatch):
    monkeypatch.setattr(solver.mdp, "MAX_STATES", 3)
    answer = solve(EXAMPLE, cat, Admission.from_dict(HAND))
    assert answer["status"] == "TOO_LARGE" and "7 courses" in answer["reasons"][0]


def test_course_terms_without_report_rows_are_listed_with_the_value_used(cat):
    table = Admission.load("round1")
    del table.table[("CS2106", 1)], table.table[("CS2106", 2)]
    answer = solve(one_course(), cat, table)
    assert answer["model"]["no_data"] == {"CS2106": [1, 2]} and answer["model"]["no_data_p"] == table.missing
    assert answer["admission"] == {"CS2106": {"1": table.missing, "2": table.missing}}
    assert answer["on_time_probability"] == round(1 - (1 - table.missing) ** 2, 3)
    one_term = Admission.load("round1")
    del one_term.table[("CS2106", 2)]
    assert solve(one_course(), cat, one_term)["model"]["no_data"] == {"CS2106": [2]}
    given = solve(one_course(), cat, Admission.from_dict({"CS2100": 0.5}))
    assert given["model"]["no_data"] == {} and given["model"]["no_data_p"] is None


def test_the_default_penalty_does_not_gamble_on_a_single_try(cat):
    """q2-tight-14, round1: with overrun 2 the policy tries CS4234 once, to finish in semester 7 if it
    succeeds; the default penalty bids for it in semester 5 so that it can be tried twice."""
    spec = for_graduation(next(r for r in PLANS if r["id"] == "q2-tight-14")["gold_spec"])
    admission = Admission.load("round1")
    _, gamble, _, _ = build(spec, cat, admission, overrun=2)
    _, default, _, _ = build(spec, cat, admission)
    assert "CS4234" not in gamble.policy(5, START) and "CS4234" in default.policy(5, START)
    assert on_time(default.evaluate()) > on_time(gamble.evaluate()) + 0.1


def test_the_spec_is_not_changed(cat):
    spec = copy.deepcopy(EXAMPLE)
    solve(spec, cat)
    assert spec == EXAMPLE


# ---- the experiment --------------------------------------------------------------------------------

def test_experiment_row(cat):
    spec = for_graduation({"objective": "none", "early": ["X"], "rules": [], "mc_max": 8})
    assert spec == {"objective": "earliest_graduation", "mc_max": 8}
    instance = next(r for r in PLANS if r["id"] == "q2-tight-04")
    result = row_of(instance, "round1", Admission.load("round1"), cat)
    assert result["mdp_cost"] <= result["replan_cost"] + 1e-9
    assert 0.0 <= result["plan_success"] <= 1.0 and result["cpsat_calls"] >= 1
    assert result["mdp_on_time"] > result["replan_on_time"]
