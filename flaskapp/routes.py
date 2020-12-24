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


@app.route('/applicants/<int:applicant_id>', methods=['PUT'])
def update_applicant(applicant_id):
	request_data = json.loads(request.data)
	now_active = request_data['now_active']
	applicant = Applicant.query.get(applicant_id)
	if applicant.is_dormant and now_active:
		world.add_applicant(applicant)
	elif not applicant.is_dormant and now_active:
		world.peel_applicant(applicant)
	elif not applicant.is_dormant and not now_active:
		world.remove_applicant(applicant)
	applicant.is_dormant = not now_active if applicant.is_dormant == now_active else applicant.is_dormant


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


@app.route('/businesses/<int:business_id>', methods=['PUT'])
def update_business(business_id):
	request_data = json.loads(request.data)
	now_active = request_data['now_active']
	business = Business.query.get(business_id)
	if business.is_dormant and now_active:
		world.add_business(business)
	elif not business.is_dormant and now_active:
		world.peel_business(business)
	elif not business.is_dormant and not now_active:
		world.remove_business(business)
	business.is_dormant = not now_active if business.is_dormant == now_active else business.is_dormant


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
