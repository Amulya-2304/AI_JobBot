from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session
from dotenv import load_dotenv
import os

from app.db import db

mail = Mail()
load_dotenv()

from flask_login import current_user



def create_app():
    app = Flask(__name__)

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # 🔐 Secret key
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # 📦 Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # 📁 Upload folder
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

    # 📧 Mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

    # 💾 Server-side session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    Session(app)

    # 🔧 Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # 🔗 Register routes
    from app.routes.auth_routes import auth
    from app.routes.dashboard_routes import dashboard
    from app.routes.profile_routes import profile

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(profile)

    return app