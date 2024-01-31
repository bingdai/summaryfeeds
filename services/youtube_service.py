import requests
from youtube_transcript_api import YouTubeTranscriptApi


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
    
    # get_video_transcripts() method
    def get_video_transcripts(self, video_id):
        try:
            return YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            return None
    
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


    def get_channel_info(self, channel_id):
        # implement the API call to get channel info
        pass