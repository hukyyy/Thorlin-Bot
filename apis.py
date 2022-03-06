#!/usr/bin/python3
from dotenv import load_dotenv
import os
import praw

load_dotenv()

class apis():
    def __init__(self):
        self.reddit = praw.Reddit(
        client_id = os.getenv('REDDIT_CLIENT_ID'),
        client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
        refresh_token = os.getenv('REDDIT_REFRESH_TOKEN'),
        user_agent = os.getenv('REDDIT_USER_AGENT'),
        )
        self.reddit.read_only = True
