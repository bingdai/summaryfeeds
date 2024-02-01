from flask import Flask, render_template, request, redirect, url_for, session
from services.youtube_service import YouTubeService
from services.transcript_service import TranscriptService
from services.transcript_fetcher_and_storer import TranscriptFetcherAndStorer
from config import Config
from database.connection import init_db
from database.models.channel import Channel
from datetime import datetime
import pytz
import os

# Initialize the Flask application
application = Flask(__name__)

# Load environment variables
application.config.from_object(Config)

if not Config.YT_API_KEY:
    raise RuntimeError("YT_API_KEY not set")
youtube_service = YouTubeService(api_key=Config.YT_API_KEY)

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
        if videos is not None and videos['items']:
            channel_url = f"https://www.youtube.com/channel/{channel.channel_id}"
            # Convert each video's publishedAt to Pacific Timezone
            for video in videos['items']:
                pacific = pytz.timezone('US/Pacific')
                published_at = datetime.fromisoformat(video['snippet']['publishedAt'][:-1])
                local_published_at = published_at.astimezone(pacific)
                video['snippet']['formattedPublishedAt'] = local_published_at.strftime('%Y-%m-%d')            
                playlists[channel.channel_title] = {'videos': videos, 'url': channel_url}

    return render_template('index.html', playlists=playlists)

@application.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    # Fetch featured channels and their videos
    featured_channels = Channel.query.filter_by(featured=True).all()
    featured_videos = {}
    for channel in featured_channels:
        playlist_id = 'UU' + channel.channel_id[2:]
        videos_response = youtube_service.get_latest_videos(playlist_id)
        if videos_response and 'items' in videos_response:
            videos = videos_response['items']
            featured_videos[channel.channel_title] = [{'id': video['contentDetails']['videoId'], 'title': video['snippet']['title']} for video in videos]
    
    return render_template('admin.html', featured_videos=featured_videos)    

@application.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('admin_update'))
        else:
            return 'Invalid Credentials'
    return render_template('admin_login.html')

@application.route('/admin/update', methods=['POST'])
def admin_update():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    # Placeholder for update process
    return 'Update process started'




if __name__ == '__main__':
    application.run(debug=True)
