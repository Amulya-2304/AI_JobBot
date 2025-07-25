from app.db import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cv_filename = db.Column(db.String(200), nullable=True)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)