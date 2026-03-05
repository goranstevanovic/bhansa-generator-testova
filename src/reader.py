"""Excel file reading functionality."""

import re
from pathlib import Path

import openpyxl


def _load_cell_value(file: Path, cell: str) -> str:
    """Load a single cell value from Excel file."""
    workbook = openpyxl.load_workbook(file, data_only=True)
    sheet = workbook.active

    if sheet is None:
        return ""

    cell_obj = sheet[cell]

    if cell_obj is None:
        return ""

    value = cell_obj.value

    return str(value) if value is not None else ""


def _parse_subject_abbreviation(text: str) -> str | None:
    """Extract abbreviation from subject title."""
    pattern = re.compile(r"\(([A-Za-z]{3,})\)$")
    match = pattern.search(text)

    if match:
        return match.group(1).lower()

    return None


def _parse_subject_title(text: str) -> str:
    """Extract title only from subject title, removing abbreviation."""
    pattern = re.compile(r"\s*\([A-Za-z]{3,}\)$")
    return pattern.sub("", text).replace("\n", " ").strip().lower()
