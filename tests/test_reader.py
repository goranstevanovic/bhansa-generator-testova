"""Tests for reader module."""

from pathlib import Path

import pytest

from reader import _load_cell_value, _parse_subject_abbreviation, _parse_subject_title

SAMPLE_FORM = Path("tests/fixtures/test-form.xlsm")


# Tests for _load_cell_value()
class TestLoadCellValue:
    def test_loads_cell_value(self):
        result = _load_cell_value(SAMPLE_FORM, "B4")
        expected_result = "Marko Marković ATCO.0123"
        assert result == expected_result


# Tests for _parse_subject_abbreviation()
class TestParseSubjectAbbreviations:
    def test_with_valid_abbreviation(self):
        assert _parse_subject_abbreviation("NAZIV PRVE OBLASTI (NPO)") == "npo"
        assert _parse_subject_abbreviation("NAZIV DRUGE OBLASTI (NDO)") == "ndo"
        assert _parse_subject_abbreviation("NAZIV TREĆE OBLASTI (NTO)") == "nto"

    def test_without_abbreviation(self):
        assert _parse_subject_abbreviation("NAZIV OBLASTI") is None
        assert _parse_subject_abbreviation("") is None
