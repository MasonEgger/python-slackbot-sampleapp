import os
import re
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from randombot import RandomBot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACKBOT_TOKEN"))

def random_action(channel, action=None, **kwargs):
    """Determine which action to perform based on parameter. For roll die if 
    a kwarg of sides is passed in and it's a valid integer roll a dSIDES die
    """
    # Create a new CoinBot
    random_bot = RandomBot(channel)

    if action == "coin":
        message = random_bot.flip_coin()
    elif action == "die":
        sides = kwargs.get("sides", None)
        if sides is None or isinstance(sides, int) is False:
            message = random_bot.roll_die()
        else:
            print(f"We got here. Sides: {sides}")
            message = random_bot.roll_die(sides)
    elif action == "card":
        message = random_bot.random_card()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "flip a coin" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")
        # Execute the random action as a coin flip
        return random_action(channel_id, action="coin")
    elif "roll a die" in text.lower() or "roll a dice" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")
        # Execute the random action as a coin flip
        return random_action(channel_id, action="die")
    elif "pick a card" in text.lower() or "choose a card" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")
        # Execute the random action as a coin flip
        return random_action(channel_id, action="card")
    elif "roll a d" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Strip out the number from the command
        droll = text.split("roll a")[1].strip().split()[0]
        try:
            int(droll[1:])
        except ValueError:
            pass
        else:
            return random_action(channel_id, action="die", sides=int(droll[1:]))

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=8080)