from flask import request
from flask_socketio import emit
from flaskapp import socket_io, db
from flaskapp.models import User, Chat, Message


@socket_io.on('user', namespace='/private')
def receive_user(user_id):
	user = User.query.get(user_id)
	user.session_id = request.sid


@socket_io.on('message', namespace='/private')
def send_message(payload):
	sender = User.query.get(payload['sender_id'])
	recipient = User.query.get(payload['recipient_id'])
	chat = Chat.query.get(payload['chat_id'])
	message = Message(type=sender.type, message=payload['message'], chat_id=chat.id)
	recipient_session_id = recipient.session_id
	emit('new_message', payload['message'], room=recipient_session_id)
	db.session.add(message)
	db.session.commit()
