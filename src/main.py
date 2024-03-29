#For some reason I get different numbers when looking at lobbying amounts
#The website top receipients list gives about double the amount per candidate

#TODO
#Make it save which candidates were already talked about and then retry XXX
#Refer to senators as senators, etc XXX
#Make sure tweet is under 280 XXX
#   Reduce size of message + equivalents XXX
#   Check if len > 280 then retry if it still is after shortening XXX
#Automatic tweeting every x hour each day XXX
#README
#Use tolerance_limit XXX
#Figure out where to host XXX
#Annonce ?
#Entertainment purposes pinned tweet XXX
#pretty numbers with commas XXX

import os
import time
import json
import random
import tweepy
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv

import wrapper

#Why twitter gotta have like 5 secrets to post a tweet, smh
load_dotenv()
API_KEY = os.environ.get("API_KEY")
TWITTER_KEY = os.environ.get("TWITTER_KEY")
TWITTER_SECRET_KEY = os.environ.get("TWITTER_SECRET_KEY")
TWITTER_TOKEN = os.environ.get("TWITTER_TOKEN")
TWITTER_SECRET_TOKEN = os.environ.get("TWITTER_SECRET_TOKEN")
# BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

TWITTER_CHARACTER_LIMIT = 280
POST_HOUR = 7
TOLERANCE_LIMIT = 1 #Anything lower than this isn't fun to display
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
                   "burgers": 2.55,
                   "warhammer minis": 9.29,
                   "yachts": 200000,
                   "grams of gold": 65,
                   "PS5s": 500,
                   "russian monthly salaries": 1130,
                   "ambulance rides": 1277,
                   "monopoly money": 0.000857993496409,
                   "Clash Royale gems": 0.808080808081,
                   "dogecoin": 0.083,
                   "gallons of gas": 3.68,
                   "pepsi logos": 1000000,
                   "sacs of potatoes": 68.84,
                   "months of Hustler's University": 49,
                   "months of LA rent": 3258,
                   }

def getRandomLegislator(blacklist=None) -> (object, object):
    state_code = random.choice(STATE_CODES)
    legislators = wrapper.getLegislators(API_KEY, id=state_code)
    picked_legislator = random.choice(legislators)["@attributes"]

    try:            
        report = wrapper.candIndByInd(
            API_KEY, 
            picked_legislator["cid"], 
            industry="K02")["@attributes"]
    except:
        print("LOBBYING REQUEST NOT FOUND, RETRYING")
        return getRandomLegislator()
    
    #Check if candidate already picked before
    if (blacklist != None) and (picked_legislator["cid"] in blacklist):
        print("CANDIDATE IN BLACKLIST, RETRYING")
        return getRandomLegislator()

    if int(report["total"]) < TOLERANCE_LIMIT:
        print(f"{report['total']}$ IS TOO LOW, RETRYING")
        picked_legislator, report = getRandomLegislator()

    return (picked_legislator, report)

def getRandomEquivalent(n: int) -> list:
    equivalents = random.sample(list(MEASURING_UNITS.items()), n)

    return equivalents

def writeMessage(legislator, report) -> str:
    title = ""
    match report["chamber"]:
        case "H": title = "representative "
        case "S": title = "senator "

    message = (
        f"According to {report['origin']}, {title}{legislator['firstlast']} " 
        f"received {int(report['total']):,}$ for their campaign from "
        f"lobbyists in the {report['cycle']} cycle equivalent to:\n"
    )

    equivalents = getRandomEquivalent(5)    
    for item in equivalents:
        message += f"• {float(report['total']) / item[1]:,.2f} {item[0]}\n"

    if len(message) > TWITTER_CHARACTER_LIMIT:
        print("TOO LONG, RETRYING")
        message = writeMessage(legislator, report)

    return message

def tweet(client, blacklist):
    legislator, report = getRandomLegislator(blacklist)
    message = writeMessage(legislator, report)

    pprint(legislator)
    pprint(report)
    pprint(message)

    client.create_tweet(text=message)

    #Save blacklist
    blacklist.append(legislator["cid"])
    with open("blacklist.json", "w") as file:
        json.dump({"list": blacklist}, file, indent=4)

try:
    with open("blacklist.json", "r") as file:
        blacklist = json.load(file)["list"]
        print(type(blacklist))
        print(blacklist)
except IOError:
    with open("blacklist.json", "w") as file:
        json.dump({"list": []}, file)
        blacklist = []

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET_KEY)
auth.set_access_token(TWITTER_TOKEN, TWITTER_SECRET_TOKEN)

client = tweepy.Client(
    consumer_key= TWITTER_KEY,
    consumer_secret= TWITTER_SECRET_KEY,
    access_token= TWITTER_TOKEN,
    access_token_secret= TWITTER_SECRET_TOKEN
)

print(client.get_me())

already_posted = False
while True:
    print(already_posted)

    now = datetime.now()
    current_hour = now.strftime("%H") 
    print("Current hour =", current_hour)

    if int(current_hour) == POST_HOUR:
        if already_posted == False:
            tweet(client, blacklist)
            already_posted = True
    else:
        already_posted = False

    time.sleep(300)


