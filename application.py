from email.mime import application
from flask import Flask, render_template
from services.youtube_service import YouTubeService
from database.connection import init_db
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('YT_API_KEY')
if not api_key:
    raise RuntimeError("YT_API_KEY not set")

application = Flask(__name__)
youtube_service = YouTubeService(api_key=api_key)
db = init_db(application)

@application.route('/')
def index():
    playlist_ids = [
        'UUGaVdbSav8xWuFWTadK6loA', 
        'UUcefcZRL2oaA_uBNeo5UOWg',
        'UUNJ1Ymd5yFuUPtn21xtRbbw'
        ]  # Add your playlist IDs here
    playlists = {}
    for playlist_id in playlist_ids:
        videos = youtube_service.get_latest_videos(playlist_id)
        if videos['items']:
            channel_title = videos['items'][0]['snippet']['channelTitle']
            channel_id = videos['items'][0]['snippet']['channelId']
            channel_url = f"https://www.youtube.com/channel/{channel_id}"
            playlists[channel_title] = {'videos': videos, 'url': channel_url}
    return render_template('index.html', playlists=playlists)

if __name__ == '__main__':
    application.run(debug=True)
