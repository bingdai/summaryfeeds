from database.connection import db
from database.models.channel import Channel

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(255), unique=True, nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    channel_id = db.Column(db.String(255), db.ForeignKey('channels.channel_id'))
    default_language = db.Column(db.String(50))
    default_audio_language = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    caption = db.Column(db.Boolean)
    privacy_status = db.Column(db.String(50))
    made_for_kids = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Video {self.title}>'
