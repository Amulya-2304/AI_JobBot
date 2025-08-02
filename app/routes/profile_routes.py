from flask import Blueprint, render_template, session, redirect, url_for, flash, request, send_from_directory
from app.models.user import User
from app import db
import os
from werkzeug.utils import secure_filename
from app.models.applied_jobs import AppliedJobs

profile = Blueprint('profile', __name__)

UPLOAD_FOLDER = 'app/static/uploads'

@profile.route('/profile', methods=['GET'])
def profile_page():
    if 'user_id' not in session:
        flash("Please log in to access your profile.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    applied_jobs = AppliedJobs.query.filter_by(user_id=user.id).all()

    return render_template("profile.html", user=user, applied_jobs=applied_jobs)

@profile.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash("Please log in to edit your profile.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('new_password')

        # Update username and email
        if username:
            user.username = username
        if email:
            user.email = email

        # Update password if provided
        if new_password and new_password.strip() != "":
            from werkzeug.security import generate_password_hash
            user.password = generate_password_hash(new_password)

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile.profile_page'))

    return render_template("edit_profile.html", user=user)

@profile.route('/upload-new-cv', methods=['POST'])
def upload_new_cv():
    """Upload a new CV (replaces old one if exists)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    file = request.files.get('cv_file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Remove old CV if it exists
        if user.cv_filename:
            old_path = os.path.join(UPLOAD_FOLDER, user.cv_filename)
            if os.path.exists(old_path):
                os.remove(old_path)

        user.cv_filename = filename
        db.session.commit()
        flash("New CV uploaded successfully.", "success")

    return redirect(url_for('profile.profile_page'))


@profile.route('/delete-cv', methods=['POST'])
def delete_cv():
    """Delete user's uploaded CV"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if user and user.cv_filename:
        cv_path = os.path.join(UPLOAD_FOLDER, user.cv_filename)
        if os.path.exists(cv_path):
            os.remove(cv_path)
        user.cv_filename = None
        db.session.commit()
        flash("CV deleted successfully.", "info")

    return redirect(url_for('profile.profile_page'))


@profile.route('/uploads/<filename>')
def view_cv(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)