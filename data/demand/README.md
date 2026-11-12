# CourseReg demand and allocation data

`allocation.csv` is generated. Do not edit it by hand.

**Source.** NUS Registrar's Office, *Course Class Demand and Allocation Report*, Undergraduate Courses,
Select Courses, rounds 1 to 3, for Semesters 1 and 2 of AY2024/25 and AY2025/26 (12 reports). The PDFs were
taken on 12 Nov 2026 from the mirror at `https://courserekt.vercel.app/pdfs/<yyyy>/<semester>/ug/round_<n>.pdf`
(`<yyyy>` is `2425` or `2526`). The PDFs are not kept in this repo.

**Content.** 4,336 rows: every report line whose course code is in `data/processed/AY2026-2027/catalog.json`.

| Column | Meaning |
|---|---|
| `acad_year`, `semester`, `round` | which report the row comes from |
| `code`, `class` | course and class (lecture or sectional group) |
| `vacancy` | places offered in that round |
| `demand` | the report's Demand column: students asking for the class in that round |
| `main`, `reserve` | students allocated from their main list and from their reserve list |
| `quota`, `timetable`, `workload`, `others` | students not allocated, by reason |

In every row `demand = main + quota + timetable + workload + others`. The extraction stops if a line does not
add up, and `tests/test_mdp.py` checks the committed file.

**Regenerate.**

```bash
pdftotext -layout round_1.pdf round_1.txt             # once per report, into one folder
python -m experiments.extract_demand <that folder>
```

How the rows become probabilities: [`docs/MDP_GUIDE.md`](../../docs/MDP_GUIDE.md) section 3 and
`solver/admission.py`.
