import argparse
import requests

def get_user_data(username):
    url = f"https://api.github.com/users/{username}/events?per_page=10"
    response = requests.get(url)
    user_data = response.json()
    if response.status_code == 200:
        for event in user_data:
            repo = event["repo"]["name"]
            if event["type"]=="CommitCommentEvent":
             action = event["payload"]["action"]
             comment = event["payload"]["comment"]
             print(f"-{action} a comment in {repo} ('{comment}')")
            elif event["type"] == "CreateEvent":
                print(f"- Created a {event["payload"]["ref_type"]} in {repo}")
            elif event["type"] == "DeleteEvent":
             thing = event["payload"]["ref_type"]
             print(f"- Deleted a {thing} in {repo}")
            elif event["type"] == "DiscussionEvent":
             action = event["payload"]["action"]
             print(f"- {action} a discussion in {repo}")
            elif event["type"] == "ForkEvent":
             action = event["payload"]["action"]
             print(f"- {action} {event["payload"]["forkee"]["name"]} to {event["payload"]["forkee"]["full_name"]}")
            elif event["type"] == "GollumEvent":
             action = event["payload"]["pages"]["action"]
             name = event["payload"]["pages"]["page_name"]
             url = event["[payload"]["pages"]["html_url"]
             print(f"- {action} the wiki page: {name} (URL:{url}")
            elif event["type"] == "IssueCommentEvent":
             action = event["payload"]["action"]
             issue_number = event["payload"]["issue"]["number"]
             print(f"- {action} an issue comment on {repo} (issue #{issue_number})")
            elif event["type"] == "IssuesEvent":
             payload = event["payload"]
             print(f"- Issue status: {payload["action"]} {repo} #{event["issue"]["number"]}")
            elif event["type"]=="MemberEvent":
                member = event["payload"]["member"]["login"]
                print(f"- {member} was {event["payload"]["action"]} as a member of {repo}")
            elif event["type"]=="PullRequestEvent":
                payload = event["payload"]
                number = payload["number"]
                print(f"- {payload["action"]} #{number} in {repo}: https://github.com/{repo}/pull/{number}")
            elif event["type"]=="PullRequestReviewEvent":
                payload = event["payload"]
                review = payload["review"]
                pr = payload["pull_request"]
                print(f"- {review["state"]} review on {repo} #{pr["number"]}: {review["_links"]["html"]["href"]}")
            elif event["type"]=="PushEvent":
                payload = event["payload"]
                try:
                 commit_count_url = f"https://api.github.com/repos/{repo}/compare/{payload["before"]}...{payload["head"]}"
                 commit_count_response = requests.get(commit_count_url)
                 commit_count_data = commit_count_response.json()
                 commit_amount = commit_count_data["total_commits"]
                 if commit_amount > 1:
                  print(f"- Pushed {commit_amount} commits in {repo}")
                 else:
                  print(f"- Pushed {commit_amount} commit in {repo}")
                except KeyError:
                        print(f"- Pushed to {repo}")
            elif event["type"]=="WatchEvent":
                print(f"- Had a peek inside {repo}")
            elif "API rate limit exceeded" in user_data("message", ""):
                print("Rate limit exceeded, try again later")
            else:
                print(f"Failed to retrieve data {response.status_code}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username")
    args = parser.parse_args()
    get_user_data(args.username)


if __name__ == "__main__":
    main()