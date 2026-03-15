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
from ui import (
    print_title,
    print_candidate_info,
    print_assessor_info,
    print_subjects_summary,
)


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

    print_title()
    print_candidate_info(candidate)
    print_assessor_info(assessor)
    print_subjects_summary(subjects)

    # Generate tests
    generate_all_tests(subjects, candidate)

    print("Svi testovi su generisani")

    # Wait for user input before exiting
    input("\nPritisnite Enter za izlaz...")


if __name__ == "__main__":
    main()
