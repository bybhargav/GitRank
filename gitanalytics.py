# ----- CONTRIBUTOR STASTICS ----- 

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