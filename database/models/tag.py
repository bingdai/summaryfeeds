# In file database/models/tag.py

from database.connection import db

class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.tag}>'
