import sys
import argparse
import gitinfo as git
from pathlib import Path
import gitanalytics as analytics
from validator import path_validator

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p","--path",required=True,
                        help="Path to the Git repository")

    parser.add_argument("-u","--user",
                        help="Show contributor statistics")


    args = parser.parse_args()
    repository_path = Path(args.path)


    # ----- Repository Validation -----

    git_path = path_validator(repository_path)

    if git_path is None:
        sys.exit("Error: This directory doesn't contain a .git folder.")


    # -----  HEAD Resolution ----- 

    head_ref = git.resolve_head(git_path)
    current_commit_hash = git.read_ref(head_ref)


    # ----- OUTPUT -----

    commits = git.walk_commit_history(git_path,current_commit_hash)
    contributors = analytics.analyze_contributors(commits)
  
    if args.user:
        user_commits = analytics.get_user_commits(commits,args.user)
        if user_commits is None:
            sys.exit(f"\n Error: Contributor '{args.user}' was not found.\n")
        else:
            details = analytics.user_details(user_commits)
            analytics.print_user_details(details)
    
    else:
        ranks = analytics.rank_contributors(contributors)
        analytics.print_contributor_ranking(ranks)


# ----- MAIN -----
if __name__ == "__main__":
    main()