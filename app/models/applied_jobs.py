from app.db import db
from datetime import datetime

class AppliedJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    apply_link = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='Applied')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)