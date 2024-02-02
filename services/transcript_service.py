# In services/transcript_service.py

from database.models.video_transcript import VideoTranscript
from database.connection import db
from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptService:
    def __init__(self, api=YouTubeTranscriptApi):
        self.api = api

    def get_or_fetch_transcript(self, video_id):
        # Check if transcript exists in DB first
        transcript = VideoTranscript.query.filter_by(video_id=video_id).order_by(VideoTranscript.retrieved_at.desc()).first()
        if transcript:
            return transcript.full_transcript
        else:
            # Fetch and store if not found
            return self.fetch_and_store_transcript(video_id)

    def fetch_and_store_transcript(self, video_id):
        try:
            transcript_data = self.api.get_transcript(video_id, languages=['en'])
            if transcript_data:
                full_transcript = ' '.join([item['text'] for item in transcript_data])
                new_transcript = VideoTranscript(
                    video_id=video_id,
                    full_transcript=full_transcript,
                    is_generated=False
                )
                db.session.add(new_transcript)
                db.session.commit()
                return full_transcript
        except Exception as e:
            print(f"Error fetching or storing transcript for video {video_id}: {e}")
            return None
