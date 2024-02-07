from datetime import datetime
from database.models.video import Video
from database.connection import db
from database.models.channel import Channel

class VideoFetcher:
    def __init__(self, youtube_service):
        self.youtube_service = youtube_service

    def fetch_and_store_new_videos(self):
        channels = Channel.query.all()
        
        for channel in channels:
            print(f"Fetching videos for channel {channel.channel_id}")
            playlist_id = 'UU' + channel.channel_id[2:]
            videos_response = self.youtube_service.get_latest_videos(playlist_id)

            if not videos_response or 'items' not in videos_response or not videos_response['items']:
                print(f"No videos found for playlist {playlist_id}. Skipping.")
                continue

            for video_data in videos_response['items']:
                video_id = video_data['contentDetails']['videoId']
                video_info = self.youtube_service.get_video_info(video_id)

                if not video_info:
                    print(f"No detailed info for video {video_id}")
                    continue

                default_language = video_info['snippet'].get('defaultLanguage')
                default_audio_language = video_info['snippet'].get('defaultAudioLanguage')
                duration = video_info['contentDetails'].get('duration')
                caption = video_info['contentDetails'].get('caption') == 'true'
                privacy_status = video_info['status'].get('privacyStatus')
                made_for_kids = video_info['status'].get('madeForKids', False)

                existing_video = Video.query.filter_by(video_id=video_id).first()
                if not existing_video:
                    new_video = Video(
                        video_id=video_id,
                        title=video_info['snippet']['title'],
                        description=video_info['snippet']['description'],
                        published_at=datetime.strptime(video_info['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                        channel_id=video_info['snippet']['channelId'],
                        default_language=default_language,
                        default_audio_language=default_audio_language,
                        duration=duration,
                        caption=caption,
                        privacy_status=privacy_status,
                        made_for_kids=made_for_kids
                    )
                    db.session.add(new_video)

        db.session.commit()
