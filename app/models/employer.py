from app.extensions import db

class EmployerProfile(db.Model):
    __tablename__ = "employer_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    company_description = db.Column(db.Text)
    website = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))

    jobs = db.relationship("Job", backref="employer", lazy=True)
