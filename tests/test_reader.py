"""Tests for reader module."""

from pathlib import Path

import pytest

from reader import _load_cell_value

SAMPLE_FORM = Path("tests/fixtures/test-form.xlsm")


class TestLoadCellValue:
    def test_loads_cell_value(self):
        result = _load_cell_value(SAMPLE_FORM, "B4")
        expected_result = "Marko Marković ATCO.0123"
        assert result == expected_result
