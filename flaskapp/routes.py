from flaskapp import app, db, bcrypt
from flaskapp.models import Applicant, Business, Cluster, Chat
from flask import json, jsonify, request
import cluster_world as world


# TODO: need to create requests that the applicant sends to business when they first apply

def applicant_serializer(applicant):
	return {
		'id': applicant.id,
		'name': applicant.name,
		'email': applicant.email,
		'features': applicant.features,
		'links': {
			'self': f'/applicants/{applicant.id}',
			'cluster': f'/clusters/{applicant.cluster_id}',
			'businesses': f'clusters/{applicant.cluster_id}/businesses',
			'applied': f'/applicants/{applicant.id}/applied',
			'interested': f'/applicants/{applicant.id}/interested',
			'reviewed': f'/applicants/{applicant.id}/reviewed',
			'declined': f'/applicants/{applicant.id}/declined',
			'rejected': f'/applicants/{applicant.id}/rejected',
			'chats': f'/applicants/{applicant.id}/chats'
		} if applicant.cluster_id else {
			'self': f'/applicants/{applicant.id}'
		}
	}


@app.route('/applicants', methods=['GET'])
def find_applicant():
	args = request.args
	if 'email' in args:
		return jsonify(list(map(applicant_serializer, Applicant.query.filter_by(email=args['email']))))
	return jsonify(list(map(applicant_serializer, Applicant.query.all())))


@app.route('/applicants', methods=['POST'])
def create_applicant():
	request_data = json.loads(request.data)
	applicant = Applicant(name=request_data['name'], email=request_data['email'],
	                      password=bcrypt.generate_password_hash(request_data['password']),
	                      features=request_data['features'])
	db.session.add(applicant)
	db.session.commit()
	return jsonify(applicant_serializer(applicant))


@app.route('/applicants/<int:applicant_id>', methods=['GET'])
def get_applicant(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(applicant_serializer(applicant))


@app.route('/applicants/<int:applicant_id>', methods=['DELETE'])
def delete_applicant(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	if applicant.cluster_id:
		world.remove_applicant(applicant)
	db.session.delete(applicant)
	db.session.commit()


@app.route('/applicants/<int:applicant_id>', methods=['POST'])
def transition_applicant(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant = Applicant.query.get(applicant_id)
	if action == 'join':
		world.add_applicant(applicant)
	elif action == 'peel':
		world.peel_applicant(applicant)
	elif action == 'leave':
		world.remove_applicant(applicant)
	return jsonify(applicant_serializer(applicant))


@app.route('/applicants/<int:applicant_id>', methods=['PUT'])
def update_applicant(applicant_id):
	request_data = json.loads(request.data)
	name = request_data['name']
	email = request_data['email']
	features = request_data['features']
	applicant = Applicant.query.get(applicant_id)
	applicant.name = name
	applicant.email = email
	applicant.features = features
	db.session.commit()
	return jsonify(applicant_serializer(applicant))


@app.route('/applicants/<int:applicant_id>/applied', methods=['GET'])
def get_applied(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/applicants/<int:applicant_id>/applied', methods=['PUT'])
def update_applied(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['business_id']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	if action == 'apply':
		if business in applicant.applied:
			return
		applicant.applied.append(business)
	elif action == 'cancel':
		if business not in applicant.applied:
			return
		applicant.applied.remove(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/applicants/<int:applicant_id>/interested', methods=['GET'])
def get_applicant_interested(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.interested)))


@app.route('/applicants/<int:applicant_id>/interested', methods=['PUT'])
def update_applicant_interested(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['business_id']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id)
	if business not in applicant.interested:
		return
	elif action == 'decline':
		applicant.interested.remove(business)
		applicant.declined.append(business)
		db.session.delete(chat)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.interested)))


@app.route('/applicants/<int:applicant_id>/reviewed', methods=['GET'])
def get_reviewed(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.reviewed)))


@app.route('/applicants/<int:applicant_id>/reviewed', methods=['PUT'])
def update_reviewed(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['business_id']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id)
	if business not in applicant.reviewed:
		return
	elif action == 'accept':
		applicant.reviewed.remove(business)
		db.session.delete(chat)
	elif action == 'decline':
		applicant.reviewed.remove(business)
		applicant.declined.append(business)
		db.session.delete(chat)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.reviewed)))


@app.route('/applicants/<int:applicant_id>/declined', methods=['GET'])
def get_applicant_declined(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.declined)))


@app.route('/applicants/<int:applicant_id>/declined', methods=['PUT'])
def updated_applicant_declined(applicant_id):
	request_data = json.loads(request.data)
	applicant = Applicant.query.get(applicant_id)
	action = request_data['action']
	if action == 'clear':
		applicant.declined.clear()
	elif action == 'remove':
		business_id = request_data['business_id']
		business = Business.query.get(business_id)
		applicant.declined.remove(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.declined)))


@app.route('/applicants/<int:applicant_id>/rejected', methods=['GET'])
def get_applicant_rejected(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.rejected)))


def applicant_chat_serializer(chat):
	return {
		'id': chat.id,
		'business_name': chat.business.name,
		'links': {
			'self': f'/applicants/{chat.applicant.id}/chats/{chat.id}',
			'applicant': f'/applicants/{chat.applicant.id}',
			'messages': f'/applicants/{chat.applicant.id}/chats/{chat.id}/messages'
		}
	}


@app.route('/applicants/<int:applicant_id>/chats', methods=['GET'])
def get_applicant_chats(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(applicant_chat_serializer, applicant.chats)))


@app.route('/applicants/<int:applicant_id>/chats/<int:chat_id>', methods=['GET'])
def get_applicant_chat(applicant_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(applicant_chat_serializer(chat))


def applicant_message_serializer(message):
	return {
		'id': message.id,
		'origin': message.origin,
		'date_posted': message.date_posted,
		'message': message.message,
		'links': {
			'self': f'/applicants/{message.chat.applicant.id}/chats/{message.chat.id}/messages/{message.id}',
			'messages': f'/applicants/{message.chat.applicant.id}/chats/{message.chat.id}/messages',
			'chat': f'/applicants/{message.chat.applicant.id}/chats/{message.chat.id}',
			'applicant': f'/applicants/{message.chat.applicant.id}'
		}

	}


@app.route('/applicants/<int:applicant_id>/chats/<int:chat_id>/messages', methods=['GET'])
def get_applicant_chat_messages(applicant_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(list(map(applicant_message_serializer, chat.messages)))


def business_serializer(business):
	return {
		'id': business.id,
		'name': business.name,
		'email': business.email,
		'features': business.features,
		'links': {
			'self': f'/businesses/{business.id}',
			'cluster': f'/clusters/{business.cluster_id}',
			'applicants': f'clusters/{business.cluster_id}/applicants',
			'received': f'/businesses/{business.id}/received',
			'interested': f'/businesses/{business.id}/interested',
			'offered': f'/businesses/{business.id}/offered',
			'declined': f'/businesses/{business.id}/declined',
			'rejected': f'/businesses/{business.id}/rejected',
			'chats': f'/businesses/{business.id}/chats'
		} if business.cluster_id else {
			'self': f'/businesses/{business.id}'
		}
	}


@app.route('/businesses', methods=['GET'])
def find_business():
	args = request.args
	if 'email' in args:
		return jsonify(list(map(business_serializer, Business.query.filter_by(email=args['email']))))
	return jsonify(list(map(business_serializer, Business.query.all())))


@app.route('/businesses', methods=['POST'])
def create_business():
	request_data = json.loads(request.data)
	business = Business(name=request_data['name'], email=request_data['email'],
	                    password=bcrypt.generate_password_hash(request_data['password']),
	                    features=request_data['features'])
	db.session.add(business)
	db.session.commit()
	return jsonify(business_serializer(business))


@app.route('/businesses/<int:business_id>', methods=['GET'])
def get_business(business_id):
	business = Business.query.get(business_id)
	return jsonify(business_serializer(business))


@app.route('/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
	business = Business.query.get(business_id)
	if business.cluster_id:
		world.remove_business(business)
	db.session.delete(business)
	db.session.commit()


@app.route('/businesses/<int:business_id>', methods=['POST'])
def transition_business(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business = Business.query.get(business_id)
	if action == 'join':
		world.add_business(business)
	elif action == 'peel':
		world.peel_business(business)
	elif action == 'leave':
		world.remove_business(business)
	return jsonify(business_serializer(business))


@app.route('/businesses/<int:business_id>', methods=['PUT'])
def update_business(business_id):
	request_data = json.loads(request.data)
	name = request_data['name']
	email = request_data['email']
	features = request_data['features']
	business = Business.query.get(business_id)
	business.name = name
	business.email = email
	business.features = features
	db.session.commit()
	return jsonify(business_serializer(business))


@app.route('/businesses/<int:business_id>/received', methods=['GET'])
def get_received(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/businesses/<int:business_id>/received', methods=['PUT'])
def update_received(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicant_id']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	if applicant not in business.received:
		return
	elif action == 'accept':
		chat = Chat(applicant_id=applicant.id, business_id=business.id)
		db.session.add(chat)
		business.received.remove(applicant)
		business.interested.append(applicant)
	elif action == 'decline':
		business.received.remove(applicant)
		business.declined.append(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/businesses/<int:business_id>/interested', methods=['GET'])
def get_business_interested(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.interested)))


@app.route('/businesses/<int:business_id>/interested', methods=['PUT'])
def update_business_interested(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicant_id']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if applicant not in business.received:
		return
	elif action == 'offer':
		business.interested.remove(applicant)
		business.offered.append(applicant)
	elif action == 'decline':
		db.session.delete(chat)
		business.interested.remove(applicant)
		business.declined.append(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/businesses/<int:business_id>/offered', methods=['GET'])
def get_offered(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/businesses/<int:business_id>/offered', methods=['PUT'])
def update_offered(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicant_id']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if applicant not in business.offered:
		return
	elif action == 'decline':
		db.session.delete(chat)
		business.offered.remove(applicant)
		business.declined.append(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/businesses/<int:business_id>/declined', methods=['GET'])
def get_business_declined(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.declined)))


@app.route('/businesses/<int:business_id>/declined', methods=['PUT'])
def updated_business_declined(business_id):
	request_data = json.loads(request.data)
	business = Business.query.get(business_id)
	action = request_data['action']
	if action == 'clear':
		business.declined.clear()
	elif action == 'remove':
		applicant_id = request_data['applicant_id']
		applicant = Applicant.query.get(applicant_id)
		business.declined.remove(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.declined)))


@app.route('/businesses/<int:business_id>/rejected', methods=['GET'])
def get_business_rejected(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.rejected)))


def business_chat_serializer(chat):
	return {
		'id': chat.id,
		'applicant_name': chat.applicant.name,
		'links': {
			'self': f'/businesses/{chat.business.id}/chats/{chat.id}',
			'business': f'/businesses/{chat.business.id}',
			'messages': f'/businesses/{chat.business.id}/chats/{chat.id}/messages'
		}
	}


@app.route('/businesses/<int:business_id/chats', methods=['GET'])
def get_business_chats(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(business_chat_serializer, business.chats)))


@app.route('/businesses/<int:business_id>/chats/<int:chat_id>', methods=['GET'])
def get_business_chat(business_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(business_chat_serializer(chat))


def business_message_serializer(message):
	return {
		'id': message.id,
		'origin': message.origin,
		'date_posted': message.date_posted,
		'message': message.message,
		'links': {
			'self': f'/businesses/{message.chat.business.id}/chats/{message.chat.id}/messages/{message.id}',
			'messages': f'/businesses/{message.chat.business.id}/chats/{message.chat.id}/messages',
			'chat': f'/businesses/{message.chat.business.id}/chats/{message.chat.id}',
			'business': f'/businesses/{message.chat.business.id}'
		}

	}


@app.route('/businesses/<int:business_id>/chats/<int:chat_id>/messages', methods=['GET'])
def get_business_chat_messages(business_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(list(map(business_message_serializer, chat.messages)))


def cluster_serializer(cluster):
	return {
		'id': cluster.id,
		'applicant_pop': cluster.applicant_pop,
		'business_pop': cluster.business_pop,
		'size': cluster.size,
		'links': {
			'self': f'/clusters/{cluster.id}',
			'applicants': f'/clusters/{cluster.id}/applicants',
			'businesses': f'/clusters/{cluster.id}/businesses'
		}
	}


@app.route('/clusters/<int:cluster_id>', methods=['GET'])
def get_cluster(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(cluster_serializer(cluster))


@app.route('/clusters/<int:cluster_id>/applicants', methods=['GET'])
def get_active_applicants(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(applicant_serializer, cluster.applicants)))


@app.route('/clusters/<int:cluster_id>/businesses', methods=['GET'])
def get_active_businesses(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(business_serializer, cluster.businesses)))
