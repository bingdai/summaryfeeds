# In file database/models/video_tag_mapping.py

from database.connection import db

class VideoTagMapping(db.Model):
    __tablename__ = 'video_tag_mapping'

    video_id = db.Column(db.String(255), db.ForeignKey('videos.video_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)

    def __repr__(self):
        return f'<VideoTagMapping video_id={self.video_id} tag_id={self.tag_id}>'
