import sys
from pathlib import Path
from validator import path_validator


if len(sys.argv) == 1:
    sys.exit("Usage: python main.py <repository_path>")

path = Path(sys.argv[1])

git_path = path_validator(path)

if git_path is None:
    sys.exit("Error: This directory doesn't contain any .git folder")
