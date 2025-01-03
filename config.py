import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'  # You can change this to use PostgreSQL or MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Set the JWT secret key
