from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    job_type = db.Column(db.String(50), nullable=False)  # e.g., full-time, part-time
    employer_id = db.Column(db.Integer, nullable=False)  # Assuming employer ID is an integer
