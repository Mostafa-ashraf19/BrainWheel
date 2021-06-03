import numpy as np

OCC_GRID_SHAPE = (301, 401)

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
    x, y, z = point_cloud[:,:,0], point_cloud[:,:,1], point_cloud[:,:,2]
    print('here', x.shpae, ground_mask.shape)
    occ_grid = np.where(
        #cond1
        ground_mask != 1 & np.isfinite(x) & np.isfinite(z)
        ,
        #case1 value
        1
        ,
        #else
        np.where(
            #cond2
            ground_mask != 1 & np.isfinite(x) & np.isfinite(z)
            ,
            #case2 value
            0
            ,
            #else value
            0.5
        )
    )

    return occ_grid