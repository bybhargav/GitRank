from pathlib import Path
import zlib


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

def main():
    repo = Path(".git")


if __name__ == "__main__":
    main()