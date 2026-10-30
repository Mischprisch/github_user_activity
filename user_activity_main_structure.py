import argparse
import requests


parser = argparse.ArgumentParser()

parser.add_argument("username", help="username")

args = parser.parse_args()



def get_user_data(username):
    url = f"https://api.github.com/users/{username}/events?per_page=5"
    response = requests.get(url)
    user_data = response.json()
    if response.status_code == 200:
        events = user_data
        for event in events:
            if event["type"]=="CreateEvent":
                print(f"- Created something in {event["repo"]["name"]}")
            elif event["type"]=="MemberEvent":
                print(f"- {event["payload"]["member"]["login"]} was {event["payload"]["action"]} as a member of {event["repo"]["name"]}")
            elif event["type"]=="PullRequestReviewEvent":
                payload = event["payload"]
                review = payload["review"]
                pr = payload["pull_request"]
                print(f"- {review["state"]} review on {event["repo"]["name"]}#{pr["number"]}: {review["_links"]["html"]["href"]}")
            elif event["type"]=="PushEvent":
                payload = event["payload"]
                try:
                    commit_count_url = f"https://api.github.com/repos/{event["repo"]["name"]}/compare/{payload["before"]}...{payload["head"]}"
                    commit_count_response = requests.get(commit_count_url)
                    commit_count_data = commit_count_response.json()
                    commit_amount = commit_count_data["total_commits"]
                    print(f"- Pushed {commit_amount} commit(s) in {event["repo"]["name"]}")
                except KeyError:
                        print(f"- Pushed to {event["repo"]["name"]}")
            elif event["type"]=="WatchEvent":
                print(f"- Had a peek inside {event["repo"]["name"]}")

    elif response.status_code == 403 and "API rate limit exceeded" in user_data["message"]:
        print("Rate limit exceeded, try again later")
    else:
        print(f"Failed to retrieve data {response.status_code}")


if args.username:
    get_user_data(args.username)

