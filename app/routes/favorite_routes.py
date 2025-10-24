from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.favorite import Favorite
from app.schemas.favorite_schema import FavoriteSchema

favorite_bp = Blueprint("favorite_bp", __name__, url_prefix="/api/favorites")

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)

# Get all favorites
@favorite_bp.route("/", methods=["GET"])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify(favorites_schema.dump(favorites)), 200

# Get a single favorite
@favorite_bp.route("/<int:id>", methods=["GET"])
def get_favorite(id):
    favorite = Favorite.query.get_or_404(id)
    return jsonify(favorite_schema.dump(favorite)), 200

# Create a favorite
@favorite_bp.route("/", methods=["POST"])
def create_favorite():
    data = request.get_json()
    new_favorite = Favorite(
        job_id=data["job_id"],
        jobseeker_id=data["jobseeker_id"]
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(favorite_schema.dump(new_favorite)), 201

# Delete a favorite
@favorite_bp.route("/<int:id>", methods=["DELETE"])
def delete_favorite(id):
    favorite = Favorite.query.get_or_404(id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200
