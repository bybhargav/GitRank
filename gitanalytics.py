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

# ----- GRAPH DEALINGS -----
def build_commit_graph(commits):
    graph = {}

    for commit in commits:
        graph[commit['hash']] = commit['metadata'].get('parents',[])

    return graph


def order_commits_for_graph(
    commits: list[dict],
    graph: dict[str, list[str]],
    branch_hashes: list[str],
) -> list[dict]:
    """Topologically orders commits top-down (children before parents)."""

    if not commits:
        return []

    commit_by_hash = {c["hash"]: c for c in commits}

    # 1. Map parent -> children to track top-down dependencies
    children_map = {chash: set() for chash in commit_by_hash}

    for chash, parents in graph.items():
        if chash not in commit_by_hash:
            continue

        for p in parents:
            if p in children_map:
                children_map[p].add(chash)

    # 2. Count remaining unvisited children for each commit
    remaining_children = {
        chash: len(children)
        for chash, children in children_map.items()
    }

    def get_timestamp(chash: str) -> int:
        c = commit_by_hash.get(chash)

        if not c:
            return 0

        return c.get("metadata", {}).get("author", {}).get("time", 0)

    # 3. Find all entry points
    ready = [
        chash
        for chash, count in remaining_children.items()
        if count == 0
    ]

    ready.sort(
        key=get_timestamp,
        reverse=True,
    )

    ordered = []
    visited = set()

    # 4. Topological traversal loop
    while ready:
        curr_hash = ready.pop(0)

        if curr_hash in visited:
            continue

        visited.add(curr_hash)
        ordered.append(commit_by_hash[curr_hash])

        # Decrease remaining children count for all parents
        parents = [
            p
            for p in graph.get(curr_hash, [])
            if p in commit_by_hash
        ]

        for parent in parents:
            remaining_children[parent] -= 1

            if (
                remaining_children[parent] == 0
                and parent not in visited
            ):
                ready.append(parent)

        # Re-sort ready candidates
        ready.sort(
            key=get_timestamp,
            reverse=True,
        )

    return ordered


def print_commit_graph(
    ordered_commits: list[dict],
    graph: dict[str, list[str]],
):
    """Render the ordered commits as an ASCII graph."""

    if not ordered_commits:
        return

    commit_by_hash = {
        c["hash"]: c
        for c in ordered_commits
    }

    lanes = []

    print()
    print("--------------- GitRank - Commit Graph ---------------")
    print()

    for commit in ordered_commits:
        chash = commit["hash"]

        parents = [
            p
            for p in graph.get(chash, [])
            if p in commit_by_hash
        ]

        message = commit["message"].decode().splitlines()[0]

        # Assign column lane

        if chash not in lanes:
            lanes.append(chash)

        idx = lanes.index(chash)

        # --- Render Commit Line ---

        node_symbols = [
            "*"
            if i == idx
            else "|"
            for i in range(len(lanes))
        ]

        print(
            f"{' '.join(node_symbols)} "
            f"{chash[:7]} "
            f"{message}"
        )

        # --- Render Transitions & Update Lanes ---

        if len(parents) > 1:
            # MERGE SPLIT (|\)

            lanes[idx] = parents[0]

            lanes.insert(
                idx + 1,
                parents[1],
            )

            split_parts = []

            for i in range(len(lanes) - 1):
                if i == idx:
                    split_parts.append("|\\")
                else:
                    split_parts.append("|")

            print(
                "".join(
                    p
                    if p == "|\\"
                    else f"{p} "
                    for p in split_parts
                ).rstrip()
            )

        elif len(parents) == 1:
            parent = parents[0]

            if (
                parent in lanes
                and lanes.index(parent) != idx
            ):
                # MERGE JOIN (|/)

                target_idx = lanes.index(parent)

                join_tokens = []

                for i in range(len(lanes)):
                    if (
                        i == target_idx
                        and idx == target_idx + 1
                    ):
                        join_tokens.append("|/")

                    elif i == idx:
                        continue

                    else:
                        join_tokens.append("|")

                print(
                    " ".join(join_tokens)
                )

                lanes.pop(idx)

            else:
                # LINEAR STEP

                lanes[idx] = parent

                if (
                    len(lanes) > 1
                    or commit != ordered_commits[-1]
                ):
                    print(
                        " ".join(
                            "|" for _ in lanes
                        )
                    )

        else:
            # ROOT COMMIT

            lanes.pop(idx)

            if lanes:
                print(
                    " ".join(
                        "|" for _ in lanes
                    )
                )

    print()