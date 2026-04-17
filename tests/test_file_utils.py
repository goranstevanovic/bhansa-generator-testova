"""Tests for file utils module."""

from pathlib import Path
from unittest.mock import patch

from file_utils import check_file_availability

FIXTURES_PATH = Path("tests/fixtures")
SAMPLE_QUESTIONS_PATH = FIXTURES_PATH / "baza" / "pitanja"


# Tests for check_file_availability()
class TestCheckFileAvailability:
    @patch("file_utils.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_all_files_are_available(self):
        result = check_file_availability("npo", [1, 2, 6, 8, 10])
        expected_result = []

        assert result == expected_result
