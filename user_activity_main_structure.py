import argparse
import requests


parser = argparse.ArgumentParser()

parser.add_argument("username", help="username")

args = parser.parse_args()

def get_user_data(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        events = [user_data[0], user_data[1], user_data[2]]
        for event in events:
            if event["type"]=="CreateEvent":
                print(f"- Created something in {event["repo"]["name"]}")
            if event["type"]=="PushEvent":
                try:
                  commit_count_url = f"https://api.github.com/repos/{event["repo"]["name"]}/compare/{event["payload"]["before"]}...{event["payload"]["head"]}"
                  commit_count_response = requests.get(commit_count_url)
                  commit_count_data = commit_count_response.json()
                  commit_amount = commit_count_data["total_commits"]
                  print(f"- Pushed {commit_amount} commits in {event["repo"]["name"]}")
                except KeyError:
                    print(f"- Pushed to {event["repo"]["name"]}")
    else:
        print(f"Failed to retrieve data {response.status_code}")
        pass


if args.username:
    get_user_data(args.username)

