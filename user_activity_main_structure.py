import json
import argparse
import requests



parser = argparse.ArgumentParser()

parser.add_argument("username", type=str)

args = parser.parse_args()

def get_user_data(username):
    url = f"https://api.github.com/users/{username}/events"
    