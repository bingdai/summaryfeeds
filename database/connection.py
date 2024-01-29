import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize SQLAlchemy with no parameters
db = SQLAlchemy()

def init_db(app):
    # Fetching database credentials from environment variables or .env file
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')

    # Constructing the database URL
    DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    # Setting configurations for the Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initializing the app with the SQLAlchemy instance
    db.init_app(app)

    # Optional: Test database connection
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print('Database connection successful!')
        except Exception as e:
            print(f'Error connecting to the database: {e}')

    return db
