from pathlib import Path

from config import OUTPUT_PATH
from models import EmployeeData, SubjectData


def create_output_document_path(subject: SubjectData, employee: EmployeeData) -> Path:
    """Create a file path for a test document."""
    subject_abbrev = subject["abbreviation"]
    employee_name = employee["name"]
    employee_license = employee["license"]

    folder_path = OUTPUT_PATH / f"{employee_name} {employee_license}"
    folder_path.mkdir(parents=True, exist_ok=True)

    file_name = f"{employee_name} {employee_license} {subject_abbrev.upper()}.docx"

    return folder_path / file_name
