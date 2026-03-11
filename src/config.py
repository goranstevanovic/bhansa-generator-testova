"""Configuration constants for test generator."""

from pathlib import Path

# Question number generator file
QUESTIONS_GENERATOR = "TRE.FORM.371.xlsm"

# Cell addresses for employees' data
CANDIDATE_CELL = "B4"
ASSESSOR_CELL = "B5"

# Cell ranges for subject data
SUBJECT_NAME_RANGE = "A10:A29"
TOTAL_QUESTIONS_RANGE = "D10:D29"
PERCENTAGE_RANGE = "E10:E29"
GENERATED_NUMBERS_RANGE = "F10:F29"

# Folder paths
BASE_PATH = Path("baza")
QUESTIONS_PATH = BASE_PATH / "pitanja"
TEMPLATES_PATH = BASE_PATH / "predlosci"
OUTPUT_PATH = Path("generisani-testovi")
TEMPORARY_PATH = Path("tmp")

# Question bank locations
QUESTION_BANKS = {
    "ass": QUESTIONS_PATH / "ass",
    "emr": QUESTIONS_PATH / "emr",
    "eqp": QUESTIONS_PATH / "eqp",
    "lgc": QUESTIONS_PATH / "lgc",
    "lnf": QUESTIONS_PATH / "lnf",
    "lpi": QUESTIONS_PATH / "lpi",
}

# Cover page template file
COVER_TEMPLATE = TEMPLATES_PATH / "template-naslovna.docx"
TEMPLATE_TITLE_STRING = "naziv"
TEMPLATE_ABBREVIATION_STRING = "skracenica"
