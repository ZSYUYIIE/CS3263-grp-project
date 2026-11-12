"""Extract course rows from NUS CourseReg "Demand and Allocation Report" text files.

    pdftotext -layout round_1.pdf round_1.txt          # once per report, outside this repo
    python -m experiments.extract_demand <folder of .txt files>

Writes `data/demand/allocation.csv`: one row per (academic year, semester, round, course, class),
for the courses in the catalogue only. Each row is one line of a report, so it can be checked against
the PDF. Every report row satisfies
    demand = main + quota + timetable + workload + others
and the script stops if a parsed row does not, which catches a line read with shifted columns.
See data/demand/README.md for the source and docs/MDP_GUIDE.md section 3 for how the rows are used.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data/processed/AY2026-2027/catalog.json"
OUT = ROOT / "data/demand/allocation.csv"

COLUMNS = ["acad_year", "semester", "round", "code", "class", "vacancy", "demand",
           "main", "reserve", "quota", "timetable", "workload", "others"]

# course code ... class, vacancy, then seven counts at the end of the line
ROW = re.compile(
    r"\b([A-Z]{2,4}\d{4}[A-Z]{0,3})\b.*?\s(\S+)\s+(\S+)"
    r"\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$"
)
ROUND = re.compile(r"Undergraduate Courses, Select Courses \(Round (\d)\)")
TERM = re.compile(r"Semester (\d), AY(\d{4})/(\d{4})")


def parse_report(text: str) -> list[dict]:
    """Rows of one report (every course, not only the catalogue's)."""
    round_match, term_match = ROUND.search(text), TERM.search(text)
    if not round_match or not term_match:
        raise ValueError("not an undergraduate Select Courses report: the title lines are missing")
    head = {
        "acad_year": f"{term_match.group(2)}-{term_match.group(3)}",
        "semester": int(term_match.group(1)),
        "round": int(round_match.group(1)),
    }
    rows = []
    for line in text.splitlines():
        found = ROW.search(line)
        if not found:
            continue
        code, klass, vacancy, *counts = found.groups()
        demand, main, reserve, quota, timetable, workload, others = (int(x) for x in counts)
        if demand != main + quota + timetable + workload + others:
            raise ValueError(f"columns do not add up in: {line.strip()}")
        rows.append({**head, "code": code, "class": klass, "vacancy": vacancy, "demand": demand,
                     "main": main, "reserve": reserve, "quota": quota, "timetable": timetable,
                     "workload": workload, "others": others})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", help="folder holding the pdftotext -layout output of each report")
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()

    wanted = set(json.loads(CATALOG.read_text(encoding="utf-8"))["courses"])
    rows, seen = [], set()
    for path in sorted(Path(args.folder).glob("*.txt")):
        report = parse_report(path.read_text(encoding="utf-8"))
        key = (report[0]["acad_year"], report[0]["semester"], report[0]["round"])
        if key in seen:
            raise ValueError(f"{path.name} repeats the report {key}")
        seen.add(key)
        kept = [row for row in report if row["code"] in wanted]
        for row in kept:
            if not row["vacancy"].isdigit():
                raise ValueError(f"{path.name}: no vacancy number for {row['code']} {row['class']}")
        rows += kept
        print(f"{path.name}: AY{key[0]} semester {key[1]} round {key[2]}: "
              f"{len(report)} rows, {len(kept)} in the catalogue")
    rows.sort(key=lambda r: (r["acad_year"], r["semester"], r["round"], r["code"], r["class"]))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows from {len(seen)} reports to {args.out}")


if __name__ == "__main__":
    main()
