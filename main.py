import sys
from pathlib import Path
from validator import path_validator
import gitinfo as git
import gitanalytics as analytics


# -----  Repository Input ----- 

if len(sys.argv) != 2:
    sys.exit("Usage: python main.py <repository_path>")

repository_path = Path(sys.argv[1])


# -----  Repository Validation ----- 

git_path = path_validator(repository_path)

if git_path is None:
    sys.exit("Error: This directory doesn't contain a .git folder.")


# -----  HEAD Resolution ----- 

head_ref = git.resolve_head(git_path)
current_commit_hash = git.read_ref(head_ref)


# ----- commit object -----
commit_metadata, commit_message = git.load_commit(
    git_path,
    current_commit_hash,
)

tree_hash = commit_metadata["tree"]


# ----- Repository Tree -----

repository_files = git.walk_tree(git_path,tree_hash)


# ----- OUTPUT -----

commits = (git.walk_commit_history(git_path,current_commit_hash))
print(type(commits))
contributors = analytics.analyze_contributors(commits)

ranks = analytics.rank_contributors(contributors)
print()
print("------------- GitRank Statistics -----------")
print(f"{'Rank':<8}{'Name':<25}{'Commits':>10}")
print("--------------------------------------------")

for contributor in ranks:
    print(
        f"{contributor['rank']:<8}"
        f"{contributor['name']:<25}"
        f"{contributor['commits']:>10}"
    )

print("--------------------------------------------")
print()