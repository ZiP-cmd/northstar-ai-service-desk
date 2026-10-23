import json
from pathlib import Path
import pytest
from llm_evaluation import summarize, validate, weighted_score

SAMPLES = Path(__file__).resolve().parents[1] / "evaluation_samples.json"


def samples():
    return json.loads(SAMPLES.read_text(encoding="utf-8"))


def test_samples_validate():
    validate(samples())


def test_weighted_score_for_uniform_rubric():
    assert weighted_score({d: 4 for d in ("accuracy", "instruction_following", "helpfulness", "safety")}) == 4


def test_report_identifies_disagreement():
    rows, overall = summarize(samples())
    assert overall["cases"] == 4
    assert overall["annotations"] == 8
    assert overall["cases_with_preference_disagreement"] == 1
    assert rows[-1]["review_required"] is True


def test_confidentiality_response_is_preferred():
    rows, _ = summarize(samples())
    assert next(r for r in rows if r["id"] == "salary-002")["majority_preference"] == "B"


def test_duplicate_identifiers_rejected():
    items = samples()
    items.append(dict(items[0]))
    with pytest.raises(ValueError, match="Duplicate"):
        validate(items)


def test_missing_rationale_rejected():
    items = samples()
    items[0]["annotations"][0]["rationale"] = " "
    with pytest.raises(ValueError, match="rationale"):
        validate(items)


def test_invalid_score_rejected():
    items = samples()
    items[0]["annotations"][0]["scores_a"]["safety"] = 6
    with pytest.raises(ValueError, match="between 1 and 5"):
        validate(items)


def test_tied_votes_flagged_as_disputed():
    rows, _ = summarize(samples())
    assert rows[-1]["majority_preference"] == "disputed"
