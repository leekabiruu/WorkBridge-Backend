from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # job_seeker, employer, admin
    is_active = db.Column(db.Boolean, default=True)

    job_seeker_profile = db.relationship('JobSeekerProfile', backref='user', uselist=False)
    employer_profile = db.relationship('EmployerProfile', backref='user', uselist=False)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
