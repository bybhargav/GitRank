import sys
import argparse
from pathlib import Path

import gitinfo as git
import gitanalytics as analytics
from validator import path_validator


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help="Path to the Git repository",
    )

    parser.add_argument(
        "-u",
        "--user",
        help="Show contributor statistics",
    )

    args = parser.parse_args()
    repository_path = Path(args.path)

    # ----- Repository Validation -----

    git_path = path_validator(repository_path)

    if git_path is None:
        sys.exit("Error: This directory doesn't contain a .git folder.")

    # ----- Repository History -----

    branch_hashes = git.get_branch_refs(git_path)

    commits = git.walk_commit_history(git_path,branch_hashes)

    # ----- Analytics -----

    contributors = analytics.analyze_contributors(commits)

    graph = analytics.build_commit_graph(commits)

    # 1. Order the commits top-down from branch heads
    ordered_commits = analytics.order_commits_for_graph(commits, graph, branch_hashes)

    # 2. Render the graph
    analytics.print_commit_graph(ordered_commits, graph)

    # ----- User Statistics / Contributor Ranking -----

    if args.user:
        user_commits = analytics.get_user_commits(
            commits,
            args.user,
        )

        if user_commits is None:
            sys.exit(
                f"\nError: Contributor '{args.user}' was not found.\n"
            )

        details = analytics.user_details(user_commits)
        analytics.print_user_details(details)

    else:
        ranks = analytics.rank_contributors(contributors)
        analytics.print_contributor_ranking(ranks)


# ----- MAIN -----

if __name__ == "__main__":
    main()