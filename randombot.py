# import the random library to help us generate the random numbers
import random

# Create the RandomBot Class
class RandomBot:

    # Create a constant that contains the default text for the message
    MESSAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ""
        },
    }

    # The constructor for the class. It takes the channel name as the a
    # parameter and then sets it as an instance variable
    def __init__(self, channel):
        self.channel = channel

    # Generate a random number to simulate flipping a coin. Then return the
    # crafted slack payload with the coin flip message.
    def flip_coin(self):
        rand_int =  random.randint(0,1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"

        message = f"The result is {results}"

        self.MESSAGE_BLOCK["text"]["text"] = message
        return {
            "channel": self.channel,
            "blocks": [
                self.MESSAGE_BLOCK
            ],
        }

    # Generate a random number to simulate rolling a die. Accept the number of
    # sides on the die as a paramter, defaulting to a typical 6 sided die.
    # Then return the crafted slack payload with the die roll message.
    def roll_die(self, sides=6):
        rand_int =  random.randint(1, sides)

        message = f"You rolled a {rand_int}"

        self.MESSAGE_BLOCK["text"]["text"] = message
        return {
            "channel": self.channel,
            "blocks": [
                self.MESSAGE_BLOCK
            ],
        }

    # Generate a random number to simulate suit and a random number to simulate
    # card number. 
    # Then return the crafted slack payload with the die roll message.
    def random_card(self):
        suit = ["Hearts", "Spades", "Clubs", "Diamonds"]
        cards = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
                 "Eight", "Nine", "Jack", "Queen", "King"]

        message = f"You picked the {random.choice(cards)} of {random.choice(suit)}"

        self.MESSAGE_BLOCK["text"]["text"] = message
        return {
            "channel": self.channel,
            "blocks": [
                self.MESSAGE_BLOCK
            ],
        }
