#The other api wrapper was wrtten like 11 years ago + plus I want my own
#And I want it more functional
import requests
import urllib

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
def getLegislators(id: str):
    result = api_call("getLegislators", {"id": id})

    return result

# cid: 	(required) CRP CandidateID
# year: 	2013, 2014, 2015 and 2016 data provided where available
def memPFDprofile(cid: str, year=None):
    result = api_call("memPFDprofile", {"cid": cid, "year": year})

    return result

# cid: 	(required) CRP CandidateID
# cycle: 	2012, 2014, 2016, 2018, 2020, 2022; leave blank for latest cycle
def candSummary(cid: str, cycle=None):
    result = api_call("candSummary", {"cid": cid, "cycle": cycle})

    return result

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
def candContrib(cid: str, cycle=None):
    result = api_call("candContrib", {"cid": cid, "cycle": cycle})

    return result

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
def candIndustry(cid: str, cycle=None):
    result = api_call("candIndustry", {"cid": cid, "cycle": cycle})

    return result

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
# ind: 	(required) a 3-character industry code
def candIndByInd(cid: str, industry: str, cycle=None):
    result = api_call("candIndByInd", {
        "cid": cid, 
        "ind": industry, 
        "cycle": cycle
    })

    return result

# cid: 	(required) CRP CandidateID
# cycle: 	(optional) 2012, 2014, 2016, 2018, 2020, 2022 
# (blank or out of range cycle will return most recent cycle)
def candSector(cid: str, cycle=None):
    result = api_call("candSector", {"cid": cid, "cycle": cycle})

    return result

# cmte: 	(required) Committee ID in CQ format
# congno: 	112 (uses 2012 data), 113 (uses 2014 data), 
# 114 (uses 2016 data), 115 (uses 2018 data), 116 (uses 2020 data); 
# leave blank for latest congress
# indus: 	(required) Industry code
def congCommiteeIndustry(committee: str, industry: str, congnum=None):
    result = api_call("congCmteIndus", {
        "cmte": committee,
        "congno": congnum,
        "indus": industry
    })

    return result

# org: 	(required) name or partial name of organization requested
def getOrgs(org: str):
    result = api_call("getOrgs", {"org": org})

    return result

# id: 	(required) CRP orgid (available via getOrgID method)
def orgSummary(id: str):
    result = api_call("orgSummary", {"id": id})

    return result

#No parameters
def independentExpend():
    result = api_call("independentExpend", {})

    return result


