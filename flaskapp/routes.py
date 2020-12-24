from flaskapp import app, db, bcrypt
from flaskapp.models import Applicant, Business, Cluster
from flask import json, jsonify, request


@app.route('/applicants', methods=['POST'])
def applicants():
	request_data = json.loads(request.data)
	applicant = Applicant(name=request_data['name'], email=request_data['email'],
	                      password=bcrypt.generate_password_hash(request_data['password']),
	                      features=request_data['features'])
	db.session.add(applicant)
	db.session.commit()
	return {'201': 'Applicant Created Successfully'}


def applicant_serializer(applicant):
	return {
		'id': applicant.id,
		'name': applicant.name,
		'email': applicant.email,
		'features': applicant.features,
		'cluster_id': applicant.cluster_id,
		'applied': [business.id for business in applicant.applied],
		'rejected': [business.id for business in applicant.rejected],
		'reviewed': [business.id for business in applicant.reviewed]
	}


@app.route('/applicants/<int:applicant_id>', methods=['GET', 'PUT'])
def applicant(applicant_id):
	return jsonify(list(map(applicant_serializer, Applicant.query.filter_by(id=applicant_id))))


@app.route('/businesses', methods=['POST'])
def businesses():
	request_data = json.loads(request.data)
	business = Business(name=request_data['name'], email=request_data['email'],
	                    password=bcrypt.generate_password_hash(request_data['password']),
	                    features=request_data['features'])
	db.session.add(business)
	db.session.commit()
	return {'201': 'Business Created Successfully'}


def business_serializer(business):
	return {
		'id': business.id,
		'name': business.name,
		'email': business.email,
		'features': business.features,
		'cluster_id': business.cluster_id,
		'applied': [applicant.id for applicant in business.received],
		'rejected': [applicant.id for applicant in business.rejected],
		'reviewed': [applicant.id for applicant in business.offered]
	}


@app.route('/businesses/<int:business_id>', methods=['GET', 'PUT'])
def business(business_id):
	return jsonify(list(map(business_serializer, Business.query.filter_by(id=business_id))))


def cluster_serializer(cluster):
	return {
		'id': cluster.id,
		'applicant_pop': cluster.applicant_pop,
		'business_pop': cluster.business_pop,
		'size': cluster.size
	}


@app.route('/clusters/<int:cluster_id>', methods=['GET'])
def cluster(cluster_id):
	return jsonify(list(map(cluster_serializer, Cluster.query.filter_by(id=cluster_id))))


@app.route('clusters/<int:cluster_id>/applicants', methods=['GET'])
def active_applicants(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(applicant_serializer, cluster.applicants)))


@app.route('clusters/<int:cluster_id>/businesses', methods=['GET'])
def active_businesses(cluster_id):
	cluster = Cluster.query.get(cluster_id)
	return jsonify(list(map(business_serializer, cluster.businesses)))
