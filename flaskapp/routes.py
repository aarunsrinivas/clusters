from flaskapp import app, db
from flaskapp.models import Applicant, Business, User, Cluster, ClusterWorld, Chat, Major, Course, Standing, Skill, \
	Interest
from flask import json, jsonify, request


def applicant_serializer(applicant):
	return {
		'id': applicant.id,
		'name': applicant.name,
		'email': applicant.email,
		'password': applicant.password,
		'clusterId': applicant.cluster_id,
		'worldId': applicant.world_id,
		'cap': applicant.cap,
		'features': applicant.features.serialized,
		'links': {
			'self': f'/worlds/{applicant.world_id}/applicants/{applicant.id}',
			'cluster': f'/worlds/{applicant.world_id}/clusters/{applicant.cluster_id}',
			'pool': f'/worlds/{applicant.world_id}/clusters/{applicant.cluster_id}/businesses',
			'all': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/all',
			'applied': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/applied',
			'received': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/received',
			'interested': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/interested',
			'reviewed': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/reviewed',
			'accepted': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/accepted',
			'declined': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/declined',
			'rejected': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/rejected',
			'chats': f'/worlds/{applicant.world_id}/applicants/{applicant.id}/chats'
		} if applicant.cluster_id else {
			'self': f'/worlds/{applicant.world_id}/applicants/{applicant.id}'
		}
	}


def business_serializer(business):
	return {
		'id': business.id,
		'name': business.name,
		'email': business.email,
		'password': business.password,
		'clusterId': business.cluster_id,
		'worldId': business.world_id,
		'cap': business.cap,
		'features': business.features.serialized,
		'links': {
			'self': f'/worlds/{business.world_id}/businesses/{business.id}',
			'cluster': f'/worlds/{business.world_id}/clusters/{business.cluster_id}',
			'pool': f'/worlds/{business.world_id}/clusters/{business.cluster_id}/applicants',
			'all': f'/worlds/{business.world_id}/businesses/{business.id}/all',
			'reached': f'/worlds/{business.world_id}/businesses/{business.id}/reached',
			'received': f'/worlds/{business.world_id}/businesses/{business.id}/received',
			'interested': f'/worlds/{business.world_id}/businesses/{business.id}/interested',
			'offered': f'/worlds/{business.world_id}/businesses/{business.id}/offered',
			'accepted': f'/worlds/{business.world_id}/businesses/{business.id}/accepted',
			'declined': f'/worlds/{business.world_id}/businesses/{business.id}/declined',
			'rejected': f'/worlds/{business.world_id}/businesses/{business.id}/rejected',
			'chats': f'/worlds/{business.world_id}/businesses/{business.id}/chats'
		} if business.cluster_id else {
			'self': f'/worlds/{business.world_id}/businesses/{business.id}'
		}
	}


def applicant_chat_serializer(chat):
	return {
		'id': chat.id,
		'senderId': chat.applicant_id,
		'recipientId': chat.business_id,
		'recipientName': chat.business.name,
		'links': {
			'self': f'/worlds/{chat.applicant.world_id}/applicants/{chat.applicant.id}/chats/{chat.id}',
			'messages': f'/worlds/{chat.applicant.world_id}/applicants/{chat.applicant.id}/chats/{chat.id}/messages'
		}
	}


def business_chat_serializer(chat):
	return {
		'id': chat.id,
		'senderId': chat.business_id,
		'recipientId': chat.applicant_id,
		'recipientName': chat.applicant.name,
		'links': {
			'self': f'/worlds/{chat.business.world_id}/businesses/{chat.business.id}/chats/{chat.id}',
			'messages': f'/worlds/{chat.business.world_id}/businesses/{chat.business.id}/chats/{chat.id}/messages'
		}
	}


def applicant_message_serializer(message):
	return {
		'id': message.id,
		'origin': message.origin,
		'message': message.message,
		'links': {
			'self': f'/worlds/{message.chat.applicant.world_id}/applicants/{message.chat.applicant.id}/chats/{message.chat.id}/messages/{message.id}'
		}

	}


def business_message_serializer(message):
	return {
		'id': message.id,
		'origin': message.origin,
		'message': message.message,
		'links': {
			'self': f'/worlds/{message.chat.business.world_id}/businesses/{message.chat.business.id}/chats/{message.chat.id}/messages/{message.id}',
		}

	}


def world_serializer(world):
	return {
		'id': world.id,
		'links': {
			'self': f'/worlds/{world.id}',
			'applicants': f'/worlds/{world.id}/applicants',
			'businesses': f'/worlds/{world.id}/businesses',
			'clusters': f'/worlds/{world.id}/clusters',
			'majors': f'/worlds/{world.id}/majors',
			'courses': f'/worlds/{world.id}/courses'
		}
	}


@app.route('/worlds', methods=['GET'])
def find_world():
	args = request.args
	if 'id' in args:
		return jsonify(list(map(world_serializer, ClusterWorld.query.filter_by(id=args['id']).all())))
	return jsonify(list(map(world_serializer, ClusterWorld.query.all())))


@app.route('/users', methods=['GET'])
def find_user():
	args = request.args
	if 'email' in args:
		return jsonify([applicant_serializer(user) if user.type == 'applicant'
		                else business_serializer(user) for user in
		                User.query.filter_by(email=args['email']).all()])
	return jsonify([applicant_serializer(user) if user.type == 'applicant'
	                else business_serializer(user) for user in
	                User.query.all()])


@app.route('/worlds/<string:world_id>/applicants', methods=['POST'])
def create_applicant(world_id):
	request_data = json.loads(request.data)
	applicant = Applicant(name=request_data['name'], email=request_data['email'],
	                      password=request_data['password'],
	                      world_id=world_id)
	db.session.add(applicant)
	db.session.commit()
	return jsonify(applicant_serializer(applicant))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>', methods=['GET'])
def get_applicant(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(applicant_serializer(applicant))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>', methods=['DELETE'])
def delete_applicant(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	world = applicant.world
	if applicant.cluster_id:
		world.remove_applicant(applicant)
	db.session.delete(applicant)
	db.session.commit()


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>', methods=['POST'])
def transition_applicant(world_id, applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant = Applicant.query.get(applicant_id)
	world = applicant.world
	if action == 'join':
		world.add(applicant)
	elif action == 'peel':
		world.peel(applicant)
	elif action == 'leave':
		world.remove(applicant)
	return jsonify(applicant_serializer(applicant))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>', methods=['PUT'])
def update_applicant(world_id, applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant = Applicant.query.get(applicant_id)
	if action == 'features':
		applicant.cap = request_data['cap']
		applicant.features.gpa = request_data['gpa']
		applicant.features.majors = {Major.query.get(major) or Major(id=major) for major in request_data['majors']}
		applicant.features.standings = {Standing.query.get(standing) or Standing(id=standing) for standing in
		                                request_data['standings']}
		applicant.features.skills = {Skill.query.get(skill) or Skill(id=skill) for skill in request_data['skills']}
		applicant.features.interests = {Interest.query.get(interest) or Interest(id=interest) for interest in
		                                request_data['interests']}
		applicant.features.courses = {Course.query.get(course) or Course(id=course) for course in
		                              request_data['courses']}
	elif action == 'account':
		applicant.name = request_data['name']
		applicant.email = request_data['email']
		applicant.password = request_data['password']
		applicant.set_world(request_data['worldId'])
	db.session.commit()
	return jsonify(applicant_serializer(applicant))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/all', methods=['GET'])
def get_applicant_all(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	cap = applicant.cap
	pool = list(map(business_serializer, applicant.cluster.businesses))
	applied = list(map(business_serializer, applicant.applied))
	received = list(map(business_serializer, applicant.received))
	interested = list(map(business_serializer, applicant.interested))
	reviewed = list(map(business_serializer, applicant.reviewed))
	accepted = list(map(business_serializer, applicant.accepted))
	declined = list(map(business_serializer, applicant.declined))
	rejected = list(map(business_serializer, applicant.rejected))
	return jsonify({'cap': cap, 'pool': pool, 'applied': applied, 'received': received, 'interested': interested,
	                'reviewed': reviewed, 'accepted': accepted, 'declined': declined, 'rejected': rejected})


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/applied', methods=['GET'])
def get_applied(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/applied', methods=['PUT'])
def update_applied(world_id, applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	if action == 'apply':
		if business not in applicant.applied:
			applicant.applied.add(business)
	elif action == 'cancel':
		if business in applicant.applied:
			applicant.applied.remove(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/received', methods=['GET'])
def get_applicant_received(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.received)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/received', methods=['PUT'])
def update_applicant_received(world_id, applicant_id):
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
			applicant.interested.add(business)
		elif action == 'decline':
			applicant.received.remove(business)
			applicant.declined.add(business)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.received)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/interested', methods=['GET'])
def get_applicant_interested(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.interested)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/interested', methods=['PUT'])
def update_applicant_interested(world_id, applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if business in applicant.interested and action == 'decline':
		applicant.interested.remove(business)
		applicant.declined.add(business)
		db.session.delete(chat)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.interested)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/reviewed', methods=['GET'])
def get_reviewed(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.reviewed)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/reviewed', methods=['PUT'])
def update_reviewed(world_id, applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business_id = request_data['businessId']
	business = Business.query.get(business_id)
	applicant = Applicant.query.get(applicant_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if business in applicant.reviewed:
		if action == 'accept':
			applicant.reviewed.remove(business)
			applicant.accepted.add(business)
			applicant.cap -= 1
			business.cap -= 1
			db.session.delete(chat)
		elif action == 'decline':
			applicant.reviewed.remove(business)
			applicant.declined.add(business)
			db.session.delete(chat)
	db.session.commit()
	return jsonify(list(map(business_serializer, applicant.reviewed)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/accepted', methods=['GET'])
def get_applicant_accepted(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.accepted)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/declined', methods=['GET'])
def get_applicant_declined(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.declined)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/declined', methods=['PUT'])
def updated_applicant_declined(world_id, applicant_id):
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


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/rejected', methods=['GET'])
def get_applicant_rejected(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.rejected)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/chats', methods=['GET'])
def get_applicant_chats(world_id, applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(applicant_chat_serializer, applicant.chats)))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/chats/<int:chat_id>', methods=['GET'])
def get_applicant_chat(world_id, applicant_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(applicant_chat_serializer(chat))


@app.route('/worlds/<string:world_id>/applicants/<int:applicant_id>/chats/<int:chat_id>/messages', methods=['GET'])
def get_applicant_chat_messages(world_id, applicant_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(list(map(applicant_message_serializer, chat.messages)))


@app.route('/worlds/<string:world_id>/businesses', methods=['POST'])
def create_business(world_id):
	request_data = json.loads(request.data)
	business = Business(name=request_data['name'], email=request_data['email'],
	                    password=request_data['password'],
	                    world_id=world_id)
	db.session.add(business)
	db.session.commit()
	return jsonify(business_serializer(business))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>', methods=['GET'])
def get_business(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(business_serializer(business))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(world_id, business_id):
	business = Business.query.get(business_id)
	world = business.world
	if business.cluster_id:
		world.remove_business(business)
	db.session.delete(business)
	db.session.commit()


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>', methods=['POST'])
def transition_business(world_id, business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business = Business.query.get(business_id)
	world = business.world
	if action == 'join':
		world.add(business)
	elif action == 'peel':
		world.peel(business)
	elif action == 'leave':
		world.remove(business)
	return jsonify(business_serializer(business))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>', methods=['PUT'])
def update_business(world_id, business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business = Business.query.get(business_id)
	if action == 'features':
		business.cap = request_data['cap']
		business.features.gpa = request_data['gpa']
		business.features.majors = {Major.query.get(major) or Major(id=major) for major in request_data['majors']}
		business.features.standings = {Standing.query.get(standing) or Standing(id=standing) for standing in
		                               request_data['standings']}
		business.features.skills = {Skill.query.get(skill) or Skill(id=skill) for skill in request_data['skills']}
		business.features.interests = {Interest.query.get(interest) or Interest(id=interest) for interest in
		                               request_data['interests']}
		business.features.courses = {Course.query.get(course) or Course(id=course) for course in
		                             request_data['courses']}
	elif action == 'account':
		business.name = request_data['name']
		business.email = request_data['email']
		business.password = request_data['password']
		business.set_world(request_data['worldId'])
	db.session.commit()
	return jsonify(business_serializer(business))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/all', methods=['GET'])
def get_business_all(world_id, business_id):
	business = Business.query.get(business_id)
	cap = business.cap
	pool = list(map(applicant_serializer, business.cluster.applicants))
	reached = list(map(applicant_serializer, business.reached))
	received = list(map(applicant_serializer, business.received))
	interested = list(map(applicant_serializer, business.interested))
	offered = list(map(applicant_serializer, business.offered))
	accepted = list(map(applicant_serializer, business.accepted))
	declined = list(map(applicant_serializer, business.declined))
	rejected = list(map(applicant_serializer, business.rejected))
	return jsonify({'cap': cap, 'pool': pool, 'reached': reached, 'received': received, 'interested': interested,
	                'offered': offered, 'accepted': accepted, 'declined': declined, 'rejected': rejected})


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/reached', methods=['GET'])
def get_reached(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.reached)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/reached', methods=['PUT'])
def update_reached(world_id, business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	if action == 'reach':
		if applicant not in business.reached:
			business.reached.add(applicant)
	elif action == 'cancel':
		if applicant in business.reached:
			business.reached.remove(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.reached)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/received', methods=['GET'])
def get_received(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/received', methods=['PUT'])
def update_business_received(world_id, business_id):
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
			business.interested.add(applicant)
		elif action == 'decline':
			business.received.remove(applicant)
			business.declined.add(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/interested', methods=['GET'])
def get_business_interested(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.interested)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/interested', methods=['PUT'])
def update_business_interested(world_id, business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if applicant in business.interested:
		if action == 'offer':
			business.interested.remove(applicant)
			business.offered.add(applicant)
		elif action == 'decline':
			db.session.delete(chat)
			business.interested.remove(applicant)
			business.declined.add(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.interested)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/offered', methods=['GET'])
def get_offered(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/offered', methods=['PUT'])
def update_offered(world_id, business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant_id = request_data['applicantId']
	applicant = Applicant.query.get(applicant_id)
	business = Business.query.get(business_id)
	chat = Chat.query.filter_by(applicant_id=applicant.id, business_id=business.id).first()
	if applicant in business.offered and action == 'rescind':
		db.session.delete(chat)
		business.offered.remove(applicant)
		business.declined.add(applicant)
	db.session.commit()
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/accepted', methods=['GET'])
def get_business_accepted(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.accepted)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/declined', methods=['GET'])
def get_business_declined(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.declined)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/declined', methods=['PUT'])
def updated_business_declined(world_id, business_id):
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


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/rejected', methods=['GET'])
def get_business_rejected(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.rejected)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/chats', methods=['GET'])
def get_business_chats(world_id, business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(business_chat_serializer, business.chats)))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/chats/<int:chat_id>', methods=['GET'])
def get_business_chat(world_id, business_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(business_chat_serializer(chat))


@app.route('/worlds/<string:world_id>/businesses/<int:business_id>/chats/<int:chat_id>/messages', methods=['GET'])
def get_business_chat_messages(world_id, business_id, chat_id):
	chat = Chat.query.get(chat_id)
	return jsonify(list(map(business_message_serializer, chat.messages)))


@app.route('/worlds/<string:world_id>/clusters/<int:cluster_id>/applicants', methods=['GET'])
def get_active_applicants(world_id, cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(applicant_serializer, cluster.applicants)))


@app.route('/worlds/<string:world_id>/clusters/<int:cluster_id>/businesses', methods=['GET'])
def get_active_businesses(world_id, cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(business_serializer, cluster.businesses)))
