#!/usr/bin/env python3
"""Build script"""

import sys

import PyInstaller.__main__


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


def run_pyinstaller(platform: str) -> None:
    """Run PyInstaller using appropriate spec file."""
    if platform == "win32":
        spec_file = "generator-testova-win.spec"
    elif platform == "linux":
        spec_file = "generator-testova-linux.spec"

    PyInstaller.__main__.run(["--clean", spec_file])


def main() -> None:
    # Get OS/platform
    platform = get_platform()

    # Check if script is running on supported OS/platform
    try:
        check_if_platform_supported(platform)
    except Exception as err:
        print(err)
        sys.exit(1)

    # Run PyInstaller using platform-specific spec file
    run_pyinstaller(platform)


if __name__ == "__main__":
    main()
