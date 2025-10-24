from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.jobseeker import JobSeekerProfile, db
from app.models.favorite import Favorite
from app.models.application import Application
from app.models.job import Job
from app.utils.decorators import role_required
from app.schemas.jobseeker_schema import JobSeekerSchema
from app.schemas.job_schema import JobSchema

jobseeker_bp = Blueprint("jobseeker_bp", __name__)
jobseeker_schema = JobSeekerSchema()
job_schema = JobSchema(many=True)

@jobseeker_bp.route("/me", methods=["GET"])
@jwt_required()
@role_required("job_seeker")
def get_profile():
    user_id = get_jwt_identity()
    profile = JobSeekerProfile.query.filter_by(user_id=user_id).first()
    return jobseeker_schema.dump(profile)

@jobseeker_bp.route("/me", methods=["PUT"])
@jwt_required()
@role_required("job_seeker")
def update_profile():
    user_id = get_jwt_identity()
    profile = JobSeekerProfile.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    for key, value in data.items():
        setattr(profile, key, value)
    db.session.commit()
    return jobseeker_schema.dump(profile)

@jobseeker_bp.route("/jobs", methods=["GET"])
@jwt_required()
@role_required("job_seeker")
def list_jobs():
    # Filtering
    location = request.args.get("location")
    job_type = request.args.get("job_type")
    query = Job.query
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(Job.job_type.ilike(f"%{job_type}%"))
    # Pagination
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    paginated = query.paginate(page=page, per_page=per_page)
    return jsonify({
        "jobs": job_schema.dump(paginated.items),
        "total": paginated.total,
        "page": page,
        "per_page": per_page
    })

@jobseeker_bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
@jwt_required()
@role_required("job_seeker")
def apply_job(job_id):
    user_id = get_jwt_identity()
    profile = JobSeekerProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"msg": "Profile not found"}), 404
    if Application.query.filter_by(job_id=job_id, job_seeker_id=profile.id).first():
        return jsonify({"msg": "Already applied"}), 400
    application = Application(job_id=job_id, job_seeker_id=profile.id)
    db.session.add(application)
    db.session.commit()
    return jsonify({"msg": "Application submitted"}), 201

@jobseeker_bp.route("/favorites/<int:job_id>", methods=["POST"])
@jwt_required()
@role_required("job_seeker")
def add_favorite(job_id):
    user_id = get_jwt_identity()
    profile = JobSeekerProfile.query.filter_by(user_id=user_id).first()
    if FavoriteJob.query.filter_by(job_id=job_id, job_seeker_id=profile.id).first():
        return jsonify({"msg": "Already in favorites"}), 400
    fav = FavoriteJob(job_seeker_id=profile.id, job_id=job_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Job added to favorites"}), 201
