import subprocess
import sys
import os
import pathlib


def is_render_all():
    """
    Returns true if quarto is set to render all
    """
    return os.getenv("QUARTO_PROJECT_RENDER_ALL")


def get_project_files():
    """
    Get all the project files being rendered as a list of paths
    """
    return list(map(pathlib.Path, os.getenv("QUARTO_PROJECT_INPUT_FILES").split("\n")))


def get_requiements_path(project_file):
    return project_file.parent / "requirements.txt"


def file_exists(project_file):
    return project_file.exists()


def install(path):
    """
    Install all requirements at the path
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", path])


if __name__ == "__main__":
    if is_render_all():
        print("Not rendering a specific .qmd file, so will not install requirements. Exiting.")
        sys.exit()
    
    project_files = get_project_files()
    all_requirements_files = map(get_requiements_path, project_files)
    all_existing_requirements_files = filter(file_exists, all_requirements_files)
    all_existing_requirements_files_str = list(set(map(str, all_existing_requirements_files)))

    if len(all_existing_requirements_files_str) == 0:
        print("No python requirements to be installed. Exiting.")
        sys.exit()

    if len(all_existing_requirements_files_str) > 1:
        print("Multiple python requirements to be installed. Might cause conflicts. Exiting.")
        sys.exit()

    requirements_path = all_existing_requirements_files_str[0]
    print(f"Installing requirements from {requirements_path}")
    install(requirements_path)
