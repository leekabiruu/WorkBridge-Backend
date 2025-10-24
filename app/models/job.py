from app.extensions import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey("employer_profiles.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract
    salary_range = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applications = db.relationship("Application", backref="job", lazy=True)
    favorites = db.relationship("FavoriteJob", backref="job", lazy=True)
