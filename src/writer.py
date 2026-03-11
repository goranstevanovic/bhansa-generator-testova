from pathlib import Path

from docxtpl import DocxTemplate

from config import (
    OUTPUT_PATH,
    TEMPORARY_PATH,
    COVER_TEMPLATE,
    TEMPLATE_TITLE_STRING,
    TEMPLATE_ABBREVIATION_STRING,
)
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


def create_cover_page(subject: SubjectData) -> Path:
    """Create cover page and return temporary file path."""
    cover_page = DocxTemplate(COVER_TEMPLATE)
    context = {
        TEMPLATE_TITLE_STRING: subject["title"],
        TEMPLATE_ABBREVIATION_STRING: subject["abbreviation"],
    }
    cover_page.render(context)

    temp_file = TEMPORARY_PATH / f"cover-{subject['abbreviation']}.docx"
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    cover_page.save(str(temp_file))

    return temp_file
