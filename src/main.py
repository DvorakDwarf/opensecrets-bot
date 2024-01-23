#For some reason I get different numbers when looking at lobbying amounts
#The website top receipients list gives about double the amount per candidate

import os
from dotenv import load_dotenv
import wrapper
import tweepy
import pandas as pd
import random
from pprint import pprint

load_dotenv()
API_KEY = os.environ.get("API_KEY")
TWITTER_KEY = os.environ.get("TWITTER_KEY")
TWITTER_SECRET_KEY = os.environ.get("TWITTER_SECRET_KEY")
TWITTER_TOKEN = os.environ.get("TWITTER_TOKEN")
TWITTER_SECRET_TOKEN = os.environ.get("TWITTER_SECRET_TOKEN")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

STATE_CODES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
               "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
               "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
               "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
               "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
MEASURING_UNITS = {"GTX 4090": 1599, 
                   "seconds of the US military budget": 25754,
                   "months of food": 415.53,
                   "AAA games": 60,
                   "student debters": 28950,
                   "cheeseburgers": 2.55,
                   "warhammer miniatures": 9.29,
                   "yachts": 200000,
                   "grams of gold": 65,
                   "PS5s": 500,
                   "russian citizen monthly salaries": 1130,
                   "ambulance rides": 1277,
                   "monopoly money": 0.000857993496409,
                   "Clash Royale gems": 0.808080808081,
                   "dogecoin": 0.083,
                   "gallons of gas": 3.68,
                   "pepsi logos": 1000000,
                   "sacs of potatoes": 68.84,
                   "months of Hustler's University": 49,
                   }

TWITTER_CHARACTER_LIMIT = 280
TOLERANCE_LIMIT = 20000 #Anything lower than this isn't fun to display

def getRandomLegislator():
    state_code = random.choice(STATE_CODES)
    legislators = wrapper.getLegislators(API_KEY, id=state_code)
    picked_legislator = random.choice(legislators)["@attributes"]

    return picked_legislator

def getRandomEquivalent(n: int) -> list:
    equivalents = random.sample(list(MEASURING_UNITS.items()), n)

    return equivalents

def writeMessage(legislator, report) -> str:
    message = (f"According to {report['origin']}, legislator {legislator['firstlast']} " 
                f"has received {report['total']}$ for their campaign from "
                f"lobbyists in the {report['cycle']} cycle equivalent to:\n"
    )

    equivalents = getRandomEquivalent(5)    
    for item in equivalents:
        message += f"{round(float(report['total']) / item[1], 2)} {item[0]}\n"

    print(message)
    print(len(message))

    return message


# legislator = getRandomLegislator()
# report = wrapper.candIndByInd(
#             API_KEY, 
#             legislator["cid"], 
#             industry="K02"
#         )["@attributes"]

# # pprint(report)
# # pprint(legislator)

# message = writeMessage(legislator, report)

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET_KEY)
auth.set_access_token(TWITTER_TOKEN, TWITTER_SECRET_TOKEN)

api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


client = tweepy.Client(
    consumer_key= TWITTER_KEY,
    consumer_secret= TWITTER_SECRET_KEY,
    access_token= TWITTER_TOKEN,
    access_token_secret= TWITTER_SECRET_TOKEN)

try:
    client.update_status('Hello, world!')
    print('Tweet successfully sent!')
except Exception as e:
    print('Error:', e)