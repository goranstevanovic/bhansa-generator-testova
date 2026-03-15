"""User interface functions."""

from config import PROGRAM_TITLE
from models import EmployeeData


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
