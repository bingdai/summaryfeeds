from database.connection import db
from database.models.video import Video
from datetime import datetime

class VideoSummary(db.Model):
    __tablename__ = 'video_summaries'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(255), db.ForeignKey('videos.video_id'), nullable=False)
    transcript = db.Column(db.Text)
    summary = db.Column(db.Text)
    prompt = db.Column(db.Text)
    retrieved_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')

    # Establish a relationship to the Video model
    video = db.relationship('Video', backref=db.backref('summaries', lazy=True))

    def __repr__(self):
        return f'<VideoSummary {self.id} for Video {self.video_id}>'
