#!/usr/bin/env python3
"""Build script"""

import sys
import subprocess
import os
import shutil
from pathlib import Path

import PyInstaller.__main__

from _version import VERSION

VERSION_FILE_PATH = Path("src", "_version.py")
BUNDLE_ROOT_FOLDER_TEMP_NAME = Path("dist", "generator-testova-bundle")
BUNDLE_ROOT_FOLDER_FINAL_NAME = Path("dist", "generator-testova")
WINDOWS_EXE_PATH = Path("dist", "generator-testova.exe")
LINUX_EXE_PATH = Path("dist", "generator-testova")


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
    tag = get_current_commit_tag()
    hash = get_current_commit_hash()

    if tag.startswith("v"):
        return tag[1:]
    else:
        # Use only x.x.x part, ignore - and rest
        return f"{VERSION.split("-")[0]}-dev+{hash}"


def update_version_file(is_test_build):
    version_file_content = f'VERSION = "{create_version_number()}"\n'
    version_file_content += f'DATE = "{get_current_commit_date()}"\n'

    if is_test_build:
        version_file_content += "IS_TEST_BUILD = True\n"
    else:
        version_file_content += "IS_TEST_BUILD = False\n"

    with open(VERSION_FILE_PATH, "w") as file:
        file.write(version_file_content)


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


def create_folder_structure():
    # Create bundle folder
    os.makedirs(BUNDLE_ROOT_FOLDER_TEMP_NAME)

    # Move executable file into bundle folder
    if get_platform() == "win32":
        shutil.move(WINDOWS_EXE_PATH, BUNDLE_ROOT_FOLDER_TEMP_NAME)
    elif get_platform() == "linux":
        shutil.move(LINUX_EXE_PATH, BUNDLE_ROOT_FOLDER_TEMP_NAME)

    # Rename bundle root folder
    shutil.move(BUNDLE_ROOT_FOLDER_TEMP_NAME, BUNDLE_ROOT_FOLDER_FINAL_NAME)


def main() -> None:
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

    create_folder_structure()


if __name__ == "__main__":
    main()
