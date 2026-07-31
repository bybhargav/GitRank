from pathlib import Path


def read_head(path:Path):
    
    main_path = open(path/"HEAD", "r")
    content = main_path.read()
    main_path.close()
    return content.removeprefix("ref: ")

def resolve_head(path:Path):
    return path/read_head(path)

def main():

    repo = Path("/Users/sairaju/Documents/bybhargav/GitRank/.git")
    print(read_head(repo))


if __name__ == "__main__":
    main()
