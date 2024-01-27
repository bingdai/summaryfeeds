from flask import Flask, render_template
from services.youtube_service import YouTubeService
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('YT_API_KEY')

app = Flask(__name__)
youtube_service = YouTubeService(api_key=api_key)

@app.route('/')
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
    app.run(debug=True)
