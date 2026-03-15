"""User interface functions."""

from config import PROGRAM_TITLE
from models import EmployeeData, SubjectData


def print_title():
    print()
    print(PROGRAM_TITLE)
    print()


def print_candidate_info(candidate: EmployeeData):
    print("KVS ime, prezime, serijski broj dozvole:")
    print(candidate["name"], candidate["license"])
    print()


def print_assessor_info(assessor: EmployeeData):
    print("ASSE ime, prezime, serijski broj dozvole:")
    print(assessor["name"], assessor["license"])
    print()


def print_subjects_summary(subjects: list[SubjectData]):
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


def print_test_generation_done(generated_tests):
    output_folder, candidate_folder, _ = str(generated_tests[0]).split("/")

    print("Testovi su generisani.")
    print()
    print(f"Testovi su sačuvani u folderu '{output_folder}' / '{candidate_folder}'")

    for test in generated_tests:
        file_name = str(test).split("/")[2]
        print(f"  - {file_name}")


def wait_for_exit():
    input("\nPritisnite Enter za izlaz iz programa...")
