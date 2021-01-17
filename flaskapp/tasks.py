import numpy as np
from flaskapp import db

IDEAL_SIZE = 15
IDEAL_RATIO = 2
IDEAL_INACTIVITY = 0


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
		# calc prob of split
		pass
	for cluster in world.bottom:
		# calc prob of merge
		pass
