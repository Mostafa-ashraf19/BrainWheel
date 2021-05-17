# Unit Tests
import numpy as np
import cv2
from computer_vision import ComputerVision

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
	SS_image_dir = './test images/'
	for img_name in SS_image_list:
		img_name = SS_image_dir + img_name
		img = cv2.imread(img_name)
		CV.semantic_segmentation(img, show=True, keep_showing=True)
		CV.object_detection(img, show=True, keep_showing=False)

def og_and_d2c_on_course_data_test():
	data_dir = ('D:/Courses/University of Toronto - Self Driving Cars Specialization/'
					+ '3) Visual Preception for Self Driving Cars/Week 6/module6/data/')

	od_bbox = [
		[[[20.0, 406.0, 280.0, 599.0]]],
		[[[180.0, 390.0, 470.0, 600.0], [620.0, 438.0, 760.0, 558.0]]],
		[[[140.0, 450.0, 310.0, 700.0], [615.0, 471.0, 678.0, 512.0]]]
	] # (img, 1, obj, dims)
	od_scores = [
		[[0.99]],
		[[0.68, 0.98]],
		[[0.89, 0.56]]
	] # (img, 1, obj)
	od_classes = [
		[[3]],
		[[3, 3]],
		[[2, 3]]
	]# (img, 1, obj)
	od_valid_detections = [[1], [2], [2]] # (img, 1)

	for i in range(3):
		img_dir = data_dir + 'rgb/' + str(i) + '.png'
		depth_dir = data_dir + 'depth/' + str(i) + '.dat'
		seg_dir = data_dir + 'segmentation/' + str(i) + '.dat'

		img = cv2.imread(img_dir)[:, :, ::-1]
		depth_map = np.loadtxt(depth_dir, delimiter=',', dtype=np.float64) * 1000.0
		seg_data = np.loadtxt(seg_dir, delimiter=',')
		od_data = od_bbox[i], od_scores[i], od_classes[i], od_valid_detections[i]

		print(i, ':', CV.distance_to_collision(od_data, depth_map))
		CV.occupancy_grid(depth_map, seg_data, show=True, keep_showing=False)


if __name__ == '__main__':
	general_test()
	# ss_and_od_test_on_college_data_test()
	# og_and_d2c_on_course_data_test()

	cv2.destroyAllWindows()
