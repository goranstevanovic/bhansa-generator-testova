"""Data models for test generator."""

from typing import TypedDict


class EmployeeData(TypedDict):
    """Data about the instructor or candidate."""

    name: str
    license: str
