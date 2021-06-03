import numpy as np

def ransac_plane_fit(xyz_data):
    """
    Computes plane coefficients a,b,c,d of the plane in the form ax+by+cz+d = 0
    using ransac for outlier rejection.

    Arguments:
    xyz_data -- tensor of dimension (3, N), contains all data points from which random sampling will proceed.
    num_itr -- 
    distance_threshold -- Distance threshold from plane for a point to be considered an inlier.

    Returns:
    p -- tensor of dimension (1, 4) containing the plane parameters a,b,c,d
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
        distances = _dist_to_plane(plane, *xyz_data)

        current_num_inliers = sum(distances < distance_threshold)
        if current_num_inliers > max_num_inliers:
            max_num_inliers = current_num_inliers
            output_plane = plane
        
        if current_num_inliers > min_num_inliers:
            break

    return output_plane 


def _compute_plane(xyz_chosen):
    """
    Computes plane coefficients a,b,c,d of the plane in the form ax+by+cz+d = 0

    Arguments:
    xyz -- tensor of dimension (3, N), contains points needed to fit plane.
    k -- tensor of dimension (3x3), the intrinsic camera matrix

    Returns:
    p -- tensor of dimension (1, 4) containing the plane parameters a,b,c,d
    """
    ctr = xyz.mean(axis=1)
    normalized = xyz - ctr[:, np.newaxis]
    M = np.dot(normalized, normalized.T)

    plane = np.linalg.svd(M)[0][:, -1]
    d = np.matmul(plane, ctr)

    plane = np.append(plane, -d)

    return plane


def abs_dist_to_plane(plane, x,y,z):
    return np.abs(_dist_to_pane(plane, x,y,z))


def _dist_to_plane(plane, x,y,z):
    """
    Computes distance between points provided by their x, and y, z coordinates
    and a plane in the form ax+by+cz+d = 0

    Arguments:
    plane -- tensor of dimension (4,1), containing the plane parameters [a,b,c,d]
    x -- tensor of dimension (Nx1), containing the x coordinates of the points
    y -- tensor of dimension (Nx1), containing the y coordinates of the points
    z -- tensor of dimension (Nx1), containing the z coordinates of the points

    Returns:
    distance -- tensor of dimension (N, 1) containing the distance between points and the plane
    """
    a, b, c, d = plane
    dist = (a * x + b * y + c * z + d) / np.sqrt(a**2 + b**2 + c**2)

    return dist


#TODO: fix this function
def get_free_space(ground_mask, point_cloud):
    sz = depth_map.shape
    f = self.l_proj_mat[0, 0]
    c_u = self.l_proj_mat[0, 2]

    # Generate a grid of coordinates corresponding to the shape of the depth
    # map
    u, v = np.meshgrid(np.arange(1, sz[1] + 1, 1),
                        np.arange(1, sz[0] + 1, 1))

    # Compute x and y coordinates
    xx = ((u - c_u) * depth_map) / f

    xx = xx * 10 + 200
    xx = np.maximum(0, np.minimum(xx, 399))

    depth_map = depth_map * 10
    depth_map[depth_map > 300] = np.nan

    occ_grid = np.full([301, 401], 0.5)

    for x, z, seg in zip(xx.flatten('C'), depth_map.flatten('C'),
                            ground_mask.flatten('C')):
        if not(seg == 1):
            if not np.isnan(x) and not np.isnan(z):
                x = int(x)
                z = int(z)
                occ_grid[z, x] = 1

    for x, z, seg in zip(xx.flatten('C'), depth_map.flatten('C'),
                            ground_mask.flatten('C')):
        if seg == 1:
            if not np.isnan(x) and not np.isnan(z):
                x = int(x)
                z = int(z)
                if not occ_grid[z, x] == 1:
                    occ_grid[z, x] = 0
    return occ_grid