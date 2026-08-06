import sys
from pathlib import Path

from validator import path_validator
from gitinfo import (
    resolve_head,
    read_ref,
    load_commit,
    walk_tree,
    walk_commit_history,
)


# ============================================================
# Repository Input
# ============================================================

if len(sys.argv) != 2:
    sys.exit("Usage: python main.py <repository_path>")

repository_path = Path(sys.argv[1])


# ============================================================
# Repository Validation
# ============================================================

git_path = path_validator(repository_path)

if git_path is None:
    sys.exit("Error: This directory doesn't contain a .git folder.")


# ============================================================
# HEAD Resolution
# ============================================================

head_ref = resolve_head(git_path)
current_commit_hash = read_ref(head_ref)


# ============================================================
# Commit Object
# ============================================================

commit_metadata, commit_message = load_commit(
    git_path,
    current_commit_hash,
)

tree_hash = commit_metadata["tree"]


# ============================================================
# Repository Tree
# ============================================================

repository_files = walk_tree(
    git_path,
    tree_hash,
)


# ============================================================
# Output
# ============================================================

"""print("Commit Metadata")
print("================")
print(commit_metadata)

print("\nCommit Message")
print("==============")
print(commit_message.decode())

print("\nRepository Files")
print("================")


for entry in repository_files:
    print(entry)"""

commits = walk_commit_history(git_path,current_commit_hash)

for commit in commits:
    print(commit["metadata"]["author"]["name"])
    print(commit["message"].decode())
    print("-" * 40)