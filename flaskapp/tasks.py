import numpy as np


# define tasks for scheduler to perform

def troubleshoot(cluster):
	world = cluster.world
	min_idx = np.argmin([cluster.index for cluster in world.top])
	max_idx = np.argmax([cluster.index for cluster in world.bottom])
	if cluster.index > world.top[min_idx].index:
		world.top[min_idx] = cluster
	elif cluster.index < world.bottom[max_idx].index:
		world.bottom[max_idx] = cluster


def manage(cluster):
	pass
