from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.user import User
from ..schemas.user_schema import RegisterSchema, UserSchema
from ..services.auth_service import create_user
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
user_schema = UserSchema()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    errors = register_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    user, err = create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        full_name=data.get("full_name")
    )
    if err:
        return {"message": err}, 400

    return user_schema.dump(user), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = data.get("username") or data.get("email")
    password = data.get("password")
    if not identifier or not password:
        return {"message": "Provide username/email and password"}, 400

    # Allow login by username or email
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid credentials"}, 401

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return {"access_token": access, "refresh_token": refresh, "user": user_schema.dump(user)}, 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access = create_access_token(identity=current_user)
    return {"access_token": access}, 200
