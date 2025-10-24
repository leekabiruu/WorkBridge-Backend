from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.message import Message, db
from app.utils.decorators import role_required

message_bp = Blueprint("message_bp", __name__)

@message_bp.route("/", methods=["GET"])
@jwt_required()
def list_conversations():
    user_id = get_jwt_identity()
    messages = Message.query.filter(
        (Message.sender_id==user_id) | (Message.recipient_id==user_id)
    ).all()
    # Group by conversation_id or recipient
    return jsonify([{"id": m.id, "text": m.text, "sender_id": m.sender_id,
                     "recipient_id": m.recipient_id, "timestamp": m.timestamp} for m in messages])

@message_bp.route("/", methods=["POST"])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    message = Message(
        sender_id=user_id,
        recipient_id=data["recipient_id"],
        text=data["text"],
        attachment_url=data.get("attachment_url")
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({"msg": "Message sent", "message_id": message.id}), 201
