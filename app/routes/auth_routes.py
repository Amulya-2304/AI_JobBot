from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app.models.user import User
from app import db, mail
import os
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

auth = Blueprint('auth', __name__)


def send_reset_email(to_email, reset_link):
    """Sends the password reset email"""
    msg = Message("Password Reset - AI JobBot",
                  sender="noreply@AIbot.com",
                  recipients=[to_email])
    msg.body = f"""Hi,

To reset your password, click the link below:

{reset_link}

If you did not request this, please ignore this email.

Best,
AI JobBot Team
"""
    mail.send(msg)


@auth.route('/')
def home():
    """Landing page - Welcome screen"""
    return render_template('home.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for existing users"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard.dashboard_home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        return redirect(url_for('auth.upload_cv'))

    return render_template('register.html')


@auth.route('/upload-cv', methods=['GET', 'POST'])
def upload_cv():
    """CV upload page"""
    if request.method == 'POST':
        file = request.files['cv_file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join('app/static/uploads', filename)
            file.save(filepath)

            user = User.query.get(session['user_id'])
            user.cv_filename = filename
            db.session.commit()

            flash("CV uploaded successfully.", "success")
        return redirect(url_for('auth.login'))

    return render_template('upload_cv.html')


@auth.route('/skip-cv', methods=['POST'])
def skip_cv():
    """Skip CV upload and continue"""
    flash("You skipped CV upload. You can upload it later from profile.", "info")
    return redirect(url_for('auth.login'))


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt='reset-password')
            link = url_for('auth.reset_password', token=token, _external=True)
            send_reset_email(email, link)
            flash("Password reset link sent to your email.", "info")
        else:
            flash("Email not found.", "danger")
    return render_template('forgot_password.html')


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=3600)
    except:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            flash("Password updated. Please log in.", "success")
            return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

@auth.route('/logout')
def logout():
    """Log the user out and redirect to login page."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))