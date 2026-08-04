from pathlib import Path
import zlib
from datetime import datetime

# ============================================================
# HEAD
# ============================================================

def read_head(path: Path) -> str:
    """Read the HEAD file and return the current reference path."""
    file = open(path / "HEAD", "r")
    content = file.read().strip()
    file.close()

    return content.removeprefix("ref: ")


def resolve_head(path: Path) -> Path:
    """Resolve HEAD to the reference file of the current branch."""
    return path / read_head(path)


# ============================================================
# REFERENCES
# ============================================================

def read_ref(path: Path) -> str:
    """Read a Git reference file and return its commit hash."""
    file = open(path, "r")
    content = file.read().strip()
    file.close()

    return content


# ============================================================
# OBJECTS
# ============================================================

def locate_object(git_path: Path, object_hash: str) -> Path:
    """Locate a Git object using its SHA-1 hash."""
    return git_path / "objects" / object_hash[:2] / object_hash[2:]


def read_object(object_path: Path) -> bytes:
    """Read a compressed Git object from disk."""
    file = open(object_path, "rb")
    byte_data = file.read()
    file.close()

    return byte_data


def decompress_object(byte_data: bytes) -> bytes:
    """Decompress a Git object using zlib."""
    return zlib.decompress(byte_data)


def split_object(combined_data: bytes) -> tuple[bytes, bytes]:
    """Split a Git object into its header and body."""
    header, body = combined_data.split(b"\x00", maxsplit=1)
    return header, body


def split_header(header: bytes) -> tuple[bytes, bytes]:
    """Split an object header into its type and size."""
    object_type, object_size = header.split(b" ", maxsplit=1)
    return object_type, object_size


def parse_header(
    object_type_bytes: bytes,
    object_size_bytes: bytes,
) -> tuple[str, int]:
    """Convert header bytes into Python types."""
    object_type = object_type_bytes.decode()
    object_size = int(object_size_bytes)

    return object_type, object_size


# ============================================================
# COMMIT OBJECT
# ============================================================

def parse_commit_body(body: bytes) -> tuple[dict, bytes]:
    """Parse a commit body into commit metadata and commit message."""

    # A commit body consists of:
    #
    # metadata
    #
    # commit message
    metadata_bytes, commit_message = body.split(b"\n\n", maxsplit=1)

    parsed_metadata = parse_metadata(metadata_bytes)

    return parsed_metadata, commit_message


def parse_metadata(metadata_bytes: bytes) -> dict[str, str | dict | list[str]]:
    """Parse commit metadata into structured Python objects."""

    parsed_metadata = {}

    # Read every metadata line.
    for line in metadata_bytes.split(b"\n"):

        # Every metadata line begins with:
        #
        # key value
        key, value = line.split(b" ", maxsplit=1)

        # A commit may contain multiple parent commits.
        if key == b"parent":

            if "parents" not in parsed_metadata:
                parsed_metadata["parents"] = []

            parsed_metadata["parents"].append(value.decode())

        else:
            parsed_metadata[key.decode()] = value.decode()

    # Convert author and committer metadata into structured dictionaries.
    parsed_metadata["author"] = parse_identity(parsed_metadata["author"])
    parsed_metadata["committer"] = parse_identity(parsed_metadata["committer"])

    return parsed_metadata


def parse_identity(identity: str) -> dict:
    """Parse an author or committer identity."""

    identity_parts = identity.split()

    timestamp = int(identity_parts[-2])
    dt = datetime.fromtimestamp(timestamp)

    return {
        "name": " ".join(identity_parts[:-3]),
        "email": identity_parts[-3],
        "time": timestamp,
        "datetime": dt.strftime("%d-%m-%Y %H:%M:%S"),
        "time_zone": identity_parts[-1],
    }


# ============================================================
# TREE OBJECT
# ============================================================

def parse_tree_body(tree_body: bytes) -> list[dict[str, str]]:
    """Parse a Git tree body into a list of tree entries."""

    entries = []
    offset = 0

    # Read one tree entry at a time until the end of the tree body.
    while offset < len(tree_body):

        # Read the file mode.
        # Examples:
        #   100644 -> regular file
        #   100755 -> executable
        #   40000  -> directory
        space_index = tree_body.find(b" ", offset)
        mode = tree_body[offset:space_index]
        offset = space_index + 1

        # Read the file or directory name.
        # The name ends at the NUL (\x00) separator.
        null_index = tree_body.find(b"\x00", offset)
        filename = tree_body[offset:null_index]
        offset = null_index + 1

        # Read the raw 20-byte SHA-1 object ID.
        hash_bytes = tree_body[offset:offset + 20]
        offset += 20
        
        # Convert the parsed entry into Python types.
        entries.append(
            {
                "mode": parse_mode(mode.decode()),
                "name": filename.decode(),
                "hash": hash_bytes.hex(),
            }
        )

    return entries

def parse_mode(mode: str) -> dict[str, str]:
    """Parse a Git file mode into structured metadata."""

    mode_map = {
        "100644": "regular_file",
        "100755": "executable_file",
        "40000": "directory",
        "120000": "symbolic_link",
        "160000": "git_submodule",
    }

    return {
        "value": mode,
        "type": mode_map.get(mode, "unknown"),
    }

from pathlib import Path


def walk_tree(
    git_path: Path,
    tree_hash: str,
    current_path: Path = Path(),
) -> list[dict]:
    """
    Recursively traverse a Git tree and return every file entry
    with its full repository path.
    """

    results = []

    # ============================================================
    # Load and parse the current tree object.
    # ============================================================

    tree_object_path = locate_object(git_path, tree_hash)
    tree_object_bytes = read_object(tree_object_path)
    tree_object_data = decompress_object(tree_object_bytes)

    tree_header, tree_body = split_object(tree_object_data)
    tree_entries = parse_body(tree_header, tree_body)

    # ============================================================
    # Walk through every entry in the current tree.
    # ============================================================

    for entry in tree_entries:

        # Build the complete repository path for this entry.
        full_path = current_path / entry["name"]

        # Directory → recurse into the child tree.
        if entry["mode"]["type"] == "directory":

            child_results = walk_tree(
                git_path,
                entry["hash"],
                full_path,
            )

            results.extend(child_results)

        # File → store its metadata.
        else:

            file_entry = entry.copy()
            file_entry["path"] = str(full_path)

            results.append(file_entry)

    return results
        
  

    return tree_entries


# ============================================================
# BLOB OBJECT
# ============================================================

def parse_blob_body(body: bytes):
    """Parse a blob object."""
    return body


# ============================================================
# OBJECT DISPATCHER
# ============================================================

def parse_body(header: bytes, body: bytes):
    """Dispatch an object body to its corresponding parser."""

    object_type_bytes, object_size_bytes = split_header(header)

    object_type, _ = parse_header(
        object_type_bytes,
        object_size_bytes,
    )

    if object_type == "commit":
        return parse_commit_body(body)

    elif object_type == "tree":
        return parse_tree_body(body)

    elif object_type == "blob":
        return parse_blob_body(body)

    raise ValueError(f"Unsupported object type: {object_type}")


def main():
    repo = Path(".git")


if __name__ == "__main__":
    main()