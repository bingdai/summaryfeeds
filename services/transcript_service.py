# In services/transcript_service.py

from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptService:
    def __init__(self, api=YouTubeTranscriptApi):
        self.api = api

    def get_transcript(self, video_id):
        try:
            return self.api.get_transcript(video_id, languages=['en'])
        except Exception as e:
            print(f"Error fetching transcript for video {video_id}: {e}")
            return None

# Usage in other parts of the application
# from services.transcript_service import TranscriptService
# transcript_service = TranscriptService()
# transcript = transcript_service.get_transcript("video_id_here")
