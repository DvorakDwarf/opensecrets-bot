import os
from dotenv import load_dotenv
import wrapper
import random
from pprint import pprint

load_dotenv()
API_KEY = os.environ.get("API_KEY")

STATE_CODES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
               "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
               "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
               "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
               "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
MEASURING_UNITS = {"rtx": 1600, }
TWITTER_CHARACTER_LIMIT = 280

def getRandomLegislator():
    state_code = random.choice(STATE_CODES)
    legislators = wrapper.getLegislators(API_KEY, id=state_code)
    picked_legislator = random.choice(legislators)["@attributes"]
    pprint(picked_legislator)

    return picked_legislator

def writeMessage(legislator, report):
    message = (f"According to {legislator['origin']}, legislator {legislator['firstlast']}" 
                "has received a total campaign contribution of {report['total']}$ from"
                "lobbyists. It is equivalent to:\n"
    )
    


legislator = getRandomLegislator()
report = wrapper.candIndByInd(
            API_KEY, 
            legislator["cid"], 
            industry="K02"
        )["@attributes"]

pprint(report)

pprint(wrapper.candIndByInd(API_KEY, cid="N00007360", industry="K02"))
