from app.extensions import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey("jobseekers.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    job = db.relationship("Job", backref="favorites", lazy=True)
    jobseeker = db.relationship("JobSeeker", backref="favorites", lazy=True)
