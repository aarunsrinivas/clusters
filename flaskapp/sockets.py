from flask import request
from flask_socketio import emit
from flaskapp import socket_io, db
from flaskapp.models import User, Message
from flaskapp.routes import applicant_message_serializer, business_message_serializer


@socket_io.on('join', namespace='/messaging')
def join(payload):
	user = User.query.get(payload['userId'])
	user.session_id = request.sid
	db.session.commit()


@socket_io.on('leave', namespace='/messaging')
def leave(user_id):
	user = User.query.get(user_id)
	user.session_id = None
	db.session.commit()


@socket_io.on('message', namespace='/messaging')
def message(payload):
	print(payload)
	sender = User.query.get(payload['senderId'])
	recipient = User.query.get(payload['recipientId'])
	msg = Message(origin=payload['senderId'], message=payload['message'], chat_id=payload['chatId'])
	sender_session_id = sender.session_id
	recipient_session_id = recipient.session_id
	db.session.add(msg)
	db.session.commit()
	sender_serialized_message = applicant_message_serializer(msg) if sender.type == 'applicant' \
		else business_message_serializer(msg)
	recipient_serialized_message = applicant_message_serializer(msg) if recipient.type == 'applicant' \
		else business_message_serializer(msg)
	if recipient_session_id:
		emit('newMessage', recipient_serialized_message, room=recipient_session_id)
	emit('message', sender_serialized_message, room=sender_session_id)
