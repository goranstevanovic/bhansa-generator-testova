"""Data models for test generator."""

from typing import TypedDict


class EmployeeData(TypedDict):
    """Data about the instructor or candidate."""

    name: str
    license: str


class SubjectData(TypedDict):
    """Complete data about a single subject."""

    abbreviation: str
    title: str
    total_questions: int
    percentage: int
    generated_numbers: list[int]
