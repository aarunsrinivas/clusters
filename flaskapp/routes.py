from flaskapp import app, db
from flaskapp.models import Applicant, Business, User, Cluster, Chat
from flask import json, jsonify, request
import cluster_world as world


def applicant_serializer(applicant):
	return {
		'id': applicant.id,
		'name': applicant.name,
		'email': applicant.email,
		'password': applicant.password,
		'clusterId': applicant.cluster_id,
		'features': applicant.features,
		'links': {
			'self': f'/applicants/{applicant.id}',
			'cluster': f'/clusters/{applicant.cluster_id}',
			'pool': f'clusters/{applicant.cluster_id}/businesses',
			'all': f'applicants/{applicant.id}/all',
			'applied': f'/applicants/{applicant.id}/applied',
			'received': f'/applicants/{applicant.id}/received',
			'interested': f'/applicants/{applicant.id}/interested',
			'reviewed': f'/applicants/{applicant.id}/reviewed',
			'accepted': f'/applicants/{applicant.id}/accepted',
			'declined': f'/applicants/{applicant.id}/declined',
			'rejected': f'/applicants/{applicant.id}/rejected',
			'chats': f'/applicants/{applicant.id}/chats'
		} if applicant.cluster_id else {
			'self': f'/applicants/{applicant.id}'
		}
	}


def business_serializer(business):
	return {
		'id': business.id,
		'name': business.name,
		'email': business.email,
		'password': business.password,
		'clusterId': business.cluster_id,
		'features': business.features,
		'links': {
			'self': f'/businesses/{business.id}',
			'cluster': f'/clusters/{business.cluster_id}',
			'pool': f'clusters/{business.cluster_id}/applicants',
			'all': f'businesses/{business.id}/all',
			'reached': f'businesses/{business.id}/reached',
			'received': f'/businesses/{business.id}/received',
			'interested': f'/businesses/{business.id}/interested',
			'offered': f'/businesses/{business.id}/offered',
			'accepted': f'/businesses/{business.id}/accepted',
			'declined': f'/businesses/{business.id}/declined',
			'rejected': f'/businesses/{business.id}/rejected',
			'chats': f'/businesses/{business.id}/chats'
		} if business.cluster_id else {
			'self': f'/businesses/{business.id}'
		}
	}


def applicant_chat_serializer(chat):
	return {
		'id': chat.id,
		'senderId': chat.applicant_id,
		'recipientId': chat.business_id,
		'recipientName': chat.business.name,
		'links': {
			'self': f'/applicants/{chat.applicant.id}/chats/{chat.id}',
			'messages': f'/applicants/{chat.applicant.id}/chats/{chat.id}/messages'
		}
	}


def business_chat_serializer(chat):
	return {
		'id': chat.id,
		'senderId': chat.business_id,
		'recipientId': chat.applicant_id,
		'recipientName': chat.applicant.name,
		'links': {
			'self': f'/businesses/{chat.business.id}/chats/{chat.id}',
			'messages': f'/businesses/{chat.business.id}/chats/{chat.id}/messages'
		}
	}


def applicant_message_serializer(message):
	return {
		'id': message.id,
		'origin': message.origin,
		'message': message.message,
		'links': {
			'self': f'/applicants/{message.chat.applicant.id}/chats/{message.chat.id}/messages/{message.id}'
		}

	}


def business_message_serializer(message):
	return {
		'id': message.id,
		'origin': message.origin,
		'message': message.message,
		'links': {
			'self': f'/businesses/{message.chat.business.id}/chats/{message.chat.id}/messages/{message.id}',
		}

	}


def cluster_serializer(cluster):
	return {
		'id': cluster.id,
		'applicantPop': cluster.applicant_pop,
		'businessPop': cluster.business_pop,
		'size': cluster.size,
		'links': {
			'self': f'/clusters/{cluster.id}',
			'applicants': f'/clusters/{cluster.id}/applicants',
			'businesses': f'/clusters/{cluster.id}/businesses'
		}
	}


@app.route('/users', methods=['GET'])
def find_user():
	args = request.args
	if 'email' in args:
		return jsonify([applicant_serializer(user) if isinstance(user, Applicant)
		                else business_serializer(user) for user in
		                User.query.filter_by(email=args['email']).all()])
	return jsonify([applicant_serializer(user) if isinstance(user, Applicant)
	                else business_serializer(user) for user in
	                User.query.all()])


@app.route('/applicants', methods=['GET'])
def find_applicant():
	args = request.args
	if 'email' in args:
		return jsonify(list(map(applicant_serializer, Applicant.query.filter_by(email=args['email']).all())))
	return jsonify(list(map(applicant_serializer, Applicant.query.all())))


@app.route('/applicants', methods=['POST'])
def create_applicant():
	request_data = json.loads(request.data)
	applicant = Applicant(name=request_data['name'], email=request_data['email'],
	                      password=request_data['password'],
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


@app.route('/applicants/<int:applicant_id>/all', methods=['GET'])
def get_applicant_all(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	pool = list(map(business_serializer, applicant.cluster.businesses))
	applied = list(map(business_serializer, applicant.applied))
	received = list(map(business_serializer, applicant.received))
	interested = list(map(business_serializer, applicant.interested))
	reviewed = list(map(business_serializer, applicant.reviewed))
	accepted = list(map(business_serializer, applicant.accepted))
	declined = list(map(business_serializer, applicant.declined))
	rejected = list(map(business_serializer, applicant.rejected))
	return jsonify({'pool': pool, 'applied': applied, 'received': received, 'interested': interested,
	                'reviewed': reviewed, 'accepted': accepted, 'declined': declined, 'rejected': rejected})


@app.route('/applicants/<int:applicant_id>/applied', methods=['GET'])
def get_applied(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/applicants/<int:applicant_id>/applied', methods=['PUT'])
def update_applied(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	if action == 'apply':
		if business not in applicant.applied:
			applicant.applied.append(business)
	elif action == 'cancel':
		if business in applicant.applied:
			applicant.applied.remove(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/applicants/<int:applicant_id>/received', methods=['GET'])
def get_applicant_received(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.received)))


@app.route('/applicants/<int:applicant_id>/received', methods=['PUT'])
def update_applicant_received(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	if business in applicant.received:
		if action == 'accept':
			chat = Chat(applicant_id=applicant.id, business_id=business.id)
			db.session.add(chat)
			applicant.received.remove(business)
			applicant.interested.append(business)
		elif action == 'decline':
			applicant.received.remove(business)
			applicant.declined.append(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.received)))


@app.route('/applicants/<int:applicant_id>/interested', methods=['GET'])
def get_applicant_interested(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.interested)))


@app.route('/applicants/<int:applicant_id>/interested', methods=['PUT'])
def update_applicant_interested(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if business in applicant.interested and action == 'decline':
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
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if business in applicant.reviewed:
		if action == 'accept':
			applicant.reviewed.remove(business)
			applicant.accepted.append(business)
			db.session.delete(chat)
		elif action == 'decline':
			applicant.reviewed.remove(business)
			applicant.declined.append(business)
			db.session.delete(chat)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.reviewed)))


@app.route('/applicants/<int:applicant_id>/accepted', methods=['GET'])
def get_applicant_accepted(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.accepted)))


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
		business_id = request_data['businessId']
		business = Business.query.get(business_id)
		if business in applicant.declined:
			applicant.declined.remove(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.declined)))


@app.route('/applicants/<int:applicant_id>/rejected', methods=['GET'])
def get_applicant_rejected(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.rejected)))


@app.route('/applicants/<int:applicant_id>/chats', methods=['GET'])
def get_applicant_chats(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(applicant_chat_serializer, applicant.chats)))


@app.route('/applicants/<int:applicant_id>/chats/<int:chat_id>', methods=['GET'])
def get_applicant_chat(applicant_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(applicant_chat_serializer(chat))


@app.route('/applicants/<int:applicant_id>/chats/<int:chat_id>/messages', methods=['GET'])
def get_applicant_chat_messages(applicant_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(list(map(applicant_message_serializer, chat.messages)))


@app.route('/businesses', methods=['GET'])
def find_business():
	args = request.args
	if 'email' in args:
		return jsonify(list(map(business_serializer, Business.query.filter_by(email=args['email']).all())))
	return jsonify(list(map(business_serializer, Business.query.all())))


@app.route('/businesses', methods=['POST'])
def create_business():
	request_data = json.loads(request.data)
	business = Business(name=request_data['name'], email=request_data['email'],
	                    password=request_data['password'],
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


@app.route('/businesses/<int:business_id>/all', methods=['GET'])
def get_business_all(business_id):
	business = Business.query.get(business_id)
	pool = list(map(applicant_serializer, business.cluster.applicants))
	reached = list(map(applicant_serializer, business.reached))
	received = list(map(applicant_serializer, business.received))
	interested = list(map(applicant_serializer, business.interested))
	offered = list(map(applicant_serializer, business.offered))
	accepted = list(map(applicant_serializer, business.accepted))
	declined = list(map(applicant_serializer, business.declined))
	rejected = list(map(applicant_serializer, business.rejected))
	return jsonify({'pool': pool, 'reached': reached, 'received': received, 'interested': interested,
	                'offered': offered, 'accepted': accepted, 'declined': declined, 'rejected': rejected})


@app.route('/businesses/<int:business_id>/reached', methods=['GET'])
def get_reached(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.reached)))


@app.route('/businesses/<int:business_id>/reached', methods=['PUT'])
def update_reached(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	if action == 'reach':
		if applicant not in business.reached:
			business.reached.append(applicant)
	elif action == 'cancel':
		if applicant in business.reached:
			business.reached.remove(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.reached)))


@app.route('/businesses/<int:business_id>/received', methods=['GET'])
def get_received(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/businesses/<int:business_id>/received', methods=['PUT'])
def update_business_received(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	if applicant in business.received:
		if action == 'accept':
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
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if applicant in business.interested:
		if action == 'offer':
			business.interested.remove(applicant)
			business.offered.append(applicant)
		elif action == 'decline':
			db.session.delete(chat)
			business.interested.remove(applicant)
			business.declined.append(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.interested)))


@app.route('/businesses/<int:business_id>/offered', methods=['GET'])
def get_offered(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/businesses/<int:business_id>/offered', methods=['PUT'])
def update_offered(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if applicant in business.offered and action == 'rescind':
		db.session.delete(chat)
		business.offered.remove(applicant)
		business.declined.append(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/businesses/<int:business_id>/accepted', methods=['GET'])
def get_business_accepted(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.accepted)))


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
		applicant_id = request_data['applicantId']
		applicant = Applicant.query.get(applicant_id)
		if applicant in business.declined:
			business.declined.remove(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.declined)))


@app.route('/businesses/<int:business_id>/rejected', methods=['GET'])
def get_business_rejected(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.rejected)))


@app.route('/businesses/<int:business_id>/chats', methods=['GET'])
def get_business_chats(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(business_chat_serializer, business.chats)))


@app.route('/businesses/<int:business_id>/chats/<int:chat_id>', methods=['GET'])
def get_business_chat(business_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(business_chat_serializer(chat))


@app.route('/businesses/<int:business_id>/chats/<int:chat_id>/messages', methods=['GET'])
def get_business_chat_messages(business_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(list(map(business_message_serializer, chat.messages)))


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
