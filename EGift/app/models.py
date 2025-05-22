import pyodbc
from flask_login import UserMixin
from app import login_manager

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, mfa_secret=None, mfa_enabled=False):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.mfa_secret = mfa_secret
        self.mfa_enabled = mfa_enabled

def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server;'
        'DATABASE=gift_shop;'
        'UID=your_username;'
        'PWD=your_password'
    )