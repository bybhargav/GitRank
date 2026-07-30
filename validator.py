from pathlib import Path
import sys


def path_validator(path:Path):

    if not path.exists():
        sys.exit("Error: Path does not exist.")

    if not path.is_dir():
        sys.exit("Error: Please provide a directory.")

    git_path = path/".git"
    if git_path.is_dir():
        return git_path
    
    return None
