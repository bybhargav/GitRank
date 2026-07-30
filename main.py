import sys
from pathlib import Path

# Repository statistics
directory = 0
files = 0
GitPath = None


def dir_count(path: Path):
    """
    Recursively traverse a directory and count
    all files and subdirectories.
    """
    global directory, files

    for entry in path.iterdir():

        if entry.is_file():
            files += 1

        if entry.is_dir():
            directory += 1
            dir_count(entry)


def main():
    """
    Entry point of GitRank.
    Validates user input and scans the repository.
    """
    global directory, files, GitPath

    # --------------------------------------------------
    # Validate command-line arguments
    # --------------------------------------------------
    if len(sys.argv) == 1:
        sys.exit("Usage: python main.py <repository_path>")

    path = Path(sys.argv[1])

    # --------------------------------------------------
    # Validate repository path
    # --------------------------------------------------
    if not path.exists():
        sys.exit("Error: Path does not exist.")

    if not path.is_dir():
        sys.exit("Error: Please provide a directory.")

    print(f"Scanning repository: {path}")

    # --------------------------------------------------
    # Scan repository contents
    # --------------------------------------------------
    for item in path.iterdir():

        # Detect Git repository
        if item.name == ".git":
            GitPath = item

        # Count directories recursively
        if item.is_dir():
            directory += 1
            dir_count(item)

        # Count files
        if item.is_file():
            files += 1

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------
    print(f"Directories : {directory}")
    print(f"Files       : {files}")

    if GitPath is not None:
        print(f"Git Directory: {GitPath}")
    else:
        print("Not a Git repository.")


if __name__ == "__main__":
    main()