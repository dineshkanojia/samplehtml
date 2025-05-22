from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, get_db_connection
from .utils.security import hash_password, verify_password
from .utils.mfa import generate_mfa_secret, get_mfa_uri, verify_mfa_code
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", email)
        user_data = cursor.fetchone()
        
        if user_data and verify_password(password, user_data.password_hash):
            user = User(user_data)
            if user.mfa_enabled:
                return redirect(url_for('auth.mfa_verify', user_id=user.id))
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth.route('/mfa-verify/<user_id>', methods=['GET', 'POST'])
def mfa_verify(user_id):
    if request.method == 'POST':
        code = request.form.get('code')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT mfa_secret FROM users WHERE id = ?", user_id)
        secret = cursor.fetchone()[0]
        if verify_mfa_code(secret, code):
            return redirect(url_for('main.index'))
        flash('Invalid MFA code')
    return render_template('mfa_verify.html')