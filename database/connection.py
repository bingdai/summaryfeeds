import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


# Initialize SQLAlchemy with no parameters
db = SQLAlchemy()

def init_db(app):
    # Fetching database credentials from environment variables or .env file
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    # Constructing the database URL
    DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    print(f'Database URL: {DATABASE_URL}')

    # Setting configurations for the Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initializing the app with the SQLAlchemy instance
    db.init_app(app)

    # Optional: Test database connection and print tables
    with app.app_context():
        try:
            result = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print('Database connection successful!')
            print('Tables in the database:', tables)
        except Exception as e:
            print(f'Error connecting to the database: {e}')

    return db