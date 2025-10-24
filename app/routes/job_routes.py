from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.job import Job

job_bp = Blueprint("job_bp", __name__)

@job_bp.route("/", methods=["GET"])
def list_all_jobs():
    jobs = Job.query.all()
    return jsonify([{
        "id": j.id, "title": j.title, "location": j.location,
        "job_type": j.job_type, "salary_range": j.salary_range
    } for j in jobs])
