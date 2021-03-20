import numpy as np


def compute_plane(xyz):
	"""Computes plane coefficients a,b,c,d of the plane in the form ax+by+cz+d = 0

	Private Function!

	Parameters:
		xyz
			tensor of dimension (3, N), contains points needed to fit plane.

	Returns:
		plane
			tensor of dimension (1, 4) containing the plane parameters a,b,c,d
	"""

	ctr = xyz.mean(axis=1)
	normalized = xyz - ctr[:, np.newaxis]
	M = np.dot(normalized, normalized.T)

	plane = np.linalg.svd(M)[0][:, -1]
	d = np.matmul(plane, ctr)

	plane = np.append(plane, -d)

	return plane


def dist_to_plane(plane, x, y, z):
	"""Computes distance between points provided by their x, and y, z coordinates
	and a plane in the form ax+by+cz+d = 0

	Private Function!

	Parameters:
		plane
			tensor of dimension (4,1), containing the plane parameters [a,b,c,d]
		x, y, z
			tensors of dimension (Nx1) each, containing the x, y and z coordinates of the points respectively

	Returns:
		dist
			tensor of dimension (N, 1) containing the distance between points and the plane
	"""
	a, b, c, d = plane
	dist = (a * x + b * y + c * z + d) / np.sqrt(a**2 + b**2 + c**2)

	return dist


def ransac_plane_fit(xyz_data):
	"""Computes plane coefficients a,b,c,d of the plane in the form ax+by+cz+d = 0
	using RANSAC for outlier rejection.

	Private Function!

	Parameters:
		xyz_data
			tensor of dimension (3, N), contains all data points from which random sampling will proceed.

	Returns:
		output_plane
			tensor of dimension (1, 4) containing the plane parameters a,b,c,d
	"""
	# Set thresholds:
	num_itr = 3  # RANSAC maximum number of iterations
	min_num_inliers = 3500  # RANSAC minimum number of inliers
	distance_threshold = 0.0001  # Maximum distance from point to plane for point to be considered inlier

	max_num_inliers = 0
	output_plane = None

	for i in range(num_itr):
		chosen_idx = np.random.choice(xyz_data.shape[-1], size=5)
		xyz_chosen = xyz_data[:, chosen_idx]

		plane = compute_plane(xyz_chosen)
		distances = dist_to_plane(plane, *xyz_data)

		current_num_inliers = sum(distances < distance_threshold)
		if current_num_inliers > max_num_inliers:
			max_num_inliers = current_num_inliers
			output_plane = plane

		if current_num_inliers > min_num_inliers:
			break

	return output_plane
