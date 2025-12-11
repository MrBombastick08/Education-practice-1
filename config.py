import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:p4v17102006@localhost:5432/furniture_company'
    SQLALCHEMY_TRACK_MODIFICATIONS = False