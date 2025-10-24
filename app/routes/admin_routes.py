from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.user import User, db
from app.utils.decorators import role_required

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@role_required("admin")
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "role": u.role} for u in users])

@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify({"msg": "User updated"})

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"})
