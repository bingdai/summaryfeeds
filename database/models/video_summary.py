from database.connection import db
from database.models.video import Video
from datetime import datetime

class VideoSummary(db.Model):
    """
    SQLAlchemy model for storing summaries of YouTube videos.
    """

    __tablename__ = 'video_summaries'

    # Primary key for the table
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key reference to the video table
    video_id = db.Column(db.String(255), db.ForeignKey('videos.video_id'), nullable=False)

    # Summary text generated for the video
    summary = db.Column(db.Text, nullable=False)

    # Prompt used for generating the summary (e.g., through an AI model)
    prompt = db.Column(db.Text, nullable=False)

    # Timestamp indicating when the summary was retrieved
    retrieved_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Status of the summary (e.g., 'pending', 'completed', 'failed')
    status = db.Column(db.String(50), nullable=False, default='pending')

    # Establishing a relationship with the Video model. This allows for easy access to the video
    # associated with each summary. The backref creates a virtual column in the Video model to
    # access related summaries.
    video = db.relationship('Video', backref=db.backref('summaries', lazy=True))

    def __repr__(self):
        """
        String representation of the VideoSummary instance, useful for debugging.
        """
        return f'<VideoSummary {self.id} for Video {self.video_id}>'
