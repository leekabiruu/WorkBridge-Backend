from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.application import Application
from app.schemas.application_schema import ApplicationSchema

application_bp = Blueprint("application_bp", __name__, url_prefix="/api/applications")

application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)

# Get all applications
@application_bp.route("/", methods=["GET"])
def get_applications():
    apps = Application.query.all()
    return jsonify(applications_schema.dump(apps)), 200

# Get application by ID
@application_bp.route("/<int:id>", methods=["GET"])
def get_application(id):
    app = Application.query.get_or_404(id)
    return jsonify(application_schema.dump(app)), 200

# Create a new application
@application_bp.route("/", methods=["POST"])
def create_application():
    data = request.get_json()
    new_app = Application(
        job_id=data["job_id"],
        jobseeker_id=data["jobseeker_id"],
        cover_letter=data.get("cover_letter"),
        status=data.get("status", "pending")
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify(application_schema.dump(new_app)), 201

# Update application
@application_bp.route("/<int:id>", methods=["PATCH"])
def update_application(id):
    app = Application.query.get_or_404(id)
    data = request.get_json()
    if "status" in data:
        app.status = data["status"]
    db.session.commit()
    return jsonify(application_schema.dump(app)), 200

# Delete application
@application_bp.route("/<int:id>", methods=["DELETE"])
def delete_application(id):
    app = Application.query.get_or_404(id)
    db.session.delete(app)
    db.session.commit()
    return jsonify({"msg": "Application deleted"}), 200
