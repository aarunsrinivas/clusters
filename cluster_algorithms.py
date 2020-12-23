import random
import numpy as np
from collections import Counter
from itertools import permutations


# comment
def compute_centroid(data_set, data_type):
	centroid_data = {
		'type': data_type,
		'major_dict': Counter(),
		'major_len_sum': 0,
		'standing_dict': Counter(),
		'standing_len_sum': 0,
		'gpa_sum': 0,
		'skills_dict': Counter(),
		'skills_len_sum': 0
	}

	for data in data_set:
		for major in data['major']:
			if major in centroid_data['major_dict']:
				centroid_data['major_dict'][major] += 1
			else:
				centroid_data['major_dict'][major] = 1
		centroid_data['major_len_sum'] += len(data['major'])
		for standing in data['standing']:
			if standing in centroid_data['standing_dict']:
				centroid_data['standing_dict'][standing] += 1
			else:
				centroid_data['standing_dict'][standing] = 1
		centroid_data['standing_len_sum'] += len(data['standing'])
		for skill in data['skills']:
			if skill in centroid_data['skills_dict']:
				centroid_data['skills_dict'][skill] += 1
			else:
				centroid_data['skills_dict'][skill] = 1
		centroid_data['skills_len_sum'] += len(data['skills'])
		centroid_data['gpa_sum'] += data['gpa']

	centroid = {
		'type': data_type,
		'major': sorted(centroid_data['major_dict'].keys(), key=lambda x: centroid_data['major_dict'][x], reverse=True)[
		         0: round(centroid_data['major_len_sum'] / (len(data_set) if len(data_set) else 1))],
		'standing': sorted(centroid_data['standing_dict'].keys(), key=lambda x: centroid_data['standing_dict'][x],
		                   reverse=True)[
		            0: round(centroid_data['standing_len_sum'] / (len(data_set) if len(data_set) else 1))],
		'gpa': round(centroid_data['gpa_sum'] / (len(data_set) if len(data_set) else 1), 2),
		'skills': sorted(centroid_data['skills_dict'].keys(), key=lambda x: centroid_data['skills_dict'][x],
		                 reverse=True)[
		          0: round(centroid_data['skills_len_sum'] / (len(data_set) if len(data_set) else 1))],
	}
	return centroid, centroid_data


def inflate_centroid(centroid_data, data, size):
	centroid_data = centroid_data.copy()
	for major in data['major']:
		if major in centroid_data['major_dict']:
			centroid_data['major_dict'][major] += 1
		else:
			centroid_data['major_dict'][major] = 1
	centroid_data['major_len_sum'] += len(data['major'])
	for standing in data['standing']:
		if standing in centroid_data['standing_dict']:
			centroid_data['standing_dict'][standing] += 1
		else:
			centroid_data['standing_dict'][standing] = 1
	centroid_data['standing_len_sum'] += len(data['standing'])
	for skill in data['skills']:
		if skill in centroid_data['skills_dict']:
			centroid_data['skills_dict'][skill] += 1
		else:
			centroid_data['skills_dict'][skill] = 1
	centroid_data['skills_len_sum'] += len(data['skills'])
	centroid_data['gpa_sum'] += data['gpa']

	divisor = size + 1
	centroid = {
		'type': data['type'],
		'major': sorted(centroid_data['major_dict'].keys(), key=lambda x: centroid_data['major_dict'][x], reverse=True)[
		         0: round(centroid_data['major_len_sum'] / (divisor if divisor else 1))],
		'standing': sorted(centroid_data['standing_dict'].keys(), key=lambda x: centroid_data['standing_dict'][x],
		                   reverse=True)[
		            0: round(centroid_data['standing_len_sum'] / (divisor if divisor else 1))],
		'gpa': round(centroid_data['gpa_sum'] / (divisor if divisor else 1), 2),
		'skills': sorted(centroid_data['skills_dict'].keys(), key=lambda x: centroid_data['skills_dict'][x],
		                 reverse=True)[
		          0: round(centroid_data['skills_len_sum'] / (divisor if divisor else 1))]
	}
	return centroid, centroid_data


def deflate_centroid(centroid_data, data, size):
	centroid_data = centroid_data.copy()
	for major in data['major']:
		if major in centroid_data['major_dict']:
			centroid_data['major_dict'][major] -= 1
	centroid_data['major_len_sum'] -= len(data['major'])
	for standing in data['standing']:
		if standing in centroid_data['standing_dict']:
			centroid_data['standing_dict'][standing] -= 1
	centroid_data['standing_len_sum'] -= len(data['standing'])
	for skill in data['skills']:
		if skill in centroid_data['skills_dict']:
			centroid_data['skills_dict'][skill] -= 1
	centroid_data['skills_len_sum'] -= len(data['skills'])
	centroid_data['gpa_sum'] -= data['gpa']

	divisor = size - 1
	centroid = {
		'type': data['type'],
		'major': sorted(centroid_data['major_dict'].keys(), key=lambda x: centroid_data['major_dict'][x], reverse=True)[
		         0: round(centroid_data['major_len_sum'] / (divisor if divisor else 1))],
		'standing': sorted(centroid_data['standing_dict'].keys(), key=lambda x: centroid_data['standing_dict'][x],
		                   reverse=True)[
		            0: round(centroid_data['standing_len_sum'] / (divisor if divisor else 1))],
		'gpa': round(centroid_data['gpa_sum'] / (divisor if divisor else 1), 2),
		'skills': sorted(centroid_data['skills_dict'].keys(), key=lambda x: centroid_data['skills_dict'][x],
		                 reverse=True)[
		          0: round(centroid_data['skills_len_sum'] / (divisor if divisor else 1))]
	}
	return centroid, centroid_data


def merge_centroid(centroid_data, new_centroid_data, size, new_size):
	centroid_data = centroid_data.copy()
	new_centroid_data = new_centroid_data.copy()
	centroid_data['major_dict'].update(new_centroid_data['major_dict'])
	centroid_data['major_len_sum'] += new_centroid_data['major_len_sum']
	centroid_data['standing_dict'].update(new_centroid_data['standing_dict'])
	centroid_data['standing_len_sum'] += new_centroid_data['standing_len_sum']
	centroid_data['skills_dict'].update(new_centroid_data['skills_dict'])
	centroid_data['skills_len_sum'] += new_centroid_data['skills_len_sum']
	centroid_data['gpa_sum'] += new_centroid_data['gpa_sum']

	divisor = size + new_size
	centroid = {
		'type': centroid_data['type'],
		'major': sorted(centroid_data['major_dict'].keys(), key=lambda x: centroid_data['major_dict'][x], reverse=True)[
		         0: round(centroid_data['major_len_sum'] / (divisor if divisor else 1))],
		'standing': sorted(centroid_data['standing_dict'].keys(), key=lambda x: centroid_data['standing_dict'][x],
		                   reverse=True)[
		            0: round(centroid_data['standing_len_sum'] / (divisor if divisor else 1))],
		'gpa': round(centroid_data['gpa_sum'] / (divisor if divisor else 1), 2),
		'skills': sorted(centroid_data['skills_dict'].keys(), key=lambda x: centroid_data['skills_dict'][x],
		                 reverse=True)[
		          0: round(centroid_data['skills_len_sum'] / (divisor if divisor else 1))]
	}
	return centroid, centroid_data


# compare everything relative to the first parameter
def compare_different_types(first, second):
	zero = {
		'type': first['type'],
		'major': [],
		'standing': [],
		'gpa': 0,
		'skills': []
	}
	if first == zero:
		return 0
	# compare majors
	major = 1
	major_flag = False
	for first_major in first['major']:
		for second_major in second['major']:
			if first_major == second_major:
				major = major - 1
				major_flag = True
		if major_flag:
			break
	major = major / 1
	# compare standings
	standing = 1
	standing_flag = False
	for first_standing in first['standing']:
		for second_standing in second['standing']:
			if first_standing == second_standing:
				standing = standing - 1
				standing_flag = True
		if standing_flag:
			break
	standing = standing / 1
	# compare gpa
	gpa = 0 if second['gpa'] >= first['gpa'] else 1
	# compare skills
	skills = len(first['skills'])
	for first_skills in first['skills']:
		for second_skills in second['skills']:
			if first_skills == second_skills:
				skills = skills - 1
	skills = skills / len(first['skills'])
	dist = (major ** 2 + standing ** 2 + gpa ** 2 + skills ** 2) ** (1 / 2)
	return dist


def compare_same_types(first, second):
	zero = {
		'type': first['type'],
		'major': [],
		'standing': [],
		'gpa': 0,
		'skills': []
	}
	if first == zero:
		return 0
	# compare majors
	major = 1
	major_flag = False
	for first_major in first['major']:
		for second_major in second['major']:
			if first_major == second_major:
				major = major - 1
				major_flag = True
		if major_flag:
			break
	major = major / 1
	# compare standings
	standing = 1
	standing_flag = False
	for first_standing in first['standing']:
		for second_standing in second['standing']:
			if first_standing == second_standing:
				standing = standing - 1
				standing_flag = True
		if standing_flag:
			break
	standing = standing / 1
	# compare gpa
	gpa = first['gpa'] - second['gpa']
	gpa = gpa / 4
	# compare skills
	skills = len(first['skills'])
	for first_skills in first['skills']:
		for second_skills in second['skills']:
			if first_skills == second_skills:
				skills = skills - 1
	skills = skills / len(first['skills'])
	dist = (major ** 2 + standing ** 2 + gpa ** 2 + skills ** 2) ** (1 / 2)
	return dist


def closest_cluster(data_set, dual_centroids, ids):
	distances = []
	for dual_centroid in dual_centroids:
		applicant_centroid, business_centroid = dual_centroid
		d = 0
		for data in data_set:
			if data['type'] == 'applicant':
				d += compare_different_types(business_centroid, data) + compare_same_types(applicant_centroid, data)
			else:
				d += compare_different_types(data, applicant_centroid) + compare_same_types(business_centroid, data)
		distances.append(d)
	return ids[np.argmin(distances)]


def find_clusters(data_set, n_clusters, max_iter=300, n_init=15):
	sse_lst = []
	labels_lst = []
	dual_centroids_lst = []
	applicant_data_set = []
	business_data_set = []
	for data in data_set:
		if type(data) == tuple:
			continue
		if data['type'] == 'applicant':
			applicant_data_set.append(data)
		else:
			business_data_set.append(data)

	for _ in range(n_init):
		applicant_centers = random.sample(applicant_data_set, n_clusters)
		business_centers = random.sample(business_data_set, n_clusters)
		distances = []
		for a_center in applicant_centers:
			d = []
			for b_center in business_centers:
				d.append(compare_different_types(b_center, a_center))
			distances.append(d)
		perm = list(permutations([i for i in range(n_clusters)]))
		variance = []
		for p in perm:
			t = []
			for i in range(len(p)):
				t.append(distances[i][p[i]])
			variance.append(np.var(t))
		assignment = perm[np.argmin(variance)]
		dual_centroids = [((applicant_centers[i], compute_centroid([], 'applicant')[1]),
		                   (business_centers[assignment[i]], compute_centroid([], 'business')[1]))
		                  for i in range(n_clusters)]

		iteration = 0
		while iteration < max_iter:
			clusters = {i: {'applicants': [], 'businesses': []} for i in range(n_clusters)}
			labels = []
			sse = 0
			for data in data_set:
				d = []
				for dual_centroid in dual_centroids:
					applicant_centroid, business_centroid = dual_centroid[0][0], dual_centroid[1][0]
					if type(data) == tuple:
						applicant_data, business_data = data
						d.append(0.5 * (compare_different_types(business_centroid, applicant_data) + compare_same_types(
							applicant_centroid, applicant_data)) + 0.5 * (compare_different_types(
							business_data, applicant_centroid) + compare_same_types(business_centroid, business_data)))
					else:
						if data['type'] == 'applicant':
							d.append(compare_different_types(business_centroid, data) + compare_same_types(
								applicant_centroid, data))
						else:
							d.append(compare_different_types(data, applicant_centroid) + compare_same_types(
								business_centroid, data))
				index = np.argmin(d)
				sse += d[index] ** 2
				duplicates = [i for i in range(n_clusters) if d[i] == d[index]]
				if type(data) == tuple:
					index = min(duplicates,
					            key=lambda x: len(clusters[x]['applicants']) + len(clusters[x]['businesses']))
					applicant_data, business_data = data
					clusters[index]['applicants'].append(applicant_data)
					clusters[index]['businesses'].append(business_data)
					labels.append(index)
				else:
					d_type = 'applicants' if data['type'] == 'applicant' else 'businesses'
					index = min(duplicates, key=lambda x: len(clusters[x][d_type]))
					clusters[index][d_type].append(data)
					labels.append(index)
			new_dual_centroids = [(
				compute_centroid(clusters[i]['applicants'], 'applicant') if len(clusters[i]['applicants']) else
				dual_centroids[i][0],
				compute_centroid(clusters[i]['businesses'], 'business') if len(clusters[i]['businesses']) else
				dual_centroids[i][1]) for i in range(n_clusters)]
			has_converged = True
			for i in range(len(dual_centroids)):
				for j in range(len(dual_centroids[i])):
					if compare_same_types(dual_centroids[i][j][0], new_dual_centroids[i][j][0]) != 0:
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
	index = np.argmin(sse_lst)
	labels = labels_lst[index]
	dual_centroids = dual_centroids_lst[index]
	centroids = []
	centroids_data = []
	for dual_centroid in dual_centroids:
		centroids.append((dual_centroid[0][0], dual_centroid[1][0]))
		centroids_data.append((dual_centroid[0][1], dual_centroid[1][1]))
	return labels, centroids, centroids_data
