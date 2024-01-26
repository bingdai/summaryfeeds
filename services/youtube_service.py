import requests

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_video_info(self, video_id):
        # implement the API call to get video info
        pass

    def get_channel_info(self, channel_id):
        # implement the API call to get channel info
        pass

    def get_latest_videos(self, channel_id, limit=3):
        # implement the API call to get the latest videos
        pass