"""Tests for writer module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from writer import create_output_document_path

FIXTURES_PATH = Path("tests/fixtures")
SAMPLE_OUTPUT_PATH = FIXTURES_PATH / "output"


# Sample employee
@pytest.fixture
def sample_employee():
    return {"name": "Marko Marković", "license": "ATCO.0123"}


# Sample subject
@pytest.fixture
def sample_subject():
    return {
        "abbreviation": "npo",
        "title": "naziv prve oblasti",
        "total_questions": 10,
        "percentage": 40,
        "generated_numbers": [1, 4, 7, 10],
    }


# Tests for create_output_document_path()
class TestCreateOutputDocumentPath:
    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    def test_creates_correct_output_document_path(
        self, sample_employee, sample_subject
    ):
        result = create_output_document_path(sample_subject, sample_employee)

        # Folder for generated tests
        expected_result = f"{SAMPLE_OUTPUT_PATH}/"

        # Folder with candidate's name and license number
        expected_result += f"{sample_employee["name"]} {sample_employee["license"]}/"

        # File name: candidate's name part
        expected_result += f"{sample_employee["name"]}"
        # File name: candidate's license number part
        expected_result += f" {sample_employee["license"]}"
        # File name: subject abbreviation (uppercase) part
        expected_result += f" {sample_subject["abbreviation"].upper()}"
        # File name: file extension
        expected_result += ".docx"

        assert str(result) == expected_result

    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    def test_creates_folder_if_not_exists(self, sample_subject, sample_employee):
        result = create_output_document_path(sample_subject, sample_employee)

        assert result.parent.exists()
