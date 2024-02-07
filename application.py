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
from sqlalchemy.sql import exists
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
    # Extend the query to also select channel information and order videos correctly
    video_summary_query = db.session.query(
        Video.video_id,  # Selecting video ID
        Video.title,  # Selecting video title
        func.to_char(Video.published_at, 'YYYY-MM-DD').label('published_at_str'),  # Converting the publication date to string format for display
        Video.published_at,  # Also selecting the publication date as a datetime object for accurate sorting
        VideoSummary.summary,  # Selecting the summary of the video
        Channel.channel_title,  # Selecting the title of the channel
        Channel.channel_logo_url,  # Selecting the URL for the channel's logo
        func.rank().over(
            partition_by=Video.video_id,
            order_by=VideoSummary.retrieved_at.desc()
        ).label('rank')  # Ranking summaries by retrieval date, descending, to identify the latest summary per video
    ).join(Channel, Video.channel_id == Channel.channel_id) \
    .join(VideoSummary, Video.video_id == VideoSummary.video_id) \
    .filter(Channel.featured == True) \
    .subquery()  # Making this a subquery to use its results in the outer query

    # Fetch the latest summaries using the ranked subquery
    latest_summaries = db.session.query(
        video_summary_query.c.video_id,
        video_summary_query.c.title,
        video_summary_query.c.published_at_str,
        video_summary_query.c.summary,
        video_summary_query.c.channel_title,
        video_summary_query.c.channel_logo_url
    ).filter(video_summary_query.c.rank == 1) \
    .order_by(video_summary_query.c.published_at.desc()) \
    .all()  # Ordering by the actual publication date (datetime) ensures correct chronological order. Fetching all matching records.

    # Adjust the structure to include channel info in the response
    daily_videos = defaultdict(list)
    for video_id, title, published_at_str, summary, channel_title, channel_logo_url in latest_summaries:
        daily_videos[published_at_str].append({
            'video_id': video_id,
            'title': title,
            'published_at': published_at_str,  # Using string-formatted date for display
            'summary': summary,
            'channel_title': channel_title,
            'channel_logo_url': channel_logo_url  # Including channel information for display
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
        videos = (Video.query
                  .filter_by(channel_id=channel.channel_id)
                  .order_by(Video.published_at.desc())
                  .all())

        for video in videos:
            summary_exists = (db.session.query(exists()
                              .where(VideoSummary.video_id == video.video_id))
                              .scalar())
            featured_videos.setdefault(channel.channel_title, []).append({
                'id': video.video_id, 
                'title': video.title,
                'published_at': video.published_at,
                'summary_exists': summary_exists
            })
    
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

@application.route('/admin/fetch_transcript/<video_id>', methods=['POST'])
def fetch_transcript(video_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    #video_id = request.form.get('video_id')

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
