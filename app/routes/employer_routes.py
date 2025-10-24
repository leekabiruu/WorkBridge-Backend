from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.employer import EmployerProfile, db
from app.models.job import Job
from app.models.application import Application
from app.utils.decorators import role_required
from app.schemas.employer_schema import EmployerSchema
from app.schemas.job_schema import JobSchema

employer_bp = Blueprint("employer_bp", __name__)
employer_schema = EmployerSchema()
job_schema = JobSchema(many=True)

@employer_bp.route("/me", methods=["GET"])
@jwt_required()
@role_required("employer")
def get_profile():
    user_id = get_jwt_identity()
    profile = EmployerProfile.query.filter_by(user_id=user_id).first()
    return employer_schema.dump(profile)

@employer_bp.route("/me", methods=["PUT"])
@jwt_required()
@role_required("employer")
def update_profile():
    user_id = get_jwt_identity()
    profile = EmployerProfile.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    for key, value in data.items():
        setattr(profile, key, value)
    db.session.commit()
    return employer_schema.dump(profile)

@employer_bp.route("/jobs", methods=["POST"])
@jwt_required()
@role_required("employer")
def create_job():
    user_id = get_jwt_identity()
    profile = EmployerProfile.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    job = Job(employer_id=profile.id, **data)
    db.session.add(job)
    db.session.commit()
    return jsonify({"msg": "Job created", "job_id": job.id}), 201

@employer_bp.route("/jobs/<int:job_id>", methods=["PUT"])
@jwt_required()
@role_required("employer")
def update_job(job_id):
    user_id = get_jwt_identity()
    profile = EmployerProfile.query.filter_by(user_id=user_id).first()
    job = Job.query.filter_by(id=job_id, employer_id=profile.id).first()
    if not job:
        return jsonify({"msg": "Job not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(job, key, value)
    db.session.commit()
    return jsonify({"msg": "Job updated"})

@employer_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
@jwt_required()
@role_required("employer")
def delete_job(job_id):
    user_id = get_jwt_identity()
    profile = EmployerProfile.query.filter_by(user_id=user_id).first()
    job = Job.query.filter_by(id=job_id, employer_id=profile.id).first()
    if not job:
        return jsonify({"msg": "Job not found"}), 404
    db.session.delete(job)
    db.session.commit()
    return jsonify({"msg": "Job deleted"})
