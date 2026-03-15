"""Main entry point for test generator."""

from pathlib import Path

from config import (
    QUESTIONS_GENERATOR,
    CANDIDATE_CELL,
    ASSESSOR_CELL,
    SUBJECT_NAME_RANGE,
    TOTAL_QUESTIONS_RANGE,
    PERCENTAGE_RANGE,
    GENERATED_NUMBERS_RANGE,
)
from reader import load_employee_data, load_all_subject_data
from writer import generate_all_tests


def main():
    """Run test generator."""
    # Load questions generator form file
    form_file = Path(QUESTIONS_GENERATOR)

    # Load employee data
    candidate = load_employee_data(form_file, CANDIDATE_CELL)
    assessor = load_employee_data(form_file, ASSESSOR_CELL)

    # Load all subject data
    subjects = load_all_subject_data(
        form_file,
        SUBJECT_NAME_RANGE,
        TOTAL_QUESTIONS_RANGE,
        PERCENTAGE_RANGE,
        GENERATED_NUMBERS_RANGE,
    )

    # Print title
    print()
    print("\tGENERATOR TESTOVA")
    print()

    # Print candidate's information
    print("KVS ime, prezime i serijski broj dozvole:")
    print(candidate["name"], candidate["license"])
    print()

    # Print assessor's information
    print("ASSE ime, prezime i serijski broj dozvole:")
    print(assessor["name"], assessor["license"])
    print()

    # Generate tests
    generate_all_tests(subjects, candidate)


if __name__ == "__main__":
    main()
