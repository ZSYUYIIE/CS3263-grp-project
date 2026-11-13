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
- which courses to bid for in the current semester to finish as early as possible in expectation, with a
  late finish weighted heavily;
- what to bid for next semester for each way the bids can turn out;
- the probability of finishing by semester 8, and the distribution of the finishing semester;
- what the probabilities are (an approximate scenario) and which courses had no data.

## 2. Formulation

Let `K` be the courses to schedule: the `must_take` courses not yet completed and the prerequisites CP-SAT
adds for them. CP-SAT decides *which* courses; the MDP decides *when to bid*.

| Element | Definition |
|---|---|
| State | `(s, G)`: semester `s` in `current_sem … 9` and the set `G ⊆ K` obtained so far |
| Action | a bid `a ⊆ K \ G`: every course is offered in the term of `s`, has its prerequisites in `completed ∪ G`, has its corequisites in `completed ∪ G ∪ a`, no two courses exclude each other, and the MC total is within the cap of `s` |
| Transition | each course `c ∈ a` is obtained independently with probability `p(c, term of s)`; the next state is `(s+1, G ∪ obtained)` |
| Cost | 1 for every semester started before all `must_take` courses are obtained |
| Terminal | cost 0 once `must_take ⊆ completed ∪ G`; cost `overrun` (default 10 semesters, see below) in semester 9 otherwise |

Bellman equation, solved exactly by backward induction with memoisation over the reachable states:

```
V(s, G) = 0                                              if must_take ⊆ completed ∪ G
V(9, G) = overrun                                        otherwise
V(s, G) = min over bids a of  1 + Σ_G' P(G' | G, a) · V(s+1, G')
```

The policy is the minimising bid in each state. Ties go to the first bid in a fixed order, so the answer is
reproducible.

**Choosing the objective and the penalty.** Two objectives were considered: finish early on average with a
penalty for missing semester 8 (this one), and maximise the chance of finishing by semester 8.

- Maximising only the chance of finishing by semester 8 is a poor objective. A policy that finishes in
  semester 6 and one that finishes in semester 8 both count as on time, so most bids tie, the tie-break
  decides, and the policy can put off a course for no reason.
- Ranking first by that chance and then by the finishing semester removes the ties but is brittle: it gives
  up a whole semester for a negligibly smaller chance of finishing late.
- A finite penalty sits between the two. Compare finishing one semester sooner with probability `1 − q` (and
  late otherwise) with finishing one semester later for certain. The risky bid is cheaper exactly when
  `q < 1 / (1 + overrun)`: up to 33% more chance of a late finish at `overrun = 2`, about 9% at 10.

A late finish costs an extra semester of study, and finishing the `must_take` courses sooner does not by
itself mean graduating sooner, so the default is `overrun = 10`. Example, `q2-tight-14` under `round1`:
CS4234 is offered only in Semester 1 and is obtained with probability 0.653. With `overrun = 2` the policy
bids for it once, in semester 7, so as to finish in semester 7 if the bid succeeds; it finishes late with
probability 0.35. With 10 it bids for it in semester 5, so it can try again in semester 7; it finishes in
semester 8, late with probability 0.12. On the instance set `overrun` 4 and 10 give the same on-time
probability for every request, and 2 gives a lower one for two requests (section 6). `--overrun` changes it.

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

| Scenario | Probability of getting the course | Reading |
|---|---|---|
| `round1` | `1 − f₁` | the student bids once; the lower scenario |
| `all_rounds` (default) | `1 − f₁·f₂·f₃` | the student bids again in every round, and the rounds are independent; the higher scenario |

**These are approximate scenarios, not bounds.** `round1` is never above `all_rounds`, but the probability
for one student can lie outside both, for the reasons under *Limits of the estimate*. The experiment reports
both, and every answer says which one it used in `scenario`. Example, CS4248 in Semester 1: round 1 turned
away 55 of 226, round 2 turned away 10 of 38 and round 3 turned away 17 of 31. `round1` gives 0.757 and
`all_rounds` gives 0.965.

**Coverage.** Of the 319 course-terms that can be planned, 253 have report rows. Under `all_rounds` 43 of them
have `p < 1` (4 below 0.9). Under `round1` 81 have `p < 1` (41 below 0.9).

**Course-terms without rows.** The other 66 (21%) have no estimate. Having no rows does not show that a
course is uncontested. Ten of the courses the instance set needs have no rows in the terms they are offered:
CS2100HS, CS2101, CS2111, CS3227, CS3233, CS3281, CS3282, CS4212, CS4353 and CS4430. CS4212, for example,
is offered in Semester 2 in AY2026/27 but appears only in Semester 1 reports. Such a course-term is not
treated as certain. It gets a fallback, by default the mean over the course-terms that have an estimate
under the same scenario: 0.980 for `all_rounds` and 0.953 for `round1`. `--missing certain` or
`--missing 0.9` sets it otherwise. The answer lists each such course and its terms in `model.no_data`, with
the value used in `model.no_data_p`. 24 of the 45 requests need at least one. Treating them as certain, as
the first version did, raises the mean on-time probability of the policy from 0.992 to 0.997 (`all_rounds`)
and from 0.904 to 0.917 (`round1`).

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
python -m solver.mdp examples/q2_bidding.json --missing certain     # no report rows = certain
python -m solver.mdp examples/q2_bidding.json --overrun 2           # weigh a late finish less
```

```python
from solver.admission import Admission
from solver.mdp import solve

answer = solve(spec)                                             # Admission.load("all_rounds")
answer = solve(spec, admission=Admission.load("round1", missing=0.9))
answer = solve(spec, admission=Admission.from_dict({"CS4248": 0.6}))   # courses not given are certain
```

**Interactively.** In `python -m planner`, press `C` after a plan. The planner calls `solve` for both scenarios
and prints the answer as text (`planner/formatting.py`, `format_bidding`): chances as ranges from `round1` to
`all_rounds`, whole percentages that never round a small chance to 0% or an uncertain one to 100%, the
chance of finishing by the plan's last semester and by semester 8, the hardest courses (below 95% under
`round1`), the first bid and the next bid for the five likeliest outcomes, and the courses without report
rows. The advice (`first_bid`, `if_then`) is the `round1` policy, because it leaves time to bid again.

**Statuses.** `POLICY`, or the solver's own `INVALID_SPEC`, `OUT_OF_SCOPE`, `MISSING_INFO` and `NO_PLAN`
passed through unchanged. `UNSUPPORTED` is returned for a Q1 request and for a spec with a `must` rule,
`atap_sems` or `mc_min`. `TOO_LARGE` is returned if the search passes 200,000 states.

**Fields of a `POLICY` answer.**

| Field | Meaning |
|---|---|
| `estimator` | which probabilities were used |
| `scenario` | one sentence saying what they are: the approximate scenario, its source, and the value given to course-terms without report rows |
| `first_bid` | the semester and the courses to bid for now |
| `if_then` | for each way the first bid can turn out: its probability, what was obtained and missed, and the next bid |
| `alternatives` | up to five first bids with their expected cost, best first |
| `expected_cost` | `V(current_sem, ∅)`: expected semesters used, with a late finish counted as `overrun` more |
| `on_time_probability` | probability of finishing by semester 8 |
| `finish_distribution` | probability of finishing in each semester, and `late` |
| `expected_last_semester` | mean finishing semester among the outcomes that finish by semester 8 |
| `admission` | the probabilities below 1 of the courses involved, by term, fallbacks included |
| `deterministic` | the CP-SAT answer: `last_semester`, `plan`, and `success_probability`, the chance that every bid of that plan succeeds as scheduled |
| `model` | number of courses, the uncertain ones, `no_data` (course → terms without report rows) and `no_data_p` (the value they were given), states evaluated, `overrun` |
| `notes`, `not_applied`, `warnings` | as in a Q2 answer; preferences (`prefer` rules, `early`, `late`) are listed in `not_applied` |

The objective of the spec only decides which courses are needed. The policy always minimises the expected
finishing semester, with a late finish counted as `overrun` more semesters, and a note says so when the
objective is not `earliest_graduation`. Probabilities and expected values are shown with three decimals,
as many as the probabilities that go in, so an outcome below 0.0005 shows as 0.0 and is left out of
`if_then`.

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
| Finish in semester 7 | 1.000 | 0.933 |
| Finish in semester 8 | below 0.001 | 0.049 |
| Not done by semester 8 | below 0.001 | 0.018 |
| States evaluated | 15 | 111 |

Every course here has report rows, so `model.no_data` is empty. Under `round1` the three first bids that
contain CS2109S all cost 3.251 semesters in expectation, and the bid without it costs 6.212. The policy also
gives the next step for each outcome. If CS2105 is missed
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
and two runs give the same rows. The settings are the defaults: `overrun = 10`, and course-terms without
report rows get the mean (section 3). `--overrun` and `--missing` change them.

| | `all_rounds` | `round1` |
|---|---|---|
| Requests with at least one uncertain course | 43 of 45 | 45 of 45 |
| Requests with a course-term without report rows | 24 of 45 | 24 of 45 |
| Mean probability the plan works as written | 0.947 | 0.690 |
| Mean on-time probability, replan with CP-SAT | 0.980 | 0.859 |
| Mean on-time probability, MDP policy | 0.992 | 0.904 |
| MDP better / equal / worse than replan | 14 / 31 / 0 | 25 / 20 / 0 |
| Largest gain | 0.860 → 0.980 (`q2-tight-06`) | 0.716 → 0.994 (`q2-tight-18`) |
| Mean expected cost in semesters, replan / MDP | 3.347 / 3.215 | 4.771 / 4.253 |
| CP-SAT calls made by replan, all requests | 880 | 6,129 |

The same experiment with the settings of the first version (`--overrun 2 --missing certain`) gave 0.960,
0.988 and 0.997 under `all_rounds`, and 0.714, 0.875 and 0.912 under `round1`. Most of the change comes from
the course-terms without rows. With `--overrun 2` and the mean fallback, the MDP gets 0.899 under `round1`,
against 0.904 at 4 or 10: the lower penalty gives up on-time probability in `q2-tight-14` and `q2-tight-09`.

What the numbers say:

- A deterministic plan is fragile mainly when it ends in semester 8, where one failed bid means a late finish.
- Replanning recovers most of the loss. The rest comes from tie-breaking: many plans are equally good to
  CP-SAT, and it does not know that bidding for a contested course early leaves time to try again.
- Replanning can even do worse than keeping the first plan (3 requests), because every new plan breaks ties
  afresh and can move a course into a term where it is harder to get.
- Under the higher scenario the gain is small on average (0.980 to 0.992). The extension matters for
  tight plans and contested courses, and little otherwise.
- The MDP is optimal for expected cost within the courses CP-SAT chose, so its expected cost is never above
  replanning's. It minimises expected cost, not the chance of finishing on time. It was never worse than
  replanning on on-time probability in this set, but that is an observation, not a guarantee. A high
  `overrun` makes the two aims agree more often.
- All of these are computed under approximate scenarios. They compare ways of acting under the same
  probabilities. They are not forecasts for a real student.

## 7. Size of the problem

With `n` courses to schedule and `k` semesters left there are at most `k · 2ⁿ` states. A bid with `u`
uncertain courses has `2ᵘ` outcomes. A 20 MC cap holds five 4 MC courses, so a bid usually has at most 32.

In the 45 requests `n` is 8 on average and at most 14. The states actually reached are far fewer than the
bound, because prerequisites and offering terms rule most sets out:

| | `all_rounds` | `round1` |
|---|---|---|
| States evaluated, median | 32 | 142 |
| States evaluated, largest | 10,200 | 16,170 |
| Slowest policy | 2.0 s | 5.3 s |

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
- **Risk.** The cost is expected semesters plus `overrun` for a late finish. To finish one semester sooner
  the policy accepts at most `1 / (1 + overrun)` more chance of finishing late (about 9% at the default 10).
  A student who cares even more about finishing on time can raise `--overrun`. The penalty does not depend
  on how many courses are still missing.
- **Missing data.** A course-term without report rows gets a fallback, not a measured probability. The
  default (the mean) is a guess; `--missing` and `--p` let a user try other values, and `model.no_data`
  says where it was used.
- **Not covered.** `must` rules, ATAP and `mc_min` give `UNSUPPORTED`. Preferences are not applied.
- **No LLM comparison.** Pipelines A and B were not run on this question. The spec is unchanged, so a spec
  written by pipeline B can be passed to `solver.mdp.solve` as it is.
- **Semester rules are restated.** `BiddingMDP.legal` and `bids` apply the offering, prerequisite,
  corequisite, exclusion and MC-cap rules to one semester. A change to those hard rules must be made here too.
