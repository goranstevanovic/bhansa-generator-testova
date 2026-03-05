"""Excel file reading functionality."""

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
