from database.models.video_transcript import VideoTranscript
from database.connection import db
from services.transcript_service import TranscriptService

class TranscriptFetcherAndStorer:
    def __init__(self, transcript_service):
        self.transcript_service = transcript_service

    def fetch_and_store_transcript(self, video_id):
        transcript_data = self.transcript_service.get_transcript(video_id)

        if transcript_data:
            full_transcript = ' '.join([item['text'] for item in transcript_data])
            new_transcript = VideoTranscript(
                video_id=video_id,
                full_transcript=full_transcript,
                is_generated=False  # Assuming it's not auto-generated for simplicity
            )
            db.session.add(new_transcript)
            db.session.commit()
            print(f"Transcript stored for video ID {video_id}")
        else:
            print(f"Failed to fetch transcript for video ID {video_id}")


# Usage elsewhere in your application
# from services.transcript_store_service import TranscriptStoreService
# transcript_store_service = TranscriptStoreService(TranscriptService())
# transcript_store_service.fetch_and_store_transcript("video_id_here")

# if __name__ == "__main__":
#     transcript_fetcher_and_storer = TranscriptFetcherAndStorer(TranscriptService())

#     transcript_fetcher_and_storer.fetch_and_store_transcript(video_id='j48Z7dqBcWM')