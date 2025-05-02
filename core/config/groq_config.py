from dotenv import load_dotenv
from groq import Groq
import os

# Get saved Key
load_dotenv()

# initiate Groq client
def get_client():
	return Groq(api_key=os.environ.get("GROP_KEY"),)
