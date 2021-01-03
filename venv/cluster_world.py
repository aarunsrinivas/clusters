from flaskapp import db
from flaskapp.models import Cluster, Applicant
import cluster_algorithms as alg


def add_applicant(applicant):
	clusters = Cluster.query.all()
	if not clusters:
		cluster = Cluster()
		db.session.add(cluster)
		db.session.commit()
		cluster_id = cluster.id
	else:
		dual_centroids = []
		ids = []
		for cluster in clusters:
			dual_centroids.append((cluster.applicant_centroid, cluster.business_centroid))
			ids.append(cluster.id)
		cluster_id = alg.closest_cluster([applicant.features], dual_centroids, ids)
		cluster = Cluster.query.get(cluster_id)
	applicant.cluster_id = cluster_id
	applicant.visited_clusters.append(cluster)
	cluster.applicant_centroid, cluster.applicant_centroid_data = alg.inflate_centroid(
		cluster.applicant_centroid_data, applicant.features, cluster.applicant_pop)
	cluster.applicant_pop += 1
	db.session.commit()


def add_business(business):
	clusters = Cluster.query.all()
	if not clusters:
		cluster = Cluster()
		db.session.add(cluster)
		db.session.commit()
		cluster_id = cluster.id
	else:
		dual_centroids = []
		ids = []
		for cluster in clusters:
			dual_centroids.append((cluster.applicant_centroid, cluster.business_centroid))
			ids.append(cluster.id)
		cluster_id = alg.closest_cluster([business.features], dual_centroids, ids)
		cluster = Cluster.query.get(cluster_id)
	business.cluster_id = cluster_id
	business.visited_clusters.append(cluster)
	cluster.business_centroid, cluster.business_centroid_data = alg.inflate_centroid(
		cluster.business_centroid_data, business.features, cluster.business_pop)
	cluster.business_pop += 1
	db.session.commit()


def peel_applicant(applicant):
	if not applicant.cluster_id:
		return
	clusters = Cluster.query.all()
	if len(clusters) == len(applicant.visited_clusters):
		return
	old_cluster = applicant.cluster
	old_cluster.applicant_centroid, old_cluster.applicant_centroid_data = alg.deflate_centroid(
		old_cluster.applicant_centroid_data, applicant.features, old_cluster.applicant_pop)
	old_cluster.applicant_pop -= 1
	applicant.applied.clear()
	applicant.reviewed.clear()
	applicant.interested.clear()
	applicant.chats.clear()
	dual_centroids = []
	ids = []
	for cluster in clusters:
		if cluster in applicant.visited_clusters:
			continue
		dual_centroids.append((cluster.applicant_centroid, cluster.business_centroid))
		ids.append(cluster.id)
	new_cluster_id = alg.closest_cluster([applicant.features], dual_centroids, ids)
	new_cluster = Cluster.query.get(new_cluster_id)
	applicant.cluster_id = new_cluster.id
	applicant.visited_clusters.append(new_cluster)
	new_cluster.applicant_centroid, new_cluster.applicant_centroid_data = alg.inflate_centroid(
		new_cluster.applicant_centroid_data, applicant.features, new_cluster.applicant_pop)
	new_cluster.applicant_pop += 1
	db.session.commit()


def peel_business(business):
	if not business.cluster_id:
		return
	clusters = Cluster.query.all()
	if len(clusters) == len(business.visited_clusters):
		return
	old_cluster = business.cluster
	old_cluster.business_centroid, old_cluster.business_centroid_data = alg.deflate_centroid(
		old_cluster.business_centroid_data, business.features, old_cluster.business_pop)
	old_cluster.business_pop -= 1
	business.received.clear()
	business.offered.clear()
	business.interested.clear()
	business.chats.clear()
	dual_centroids = []
	ids = []
	for cluster in clusters:
		if cluster in business.visited_clusters:
			continue
		dual_centroids.append((cluster.applicant_centroid, cluster.business_centroid))
		ids.append(cluster.id)
	new_cluster_id = alg.closest_cluster([business.features], dual_centroids, ids)
	new_cluster = Cluster.query.get(new_cluster_id)
	business.cluster_id = new_cluster.id
	business.visited_clusters.append(new_cluster)
	new_cluster.business_centroid, new_cluster.business_centroid_data = alg.inflate_centroid(
		new_cluster.business_centroid_data, business.features, new_cluster.business_pop)
	new_cluster.business_pop += 1
	db.session.commit()


def remove_applicant(applicant):
	if not applicant.cluster_id:
		return
	cluster = applicant.cluster
	applicant.cluster_id = None
	cluster.applicant_centroid, cluster.applicant_centroid_data = alg.deflate_centroid(
		cluster.applicant_centroid_data, applicant.features, cluster.applicant_pop)
	cluster.applicant_pop -= 1
	applicant.applied.clear()
	applicant.reviewed.clear()
	applicant.interested.clear()
	applicant.chats.clear()
	applicant.visited_clusters.clear()
	db.session.commit()


def remove_business(business):
	if not business.cluster_id:
		return
	cluster = business.cluster
	business.cluster_id = None
	cluster.business_centroid, cluster.business_centroid_data = alg.deflate_centroid(
		cluster.business_centroid_data, business.features, cluster.business_pop)
	cluster.business_pop -= 1
	business.received.clear()
	business.offered.clear()
	business.interested.clear()
	business.chats.clear()
	business.visited_clusters.clear()
	db.session.commit()


def split_cluster(cluster):
	graph = dict()
	visited = set()
	for applicant in cluster.applicants:
		graph[applicant] = applicant.applied + applicant.reviewed
	for business in cluster.businesses:
		graph[business] = business.received + business.offered

	def explore(vertex, component):
		component.append(vertex)
		visited.add(vertex)
		for adj_vertex in graph[vertex]:
			if adj_vertex not in visited:
				explore(adj_vertex, component)

	components = []
	for vertex in graph.keys():
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
			if isinstance(user, Applicant):
				applicant_features.append(user.features)
			else:
				business_features.append(user.features)
		if applicant_features and business_features:
			data_set.append((alg.compute_centroid(applicant_features, 'applicant')[0],
			                 alg.compute_centroid(business_features, 'business')[0]))
		elif applicant_features:
			data_set.append(alg.compute_centroid(applicant_features, 'applicant')[0])
		elif business_features:
			data_set.append(alg.compute_centroid(business_features, 'business')[0])

	labels, _, _ = alg.find_clusters(data_set, 2)
	new_cluster = Cluster()
	db.session.add(new_cluster)
	db.session.commit()

	for i in range(len(components)):
		if labels[i] == 0:
			continue
		for user in components[i]:
			user.cluster_id = new_cluster.id
			if isinstance(user, Applicant):
				cluster.applicant_centroid, cluster.applicant_centroid_data = alg.deflate_centroid(
					cluster.applicant_centroid_data, user.features, cluster.applicant_pop)
				cluster.applicant_pop -= 1
				new_cluster.applicant_centroid, new_cluster.applicant_centroid_data = alg.inflate_centroid(
					new_cluster.applicant_centroid_data, user.features, new_cluster.applicant_pop)
				new_cluster.applicant_pop += 1
			else:
				cluster.business_centroid, cluster.business_centroid_data = alg.deflate_centroid(
					cluster.business_centroid_data, user.features, cluster.business_pop)
				cluster.business_pop -= 1
				new_cluster.business_centroid, new_cluster.business_centroid_data = alg.inflate_centroid(
					new_cluster.business_centroid_data, user.features, new_cluster.business_pop)
				new_cluster.business_pop += 1
			db.session.commit()


def merge_cluster(solute_cluster):
	clusters = Cluster.query.all()
	dual_centroids = []
	ids = []
	for cluster in clusters:
		if cluster == solute_cluster:
			continue
		dual_centroids.append((cluster.applicant_centroid, cluster.business_centroid))
		ids.append(cluster.id)
	solvent_id = alg.closest_cluster([solute_cluster.applicant_centroid, solute_cluster.business_centroid],
	                                 dual_centroids, ids)
	solvent_cluster = Cluster.query.get(solvent_id)
	data = solute_cluster.applicants + solute_cluster.businesses
	for d in data:
		d.cluster_id = solvent_cluster.id
	solvent_cluster.applicant_centroid, solvent_cluster.applicant_centroid_data = alg.merge_centroid(
		solvent_cluster.applicant_centroid_data, solute_cluster.applicant_centroid_data, solvent_cluster.applicant_pop,
		solute_cluster.applicant_pop)
	solvent_cluster.business_centroid, solvent_cluster.business_centroid_data = alg.merge_centroid(
		solvent_cluster.business_centroid_data, solute_cluster.business_centroid_data, solvent_cluster.business_pop,
		solute_cluster.business_pop)
	solvent_cluster.applicant_pop += solute_cluster.applicant_pop
	solvent_cluster.business_pop += solute_cluster.business_pop
	db.session.delete(solute_cluster)
	db.session.commit()
