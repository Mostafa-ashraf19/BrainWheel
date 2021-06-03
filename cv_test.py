# Unit Tests
import numpy as np
import cv2
from BrainWheel.computer_vision import ComputerVision

CV = ComputerVision()

def general_test():
	for cache in CV.loop(l_img=True, r_img=True, depth_map=True, depth_map_img=True, point_cloud=True):
		l_img, r_img, depth_map, depth_map_img, point_cloud = cache

		# double_img = np.hstack((l_img, r_img))
		cv2.imshow('Camera Inputs', l_img)
		cv2.imshow('Depth Map', depth_map_img)
		
		print('point cloud shape:', point_cloud.shape)
		print('depth map shape:  ', depth_map.shape)

		# # Object Detection
		# od_bbox = CV.object_detection(l_img, show=True, keep_showing=True)

		# # Semantic Segmentation
		# ss_pred = CV.semantic_segmentation(l_img, show=True, keep_showing=True)

		# # Occupancy Grid
		# occ_grid = CV.occupancy_grid(point_cloud, ss_pred, show=True, keep_showing=True)

		# # Distance to Collision
		# min_dists = CV.distance_to_collision(od_bbox, point_cloud, l_img, return_image=False, show=True, keep_showing=True)
		
		# # Is Close to Collision
		# min_dist, is_close = CV.is_close_to_collision(od_bbox, min_dists, return_min_dist=True)
		# is_close = "CLOSE!!!" if is_close else "not close"
		# print(min_dist, '\t=>', is_close)

		# Is Close to Collision Simple
		min_dist, is_close = CV.is_close_to_collision_simple(depth_map, return_min_dist=True)
		is_close = "CLOSE!!!" if is_close else "not close"
		print(min_dist, '\t=>', is_close)

		
		# Press 'q' to stop ...
		# cv2.waitKey(0)
		# break

def ss_and_od_test_on_college_data_test():
	SS_image_list = ['test{:02d}.jpeg'.format(n) for n in range(22)]
	SS_image_dir = './BrainWheel/computer_vision/test images/'
	for img_name in SS_image_list:
		img_name = SS_image_dir + img_name
		img = cv2.imread(img_name)
		CV.semantic_segmentation(img, show=True, keep_showing=True)
		CV.object_detection(img, show=True, keep_showing=False)

def occ_grid_test():
	for occ_grid, occ_grid_img in CV.loop(occ_grid=True, occ_grid_img=True):
		print(type(occ_grid))
		print(occ_grid.shape)
		# print(point_cloud)
		cv2.imshow("Occupancy Grid",occ_grid_img)
		break


if __name__ == '__main__':
	# general_test()
	# ss_and_od_test_on_college_data_test()
	occ_grid_test()

	cv2.destroyAllWindows()
