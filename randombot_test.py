from slack import WebClient
from randombot import RandomBot
import os

# Create a slack client
slack_web_client = WebClient(token=os.environ.get("SLACKBOT_TOKEN"))

# Get a new CoinBot
coin_bot = RandomBot("#bot-testing")

# Get the onboarding message payload
message = coin_bot.roll_die()


# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)