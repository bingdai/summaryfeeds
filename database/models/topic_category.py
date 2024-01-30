# In file database/models/topic_category.py

from database.connection import db

class TopicCategory(db.Model):
    __tablename__ = 'topic_categories'

    topic_id = db.Column(db.Integer, primary_key=True)
    topic_category_url = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<TopicCategory {self.topic_category_url}>'
