"""Main entry point for test generator."""

from pathlib import Path

from config import QUESTIONS_GENERATOR, CANDIDATE_CELL, ASSESSOR_CELL
from reader import load_employee_data


def main():
    """Run test generator."""
    # Load questions generator form file
    form_file = Path(QUESTIONS_GENERATOR)

    # Load employee data
    candidate = load_employee_data(form_file, CANDIDATE_CELL)
    assessor = load_employee_data(form_file, ASSESSOR_CELL)

    print(candidate)
    print(assessor)


if __name__ == "__main__":
    main()
