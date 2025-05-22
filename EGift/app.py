from flask import Flask
from config import Config
from app.models import get_db_connection
from app.auth import auth
from app.routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    @app.before_first_request
    def initialize_db():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY IDENTITY,
                username NVARCHAR(64),
                email NVARCHAR(120) UNIQUE,
                password_hash NVARCHAR(128),
                mfa_secret NVARCHAR(32),
                mfa_enabled BIT
            )
        ''')
        conn.commit()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(ssl_context='adhoc') 