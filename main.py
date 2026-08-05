import sys
from pathlib import Path

from validator import path_validator
from gitinfo import (
    load_commit,
    resolve_head, load_tree,
    read_ref,
    locate_object,
    read_object,
    decompress_object,
    split_object,
    parse_commit_body, parse_tree_body, parse_blob_body,
    walk_tree,
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

# intiating commit 
commit_metadata, commit_message = load_commit( git_path, current_commit_hash)
print(commit_metadata, commit_message)

tree_entries = load_tree(git_path, commit_metadata["tree"])
tree_hash = commit_metadata["tree"]  

# Locate the root tree object.
tree_object_path = locate_object(git_path, tree_hash)

# Read the compressed tree object.
tree_object_bytes = read_object(tree_object_path)

# Decompress the tree object.
tree_object_data = decompress_object(tree_object_bytes)

# Split the tree object into its header and body.
tree_header, tree_body = split_object(tree_object_data)

# Parse every tree entry (mode, filename and object hash).
tree_entries = parse_tree_body(tree_body)  


# ============================================================
# Blob Object Resolution
# ============================================================



# ============================================================
# Output
# ============================================================

for entry in tree_entries: 
    object_path = locate_object(git_path, entry["hash"])
    object_bytes = read_object(object_path)
    object_data = decompress_object(object_bytes)
    header, body = split_object(object_data)
    blob_content = parse_blob_body( body)


tree_data = walk_tree(git_path,tree_hash)
for i in tree_data:
    print(i)
