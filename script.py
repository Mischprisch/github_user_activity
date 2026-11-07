
import requests

url = "https://api.github.com/events?per_page=100"
events = requests.get(url, timeout=10).json()

users = {
    event["actor"]["login"]
    for event in events
    if event["type"] == "IssueCommentEvent"
}

for username in users:
    url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        continue

    user_events = response.json()

    if user_events and user_events[0]["type"] == "IssueCommentEvent":
        print("Gevonden:", username)
        print("API:", url)
        break
