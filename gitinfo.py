from pathlib import Path
import zlib
from datetime import datetime

# ============================================================
# HEAD
# ============================================================

def read_head(path: Path) -> str:
    """Read the HEAD file and return the reference path."""
    file = open(path / "HEAD", "r")
    content = file.read().strip()
    file.close()

    return content.removeprefix("ref: ")


def resolve_head(path: Path) -> Path:
    """Resolve HEAD to its reference file."""
    return path / read_head(path)


# ============================================================
# REFERENCES
# ============================================================

def read_ref(path: Path) -> str:
    """Read a Git reference and return the commit hash."""
    file = open(path, "r")
    content = file.read().strip()
    file.close()

    return content


# ============================================================
# OBJECTS
# ============================================================

def locate_object(git_path: Path, commit_hash: str) -> Path:
    """Locate a Git object from its SHA-1 hash."""
    return git_path / "objects" / commit_hash[:2] / commit_hash[2:]

def read_object(object_path: Path) -> bytes:
    """Read the compressed Git object."""
    file = open(object_path, "rb")
    byte_data = file.read()
    file.close()

    return byte_data

def decompress_object(byte_data: bytes) -> bytes:
    """Decompress a Git object using zlib."""
    return zlib.decompress(byte_data)

def split_object(combined_data:bytes)-> tuple[bytes,bytes]:
    """Separate a Git object into its header and body."""
    header, body = combined_data.split(b"\x00", maxsplit=1) 
    return header, body

def split_header(header: bytes) -> tuple[bytes, bytes]:
    """Split an object header into its type and size."""
    object_type, object_size = header.split(b" ", maxsplit=1)
    return object_type, object_size

def parse_header(object_type_bytes: bytes, 
                 object_size_bytes:bytes
                 ) -> tuple[str,int]:
    """Convert header bytes into an object type and object size."""
    object_size = int(object_size_bytes)
    object_type = object_type_bytes.decode()
    
    return object_type, object_size

def parse_commit(body:bytes) -> tuple[dict,bytes]:
    metadata_bytes, commit_message = body.split(b"\n\n", maxsplit=1)
    parsed_metadata = parse_metadata(metadata_bytes)
    return parsed_metadata, commit_message

def parse_tree(body)-> tuple[dict,bytes]:
    ...

def parse_blob(body):
    ... 

def parse_metadata(metadata_bytes: bytes) -> dict[str, str | list[str]]:
    parsed_metadata = {}
    
    for line in metadata_bytes.split(b"\n"):
        key, value = line.split(b" ", maxsplit=1)

        if key == b"parent": 
            parent_hash = value.decode()
            if "parents" not in parsed_metadata:
                parsed_metadata["parents"] = []
            parsed_metadata["parents"].append(parent_hash)
            
        else: 
            parsed_metadata[key.decode()] = value.decode()

    parsed_metadata["author"] = parse_identity(parsed_metadata["author"] )
    parsed_metadata["committer"] = parse_identity(parsed_metadata["committer"])

    return parsed_metadata


def parse_body(header: bytes, body: bytes) :
    object_type_bytes, object_size_bytes = split_header(header)

    object_type, object_size = parse_header(
        object_type_bytes,
        object_size_bytes)

    if object_type == "commit":
        return parse_commit(body)

    elif object_type == "tree":
        return parse_tree(body)
    



def parse_identity(author):
    author_list = author.split()
    author_metadata = {}

    dt = datetime.fromtimestamp(int(author_list[-2]))

    author_metadata["name"] = " ".join(author_list[:-3])
    author_metadata["email"] = author_list[-3]
    author_metadata["time"] = int(author_list[-2])
    author_metadata["datetime"] = dt.strftime("%d-%m-%Y %H:%M:%S")
    author_metadata["time_zone"] = author_list[-1]

    return author_metadata



def main():
    repo = Path(".git")


if __name__ == "__main__":
    main()