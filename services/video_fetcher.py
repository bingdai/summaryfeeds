from database.models.channel import Channel
from database.models.video import Video
from database.connection import db
import datetime

class VideoFetcher:
    def __init__(self, youtube_service):
        self.youtube_service = youtube_service

    def fetch_and_store_new_videos(self):
        # Query all channels (not just featured ones)
        channels = Channel.query.all()
        
        for channel in channels:
            # Convert channel_id to playlist_id
            playlist_id = 'UU' + channel.channel_id[2:]
            videos = self.youtube_service.get_latest_videos(playlist_id)

            # Check if videos are found
            if not videos or 'items' not in videos or not videos['items']:
                print(f"No videos found for playlist {playlist_id}. Skipping.")
                continue

            for video_data in videos['items']:
                # Extract video details
                video_id = video_data['contentDetails']['videoId']
                title = video_data['snippet']['title']
                description = video_data['snippet']['description']
                published_at = datetime.datetime.strptime(
                    video_data['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'
                )

                # Check if video already exists
                existing_video = Video.query.filter_by(video_id=video_id).first()
                if not existing_video:
                    # Create new Video instance
                    new_video = Video(
                        video_id=video_id,
                        title=title,
                        description=description,
                        published_at=published_at
                    ) # type: ignore
                    db.session.add(new_video)

        db.session.commit()

