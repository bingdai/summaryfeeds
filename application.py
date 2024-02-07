from flask import Flask, flash, render_template, request, redirect, url_for, session
from sqlalchemy import func
from collections import defaultdict
from services.youtube_service import YouTubeService
from services.transcript_service import TranscriptService
from database.models.video import Video
from database.models.video_summary import VideoSummary
from database.models.channel import Channel
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

# Make GA_TRACKING_ID available in all templates
@application.context_processor
def inject_ga_id():
    return dict(GA_TRACKING_ID=os.getenv('GA_TRACKING_ID'))

@application.route('/')
def index():
    # Extend the query to also select channel information
    video_summary_query = db.session.query(
        Video.video_id,
        Video.title,
        func.to_char(Video.published_at, 'YYYY-MM-DD').label('published_at_str'),
        Video.published_at,
        VideoSummary.summary,
        Channel.channel_title,
        Channel.channel_logo_url,  
        func.rank().over(
            partition_by=Video.video_id,
            order_by=VideoSummary.retrieved_at.desc()
        ).label('rank')
    ).join(Channel, Video.channel_id == Channel.channel_id) \
    .join(VideoSummary, Video.video_id == VideoSummary.video_id) \
    .filter(Channel.featured == True) \
    .subquery()

    # Fetch the latest summaries
    latest_summaries = db.session.query(
        video_summary_query.c.video_id,
        video_summary_query.c.title,
        video_summary_query.c.published_at_str,
        video_summary_query.c.summary,
        video_summary_query.c.channel_title,
        video_summary_query.c.channel_logo_url
    ).filter(video_summary_query.c.rank == 1) \
    .order_by(video_summary_query.c.published_at.desc()) \
    .all()

    # Adjust the structure to include channel info
    daily_videos = defaultdict(list)
    for video_id, title, published_at, summary, channel_title, channel_logo_url in latest_summaries:
        daily_videos[published_at].append({
            'video_id': video_id,
            'title': title,
            'published_at': published_at,
            'summary': summary,
            'channel_title': channel_title,
            'channel_logo_url': channel_logo_url
        })

    return render_template('index.html', daily_videos=daily_videos)

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
