from email.mime import application
from flask import Flask, render_template
from services.youtube_service import YouTubeService
import os

# DEV: Load environment variables from .env file
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv('YT_API_KEY')


# PROD: Get the YouTube API key from the environment properties
api_key = os.getenv('YT_API_KEY')

if not api_key:
    raise RuntimeError("YT_API_KEY not set")

application = Flask(__name__)
youtube_service = YouTubeService(api_key=api_key)

@application.route('/')
def index():
    playlist_ids = [
        'UUGaVdbSav8xWuFWTadK6loA', 
        'UUcefcZRL2oaA_uBNeo5UOWg'
        ]  # Add your playlist IDs here
    videos = {}
    for playlist_id in playlist_ids:
        videos[playlist_id] = youtube_service.get_latest_videos(playlist_id)
    return render_template('index.html', videos=videos)

if __name__ == '__main__':
    application.run(debug=True)
