from flaskapp import app, db, bcrypt
from flaskapp.models import Applicant, Business, Cluster
from flask import json, jsonify, request
import cluster_world as world


def applicant_serializer(applicant):
	return {
		'id': applicant.id,
		'name': applicant.name,
		'email': applicant.email,
		'features': applicant.features,
		'cluster_id': applicant.cluster_id,
		'links': {
			'self': f'/applicants/{applicant.id}',
			'cluster': f'/clusters/{applicant.cluster_id}',
			'businesses': f'clusters/{applicant.cluster_id}/businesses',
			'applied': f'/applicants/{applicant.id}/applied',
			'reviewed': f'/applicants/{applicant.id}/reviewed',
			'rejected': f'/applicants/{applicant.id}/rejected'
		} if applicant.cluster_id else {
			'self': f'/applicants/{applicant.id}'
		}
	}


@app.route('/applicants', methods=['GET'])
def get_applicants():
	return jsonify(list(map(applicant_serializer, Applicant.query.all())))


@app.route('/applicants', methods=['POST'])
def create_applicant():
	request_data = json.loads(request.data)
	applicant = Applicant(name=request_data['name'], email=request_data['email'],
	                      password=bcrypt.generate_password_hash(request_data['password']),
	                      features=request_data['features'])
	db.session.add(applicant)
	db.session.commit()
	return {'201': 'Applicant Created Successfully'}


@app.route('/applicants/<int:applicant_id>', methods=['GET'])
def get_applicant(applicant_id):
	return jsonify(list(map(applicant_serializer, Applicant.query.filter_by(id=applicant_id))))


@app.route('/applicants/<int:applicant_id>', methods=['DELETE'])
def delete_applicant(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	if not applicant.is_dormant:
		world.remove_applicant(applicant)
	db.session.delete(applicant)
	db.session.commit()
	return {'204': 'Applicant Deleted Successfully'}


@app.route('/applicants/<int:applicant_id>', methods=['POST'])
def move_applicant(applicant_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	applicant = Applicant.query.get(applicant_id)
	if action == 'join':
		world.add_applicant(applicant)
		return {'200': 'Applicant Joined Cluster Successfully'}
	elif action == 'peel':
		world.peel_applicant(applicant)
		return {'200': 'Applicant Peeled Successfully'}
	elif action == 'leave':
		world.remove_applicant(applicant)
		return {'200': 'Applicant Left Cluster Successfully'}
	else:
		return {'400': 'Invalid Action Passed'}


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


@app.route('/applicants/<int:applicant_id>/applied', methods=['GET'])
def get_applied(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.applied)))


@app.route('/applicants/<int:applicant_id>/reviewed', methods=['GET'])
def get_reviewed(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.reviewed)))


@app.route('/applicants/<int:applicant_id>/rejected', methods=['GET'])
def get_applicant_rejected(applicant_id):
	applicant = Applicant.query.get(applicant_id)
	return jsonify(list(map(business_serializer, applicant.rejected)))


def business_serializer(business):
	return {
		'id': business.id,
		'name': business.name,
		'email': business.email,
		'features': business.features,
		'cluster_id': business.cluster_id,
		'links': {
			'self': f'/businesses/{business.id}',
			'cluster': f'/clusters/{business.cluster_id}',
			'applicants': f'clusters/{business.cluster_id}/applicants',
			'received': f'/businesses/{business.id}/received',
			'offered': f'/businesses/{business.id}/offered',
			'rejected': f'/businesses/{business.id}/rejected'
		} if business.cluster_id else {
			'self': f'/businesses/{business.id}'
		}
	}


@app.route('/businesses', methods=['GET'])
def get_businesses():
	return jsonify(list(map(business_serializer, Business.query.all())))


@app.route('/businesses', methods=['POST'])
def create_business():
	request_data = json.loads(request.data)
	business = Business(name=request_data['name'], email=request_data['email'],
	                    password=bcrypt.generate_password_hash(request_data['password']),
	                    features=request_data['features'])
	db.session.add(business)
	db.session.commit()
	return {'201': 'Business Created Successfully'}


@app.route('/businesses/<int:business_id>', methods=['GET'])
def get_business(business_id):
	return jsonify(list(map(business_serializer, Business.query.filter_by(id=business_id))))


@app.route('/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
	business = Business.query.get(business_id)
	if not business.is_dormant:
		world.remove_business(business)
	db.session.delete(business)
	db.session.commit()
	return {'204': 'Applicant Deleted Successfully'}


@app.route('/businesses/<int:business_id>', methods=['POST'])
def move_business(business_id):
	request_data = json.loads(request.data)
	action = request_data['action']
	business = Business.query.get(business_id)
	if action == 'join':
		world.add_business(business)
		return {'200': 'Business Joined Cluster Successfully'}
	elif action == 'peel':
		world.peel_business(business)
		return {'200': 'Business Peeled Successfully'}
	elif action == 'leave':
		world.remove_business(business)
		return {'200': 'Business Left Cluster Successfully'}
	else:
		return {'400': 'Invalid Action Passed'}


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


@app.route('/businesses/<int:business_id>/received', methods=['GET'])
def get_received(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.received)))


@app.route('/businesses/<int:business_id>/offered', methods=['GET'])
def get_offered(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.offered)))


@app.route('/businesses/<int:business_id>/rejected', methods=['GET'])
def get_business_rejected(business_id):
	business = Business.query.get(business_id)
	return jsonify(list(map(applicant_serializer, business.rejected)))


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
	return jsonify(list(map(cluster_serializer, Cluster.query.filter_by(id=cluster_id))))


@app.route('clusters/<int:cluster_id>/applicants', methods=['GET'])
def get_active_applicants(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(applicant_serializer, cluster.applicants)))


@app.route('clusters/<int:cluster_id>/businesses', methods=['GET'])
def get_active_businesses(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(business_serializer, cluster.businesses)))
