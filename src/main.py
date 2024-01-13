import os
from dotenv import load_dotenv
import wrapper

load_dotenv()
API_KEY = os.environ.get("API_KEY")

def pretty_print(response: object):
    pass

response = wrapper.api_call(API_KEY, "getLegislators", {"id": "NJ04"})

print(response.keys())
print(response['re'])
