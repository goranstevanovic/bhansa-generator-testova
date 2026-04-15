"""Functions for working with files and folders."""

import shutil
import os
from pathlib import Path

from config import TEMPORARY_PATH, QUESTIONS_PATH
from models import SubjectData


def delete_tmp_folder() -> None:
    """Delete temporary folder if it exists."""
    if TEMPORARY_PATH.exists():
        shutil.rmtree(TEMPORARY_PATH)


def check_available_files(folder: str, files: list, kind: str = "pitanja"):
    """Check if folder contains all provided files."""
    if kind == "pitanja":
        folder_path = QUESTIONS_PATH / folder
    files_in_folder = sorted(os.listdir(folder_path))
    files_in_folder_stripped = []

    for file in files_in_folder:
        # Remove file extension and convert file name to number
        file_name_stripped = int(file.split(".")[0])
        files_in_folder_stripped.append(file_name_stripped)

    files_in_folder_stripped.sort()

    return set(files).issubset(files_in_folder_stripped)


def check_questions_availability(
    subjects: list[SubjectData],
) -> tuple[list[SubjectData], list[SubjectData]]:
    """Return tuple containing two lists:
    one with subjects that have all selected questions available,
    another one with subjects that don't have all selected questions available.
    """
    question_files_available = []
    question_files_not_available = []

    for subject in subjects:
        if check_available_files(subject["abbreviation"], subject["generated_numbers"]):
            question_files_available.append(subject)
        else:
            question_files_not_available.append(subject)

    return question_files_available, question_files_not_available
