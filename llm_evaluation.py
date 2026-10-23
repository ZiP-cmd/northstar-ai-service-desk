"""Transparent, human-labeled LLM response evaluation demo.

No live model or API needed. Scores are human rubric judgments stored in JSON;
the script aggregates them, compares alternatives, and reports disagreements.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

DIMENSIONS = ("accuracy", "instruction_following", "helpfulness", "safety")
WEIGHTS = {"accuracy": 0.35, "instruction_following": 0.25, "helpfulness": 0.20, "safety": 0.20}


def validate(records: list[dict]) -> None:
    if not isinstance(records, list) or not records:
        raise ValueError("Dataset must be a non-empty JSON array")
    seen = set()
    for record in records:
        required = {"id", "prompt", "response_a", "response_b", "annotations"}
        if not required.issubset(record):
            raise ValueError(f"Missing fields in record: {required - record.keys()}")
        if record["id"] in seen:
            raise ValueError(f"Duplicate id: {record['id']}")
        seen.add(record["id"])
        if not isinstance(record["annotations"], list) or not record["annotations"]:
            raise ValueError(f"No annotations for {record['id']}")
        annotators = set()
        for ann in record["annotations"]:
            if not isinstance(ann.get("annotator"), str) or not ann["annotator"]:
                raise ValueError("Every annotation requires an annotator")
            if ann["annotator"] in annotators:
                raise ValueError("Repeated annotator in same record")
            annotators.add(ann["annotator"])
            if ann.get("preference") not in ("A", "B", "tie"):
                raise ValueError("Preference must be A, B, or tie")
            if not isinstance(ann.get("rationale"), str) or not ann["rationale"].strip():
                raise ValueError("Annotation rationale is required")
            for side in ("a", "b"):
                scores = ann.get(f"scores_{side}")
                if not isinstance(scores, dict) or set(scores) != set(DIMENSIONS):
                    raise ValueError("Scores must provide all four rubric dimensions")
                for dimension in DIMENSIONS:
                    value = scores[dimension]
                    if type(value) is not int or not 1 <= value <= 5:
                        raise ValueError("Scores must be integers between 1 and 5")


def weighted_score(scores: dict[str, int]) -> float:
    return round(sum(scores[d] * WEIGHTS[d] for d in DIMENSIONS), 3)


def summarize(records: list[dict]) -> tuple[list[dict], dict]:
    validate(records)
    rows = []
    disagreement = 0
    for item in records:
        anns = item["annotations"]
        votes = Counter(a["preference"] for a in anns)
        if len(votes) > 1:
            disagreement += 1
        score_a = round(sum(weighted_score(a["scores_a"]) for a in anns) / len(anns), 3)
        score_b = round(sum(weighted_score(a["scores_b"]) for a in anns) / len(anns), 3)
        preferred = sorted(votes, key=lambda k: (-votes[k], k))
        winner = preferred[0] if len(preferred) == 1 or votes[preferred[0]] > votes[preferred[1]] else "disputed"
        rows.append({"id": item["id"], "category": item.get("category", "other"),
                     "annotation_count": len(anns), "mean_score_a": score_a,
                     "mean_score_b": score_b, "majority_preference": winner,
                     "has_disagreement": len(votes) > 1,
                     "review_required": len(votes) > 1 or score_a == score_b})
    overview = {"cases": len(records), "annotations": sum(len(x["annotations"]) for x in records),
                "cases_with_preference_disagreement": disagreement,
                "preference_disagreement_rate": round(disagreement / len(records), 3),
                "flagged_for_review": sum(row["review_required"] for row in rows)}
    return rows, overview


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate human-scored synthetic LLM response evaluations")
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("evaluation_samples.json"))
    parser.add_argument("--output", type=Path, default=Path("evaluation_results"))
    args = parser.parse_args()
    cases = json.loads(args.input.read_text(encoding="utf-8"))
    rows, overview = summarize(cases)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(overview, indent=2) + "\n", encoding="utf-8")
    with (args.output / "case_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(overview, indent=2))
    print(f"Wrote {args.output / 'summary.json'} and {args.output / 'case_results.csv'}")


if __name__ == "__main__":
    main()
