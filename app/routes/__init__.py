# app/routes/__init__.py
from .auth_routes import auth_bp
from .job_routes import job_bp
from .employer_routes import employer_bp
from .jobseeker_routes import jobseeker_bp
from .application_routes import application_bp
from .favorite_routes import favorite_bp
from .message_routes import message_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(job_bp, url_prefix="/api/jobs")
    app.register_blueprint(employer_bp, url_prefix="/api/employers")
    app.register_blueprint(jobseeker_bp, url_prefix="/api/jobseekers")
    app.register_blueprint(application_bp, url_prefix="/api/applications")
    app.register_blueprint(favorite_bp, url_prefix="/api/favorites")
    app.register_blueprint(message_bp, url_prefix="/api/messages")
