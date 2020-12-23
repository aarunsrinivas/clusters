from flaskapp import app, db, bcrypt


@app.route('/applicants', methods=['POST'])
def applicants():
	pass


@app.route('/applicants/<int:applicant_id>', methods=['GET', 'PUT'])
def applicant(applicant_id):
	pass


@app.route('/businesses', methods=['POST'])
def businesses():
	pass


@app.route('/businesses/<int:business_id>', methods=['GET', 'PUT'])
def business(business_id):
	pass


@app.route('/clusters/<int:cluster_id>', methods=['GET'])
def cluster(cluster_id):
	pass


@app.route('clusters/<int:cluster_id>/applicants', methods=['GET'])
def active_applicants(cluster_id):
	pass


@app.route('clusters/<int:cluster_id>/businesses', methods=['GET'])
def active_businesses(cluster_id):
	pass
