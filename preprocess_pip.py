import subprocess
import sys
import os
import pathlib


def project_files():
    """
    Get all the project files as path objects
    """
    for f in os.getenv("QUARTO_PROJECT_INPUT_FILES").split("\n"):
        yield pathlib.Path(f)


def install(requirements_path):
    """
    Install all requirements at the path
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])


if __name__ == "__main__":
    for path in project_files():
        requirements_path = path.parent / "requirements.txt"
        if requirements_path.exists():
            install(str(requirements_path))

    sys.exit()
