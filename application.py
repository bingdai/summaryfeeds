from email.mime import application
from flask import Flask, render_template
from services.youtube_service import YouTubeService
from database.connection import init_db
from database.models.channel import Channel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
application = Flask(__name__)

# Initialize the YouTube service
api_key = os.getenv('YT_API_KEY')

if not api_key:
    raise RuntimeError("YT_API_KEY not set")
youtube_service = YouTubeService(api_key=api_key)

# Initialize the database
db = init_db(application)

@application.route('/')
def index():
    # Query featured channels
    featured_channels = Channel.query.filter_by(featured=True).all()
    playlists = {}
    
    for channel in featured_channels:
        playlist_id = 'UU' + channel.channel_id[2:]  # Convert channel_id to playlist_id
        videos = youtube_service.get_latest_videos(playlist_id)
        if videos['items']:
            channel_url = f"https://www.youtube.com/channel/{channel.channel_id}"
            playlists[channel.channel_title] = {'videos': videos, 'url': channel_url}

    return render_template('index.html', playlists=playlists)

if __name__ == '__main__':
    application.run(debug=True)
