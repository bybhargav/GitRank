# ----- CONTRIBUTOR STATISTICS -----

def analyze_contributors(commits):
    contributors = {}

    for commit in commits:
        author = commit["metadata"]["author"]["name"]
        
        if author not in contributors:
            contributors[author] = {"commits": 0}

        contributors[author]["commits"] += 1

    return contributors


def repo_details(commits, tree_data):
    total_contributors =len(analyze_contributors(commits))
    total_directories = set()
    
    for path in tree_data:
        # Extract the directory name from the file path.
        # Ignore the filename since only unique directories are needed.
        if "/" in path["path"]: 
            directory_name, _ = path['path'].rsplit("/", maxsplit=1)    
            total_directories.add(directory_name)

    summary = {"total_commits": len(commits), 
                    "total_contributors": total_contributors,
                    "total_files" : len(tree_data),
                    "total_directories": len(total_directories),
                    }

    return summary


def rank_contributors(contributors):
    """Rank contributors based on the number of commits."""
    rank = []
    number = 0
    for name, data in sorted(contributors.items(), key=lambda item: item[1]["commits"], reverse=True):
        number += 1
        rank.append({"rank": number,"name": name, "commits": data["commits"]})

    return rank


def print_contributor_ranking(ranks):
    """Display contributor rankings in a formatted table."""

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


def get_user_commits(commits:list, username:str) ->list | None :
    commits_made_by_user = []
    for commit in commits:
        
        if commit['metadata']['author']["name"] == username:
            commits_made_by_user.append(commit)
    if not commits_made_by_user: return None
    return commits_made_by_user


def user_details(user_commits : list)->dict:
    details = {}
    details['Name'] = user_commits[0]["metadata"]["author"]["name"]
    details['Email'] = user_commits[0]["metadata"]["author"]["email"]
    details['Total Commits'] = len(user_commits)

    first_commit = user_commits[0]
    last_commit = user_commits[0]

    for commit in user_commits:
        timestamp = commit["metadata"]["author"]["time"]
    
        if first_commit is None or timestamp < first_commit["metadata"]["author"]["time"]:
            first_commit = commit
    
        if last_commit is None or timestamp > last_commit["metadata"]["author"]["time"]:
            last_commit = commit
    merge_commits = 0

    for commit in user_commits:
        parents = commit["metadata"].get("parents", [])

        if len(parents) > 1:
            merge_commits += 1

    details["Merge Commits"] = merge_commits
    
    details["First Commit"] = first_commit["metadata"]["author"]["datetime"]  # pyright: ignore[reportOptionalSubscript]
    details["Last Commit"] = last_commit["metadata"]["author"]["datetime"] # pyright: ignore[reportOptionalSubscript]

    details["First Commit Message"] = first_commit["message"].decode().strip() # pyright: ignore[reportOptionalSubscript]
    details["Last Commit Message"] = last_commit["message"].decode().strip() # pyright: ignore[reportOptionalSubscript]

    return details 


def print_user_details(details: dict):
    """Display user details."""

    print()
    print("--------------------------------------------")
    print("--------- GitRank - User Statistics --------")
    print("--------------------------------------------")

    print(f"Name                : {details['Name']}")
    print(f"Email               : {details['Email']}")
    print(f"Total Commits       : {details['Total Commits']}")
    print(f"Merge Commits       : {details['Merge Commits']}")
    print(f"First Commit        : {details['First Commit']}")
    print(f"Last Commit         : {details['Last Commit']}")

    print()
    print(f"First Commit Message:")
    print(f"  {details['First Commit Message']}")

    print()
    print(f"Last Commit Message:")
    print(f"  {details['Last Commit Message']}")

    print("--------------------------------------------")
    print()

