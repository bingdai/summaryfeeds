# In file database/models/video_primary_category_mapping.py

from database.connection import db

class VideoPrimaryCategoryMapping(db.Model):
    __tablename__ = 'video_primary_category_mapping'

    video_id = db.Column(db.String(255), db.ForeignKey('videos.video_id'), primary_key=True)
    category_id = db.Column(db.String(50), db.ForeignKey('primary_categories.category_id'), primary_key=True)

    def __repr__(self):
        return f'<VideoPrimaryCategoryMapping video_id={self.video_id} category_id={self.category_id}>'
