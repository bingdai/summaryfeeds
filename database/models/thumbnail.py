# In file database/models/thumbnail.py

from database.connection import db

class Thumbnail(db.Model):
    __tablename__ = 'thumbnails'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(255), db.ForeignKey('videos.video_id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __repr__(self):
        return f'<Thumbnail {self.url}>'
