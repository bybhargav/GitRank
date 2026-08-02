import sys
from pathlib import Path

from validator import path_validator
from gitinfo import (
    resolve_head,
    read_ref,
    locate_object,
    read_object,
    decompress_object,
    split_object,split_header ,
    parse_header, parse_body, parse_metadata
)

# ============================================================
# Repository Input
# ============================================================

# Ensure the user provides a repository path.
if len(sys.argv) == 1:
    sys.exit("Usage: python main.py <repository_path>")

path = Path(sys.argv[1])

# ============================================================
# Repository Validation
# ============================================================

# Validate the repository and locate the .git directory.
git_path = path_validator(path)

if git_path is None:
    sys.exit("Error: This directory doesn't contain any .git folder")

# ============================================================
# HEAD Resolution
# ============================================================

# Resolve HEAD to the current branch reference and
# retrieve the latest commit hash.
head_ref = resolve_head(git_path)
current_commit = read_ref(head_ref)

# ============================================================
# Git Object Resolution
# ============================================================

# Locate the commit object using its SHA-1 hash,
# then read the compressed object from disk.
object_path = locate_object(git_path, current_commit)
byte_data = read_object(object_path)

# ============================================================
# Object Decompression
# ============================================================

# Git stores objects in compressed form (zlib).
# Decompress the object to reveal its original contents.
decompressed_data = decompress_object(byte_data)

# Split the decompressed object into its header and body.
header, body = split_object(decompressed_data)

# Parse the object body based on its header.
commit_metadata, commit_message  = parse_body(header,body)

tree_hash = commit_metadata["tree"] 
tree_object_path = locate_object(git_path, tree_hash)
tree_byte_data = read_object(tree_object_path)
decompressed_tree_byte = decompress_object(tree_byte_data)
tree_header, tree_body = split_object(decompressed_tree_byte)
#tree_metadata, tree_message = parse_body(tree_header,tree_body)