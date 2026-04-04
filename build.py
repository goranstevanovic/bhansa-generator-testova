#!/usr/bin/env python3
"""Build script"""

import sys
import subprocess
import os
import shutil
import time
from pathlib import Path

import PyInstaller.__main__

from _version import VERSION

# Base name of the release archive file
ARCHIVE_BASE_NAME = "bhansa-generator-testova"

# Root and base folders used when creating archives
ARCHIVE_ROOT_FOLDER = Path("dist")
ARCHIVE_BASE_FODLER = Path("generator-testova")

# File containing version number and date
VERSION_FILE_PATH = Path("src", "_version.py")

# Bundle folder temporary and final names
BUNDLE_ROOT_FOLDER_TEMP_NAME = Path("dist", "generator-testova-bundle")
BUNDLE_ROOT_FOLDER_FINAL_NAME = Path("dist", "generator-testova")

# Relases base folder
RELEASES_BASE_FOLDER = Path("releases")

# Generated executable files paths
WINDOWS_EXE_PATH = Path("dist", "generator-testova.exe")
LINUX_EXE_PATH = Path("dist", "generator-testova")

# Templates, questions, answers, generated tests folder paths
FOLDERS_TEMPLATES = ["baza/predlosci"]
FOLDERS_QUESTIONS = [
    "baza/pitanja/ass",
    "baza/pitanja/emr",
    "baza/pitanja/eqp",
    "baza/pitanja/lgc",
    "baza/pitanja/lnf",
    "baza/pitanja/lpi",
]
FOLDERS_ANSWERS = [
    "baza/odgovori/ass",
    "baza/odgovori/emr",
    "baza/odgovori/eqp",
    "baza/odgovori/lgc",
    "baza/odgovori/lnf",
    "baza/odgovori/lpi",
]
FOLDERS_GENERATED_TESTS = ["generisani-testovi"]

# Question number generator file
QUESTIONS_GENERATOR = "FORM.xlsm"


def get_platform() -> str:
    """Get OS/platform as a string."""
    return sys.platform


def check_if_platform_supported(platform: str) -> bool:
    """Check if current OS/platform is supported by this build script."""
    if platform == "win32" or platform == "linux":
        return True
    else:
        raise Exception(
            f"{platform} is not supported. Only Windows and Linux are supported."
        )


def get_current_commit_tag() -> str:
    """Get tag of current commit, if any."""
    cmd = ["git", "tag", "--points-at", "HEAD"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_current_commit_hash() -> str:
    """Get short hash of current commit."""
    cmd = ["git", "rev-parse", "--short", "HEAD"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_current_commit_date() -> str:
    """Get YYYY-MM-DD date of current commit."""
    cmd = ["git", "show", "-s", "--format=%cs"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def create_version_number() -> str:
    """
    Get current version number, either a version number from tag,
    or previous version number plus short commit hash.
    """
    tag = get_current_commit_tag()
    hash = get_current_commit_hash()

    if tag.startswith("v"):
        return tag[1:]
    else:
        # Use only x.x.x part, ignore - and rest
        return f"{VERSION.split("-")[0]}-dev+{hash}"


def update_version_file(is_test_build) -> str:
    """Update version file with correct version umber and date."""
    version_file_content = f'VERSION = "{create_version_number()}"\n'
    version_file_content += f'DATE = "{get_current_commit_date()}"\n'

    if is_test_build:
        version_file_content += "IS_TEST_BUILD = True\n"
    else:
        version_file_content += "IS_TEST_BUILD = False\n"

    with open(VERSION_FILE_PATH, "w") as file:
        file.write(version_file_content)

    return version_file_content


def empty_dist_folder() -> None:
    """Delete contents of dist folder before building to start fresh."""
    # Check if folder with temp name exists
    if os.path.exists(BUNDLE_ROOT_FOLDER_TEMP_NAME):
        shutil.rmtree(BUNDLE_ROOT_FOLDER_TEMP_NAME)
    # Check if folder or file with final name exists
    elif os.path.exists(BUNDLE_ROOT_FOLDER_FINAL_NAME):
        # Check if it is folder
        if os.path.isdir(BUNDLE_ROOT_FOLDER_FINAL_NAME):
            shutil.rmtree(BUNDLE_ROOT_FOLDER_FINAL_NAME)
        # Check if it is file
        elif os.path.isfile(BUNDLE_ROOT_FOLDER_FINAL_NAME):
            os.remove(BUNDLE_ROOT_FOLDER_FINAL_NAME)


def run_pyinstaller(platform: str) -> None:
    """Run PyInstaller using appropriate spec file."""
    if platform == "win32":
        spec_file = "generator-testova-win.spec"
    elif platform == "linux":
        spec_file = "generator-testova-linux.spec"

    PyInstaller.__main__.run(["--clean", spec_file])


def create_folders(folders: list[str]) -> None:
    """Create template folders."""
    for folder in folders:
        os.makedirs(BUNDLE_ROOT_FOLDER_FINAL_NAME / folder)


def create_folder_structure() -> None:
    """Create empty folder structure and copy template files."""
    # Create bundle folder
    os.makedirs(BUNDLE_ROOT_FOLDER_TEMP_NAME)

    # Move executable file into bundle folder
    if get_platform() == "win32":
        shutil.move(WINDOWS_EXE_PATH, BUNDLE_ROOT_FOLDER_TEMP_NAME)
    elif get_platform() == "linux":
        shutil.move(LINUX_EXE_PATH, BUNDLE_ROOT_FOLDER_TEMP_NAME)

    # Rename bundle root folder
    shutil.move(BUNDLE_ROOT_FOLDER_TEMP_NAME, BUNDLE_ROOT_FOLDER_FINAL_NAME)

    # Create template, questions, answers, and generated tests folders
    create_folders(FOLDERS_TEMPLATES)
    create_folders(FOLDERS_QUESTIONS)
    create_folders(FOLDERS_ANSWERS)
    create_folders(FOLDERS_GENERATED_TESTS)


def copy_files(sources: list, dest_root: Path) -> None:
    """Copy files from source folders to destination folders."""
    for source in sources:
        source = Path(source)
        destination = dest_root / source
        for file in os.listdir(source):
            shutil.copy2(source / file, destination)


def copy_basic_release_files(sources: list, dest_root: Path) -> None:
    """
    Copy basic release files from source to destination folders.
    Basic release files are template files, that don't contain sensitive
    information.

    """
    # Copy template files
    copy_files(sources, dest_root)


def copy_full_release_files() -> None:
    """
    Copy full release files from source to destination folders.
    Full release files include questions generator form,
    question documents, and answer documents
    """
    copy_files(FOLDERS_QUESTIONS, BUNDLE_ROOT_FOLDER_FINAL_NAME)
    copy_files(FOLDERS_ANSWERS, BUNDLE_ROOT_FOLDER_FINAL_NAME)
    shutil.copy2(QUESTIONS_GENERATOR, BUNDLE_ROOT_FOLDER_FINAL_NAME)


def create_release_archive(platform: str, type: str = "basic") -> None:
    """Create release archives for basic and full releases."""
    version = create_version_number()
    archive_name = f"{ARCHIVE_BASE_NAME}-v{version}"

    if platform == "win32":
        archive_name += "-windows"

        if type == "full":
            archive_name += "-full"

        archive_path = str(RELEASES_BASE_FOLDER / Path(version) / Path(archive_name))
        shutil.make_archive(
            archive_path, "zip", ARCHIVE_ROOT_FOLDER, ARCHIVE_BASE_FODLER
        )
    elif platform == "linux":
        archive_name += "-linux"

        if type == "full":
            archive_name += "-full"

        archive_path = str(RELEASES_BASE_FOLDER / Path(version) / Path(archive_name))
        shutil.make_archive(
            archive_path, "gztar", ARCHIVE_ROOT_FOLDER, ARCHIVE_BASE_FODLER
        )


def get_time_string(start_time: float, end_time: float) -> str:
    """Get time string in format h:mm:ss."""

    time_string = ""

    total_time = end_time - start_time

    hours = round(total_time // 3600)
    remaining = total_time - hours * 3600
    minutes = round(remaining // 60)
    seconds = round(remaining - minutes * 60)

    if hours > 0:
        time_string += f"{hours}h "

    if minutes > 0:
        time_string += f"{minutes:02}m "

    time_string += f"{seconds:02}s"

    return time_string


def main() -> None:
    # Get start time
    start_time = time.time()

    # Get OS/platform
    platform = get_platform()

    # Check if script is running on supported OS/platform
    try:
        check_if_platform_supported(platform)
    except Exception as err:
        print(err)
        sys.exit(1)

    # Determine if creating test build or not
    if get_current_commit_tag().startswith("v"):
        is_test_build = False
    else:
        is_test_build = True

    # Update vesion file
    if is_test_build:
        update_version_file(True)
    else:
        update_version_file(False)

    # Empty dist folder before building
    empty_dist_folder()

    # Run PyInstaller using platform-specific spec file
    run_pyinstaller(platform)

    # Create basic folder structure, empty folders, without files
    create_folder_structure()

    # Copy basic release files (templates)
    copy_basic_release_files(FOLDERS_TEMPLATES, BUNDLE_ROOT_FOLDER_FINAL_NAME)

    # Create basic release archive
    create_release_archive(platform)

    # Copy full release files (.xlsm form, .docx questions and answers)
    copy_full_release_files()

    # Create full release archive
    create_release_archive(platform, "full")

    # Get end time
    end_time = time.time()

    # Display total build time
    time_string = get_time_string(start_time, end_time)
    print("Total time:", time_string)


if __name__ == "__main__":
    main()
