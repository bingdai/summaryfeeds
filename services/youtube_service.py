import requests
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
load_dotenv()

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key=None):
        if not api_key:
            raise ValueError("API key must be provided")
        self.api_key = api_key

    # get_latest_videos() method
    def get_latest_videos(self, playlist_id, limit=3):
        url = f"{self.BASE_URL}/playlistItems"
        params = {
            'part': 'snippet,contentDetails',
            'maxResults': limit,
            'playlistId': playlist_id,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching videos for playlist {playlist_id}: {response.json()}")
            return None
        return response.json()
    
    # get_video_info() method
    def get_video_info(self, video_id):
        url = f"{self.BASE_URL}/videos"
        params = {
            'part': 'snippet,contentDetails,status',
            'id': video_id,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching video info for video ID {video_id}: {response.json()}")
            return None
        video_info = response.json().get('items', [])
        if not video_info:
            print(f"No video info found for video ID {video_id}")
            return None
        # Assuming single video ID, so we take the first item.
        return video_info[0]
    
    # get_video_transcripts() method
    def get_video_transcripts(self, video_id):
        try:
            return YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            return None

if __name__ == "__main__":

    # Load environment variables from .env file
    api_key = os.getenv('YT_API_KEY')  # Replace with your actual API key
    youtube_service = YouTubeService(api_key=api_key)

    # Test get_video_info() method
    video_info = youtube_service.get_video_info(video_id='j48Z7dqBcWM')  # Replace VIDEO_ID with an actual video ID
    print(video_info)