from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..schemas.user_schema import UserSchema
from ..extensions import db

user_bp = Blueprint("users", __name__)
user_schema = UserSchema()

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user), 200

@user_bp.route("/me", methods=["PUT", "PATCH"])
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    body = request.get_json() or {}

    # allowed updates
    if "full_name" in body:
        user.full_name = body["full_name"]
    if "email" in body:
        user.email = body["email"]
    if "username" in body:
        user.username = body["username"]

    db.session.commit()
    return user_schema.dump(user), 200
