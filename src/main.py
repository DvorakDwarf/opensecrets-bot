import os
from dotenv import load_dotenv
from crpapi import CRP

load_dotenv()
API_KEY = os.environ.get("API_KEY")

crp = CRP(API_KEY)
print(crp)
cand = crp.candidates.get('N00007360')

print(cand)

