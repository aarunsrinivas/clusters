from flaskapp import db, login_manager
from flask_login import UserMixin
from collections import Counter


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	features = db.Column(db.PickleType, nullable=False)
	cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
	type = db.Column(db.String(50))

	__mapper_args__ = {
		'polymorphic_identity': 'user',
		'polymorphic_on': type
	}


initial = db.Table('initial',
                   db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                   db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

final = db.Table('final',
                 db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                 db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

declined1 = db.Table('declined1',
                     db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                     db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

declined2 = db.Table('declined2',
                     db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                     db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

visited = db.Table('visited',
                   db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True,
                             nullable=True),
                   db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True, nullable=True),
                   db.Column('cluster_id', db.Integer, db.ForeignKey('cluster.id'), primary_key=True))


class Applicant(User):
	__tablename__ = 'applicant'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	visited_clusters = db.relationship('Cluster', secondary='visited')
	applied = db.relationship('Business', secondary='initial')
	declined = db.relationship('Business', secondary='declined1')
	rejected = db.relationship('Business', secondary='declined2')
	reviewed = db.relationship('Business', secondary='final')

	__mapper_args__ = {
		'polymorphic_identity': 'applicant'
	}

	def __repr__(self):
		return f'Applicant(id: {self.id})'


class Business(User):
	__tablename__ = 'business'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	visited_clusters = db.relationship('Cluster', secondary='visited')
	received = db.relationship('Applicant', secondary='initial')
	declined = db.relationship('Applicant', secondary='declined2')
	rejected = db.relationship('Applicant', secondary='declined1')
	offered = db.relationship('Applicant', secondary='final')

	__mapper_args__ = {
		'polymorphic_identity': 'business'
	}

	def __repr__(self):
		return f'Business(id: {self.id})'


class Cluster(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	applicant_pop = db.Column(db.Integer, default=0)
	business_pop = db.Column(db.Integer, default=0)
	size = db.column_property(applicant_pop + business_pop)
	applicant_centroid = db.Column(db.PickleType, default={
		'type': Applicant.type,
		'major': [],
		'standing': [],
		'gpa': 0,
		'skills': []
	})
	applicant_centroid_data = db.Column(db.PickleType, default={
		'type': Applicant.type,
		'major_dict': Counter(),
		'major_len_sum': 0,
		'standing_dict': Counter(),
		'standing_len_sum': 0,
		'gpa_sum': 0,
		'skills_dict': Counter(),
		'skills_len_sum': 0
	})
	business_centroid = db.Column(db.PickleType, default={
		'type': Business.type,
		'major': [],
		'standing': [],
		'gpa': 0,
		'skills': []
	})
	business_centroid_data = db.Column(db.PickleType, default={
		'type': Business.type,
		'major_dict': Counter(),
		'major_len_sum': 0,
		'standing_dict': Counter(),
		'standing_len_sum': 0,
		'gpa_sum': 0,
		'skills_dict': Counter(),
		'skills_len_sum': 0
	})
	applicants = db.relationship('Applicant', backref='cluster', lazy=True)
	businesses = db.relationship('Business', backref='cluster', lazy=True)

	def __repr__(self):
		return f'Cluster(id: {self.id}, applicant_pop: {self.applicant_pop}, business_pop: {self.business_pop})'
