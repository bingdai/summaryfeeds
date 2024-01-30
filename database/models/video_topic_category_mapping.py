# In file database/models/video_topic_category_mapping.py

from database.connection import db

class VideoTopicCategoryMapping(db.Model):
    __tablename__ = 'video_topic_category_mapping'

    video_id = db.Column(db.String(255), db.ForeignKey('videos.video_id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic_categories.topic_id'), primary_key=True)

    def __repr__(self):
        return f'<VideoTopicCategoryMapping {self.video_id}, {self.topic_id}>'
