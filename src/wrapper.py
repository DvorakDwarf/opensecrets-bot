#The other api wrapper was wrtten like 11 years ago + plus I want my own
#And I want it more functional
import requests
import urllib
import json
from pprint import pprint

def api_call(key: str, method_name: str, params: dict) -> dict:
    url = (
        f"https://www.opensecrets.org/api/?method={method_name}&output=json" +
        f"&apikey={key}&{urllib.parse.urlencode(params)}"
    )

    headers = {"User-Agent": "Mozilla/5.0"}

    print(url)

    response = requests.get(url=url, headers=headers).json()
    return response

#id: two character state code or specific CID
def getLegislators(key: str, id: str) -> dict:
    result=api_call(key, "getLegislators", {"id": id})

    return result["response"]["legislator"]

# cid: 	(required) CRP CandidateID
# year: 	2013, 2014, 2015 and 2016 data provided where available
def memPFDprofile(key: str, cid: str, year="") -> dict:
    result = api_call(key, "memPFDprofile", {"cid": cid, "year": year})

    return result["response"]["member_profile"]

# cid: 	(required) CRP CandidateID
# cycle: 	2012, 2014, 2016, 2018, 2020, 2022; leave blank for latest cycle
def candSummary(key: str, cid: str, cycle="") -> dict:
    result = api_call(key, "candSummary", {"cid": cid, "cycle": cycle})

    return result["response"]["summary"]

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
def candContrib(key: str, cid: str, cycle="") -> dict:
    result = api_call(key, "candContrib", {"cid": cid, "cycle": cycle})

    return result["response"]["contributors"]

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
def candIndustry(key: str, cid: str, cycle="") -> dict:
    result = api_call(key, "candIndustry", {"cid": cid, "cycle": cycle})

    return result["response"]["industries"]

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
# ind: 	(required) a 3-character industry code
def candIndByInd(key: str, cid: str, industry: str, cycle="") -> dict:
    result = api_call(key, "candIndByInd", {
        "cid": cid, 
        "ind": industry, 
        "cycle": cycle
    })

    return result["response"]["candIndus"]

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
def candSector(key: str, cid: str, cycle="") -> dict:
    result = api_call(key, "candSector", {"cid": cid, "cycle": cycle})

    return result["response"]["sectors"]

# cmte: 	(required) Committee ID in CQ format
# congno: 	112 (uses 2012 data), 113 (uses 2014 data), 
# 114 (uses 2016 data), 115 (uses 2018 data), 116 (uses 2020 data); 
# leave blank for latest congress
# indus: 	(required) Industry code
def congCommiteeIndustry(key: str, 
                         committee: str, 
                         industry: str, 
                         congnum="") -> dict:
    result = api_call(key, "congCmteIndus", {
        "cmte": committee,
        "congno": congnum,
        "indus": industry
    })

    return result["response"]["committee"]

# org: 	(required) name or partial name of organization requested
def getOrgs(key: str, org: str) -> dict:
    result = api_call(key, "getOrgs", {"org": org})

    return result["response"]["organization"]

# id: 	(required) CRP orgid (available via getOrgID method)
def orgSummary(key: str, id: str) -> dict:
    result = api_call(key, "orgSummary", {"id": id})

    return result["response"]["organization"]

#No parameters
def independentExpend(key: str) -> dict:
    result = api_call(key, "independentExpend", {})

    return result["response"]["indexp"]

# Probably pretty wasteful of API
# def test_functions(key: str):
    # pprint(getLegislators(key, id="NJ04"))
    # pprint(memPFDprofile(key, cid="N00007360"))
    # pprint(candSummary(key, cid="N00007360"))
    # pprint(candContrib(key, cid="N00007360"))
    # pprint(candIndustry(key, cid="N00007360"))
    # pprint(candIndByInd(key, cid="N00007360", industry="K02"))
    # pprint(candSector(key, cid="N00007360"))
    # pprint(congCommiteeIndustry(key, industry="F10", committee="HARM"))
    # pprint(getOrgs(key, org="Goldman"))
    # pprint(orgSummary(key, id="D000000125"))
    # pprint(independentExpend(key))
