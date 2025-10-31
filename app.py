from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, Job, User
from routes import jobs_bp, auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change to a secure key in production

CORS(app)
jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    db.create_all()

    if not User.query.first():
        demo_users = [
            User(username='employer1', role='employer'),
            User(username='seeker1', role='job_seeker')
        ]
        for user in demo_users:
            user.set_password('password123')  # Demo password
        db.session.add_all(demo_users)
        db.session.commit()

    if not Job.query.first():
        demo_jobs = [
            Job(title='Software Engineer', description='Develop software', location='New York', salary=80000, job_type='full-time', employer_id=1),
            Job(title='Data Analyst', description='Analyze data', location='San Francisco', salary=70000, job_type='full-time', employer_id=2),
            Job(title='Designer', description='Create designs', location='Los Angeles', salary=60000, job_type='part-time', employer_id=1)
        ]
        db.session.add_all(demo_jobs)
        db.session.commit()

app.register_blueprint(jobs_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
