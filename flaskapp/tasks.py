import numpy as np
from flaskapp import db

IDEAL_SIZE = 15
IDEAL_RATIO = 2
WORST_INACTIVITY = 2


def check(cluster):
	world = cluster.world
	min_idx = np.argmin([cluster.top_index for cluster in world.top])
	max_idx = np.argmax([cluster.bottom_index for cluster in world.bottom])
	if cluster.top_index > world.top[min_idx].top_index:
		world.top[min_idx] = cluster
	elif cluster.bottom_index < world.bottom[max_idx].bottom_index:
		world.bottom[max_idx] = cluster
	db.session.commit()


def manage(world):
	for cluster in world.top:
		size_prob = abs(cluster.size - IDEAL_SIZE) / IDEAL_SIZE
		ratio_prob = abs(cluster.ratio - IDEAL_RATIO) / IDEAL_RATIO
		time_prob = 1 - abs(cluster.inactivity - WORST_INACTIVITY) / WORST_INACTIVITY
		# normalize and cap at 1 then divide by three to obtain probability

	for cluster in world.bottom:
		# calc prob of merge
		pass
