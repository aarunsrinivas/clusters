from flaskapp import db
from collections import Counter
from datetime import datetime


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	session_id = db.Column(db.String(120), unique=True)
	features = db.Column(db.PickleType, nullable=False)
	cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
	type = db.Column(db.String(50))

	__mapper_args__ = {
		'polymorphic_identity': 'user',
		'polymorphic_on': type
	}


initial1 = db.Table('initial1',
                    db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                    db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

initial2 = db.Table('initial2',
                    db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                    db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

middle = db.Table('middle',
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
	applied = db.relationship('Business', secondary='initial1')
	received = db.relationship('Business', secondary='initial2')
	declined = db.relationship('Business', secondary='declined1')
	rejected = db.relationship('Business', secondary='declined2')
	interested = db.relationship('Business', secondary='middle')
	reviewed = db.relationship('Business', secondary='final')
	chats = db.relationship('Chat', backref='applicant', lazy=True, cascade='all, delete-orphan')

	__mapper_args__ = {
		'polymorphic_identity': 'applicant'
	}

	def __repr__(self):
		return f'Applicant(id: {self.id})'


class Business(User):
	__tablename__ = 'business'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	visited_clusters = db.relationship('Cluster', secondary='visited')
	reached = db.relationship('Applicant', secondary='initial2')
	received = db.relationship('Applicant', secondary='initial1')
	declined = db.relationship('Applicant', secondary='declined2')
	rejected = db.relationship('Applicant', secondary='declined1')
	interested = db.relationship('Applicant', secondary='middle')
	offered = db.relationship('Applicant', secondary='final')
	chats = db.relationship('Chat', backref='business', lazy=True, cascade='all, delete-orphan')

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
		'type': 'applicant',
		'major': [],
		'standing': [],
		'gpa': 0,
		'skills': []
	})
	applicant_centroid_data = db.Column(db.PickleType, default={
		'type': 'applicant',
		'major_dict': Counter(),
		'major_len_sum': 0,
		'standing_dict': Counter(),
		'standing_len_sum': 0,
		'gpa_sum': 0,
		'skills_dict': Counter(),
		'skills_len_sum': 0
	})
	business_centroid = db.Column(db.PickleType, default={
		'type': 'business',
		'major': [],
		'standing': [],
		'gpa': 0,
		'skills': []
	})
	business_centroid_data = db.Column(db.PickleType, default={
		'type': 'business',
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


class Chat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
	business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
	messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete')


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	origin = db.Column(db.String(50), nullable=False)
	message = db.Column(db.Text, nullable=False)
	# need to add default time
	date_posted = db.Column(db.DateTime, nullable=False)
	chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)


class Description(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	keyword = db.Column(db.String(20), nullable=False)
	description = db.Column(db.Text, nullable=False)
