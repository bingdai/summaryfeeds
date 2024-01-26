from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('YT_API_KEY')
print(api_key)