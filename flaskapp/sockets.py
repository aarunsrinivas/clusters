from flask import request
from flask_socketio import emit
from flaskapp import socket_io, db
from flaskapp.models import User, Chat, Message


@socket_io.on('user', namespace='/initialize')
def receive_user(user_id):
	user = User.query.get(user_id)
	user.session_id = request.sid
	print(request.sid)
	db.session.commit()


@socket_io.on('message', namespace='/messaging')
def send_message(payload):
	sender = User.query.get(payload['sender_id'])
	recipient = User.query.get(payload['recipient_id'])
	chat = Chat.query.get(payload['chat_id'])
	message = Message(origin=sender.type, message=payload['message'], chat_id=chat.id)
	recipient_session_id = recipient.session_id
	emit('new_message', payload['message'], room=recipient_session_id)
	db.session.add(message)
	db.session.commit()
