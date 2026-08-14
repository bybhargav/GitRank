import sys
import argparse
from pathlib import Path

import gitinfo as git
import gitanalytics as analytics
from progress import show_progress,show_banner
from validator import path_validator

show_banner()
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

    parser.add_argument(
        "-g",
        "--graph",
        action="store_true",
        help="Show entire commit graph",
    )

    args = parser.parse_args()
    repository_path = Path(args.path)

    show_progress("Validating repository", 10)

    git_path = path_validator(repository_path)

    if git_path is None:
        sys.exit("Error: This directory doesn't contain a .git folder.")

    show_progress("Reading commit history", 40)

    branch_hashes = git.get_branch_refs(git_path)

    commits = git.walk_commit_history(
        git_path,
        branch_hashes,
    )

    show_progress("Analyzing contributors", 70)

    contributors = analytics.analyze_contributors(commits)

    if args.graph:
        show_progress("Building commit graph", 90)

        graph = analytics.build_commit_graph(commits)

        ordered_commits = analytics.order_commits_for_graph(
            commits,
            graph,
            branch_hashes,
        )
        show_progress("Yeah. We cooked. 🔥", 100)
        analytics.print_commit_graph(ordered_commits,graph)

    elif args.user:
        show_progress("Preparing user statistics", 90)

        user_commits = analytics.get_user_commits(
            commits,
            args.user,
        )

        if user_commits is None:
            sys.exit(
                f"\nError: Contributor '{args.user}' was not found.\n"
            )

        details = analytics.user_details(user_commits)
        show_progress("Yeah. We cooked. 🔥", 100)
        analytics.print_user_details(details)

    else:
        show_progress("Preparing contributor ranking", 90)

        ranks = analytics.rank_contributors(contributors)
        show_progress("Yeah. We cooked. 🔥", 100)
        analytics.print_contributor_ranking(ranks)

    
if __name__ == "__main__":
    main()