"""Functions for working with files and folders."""

import shutil
from pathlib import Path

from config import TEMPORARY_PATH


def delete_tmp_folder() -> None:
    """Delete temporary folder if it exists."""
    if TEMPORARY_PATH.exists():
        shutil.rmtree(TEMPORARY_PATH)
