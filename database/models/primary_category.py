# In file database/models/primary_category.py

from database.connection import db

class PrimaryCategory(db.Model):
    __tablename__ = 'primary_categories'

    category_id = db.Column(db.String(50), primary_key=True)
    category_name = db.Column(db.String(255))

    def __repr__(self):
        return f'<PrimaryCategory {self.category_name}>'
