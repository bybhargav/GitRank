import sys
from pathlib import Path
from validator import path_validator
from gitinfo import resolve_head, read_ref, locate_object, read_object, decompress_object

if len(sys.argv) == 1:
    sys.exit("Usage: python main.py <repository_path>")

path = Path(sys.argv[1])

git_path = path_validator(path)

if git_path is None:
    sys.exit("Error: This directory doesn't contain any .git folder")

head_ref = resolve_head(git_path)
current_commit = read_ref(head_ref)

object_path = locate_object(git_path,current_commit)
byte_data = read_object(object_path)
decompressed_data = decompress_object(byte_data)

print(type(decompressed_data))
print(decompressed_data)