import requests

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key=None):
        if not api_key:
            raise ValueError("API key must be provided")
        self.api_key = api_key

    def get_video_info(self, video_id):
        # implement the API call to get video info
        pass

    def get_channel_info(self, channel_id):
        # implement the API call to get channel info
        pass

    def get_latest_videos(self, playlist_id, limit=3):
        url = f"{self.BASE_URL}/playlistItems"
        params = {
            'part': 'snippet,contentDetails',
            'maxResults': limit,
            'playlistId': playlist_id,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        return response.json()