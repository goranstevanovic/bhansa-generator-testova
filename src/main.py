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
    print_test_generation_done,
    wait_for_exit,
)
from file_utils import delete_tmp_folder, check_available_files


def main() -> None:
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

    question_files_available = []
    question_files_not_available = []

    # Check if all necessary question files are available for each subject
    for subject in subjects:
        all_question_files_available = check_available_files(
            subject["abbreviation"], subject["generated_numbers"]
        )

        if all_question_files_available:
            question_files_available.append(subject["abbreviation"])
        else:
            question_files_not_available.append(subject["abbreviation"])

    # Create list with subjects that contain selected questions
    subjects_with_available_questions = []

    for subject in subjects:
        if subject["abbreviation"] in question_files_available:
            subjects_with_available_questions.append(subject)

    # Generate tests
    generated_tests = generate_all_tests(subjects_with_available_questions, candidate)

    print_test_generation_done(generated_tests)

    # Show subjects for which tests were not generated
    if question_files_not_available:
        print()
        print("Testovi nisu generisani za sljedeće oblasti:")

        for subject in subjects:
            if subject["abbreviation"] in question_files_not_available:
                print(
                    f"- {(subject['abbreviation']).upper()} {(subject['title']).capitalize()}"
                )
    print()

    # Delete temporay folder
    delete_tmp_folder()

    wait_for_exit()


if __name__ == "__main__":
    main()
