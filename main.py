import sys
from pathlib import Path

from validator import path_validator
from gitinfo import (
    resolve_head,
    read_ref,
    locate_object,
    read_object,
    decompress_object,
    split_object,
    parse_body,
)

# ============================================================
# Repository Input
# ============================================================

# Ensure a repository path is provided.
if len(sys.argv) == 1:
    sys.exit("Usage: python main.py <repository_path>")

path = Path(sys.argv[1])

# ============================================================
# Repository Validation
# ============================================================

# Validate the repository and locate its .git directory.
git_path = path_validator(path)

if git_path is None:
    sys.exit("Error: This directory doesn't contain a .git folder.")

# ============================================================
# HEAD Resolution
# ============================================================

# Resolve HEAD to the currently checked-out branch
# and retrieve the latest commit hash.
head_ref = resolve_head(git_path)
current_commit_hash = read_ref(head_ref)

# ============================================================
# Commit Object Resolution
# ============================================================

# Locate the commit object using its SHA-1 hash.
commit_object_path = locate_object(git_path, current_commit_hash)

# Read the compressed commit object from disk.
commit_object_bytes = read_object(commit_object_path)

# Decompress the commit object.
commit_object_data = decompress_object(commit_object_bytes)

# Split the object into its header and body.
commit_header, commit_body = split_object(commit_object_data)

# Parse the commit body into structured Python data.
commit_metadata, commit_message = parse_body(commit_header,commit_body)

# ============================================================
# Tree Object Resolution
# ============================================================

# Every commit points to exactly one root tree.
# Retrieve its SHA-1 hash from the parsed commit metadata.
tree_hash = commit_metadata["tree"]
print(type(tree_hash))
# Locate the root tree object.
tree_object_path = locate_object(git_path, tree_hash)

# Read the compressed tree object.
tree_object_bytes = read_object(tree_object_path)

# Decompress the tree object.
tree_object_data = decompress_object(tree_object_bytes)

# Split the tree object into its header and body.
tree_header, tree_body = split_object(tree_object_data)

# Parse every tree entry (mode, filename and object hash).
tree_entries = parse_body(tree_header,tree_body)  

# ============================================================
# Output
# ============================================================

print(tree_entries)
print("\n\n\n\n")
print(commit_metadata,commit_message)