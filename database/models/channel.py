from database.connection import db

class Channel(db.Model):
    __tablename__ = 'channels'

    channel_id = db.Column(db.String(255), primary_key=True)
    channel_title = db.Column(db.String(255), nullable=False)
    featured = db.Column(db.Boolean, default=False)
    channel_logo_url = db.Column(db.String(500)) # URL to the channel's logo

    def __repr__(self):
        return f'<Channel {self.channel_title}>'
