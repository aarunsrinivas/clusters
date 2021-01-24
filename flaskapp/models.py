from flaskapp import db
from flaskapp.tasks import check, manage
from sqlalchemy.orm.collections import attribute_mapped_collection
from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import random
import numpy as np
from itertools import permutations


def compute_centroid(data_set):
	centroid = Centroid(ref_type=data_set[0].ref_type)
	centroid_data = centroid.centroid_data
	for data in data_set:
		centroid_data.add(data)
	centroid_data.update(len(data_set))
	return centroid


def find_clusters(data_set, n_clusters, max_iter=300, n_init=15):
	sse_lst = []
	labels_lst = []
	dual_centroids_lst = []
	applicant_data_set = []
	business_data_set = []
	couple_data_set = []
	for data in data_set:
		if type(data) == tuple:
			couple_data_set.append(data)
		elif data.ref_type == 'applicant':
			applicant_data_set.append(data)
		else:
			business_data_set.append(data)

	for _ in range(n_init):
		applicant_centers = random.sample(applicant_data_set, n_clusters) if len(
			applicant_data_set) >= n_clusters else None
		business_centers = random.sample(business_data_set, n_clusters) if len(
			business_data_set) >= n_clusters else None
		couple_centers = random.sample(couple_data_set, n_clusters) if len(
			couple_data_set) >= n_clusters else None
		if not (applicant_centers or business_centers or couple_centers):
			return
		elif applicant_centers and business_centers:
			distances = []
			for applicant_center in applicant_centers:
				d = []
				for business_center in business_centers:
					d.append(business_center.compare_diff(applicant_center))
				distances.append(d)
			perm = list(permutations([i for i in range(n_clusters)]))
			variance = []
			for p in perm:
				t = []
				for i in range(len(p)):
					t.append(distances[i][p[i]])
				variance.append(np.var(t))
			assignment = perm[np.argmin(variance)]
			dual_centroids = [(applicant_centers[i], business_centers[assignment[i]]) for i in range(n_clusters)]
		else:
			dual_centroids = [couple_centers[i] for i in range(n_clusters)]

		iteration = 0
		while iteration < max_iter:
			clusters = {i: {'applicant': [], 'business': []} for i in range(n_clusters)}
			labels = []
			sse = 0
			for data in data_set:
				d = []
				for dual_centroid in dual_centroids:
					applicant_centroid, business_centroid = dual_centroid
					if type(data) == tuple:
						applicant_data, business_data = data
						d.append(0.5 * (business_centroid.compare_diff(applicant_data)
						                + applicant_centroid.compare_same(applicant_data))
						         + 0.5 * (business_data.compare_diff(applicant_centroid)
						                  + business_centroid.compare_same(business_data)))
					else:
						if data.ref_type == 'applicant':
							d.append(business_centroid.compare_diff(data) + applicant_centroid.compare_same(data))
						else:
							d.append(data.compare_diff(applicant_centroid) + business_centroid.compare_same(data))
				index = np.argmin(d)
				sse += d[index] ** 2
				duplicates = [i for i in range(n_clusters) if d[i] == d[index]]
				if type(data) == tuple:
					index = min(duplicates,
					            key=lambda x: len(clusters[x]['applicant']) + len(clusters[x]['business']))
					applicant_data, business_data = data
					clusters[index]['applicant'].append(applicant_data)
					clusters[index]['business'].append(business_data)
					labels.append(index)
				else:
					index = min(duplicates, key=lambda x: len(clusters[x][data.ref_type]))
					clusters[index][data.ref_type].append(data)
					labels.append(index)
			new_dual_centroids = [(
				compute_centroid(clusters[i]['applicant']) if len(clusters[i]['applicant']) else
				dual_centroids[i][0],
				compute_centroid(clusters[i]['business']) if len(clusters[i]['business']) else
				dual_centroids[i][1]) for i in range(n_clusters)]
			has_converged = True
			for i in range(len(dual_centroids)):
				for j in range(len(dual_centroids[i])):
					if dual_centroids[i][j].compare_same(new_dual_centroids[i][j]) != 0:
						has_converged = False
				if not has_converged:
					break
			if has_converged:
				sse_lst.append(sse)
				labels_lst.append(labels)
				dual_centroids_lst.append(dual_centroids)
				break
			dual_centroids = new_dual_centroids
			iteration += 1

	return labels_lst[np.argmin(sse_lst)]


# user models

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	world_id = db.Column(db.String(50), db.ForeignKey('world.id'), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	session_id = db.Column(db.String(120), unique=True)
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

checkout = db.Table('checkout',
                    db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                    db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

declined1 = db.Table('declined1',
                     db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                     db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

declined2 = db.Table('declined2',
                     db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'), primary_key=True),
                     db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True))

visited_applicant_table = db.Table('visited_applicant_table',
                                   db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id'),
                                             primary_key=True),
                                   db.Column('cluster_id', db.Integer, db.ForeignKey('cluster.id'), primary_key=True))

visited_business_table = db.Table('visited_business_table',
                                  db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True),
                                  db.Column('cluster_id', db.Integer, db.ForeignKey('cluster.id'), primary_key=True))


class Applicant(User):
	__tablename__ = 'applicant'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
	cap = db.Column(db.Integer, default=1)
	visited_clusters = db.relationship('Cluster', collection_class=set, secondary='visited_applicant_table', lazy=True)
	applied = db.relationship('Business', collection_class=set, secondary='initial1', lazy=True)
	received = db.relationship('Business', collection_class=set, secondary='initial2', lazy=True)
	declined = db.relationship('Business', collection_class=set, secondary='declined1', lazy=True)
	rejected = db.relationship('Business', collection_class=set, secondary='declined2', lazy=True)
	interested = db.relationship('Business', collection_class=set, secondary='middle', lazy=True)
	reviewed = db.relationship('Business', collection_class=set, secondary='final', lazy=True)
	accepted = db.relationship('Business', collection_class=set, secondary='checkout', lazy=True)
	requests = db.relationship('Request', backref='applicant', lazy=True, cascade='all, delete-orphan')
	chats = db.relationship('Chat', backref='applicant', lazy=True, cascade='all, delete-orphan')
	features = db.relationship('ApplicantFeatures', backref='applicant', lazy=True, uselist=False,
	                           cascade='all, delete')

	__mapper_args__ = {
		'polymorphic_identity': 'applicant'
	}

	def __init__(self, **kwargs):
		super(Applicant, self).__init__(**kwargs)
		self.features = ApplicantFeatures()

	def __repr__(self):
		return f'Applicant(id: {self.id})'

	def set_world(self, world_id):
		if self.world_id == world_id:
			return
		self.cut_connections()
		self.world_id = world_id
		db.session.commit()

	def cut_connections(self):
		self.cap = 1
		self.applied.clear()
		self.received.clear()
		self.reviewed.clear()
		self.interested.clear()
		self.chats.clear()
		db.session.commit()


class Business(User):
	__tablename__ = 'business'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
	cap = db.Column(db.Integer, default=1)
	visited_clusters = db.relationship('Cluster', collection_class=set, secondary='visited_business_table', lazy=True)
	reached = db.relationship('Applicant', collection_class=set, secondary='initial2', lazy=True)
	received = db.relationship('Applicant', collection_class=set, secondary='initial1', lazy=True)
	declined = db.relationship('Applicant', collection_class=set, secondary='declined2', lazy=True)
	rejected = db.relationship('Applicant', collection_class=set, secondary='declined1', lazy=True)
	interested = db.relationship('Applicant', collection_class=set, secondary='middle', lazy=True)
	offered = db.relationship('Applicant', collection_class=set, secondary='final', lazy=True)
	accepted = db.relationship('Applicant', collection_class=set, secondary='checkout', lazy=True)
	requests = db.relationship('Request', backref='business', lazy=True, cascade='all, delete-orphan')
	chats = db.relationship('Chat', backref='business', lazy=True, cascade='all, delete-orphan')
	features = db.relationship('BusinessFeatures', backref='business', lazy=True, uselist=False,
	                           cascade='all, delete')

	__mapper_args__ = {
		'polymorphic_identity': 'business'
	}

	def __init__(self, **kwargs):
		super(Business, self).__init__(**kwargs)
		self.features = BusinessFeatures()

	def __repr__(self):
		return f'Business(id: {self.id})'

	def set_world(self, world_id):
		if self.world_id == world_id:
			return
		self.cut_connections()
		self.world_id = world_id
		db.session.commit()

	def cut_connections(self):
		self.cap = 1
		self.reached.clear()
		self.received.clear()
		self.offered.clear()
		self.interested.clear()
		self.chats.clear()
		db.session.commit()


# cluster models

class ClusterWorld(db.Model):
	__tablename__ = 'world'
	id = db.Column(db.String(50), primary_key=True)
	applicants = db.relationship('Applicant', backref='world', lazy=True, cascade='all, delete')
	businesses = db.relationship('Business', backref='world', lazy=True, cascade='all, delete')
	clusters = db.relationship('Cluster', backref='world', foreign_keys='Cluster.world_id', lazy=True,
	                           cascade='all, delete')
	top = db.relationship('Cluster', foreign_keys='Cluster.top_id', lazy=True)
	bottom = db.relationship('Cluster', foreign_keys='Cluster.bottom_id', lazy=True)

	def __init__(self, **kwargs):
		super(ClusterWorld, self).__init__(**kwargs)
		self.clusters.append(Cluster())
		db.session.commit()
		'''
		scheduler.schedule(
			scheduled_time=datetime.utcnow(),
			func=None,
			args=[self],
			interval=(60 * 30),
			repeat=None
		)
		'''

	@hybrid_property
	def inactivity(self):
		return db.session.query(func.max(Cluster.inactivity)).filter(Cluster.world_id == self.id).scalar()

	@hybrid_property
	def size(self):
		return db.session.query(func.max(Cluster.size)).filter(Cluster.world_id == self.id).scalar()

	@hybrid_property
	def ratio(self):
		return db.session.query(func.max(Cluster.ratio)).filter(Cluster.world_id == self.id).scalar()

	def closest_cluster(self, data_set, visited_clusters=None):
		diffs = []
		for cluster in self.clusters:
			d = 0
			for data in data_set:
				if data.ref_type == 'applicant':
					d += cluster.business_centroid.compare_diff(data) + cluster.applicant_centroid.compare_same(data)
				else:
					d += data.compare_diff(cluster.applicant_centroid) + cluster.business_centroid.compare_same(data)
			diffs.append(d)
		return self.clusters[np.argmin(diffs)]

	def add(self, user):
		cluster = self.closest_cluster([user.features], self.clusters)
		cluster.inflate(user)
		user.visited_clusters.add(cluster)
		db.session.commit()

	def peel(self, user):
		if not user.cluster_id:
			return
		if len(self.clusters) == len(user.visited_clusters):
			user.visited_clusters = {user.cluster}
			db.session.commit()
		old_cluster = user.cluster
		old_cluster.deflate(user)
		user.cut_connections()
		new_cluster = self.closest_cluster([user.features], self.clusters, user.visited_clusters)
		new_cluster.inflate(user)
		user.visited_clusters.add(new_cluster)
		db.session.commit()

	def remove(self, user):
		if not user.cluster_id:
			return
		cluster = user.cluster
		cluster.deflate(user)
		user.cut_connections()
		db.session.commit()

	def merge(self, solute_cluster):
		solvent_cluster = self.closest_cluster([solute_cluster.applicant_centroid, solute_cluster.business_centroid],
		                                       self.clusters, visited_clusters={solute_cluster})
		data_set = solute_cluster.applicants + solute_cluster.businesses
		for data in data_set:
			solvent_cluster.inflate(data)
		db.session.delete(solute_cluster)
		db.session.commit()

	def split(self, cluster):
		graph = dict()
		visited = set()
		for applicant in cluster.applicants:
			graph[applicant] = applicant.applied + applicant.received + applicant.interested + applicant.reviewed
		for business in cluster.businesses:
			graph[business] = business.reached + business.received + business.interested + business.offered

		def explore(vertex, component):
			component.append(vertex)
			visited.add(vertex)
			for adj_vertex in graph[vertex]:
				if adj_vertex not in visited:
					explore(adj_vertex, component)

		components = []
		for vertex in graph:
			component = []
			if vertex not in visited:
				explore(vertex, component)
			if component:
				components.append(component)
		if len(components) == 1:
			return

		data_set = []
		for component in components:
			applicant_features = []
			business_features = []
			for user in component:
				if user.type == 'applicant':
					applicant_features.append(user.features)
				else:
					business_features.append(user.features)
			if applicant_features and business_features:
				data_set.append(compute_centroid(applicant_features), compute_centroid(business_features))
			elif applicant_features:
				data_set.append(compute_centroid(applicant_features))
			elif business_features:
				data_set.append(compute_centroid(business_features))

		labels = find_clusters(data_set, 2)
		new_cluster = Cluster(world=self)
		db.session.add(new_cluster)
		db.session.commit()
		for i in range(len(components)):
			if labels[i] == 0:
				continue
			for user in components[i]:
				cluster.deflate(user)
				new_cluster.inflate(user)
				db.session.commit()


class Cluster(db.Model):
	__tablename__ = 'cluster'
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.DateTime, default=datetime.utcnow)
	applicant_centroid = db.relationship('ApplicantCentroid', backref='cluster',
	                                     lazy=True, uselist=False, cascade='all, delete')
	business_centroid = db.relationship('BusinessCentroid', backref='cluster', lazy=True,
	                                    uselist=False, cascade='all, delete')
	world_id = db.Column(db.String(50), db.ForeignKey('world.id'), nullable=False)
	top_id = db.Column(db.String(50), db.ForeignKey('world.id'))
	bottom_id = db.Column(db.String(50), db.ForeignKey('world.id'))
	applicants = db.relationship('Applicant', backref='cluster', lazy=True)
	businesses = db.relationship('Business', backref='cluster', lazy=True)

	@hybrid_property
	def inactivity(self):
		return (datetime.utcnow() - self.time) / timedelta(minutes=1)

	@hybrid_property
	def applicant_pop(self):
		return len(self.applicants)

	@hybrid_property
	def business_pop(self):
		return len(self.businesses)

	@hybrid_property
	def ratio(self):
		return self.applicant_pop / self.business_pop

	@hybrid_property
	def pop(self):
		return self.applicant_pop + self.business_pop

	@hybrid_property
	def top_index(self):
		return self.pop / self.world.pop + self.ratio / self.world.ratio + self.inactivity / self.world.inactivity

	@hybrid_property
	def bottom_index(self):
		return self.pop / self.world.pop + self.ratio / self.world.ratio + (1 - self.inactivity / self.world.inactivity)

	def __init__(self, **kwargs):
		super(Cluster, self).__init__(**kwargs)
		self.applicant_centroid = ApplicantCentroid()
		self.business_centroid = BusinessCentroid()
		db.session.commit()
		'''
		scheduler.schedule(
			scheduled_time=datetime.utcnow(),
			func=check,
			args=[self],
			interval=(60 * 30),
			repeat=None
		)
		'''

	def __repr__(self):
		return f'Cluster(id: {self.id}, applicant_pop: {self.applicant_pop}, business_pop: {self.business_pop})'

	def inflate(self, data):
		data.cluster_id = self.id
		centroid = self.applicant_centroid if data.type == 'applicant' else self.business_centroid
		centroid_data = centroid.centroid_data
		centroid_data.add(data.features)
		centroid.update()
		db.session.commit()

	def deflate(self, data):
		data.cluster_id = None
		centroid = self.applicant_centroid if data.type == 'applicant' else self.business_centroid
		centroid_data = centroid.centroid_data
		centroid_data.remove(data.features)
		centroid.update()
		db.session.commit()


# features/centroid models

major_table = db.Table('major_table',
                       db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                       db.Column('major_id', db.String(50), db.ForeignKey('major.id'), primary_key=True))

skill_table = db.Table('skill_table',
                       db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                       db.Column('skill_id', db.String(50), db.ForeignKey('skill.id'), primary_key=True))

interest_table = db.Table('interest_table',
                          db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                          db.Column('interest_id', db.String(50), db.ForeignKey('interest.id'), primary_key=True))

course_table = db.Table('course_table',
                        db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                        db.Column('course_id', db.String(50), db.ForeignKey('course.id'), primary_key=True))

standing_table = db.Table('standing_table',
                          db.Column('data_id', db.Integer, db.ForeignKey('data.id'), primary_key=True),
                          db.Column('standing_id', db.String(50), db.ForeignKey('standing.id'), primary_key=True))


class Data(db.Model):
	__tablename__ = 'data'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(30), nullable=False)
	ref_type = db.Column(db.String(30))
	gpa = db.Column(db.Integer, default=0)
	majors = db.relationship('Major', collection_class=set, secondary='major_table')
	standings = db.relationship('Standing', collection_class=set, secondary='standing_table')
	skills = db.relationship('Skill', collection_class=set, secondary='skill_table')
	interests = db.relationship('Interest', collection_class=set, secondary='interest_table')
	courses = db.relationship('Course', collection_class=set, secondary='course_table')

	__mapper_args__ = {
		'polymorphic_identity': 'data',
		'polymorphic_on': type
	}

	def __eq__(self, other):
		return self.gpa == other.gpa and self.majors == other.majors and self.standings == other.standings \
		       and self.skills == other.skills and self.interests == other.interests and self.courses == other.courses

	def compare_diff(self, other):
		zero = Data(gpa=0)
		if self == zero or self == other:
			return 0
		major_diff = 1
		for first_major in self.majors:
			if first_major in other.majors:
				major_diff = 0
				break
		standing_diff = 1
		for first_standing in self.standings:
			if first_standing in other.standings:
				standing_diff = 0
				break
		gpa_diff = 0 if other.gpa >= self.gpa else 1
		skill_diff = len(self.skills)
		for first_skill in self.skills:
			if first_skill in other.skills:
				skill_diff -= 1
		skill_diff /= len(self.skills)
		interest_diff = len(self.interests)
		for first_interest in self.interests:
			if first_interest in other.interests:
				interest_diff -= 1
		interest_diff /= len(self.interests)
		course_diff = len(self.courses)
		for first_course in self.courses:
			if first_course in other.courses:
				course_diff -= 1
		course_diff /= len(self.courses)
		diff = (major_diff ** 2 + standing_diff ** 2 + gpa_diff ** 2 + skill_diff ** 2 +
		        interest_diff ** 2 + course_diff ** 2) ** (1 / 2)
		return diff

	def compare_same(self, other):
		zero = Data(gpa=0)
		if self == zero or self == other:
			return 0
		major_diff = len(self.majors)
		for first_major in self.majors:
			if first_major in other.majors:
				major_diff -= 1
		major_diff /= len(self.majors)
		standing_diff = len(self.standings)
		for first_standing in self.standings:
			if first_standing in other.standings:
				standing_diff -= 1
		standing_diff /= len(self.standings)
		gpa_diff = self.gpa - other.gpa
		gpa_diff /= 4
		skill_diff = len(self.skills)
		for first_skill in self.skills:
			if first_skill in other.skills:
				skill_diff -= 1
		skill_diff /= len(self.skills)
		interest_diff = len(self.interests)
		for first_interest in self.interests:
			if first_interest in other.interests:
				interest_diff -= 1
		interest_diff /= len(self.interests)
		course_diff = len(self.courses)
		for first_course in self.courses:
			if first_course in other.courses:
				course_diff -= 1
		course_diff /= len(self.courses)
		diff = (major_diff ** 2 + standing_diff ** 2 + gpa_diff ** 2 + skill_diff ** 2 +
		        interest_diff ** 2 + course_diff ** 2) ** (1 / 2)
		return diff


class Features(Data):
	__tablename__ = 'features'
	id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'features'
	}

	@hybrid_property
	def serialized(self):
		return {
			'refType': self.ref_type,
			'gpa': self.gpa,
			'majors': [major.id for major in self.majors],
			'standings': [standing.id for standing in self.standings],
			'skills': [skill.id for skill in self.skills],
			'interests': [interest.id for interest in self.interests],
			'courses': [course.id for course in self.courses]
		}


class ApplicantFeatures(Features):
	__tablename__ = 'applicant_features'

	__mapper_args__ = {
		'polymorphic_identity': 'applicant_features'
	}

	def __init__(self, **kwargs):
		super(ApplicantFeatures, self).__init__(**kwargs)
		self.ref_type = 'applicant'


class BusinessFeatures(Features):
	__tablename__ = 'business_features'

	__mapper_args__ = {
		'polymorphic_identity': 'business_features'
	}

	def __init__(self, **kwargs):
		super(BusinessFeatures, self).__init__(**kwargs)
		self.ref_type = 'business'


class Centroid(Data):
	__tablename__ = 'centroid'
	id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
	centroid_data = db.relationship('CentroidData', backref='centroid', lazy=True, uselist=False, cascade='all, delete')
	cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))

	__mapper_args__ = {
		'polymorphic_identity': 'centroid'
	}

	def __init__(self, **kwargs):
		super(Centroid, self).__init__(**kwargs)
		self.centroid_data = CentroidData()
		db.session.commit()

	def generic_update(self, divisor):
		divisor = divisor if divisor else 1
		self.majors = set(sorted(self.centroid_data.major_counters.keys(),
		                         key=lambda x: self.centroid_data.major_counters[x].count,
		                         reverse=True)[
		                  0: round(self.centroid_data.major_lengths / divisor)])
		self.standings = set(sorted(self.centroid_data.standing_counters.keys(),
		                            key=lambda x: self.centroid_data.standing_counters[x].count,
		                            reverse=True)[
		                     0: round(self.centroid_data.standing_lengths / divisor)])
		self.skills = set(sorted(self.centroid_data.skill_counters.keys(),
		                         key=lambda x: self.centroid_data.skill_counters[x].count,
		                         reverse=True)[
		                  0: round(self.centroid_data.skill_lengths / divisor)])
		self.interests = set(sorted(self.centroid_data.interest_counters.keys(),
		                            key=lambda x: self.centroid_data.interest_counters[x].count,
		                            reverse=True)[
		                     0: round(self.centroid_data.interest_lengths / divisor)])
		self.courses = set(sorted(self.centroid_data.course_counters.keys(),
		                          key=lambda x: self.centroid_data.course_counters[x].count,
		                          reverse=True)[
		                   0: round(self.centroid_data.course_lengths / divisor)])
		self.gpa = round(self.centroid_data.gpa_total / divisor, 2)
		db.session.commit()


class ApplicantCentroid(Centroid):
	__tablename__ = 'applicant_centroid'
	id = db.Column(db.Integer, db.ForeignKey('centroid.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity': 'applicant_centroid'
	}

	def __init__(self, **kwargs):
		super(ApplicantCentroid, self).__init__(**kwargs)
		self.ref_type = 'applicant'
		self.centroid_data = ApplicantCentroidData()
		db.session.commit()

	def update(self):
		super(ApplicantCentroid, self).generic_update(self.cluster.applicant_pop)


class BusinessCentroid(Centroid):
	__tablename__ = 'business_centroid'
	id = db.Column(db.Integer, db.ForeignKey('centroid.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity': 'business_centroid'
	}

	def __init__(self, **kwargs):
		super(BusinessCentroid, self).__init__(**kwargs)
		self.ref_type = 'business'
		self.centroid_data = BusinessCentroidData()
		db.session.commit()

	def update(self):
		super(BusinessCentroid, self).generic_update(self.cluster.business_pop)


class CentroidData(db.Model):
	__tablename__ = 'centroid_data'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(50))
	ref_type = db.Column(db.String(50))
	major_counters = db.relationship('MajorCounter', backref='centroid_data',
	                                 collection_class=attribute_mapped_collection('major'), lazy=True,
	                                 cascade='all, delete-orphan')
	major_lengths = db.Column(db.Integer, default=0)
	standing_counters = db.relationship('StandingCounter', backref='centroid_data',
	                                    collection_class=attribute_mapped_collection('standing'), lazy=True,
	                                    cascade='all, delete-orphan')
	standing_lengths = db.Column(db.Integer, default=0)
	skill_counters = db.relationship('SkillCounter', backref='centroid_data',
	                                 collection_class=attribute_mapped_collection('skill'), lazy=True,
	                                 cascade='all, delete-orphan')
	skill_lengths = db.Column(db.Integer, default=0)
	interest_counters = db.relationship('InterestCounter', backref='centroid_data',
	                                    collection_class=attribute_mapped_collection('interest'), lazy=True,
	                                    cascade='all, delete-orphan')
	interest_lengths = db.Column(db.Integer, default=0)
	course_counters = db.relationship('CourseCounter', backref='centroid_data',
	                                  collection_class=attribute_mapped_collection('course'), lazy=True,
	                                  cascade='all, delete-orphan')
	course_lengths = db.Column(db.Integer, default=0)
	gpa_total = db.Column(db.Integer, default=0)
	centroid_id = db.Column(db.Integer, db.ForeignKey('centroid.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'centroid_data',
		'polymorphic_on': type
	}

	def add(self, other):
		for major in other.majors:
			if major in self.major_counters:
				self.major_counters[major].count += 1
			else:
				self.major_counters[major] = MajorCounter(major=major)
		self.major_lengths += len(other.majors)
		for skill in other.skills:
			if skill in self.skill_counters:
				self.skill_counters[skill].count += 1
			else:
				self.skill_counters[skill] = SkillCounter(skill=skill)
		self.skill_lengths += len(other.skills)
		for standing in other.standings:
			if standing in self.standing_counters:
				self.standing_counters[standing].count += 1
			else:
				self.standing_counters[standing] = StandingCounter(standing=standing)
		self.standing_lengths += len(other.standings)
		for course in other.courses:
			if course in self.course_counters:
				self.course_counters[course].count += 1
			else:
				self.course_counters[course] = CourseCounter(course=course)
		self.course_lengths += len(other.courses)
		for interest in other.interests:
			if interest in self.interest_counters:
				self.interest_counters[interest].count += 1
			else:
				self.interest_counters[interest] = InterestCounter(interest=interest)
		self.interest_lengths += len(other.interests)
		self.gpa_total += other.gpa
		db.session.commit()

	def remove(self, other):
		for major in other.majors:
			if major in self.major_counters.keys():
				self.major_counters[major].count -= 1
		self.major_lengths -= len(other.majors)
		for standing in other.standings:
			if standing in self.standing_counters.keys():
				self.standing_counters[standing].count -= 1
		self.standing_lengths -= len(other.standings)
		for skill in other.skills:
			if skill in self.skill_counters.keys():
				self.skill_counters[skill].count -= 1
		self.skill_lengths -= len(other.skills)
		for course in other.courses:
			if course in self.course_counters.keys():
				self.course_counters[course].count -= 1
		self.course_lengths -= len(other.courses)
		for interest in other.interests:
			if interest in self.interest_counters.keys():
				self.interest_counters[interest].count -= 1
		self.interest_lengths -= len(other.interests)
		self.gpa_total -= other.gpa
		db.session.commit()


class ApplicantCentroidData(CentroidData):
	__tablename__ = 'applicant_centroid_data'
	id = db.Column(db.Integer, db.ForeignKey('centroid_data.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity': 'applicant_centroid_data'
	}

	def __init__(self, **kwargs):
		super(ApplicantCentroidData, self).__init__(**kwargs)
		self.ref_type = 'applicant'


class BusinessCentroidData(CentroidData):
	__tablename__ = 'business_centroid_data'
	id = db.Column(db.Integer, db.ForeignKey('centroid_data.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity': 'business_centroid_data'
	}

	def __init__(self, **kwargs):
		super(BusinessCentroidData, self).__init__(**kwargs)
		self.ref_type = 'business'


class Counter(db.Model):
	__tablename__ = 'counter'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(50))
	count = db.Column(db.Integer, default=1)
	centroid_data_id = db.Column(db.Integer, db.ForeignKey('centroid_data.id'))

	__mapper_args__ = {
		'polymorphic_identity': 'counter',
		'polymorphic_on': type
	}


class MajorCounter(Counter):
	__tablename__ = 'major_counter'
	id = db.Column(db.Integer, db.ForeignKey('counter.id'), primary_key=True)
	major_id = db.Column(db.String(50), db.ForeignKey('major.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'major_counter'
	}


class CourseCounter(Counter):
	__tablename__ = 'course_counter'
	id = db.Column(db.Integer, db.ForeignKey('counter.id'), primary_key=True)
	course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'course_counter'
	}


class StandingCounter(Counter):
	__tablename__ = 'standing_counter'
	id = db.Column(db.Integer, db.ForeignKey('counter.id'), primary_key=True)
	standing_id = db.Column(db.String(50), db.ForeignKey('standing.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'standing_counter'
	}


class InterestCounter(Counter):
	__tablename__ = 'interest_counter'
	id = db.Column(db.Integer, db.ForeignKey('counter.id'), primary_key=True)
	interest_id = db.Column(db.String(50), db.ForeignKey('interest.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'interest_counter'
	}


class SkillCounter(Counter):
	__tablename__ = 'skill_counter'
	id = db.Column(db.Integer, db.ForeignKey('counter.id'), primary_key=True)
	skill_id = db.Column(db.String(50), db.ForeignKey('skill.id'), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity': 'skill_counter'
	}


class Characteristic(db.Model):
	__tablename__ = 'characteristic'
	id = db.Column(db.String(50), primary_key=True)
	type = db.Column(db.String(50))

	__mapper_args__ = {
		'polymorphic_identity': 'characteristic',
		'polymorphic_on': type
	}


class Major(Characteristic):
	__tablename__ = 'major'
	id = db.Column(db.String(50), db.ForeignKey('characteristic.id'), primary_key=True)
	data = db.relationship('Data', secondary='major_table')
	major_counters = db.relationship('MajorCounter', lazy=True, backref='major')

	__mapper_args__ = {
		'polymorphic_identity': 'major'
	}


class Course(Characteristic):
	__tablename__ = 'course'
	id = db.Column(db.String(50), db.ForeignKey('characteristic.id'), primary_key=True)
	data = db.relationship('Data', secondary='course_table')
	course_counters = db.relationship('CourseCounter', lazy=True, backref='course')
	description = db.Column(db.Text)

	__mapper_args__ = {
		'polymorphic_identity': 'course'
	}


class Standing(Characteristic):
	__tablename__ = 'standing'
	id = db.Column(db.String(50), db.ForeignKey('characteristic.id'), primary_key=True)
	data = db.relationship('Data', secondary='standing_table')
	standing_counters = db.relationship('StandingCounter', lazy=True, backref='standing')

	__mapper_args__ = {
		'polymorphic_identity': 'standing'
	}


class Interest(Characteristic):
	__tablename__ = 'interest'
	id = db.Column(db.String(50), db.ForeignKey('characteristic.id'), primary_key=True)
	data = db.relationship('Data', secondary='interest_table')
	interest_counters = db.relationship('InterestCounter', lazy=True, backref='interest')
	description = db.Column(db.Text)

	__mapper_args__ = {
		'polymorphic_identity': 'interest'
	}


class Skill(Characteristic):
	__tablename__ = 'skill'
	id = db.Column(db.String(50), db.ForeignKey('characteristic.id'), primary_key=True)
	data = db.relationship('Data', secondary='skill_table')
	skill_counters = db.relationship('SkillCounter', lazy=True, backref='skill')
	description = db.Column(db.Text)

	__mapper_args__ = {
		'polymorphic_identity': 'skill'
	}


# communication models

class Request(db.Model):
	__tablename__ = 'request'
	id = db.Column(db.Integer, primary_key=True)
	sender = db.Column(db.String(50), nullable=False)
	applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
	business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
	text = db.Column(db.Text, nullable=False)


class Chat(db.Model):
	__tablename__ = 'chat'
	id = db.Column(db.Integer, primary_key=True)
	applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
	business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
	messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete')


class Message(db.Model):
	__tablename__ = 'message'
	id = db.Column(db.Integer, primary_key=True)
	origin = db.Column(db.Integer, nullable=False)
	message = db.Column(db.Text, nullable=False)
	# need to add default time
	# date_posted = db.Column(db.DateTime, nullable=False)
	chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
