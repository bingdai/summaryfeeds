from flask import Flask, render_template, request, redirect, url_for, session
from services.youtube_service import YouTubeService
from database.connection import init_db
from database.models.channel import Channel
from datetime import datetime
import pytz
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize the Flask application
application = Flask(__name__)

# Set the secret key for the application
application.secret_key = os.getenv('SECRET_KEY')

# Initialize the YouTube service
api_key = os.getenv('YT_API_KEY')
if not api_key:
    raise RuntimeError("YT_API_KEY not set")
youtube_service = YouTubeService(api_key=api_key)

# Initialize the database
db = init_db(application)

def convert_to_pacific_time(time_str):
    #Convert UTC time string to Pacific Timezone and return date part
    utc_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
    pacific_timezone = pytz.timezone('America/Los_Angeles')
    pacific_time = utc_time.astimezone(pacific_timezone)
    return pacific_time.strftime('%Y-%m-%d')

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
    # Add authentication here
    return render_template('admin.html')

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
