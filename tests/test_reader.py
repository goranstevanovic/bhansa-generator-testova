"""Tests for reader module."""

from pathlib import Path

import pytest

from reader import (
    _load_cell_value,
    _parse_subject_abbreviation,
    _parse_subject_title,
    load_employee_data,
    load_subject_titles,
)

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


# Tests for _parse_subject_title()
class TestParseSubjectTitle:
    def test_with_abbreviation(self):
        assert _parse_subject_title("NAZIV PRVE OBLASTI (NPO)") == "naziv prve oblasti"
        assert (
            _parse_subject_title("NAZIV DRUGE OBLASTI (NDO)") == "naziv druge oblasti"
        )
        assert (
            _parse_subject_title("NAZIV TREĆE OBLASTI (NTO)") == "naziv treće oblasti"
        )

    def test_newline_replacement(self):
        assert _parse_subject_title("NAZIV\nOBLASTI\n(NOB)") == "naziv oblasti"


# Tests for load_employee_data()
class TestLoadEmployeeData:
    def test_load_candidate_data(self):
        result = load_employee_data(SAMPLE_FORM, "B4")
        expected_result = {"name": "Marko Marković", "license": "ATCO.0123"}
        assert result == expected_result

    def test_load_assessor_data(self):
        result = load_employee_data(SAMPLE_FORM, "B5")
        expected_result = {"name": "Petar Petrović-Petrić", "license": "ATCO.4567"}
        assert result == expected_result

    def test_load_employee_data_from_empty_cell(self):
        result = load_employee_data(SAMPLE_FORM, "A1")
        expected_result = {"name": "", "license": ""}
        assert result == expected_result


# Tests for load_subject_titles()
class TestLoadSubjectTitles:
    def test_returns_list(self):
        result = load_subject_titles(SAMPLE_FORM)
        assert isinstance(result, list)

    def test_list_contains_dicts(self):
        result = load_subject_titles(SAMPLE_FORM)
        assert "abbreviation" in result[0]
        assert "title" in result[0]

    def test_loads_correct_abbreviations_and_titles(self):
        result = load_subject_titles(SAMPLE_FORM)
        subject1, subject2, subject3 = result
        assert subject1["abbreviation"] == "npo"
        assert subject1["title"] == "naziv prve oblasti"
        assert subject2["abbreviation"] == "ndo"
        assert subject2["title"] == "naziv druge oblasti"
        assert subject3["abbreviation"] == "nto"
        assert subject3["title"] == "naziv treće oblasti"
