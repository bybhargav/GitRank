from pathlib import Path
import zlib
def read_head(path:Path):
    
    main_path = open(path/"HEAD", "r")
    content = main_path.read().strip()
    main_path.close()
    return content.removeprefix("ref: ")

def resolve_head(path:Path):
    return path/read_head(path)

def read_ref(path: Path):
    file = open(path, "r")
    content = file.read().strip()
    file.close()
    return content 

def locate_object(path: Path, commit_hash: str):
    return path / "objects" / commit_hash[:2] / commit_hash[2:]

def read_object(object_path: Path) -> bytes:
    file = open(object_path,"rb")
    byte_data = file.read()
    file.close()
    return byte_data

def decompress_object(byte_data: bytes) -> bytes:
    return zlib.decompress(byte_data)


def main():
    repo = Path(".git")


if __name__ == "__main__":
    main()
