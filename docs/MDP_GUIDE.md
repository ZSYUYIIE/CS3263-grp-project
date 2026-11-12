# Bidding under uncertainty (MDP extension)

The CP-SAT plan assumes the student gets every course in it. At NUS a course is bid for in CourseReg, and a
bid for a popular course can fail. This extension models that as a Markov decision process (MDP) and
answers with a **policy**: what to bid for now, and what to bid for next given what was obtained.

It is an add-on to the solver. It is not a pipeline, it does not change the spec, and `solver.run.run`,
pipelines A and B, the instance files and the checker do not use it.

Contents:

1. What question it answers
2. Formulation
3. Where the probabilities come from
4. How to call it
5. Worked example
6. Experiment: plan, replan or policy
7. Size of the problem
8. Assumptions and limits

## 1. What question it answers

The input is an ordinary Q2 spec (`"query": "plan"`). The output says:

- how likely the CP-SAT plan is to work exactly as written;
- which courses to bid for in the current semester to finish as early as possible in expectation;
- what to bid for next semester for each way the bids can turn out;
- the probability of finishing by semester 8, and the distribution of the finishing semester.

## 2. Formulation

Let `K` be the courses to schedule: the `must_take` courses not yet completed and the prerequisites CP-SAT
adds for them. CP-SAT decides *which* courses; the MDP decides *when to bid*.

| Element | Definition |
|---|---|
| State | `(s, G)`: semester `s` in `current_sem … 9` and the set `G ⊆ K` obtained so far |
| Action | a bid `a ⊆ K \ G`: every course is offered in the term of `s`, has its prerequisites in `completed ∪ G`, has its corequisites in `completed ∪ G ∪ a`, no two courses exclude each other, and the MC total is within the cap of `s` |
| Transition | each course `c ∈ a` is obtained independently with probability `p(c, term of s)`; the next state is `(s+1, G ∪ obtained)` |
| Cost | 1 for every semester started before all `must_take` courses are obtained |
| Terminal | cost 0 once `must_take ⊆ completed ∪ G`; cost `overrun` (default 2 semesters, one more academic year) in semester 9 otherwise |

Bellman equation, solved exactly by backward induction with memoisation over the reachable states:

```
V(s, G) = 0                                              if must_take ⊆ completed ∪ G
V(9, G) = overrun                                        otherwise
V(s, G) = min over bids a of  1 + Σ_G' P(G' | G, a) · V(s+1, G')
```

The policy is the minimising bid in each state. Ties go to the first bid in a fixed order, so the answer is
reproducible.

**The CSP is the special case `p = 1`.** Then every transition is certain, `V(current_sem, ∅)` is the number
of semesters CP-SAT needs, and the policy is one plan. `tests/test_mdp.py` checks this on all 45 committed
requests that have a plan, and checks the plan the policy follows with the independent checker.

**Only the largest bids are searched.** A bid costs nothing and holding an extra course never hurts, so a
bid that has room for one more course is never better than the larger bid. The search keeps only bids that
cannot be extended. A test compares this against searching every bid.

## 3. Where the probabilities come from

**Source.** The NUS Registrar publishes a *Course Class Demand and Allocation Report* for every CourseReg
round. We used the undergraduate "Select Courses" reports for rounds 1 to 3 of both semesters of AY2024/25
and AY2025/26 (12 reports), taken from the mirror at <https://courserekt.vercel.app/>.
`data/demand/allocation.csv` holds the 4,336 report rows for courses in our catalogue, one row per report
line ([`data/demand/README.md`](../data/demand/README.md)).

**What a row says.** For one class of one course in one round: `vacancy`, `demand`, the students allocated
from their main list (`main`) and from their reserve list (`reserve`), and the students not allocated because
the class was full (`quota`), or because of a timetable clash, their workload limit, or other reasons. In
every row `demand = main + quota + timetable + workload + others`, so reserve-list allocations are counted
outside `demand`.

**Estimate.** For one course, one academic year and one round, summed over the course's classes:

```
contested = main + quota
unmet     = max(0, quota − reserve)
```

A student turned away from a full class is usually placed in another class of the same course through the
reserve list. Example: CS2105, Semester 2 of AY2025/26, round 1. Class L2 turned away 37 students and class
L1 took 35 from reserve lists, so 2 students went without the course, not 37. The failure rate of a round is
`unmet / contested`, pooled over the two academic years. Two estimates are built from it:

| Estimator | Probability of getting the course | Reading |
|---|---|---|
| `round1` | `1 − f₁` | the student bids once; pessimistic |
| `all_rounds` (default) | `1 − f₁·f₂·f₃` | the student bids again in every round, and the rounds are independent; optimistic |

The truth lies between them, so the experiment reports both. Example, CS4248 in Semester 1: round 1 turned
away 55 of 226, round 2 turned away 10 of 38 and round 3 turned away 17 of 31. `round1` gives 0.757 and
`all_rounds` gives 0.965.

**Coverage.** Of the 319 course-terms that can be planned, 253 have report rows. Under `all_rounds` 43 of them
have `p < 1` (4 below 0.9). Under `round1` 81 have `p < 1` (41 below 0.9). A course-term with no rows is
treated as certain and is listed under `model.no_data` in the answer.

**Limits of the estimate.**

- Past rounds are used to predict AY2026/27. Demand and vacancies change from year to year.
- Allocation priority (seniority, programme requirements) is ignored. Every bidder gets the same probability.
- Students placed before round 1 are not in these reports. For a first-year core course the reports show only
  the few students who had to bid, so `round1` makes such a course look more contested than it is for a CS
  student (CS1101S: 0.45).
- A reserve-list place is counted against the overflow of the same course. Some of those places go to
  students whose main choice was a different course.
- Timetable clashes, workload limits and "others" are not counted as competition.

## 4. How to call it

```bash
python -m solver.mdp examples/q2_bidding.json                       # all_rounds estimate
python -m solver.mdp examples/q2_bidding.json --estimator round1
python -m solver.mdp examples/q2_bidding.json --p CS4248=0.6        # set one probability by hand
python -m solver.mdp examples/q2_bidding.json --overrun 10          # weigh a late finish more
```

```python
from solver.admission import Admission
from solver.mdp import solve

answer = solve(spec)                                             # Admission.load("all_rounds")
answer = solve(spec, admission=Admission.load("round1"))
answer = solve(spec, admission=Admission.from_dict({"CS4248": 0.6}))
```

**Statuses.** `POLICY`, or the solver's own `INVALID_SPEC`, `OUT_OF_SCOPE`, `MISSING_INFO` and `NO_PLAN`
passed through unchanged. `UNSUPPORTED` is returned for a Q1 request and for a spec with a `must` rule,
`atap_sems` or `mc_min`. `TOO_LARGE` is returned if the search passes 200,000 states.

**Fields of a `POLICY` answer.**

| Field | Meaning |
|---|---|
| `estimator` | which probabilities were used |
| `first_bid` | the semester and the courses to bid for now |
| `if_then` | for each way the first bid can turn out: its probability, what was obtained and missed, and the next bid |
| `alternatives` | up to five first bids with their expected cost, best first |
| `expected_cost` | `V(current_sem, ∅)`: expected semesters used, with a late finish counted as `overrun` more |
| `on_time_probability` | probability of finishing by semester 8 |
| `finish_distribution` | probability of finishing in each semester, and `late` |
| `expected_last_semester` | mean finishing semester among the outcomes that finish by semester 8 |
| `admission` | the probabilities below 1 of the courses involved, by term |
| `deterministic` | the CP-SAT answer: `last_semester`, `plan`, and `success_probability`, the chance that every bid of that plan succeeds as scheduled |
| `model` | number of courses, the uncertain ones, courses without data, states evaluated, `overrun` |
| `notes`, `not_applied`, `warnings` | as in a Q2 answer; preferences (`prefer` rules, `early`, `late`) are listed in `not_applied` |

The objective of the spec only decides which courses are needed. The policy always minimises the expected
finishing semester, and a note says so when the objective is not `earliest_graduation`.

## 5. Worked example

`examples/q2_bidding.json`: a student in semester 5 who has completed CS1101S, CS1231S, MA1521, MA1522,
CS2030S, CS2040S, ST2334, CS2100 and CS2103T, still needs CS2109S, CS3263, CS4246, CS4248, CS2106, CS2105 and
CS3230, and takes at most 12 MC of them a semester.

CP-SAT answers: finish in semester 7. The chain CS2109S → CS3263 → CS4246 needs three semesters, so CS2109S
must be obtained in semester 5.

| | `all_rounds` | `round1` |
|---|---|---|
| Probability the CP-SAT plan works as written | 0.951 | 0.603 |
| First bid of the policy | CS2105, CS2106, CS2109S | CS2105, CS2109S, CS3230 |
| Finish in semester 7 | 0.9998 | 0.933 |
| Finish in semester 8 | 0.0002 | 0.049 |
| Not done by semester 8 | below 0.0001 | 0.018 |
| States evaluated | 15 | 111 |

Under `round1` the three first bids that contain CS2109S all cost about 3.10 semesters in expectation, and
the bid without it costs 4.44. The policy also gives the next step for each outcome. If CS2105 is missed
(probability 0.025), the next bid is CS2105, CS3263 and CS4248. If CS2109S is missed (0.001), the next bid is
CS2106 and CS2109S.

## 6. Experiment: plan, replan or policy

```bash
python -m experiments.run_mdp --out rows.csv
```

For each of the 45 requests in `instances/instances.json` that have a plan, three ways of acting are compared
in the same model of failed bids:

- **plan**: follow the CP-SAT plan as written. It works only if every bid succeeds.
- **replan**: bid for the first semester of the CP-SAT plan, then ask CP-SAT again every semester with the
  courses actually obtained.
- **mdp**: the optimal policy.

Every request is solved for earliest graduation and without its preferences, so the three aim at the same
thing. Outcomes are computed exactly by pushing probability forward through the semesters, not by sampling,
and two runs give the same rows.

| | `all_rounds` | `round1` |
|---|---|---|
| Requests with at least one uncertain course | 40 of 45 | 45 of 45 |
| Mean probability the plan works as written | 0.960 | 0.714 |
| Mean on-time probability, replan with CP-SAT | 0.988 | 0.875 |
| Mean on-time probability, MDP policy | 0.997 | 0.912 |
| MDP better / equal / worse than replan | 10 / 35 / 0 | 23 / 22 / 0 |
| Largest gain | 0.877 → 1.000 (`q2-tight-06`) | 0.710 → 0.932 (`q2-tight-02`) |
| CP-SAT calls made by replan, all requests | 533 | 3,657 |

What the numbers say:

- A deterministic plan is fragile mainly when it ends in semester 8, where one failed bid means a late finish.
- Replanning recovers most of the loss. The rest comes from tie-breaking: many plans are equally good to
  CP-SAT, and it does not know that bidding for a contested course early leaves time to try again.
- Replanning can even do worse than keeping the first plan (3 requests), because every new plan breaks ties
  afresh and can move a course into a term where it is harder to get.
- Under the optimistic estimate the gain is small on average (0.988 to 0.997). The extension matters for
  tight plans and contested courses, and little otherwise.
- The MDP is optimal for expected cost within the courses CP-SAT chose. It was never worse than replanning on
  on-time probability in this set, but that is an observation, not a guarantee.

## 7. Size of the problem

With `n` courses to schedule and `k` semesters left there are at most `k · 2ⁿ` states. A bid with `u`
uncertain courses has `2ᵘ` outcomes. A 20 MC cap holds five 4 MC courses, so a bid usually has at most 32.

In the 45 requests `n` is 8 on average and at most 14. The states actually reached are far fewer than the
bound, because prerequisites and offering terms rule most sets out:

| | `all_rounds` | `round1` |
|---|---|---|
| States evaluated, median | 27 | 142 |
| States evaluated, largest | 9,295 | 16,170 |
| Slowest policy | 1.4 s | 3.7 s |

Fixing the course set with CP-SAT first is what keeps `n` small. A first prototype that let the MDP choose
among all prerequisite alternatives (20 or more courses) did not finish in several minutes.

## 8. Assumptions and limits

- **Independence.** Bids succeed independently across courses and semesters, with the same probability for
  every student.
- **A failed bid wastes its place.** The student cannot swap in another course in the same semester. In
  CourseReg a student could pick a replacement in a later round, so the cost of a failure is overstated.
- **Fixed course set.** The policy never switches to an alternative prerequisite route. A test run with such
  alternatives added found no case where the policy used one in the worked example, because the alternatives
  were ruled out by preclusions.
- **Risk.** The cost is expected semesters plus `overrun` for a late finish. A student who cares more about
  finishing on time than about finishing early can raise `--overrun`.
- **Not covered.** `must` rules, ATAP and `mc_min` give `UNSUPPORTED`. Preferences are not applied.
- **No LLM comparison.** Pipelines A and B were not run on this question. The spec is unchanged, so a spec
  written by pipeline B can be passed to `solver.mdp.solve` as it is.
- **Semester rules are restated.** `BiddingMDP.legal` and `bids` apply the offering, prerequisite,
  corequisite, exclusion and MC-cap rules to one semester. A change to those hard rules must be made here too.
