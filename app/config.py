import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or 'mysql+pymysql://todouser:todopass@localhost:3306/tododb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
