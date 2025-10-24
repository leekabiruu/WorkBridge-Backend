from app.extensions import db

class JobSeekerProfile(db.Model):
    __tablename__ = "job_seeker_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    skills = db.Column(db.String(255))
    experience = db.Column(db.Text)
    resume_url = db.Column(db.String(255))

    applications = db.relationship("Application", backref="job_seeker", lazy=True)
    favorites = db.relationship("FavoriteJob", backref="job_seeker", lazy=True)
