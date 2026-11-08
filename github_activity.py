import argparse
import requests

def get_user_data(username):
    url = f"https://api.github.com/users/{username}/events?per_page=10"
    response = requests.get(url)
    user_data = response.json()
    if response.status_code != 200:
     message = user_data.get("message", "Unknown error") if isinstance(user_data, dict) else "Unknown error"
     print(f"Failed to retrieve data: {message}")
     return
    elif response.status_code == 200:
        print("\n  10 MOST RECENT EVENTS\n  _____________________\n")
        for event in user_data:
            repo = event["repo"]["name"]
            if event["type"]=="CommitCommentEvent":
                action = event["payload"]["action"]
                comment = event["payload"]["comment"]
                print(f"-{action.capitalize()} a comment in {repo} ('{comment}')")
            elif event["type"] == "CreateEvent":
                ref_type = event["payload"]["ref_type"]
                print(f"- Created a {ref_type} in {repo}")
            elif event["type"] == "DeleteEvent":
                thing = event["payload"]["ref_type"]
                print(f"- Deleted a {thing} in {repo}")
            elif event["type"] == "DiscussionEvent":
                action = event["payload"]["action"]
                print(f"- {action.capitalize()} a discussion in {repo}")
            elif event["type"] == "ForkEvent":
                action = event["payload"]["action"]
                name = event["payload"]["forkee"]["name"]
                full_name = event["payload"]["forkee"]["full_name"]
                print(f"- {action.capitalize()} {name} to {full_name}")
            elif event["type"] == "GollumEvent":
                for page in event["payload"]["pages"]:
                    action = page["action"]
                    name = page["page_name"]
                    url = page["html_url"]
                    print(f"- {action.capitalize()} wiki page '{name}' in {repo}: {url}")
            elif event["type"] == "IssueCommentEvent":
                action = event["payload"]["action"]
                issue_number = event["payload"]["issue"]["number"]
                print(f"- {action.capitalize()} an issue comment on {repo} (issue #{issue_number})")
            elif event["type"] == "IssuesEvent":
                action = event["payload"]["action"]
                issue_number = event["payload"]["issue"]["number"]
                print(f"- {action.capitalize()} an issue in {repo} (issue #{issue_number})")
            elif event["type"]=="MemberEvent":
                member = event["payload"]["member"]["login"]
                action = event["payload"]["action"]
                print(f"- {member.capitalize()} was {action} as a member of {repo}")
            elif event["type"] == "PublicEvent":
                print(f"- Made the repo {repo} public")
            elif event["type"]=="PullRequestEvent":
                action = event["payload"]["action"]
                number = event["payload"]["number"]
                print(f"- {action.capitalize()} pull request #{number} in {repo}")
            elif event["type"]=="PullRequestReviewEvent":
                review = event["payload"]["review"]
                pr_number = event["payload"]["pull_request"]["number"]
                print(f"- {review["state"].capitalize()} on {repo} (#{pr_number})")
            elif event["type"] == "PullRequestReviewCommentEvent":
                action = event["payload"]["action"]
                print(f"- {action.capitalize()} a pull request review comment on {repo}")
            elif event["type"]=="PushEvent":
                try:
                    before = event["payload"]["before"]
                    head = event["payload"]["head"]
                    commit_count_url = f"https://api.github.com/repos/{repo}/compare/{before}...{head}"
                    commit_count_response = requests.get(commit_count_url)
                    commit_count_data = commit_count_response.json()
                    commit_amount = commit_count_data["total_commits"]
                    if commit_amount > 1:
                        print(f"- Pushed {commit_amount} commits in {repo}")
                    else:
                        print(f"- Pushed {commit_amount} commit in {repo}")
                except KeyError:
                    print(f"- Pushed to {repo}")
            elif event["type"] == "ReleaseEvent":
                action = event["payload"]["action"]
                print(f"{action.capitalize()} {repo}")
            elif event["type"] == "WatchEvent":
                print(f"- Starred {repo}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username")
    args = parser.parse_args()
    get_user_data(args.username)


if __name__ == "__main__":
    main()