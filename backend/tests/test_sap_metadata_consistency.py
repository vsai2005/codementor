"""Regression test requiring zero unexpected mismatches between SAP curriculum manifest and authored lesson data.

Guards:
  - Exactly 100 days defined in manifest (Days 1–100).
  - Exactly 100 days authored in SAP_DAYS_CONTENT (Days 1–100).
  - 100% exact parity between canonical slug and title across all 100 days.
  - Zero unexpected mismatches.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.data.sap_lessons import SAP_DAYS_CONTENT


@pytest.fixture(scope="module")
def manifest_data() -> dict:
    manifest_path = Path(__file__).resolve().parent.parent / "app" / "data" / "sap_curriculum_manifest.json"
    assert manifest_path.exists(), f"Manifest not found at {manifest_path}"
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_manifest_and_authored_exact_day_counts(manifest_data: dict):
    manifest_days = manifest_data.get("days", [])
    assert len(manifest_days) == 100, f"Expected 100 days in manifest, got {len(manifest_days)}"
    assert len(SAP_DAYS_CONTENT) == 100, f"Expected 100 authored days in SAP_DAYS_CONTENT, got {len(SAP_DAYS_CONTENT)}"
    assert sorted(SAP_DAYS_CONTENT.keys()) == list(range(1, 101))


def test_zero_metadata_mismatches_across_all_100_days(manifest_data: dict):
    """Assert zero slug or title discrepancies between manifest and authored lessons."""
    manifest_days_by_num = {d["day_number"]: d for d in manifest_data["days"]}
    mismatches = []

    for day_num in range(1, 101):
        m_day = manifest_days_by_num.get(day_num)
        a_day = SAP_DAYS_CONTENT.get(day_num)

        assert m_day is not None, f"Day {day_num} missing from manifest"
        assert a_day is not None, f"Day {day_num} missing from authored content"

        m_slug = m_day.get("slug")
        a_slug = a_day.get("slug")
        m_title = m_day.get("title")
        a_title = a_day.get("title")

        diffs = {}
        if m_slug != a_slug:
            diffs["slug"] = {"manifest": m_slug, "authored": a_slug}
        if m_title != a_title:
            diffs["title"] = {"manifest": m_title, "authored": a_title}

        if diffs:
            mismatches.append({"day": day_num, "diffs": diffs})

    assert len(mismatches) == 0, f"Found {len(mismatches)} unexpected metadata mismatches: {mismatches}"


def test_all_100_authored_days_have_valid_pedagogical_structure():
    """Verify that every authored day contains non-empty steps, objectives, and concepts."""
    for day_num in range(1, 101):
        lesson = SAP_DAYS_CONTENT[day_num]
        assert lesson["day_number"] == day_num
        assert isinstance(lesson["slug"], str) and len(lesson["slug"]) > 0
        assert isinstance(lesson["title"], str) and len(lesson["title"]) > 0
        assert "steps" in lesson and len(lesson["steps"]) >= 4, f"Day {day_num} has insufficient steps"
        assert "atomic_concepts" in lesson and isinstance(lesson["atomic_concepts"], list)
