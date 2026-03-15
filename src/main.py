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
from ui import print_title, print_candidate_info, print_assessor_info


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

    # Print all subjects' information
    print(f"Broj pronađenih oblasti u generatoru pitanja: {len(subjects)}")
    print()

    for i, subject in enumerate(subjects, 1):
        abbrev = subject["abbreviation"]
        title = subject["title"]
        total_questions = subject["total_questions"]
        percentage = subject["percentage"]
        generated_questions_qty = round(total_questions * percentage / 100)
        generated_numbers = ", ".join(str(num) for num in subject["generated_numbers"])

        print(f"{i}. {abbrev.upper()}")
        print(f"   {title.capitalize()}")
        print(f"       Ukupan broj pitanja: {total_questions}")
        print(f"       Procenat pitanja za generisanje: {percentage}%")
        print(f"       Broj pitanja za generisanje: {generated_questions_qty}")
        print(f"       Generisani brojevi pitanja:")
        print(f"         {generated_numbers}")
        print()

    # Generate tests
    generate_all_tests(subjects, candidate)

    print("Svi testovi su generisani")

    # Wait for user input before exiting
    input("\nPritisnite Enter za izlaz...")


if __name__ == "__main__":
    main()
