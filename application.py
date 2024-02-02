from flask import Flask, flash, render_template, request, redirect, url_for, session
from services.youtube_service import YouTubeService
from services.transcript_service import TranscriptService
from database.models.video_summary import VideoSummary
from services.summary_generator import SummaryGenerator
from config import Config
from database.connection import init_db, db
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
                video_id = video['contentDetails']['videoId']
                # Fetch the latest summary for each video if it exists
                summary = VideoSummary.query.filter_by(video_id=video_id).order_by(VideoSummary.retrieved_at.desc()).first()
                if summary:
                    video['summaries'] = [summary]
                else:
                    video['summaries'] = []
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

@application.route('/admin/fetch_transcript', methods=['POST'])
def fetch_transcript():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    video_id = request.form.get('video_id')

    if video_id:
        transcript_service = TranscriptService()
        transcript_text = transcript_service.get_or_fetch_transcript(video_id)

        if transcript_text:
            flash('Transcript fetched and stored successfully.', 'success')
        else:
            flash('Failed to fetch transcript.', 'error')
    else:
        flash('Video ID missing.', 'error')

    return redirect(url_for('admin'))

@application.route('/admin/generate_summary/<video_id>', methods=['POST'])
def generate_summary(video_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    transcript_service = TranscriptService()

    # Attempt to retrieve the transcript from the database first
    transcript_text = transcript_service.get_or_fetch_transcript(video_id)

    #print(f"Transcript for video {video_id}: {transcript_text}")

    # Check if transcript was successfully retrieved or stored
    if not transcript_text:
        flash('Unable to retrieve or generate transcript for video.', 'error')
        return redirect(url_for('admin'))

    # Generate summary if transcript is available
    prompt = "Summarize the following transcript into a concise paragraph."
    summary_generator = SummaryGenerator(api_key=Config.OPENAI_API_KEY)
    summary_text = summary_generator.generate_summary(video_id, transcript_text)

    if summary_text:
        new_summary = VideoSummary(
            video_id=video_id,
            summary=summary_text,
            prompt=prompt,
            retrieved_at=datetime.utcnow(),
            status='completed'
        )
        db.session.add(new_summary)
        db.session.commit()
        flash('Summary generated and stored successfully.', 'success')
    else:
        flash('Failed to generate summary. Please try again later.', 'error')

    return redirect(url_for('admin'))


if __name__ == '__main__':
    application.run(debug=True)
