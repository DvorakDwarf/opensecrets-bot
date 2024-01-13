import os
from dotenv import load_dotenv
import wrapper

load_dotenv()
API_KEY = os.environ.get("API_KEY")

wrapper.test_functions(API_KEY)
