"""Computer Vision Module for Electrical Wheelchair Graduation Project 2020-2021.
Version 2.0

Written by:
	Pierre Nabil
	Panse Yasser
"""
# imports

import numpy as np
import cv2 as cv
import pyzed.sl as sl

from errors import *

from od_model.predict import ODModel
from ss_model.predict import SSModel

# Constants

IMG_RESOLUTION = sl.RESOLUTION.HD720
CAM_FPS = 30

OD_USEFUL_CLASSES = [
	 0,  1,  2,  3,  4,
	 6,  7,  8, 11, 14,
	16, 17, 57, 58, 60,
	61, 62, 63, 72, 73
]


# Main Class

class ComputerVision:
	def __init__(self):
		# zed camera
		self.zed = sl.Camera()

		init_parameters = sl.InitParameters()
		init_params.camera_resolution = IMG_RESOLUTION
		init_params.camera_fps = CAM_FPS
		init_params.coordinate_units = sl.UNIT.CENTIMETER
		init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE

		self.zed.open(init_params)
		if not self.zed.isOpened():
			raise CameraNotConnectedError

		# machine learning models
		self.od_model = ODModel()
		self.ss_model = SSModel()

	def __del__(self):
		self.zed.close()

	def capture(self, show=False, keep_showing=False):
		"""Fetches left and right images from cameras and places them in the cache.
		
		Parameters:
			show=False
				Bool to show if the user wants to see the left and right images.

			keep_showing=False
				Bool to define whether the user wants to continue with the code while
				keeping the show window. If False, the code execution will stop until
				the window is closed.

		Returns:
			left and right images fetched.
		"""
		l_img = sl.Mat()
		r_img = sl.Mat()
		runtime_parameters = sl.RuntimeParameters()
		if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
			self.zed.retrieve_image(l_img, sl.VIEW.LEFT)
			self.zed.retrieve_image(r_img, sl.VIEW.RIGHT)

		l_img = l_img.get_data()
		r_img = r_img.get_data()

		if show:
			double_img = np.hstack((l_img, r_img))
			cv.imshow('Camera Inputs', double_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Camera Inputs')

		return l_img, r_img

	def depth_map(self, return_image=False, show=False, keep_showing=False):
		"""Returns the current depth map.

		Parameters:
			return_image=False
				Bool to define whether to return the depth map as a 2D Matrix
				or as an Image

			show=False
				Bool to show if the user wants to see the depth map.

			keep_showing=False
				Bool to define whether the user wants to continue with the code while
				keeping the show window. If False, the code execution will stop until
				the window is closed.

		Returns:
			depth_map
				The depth map as a 2D Matrix.

			depth_map_img
				the depth map as an image.
		"""
		depth_map = sl.Mat()
		depth_map_img = sl.Mat()
		runtime_parameters = sl.RuntimeParameters()
		if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
			self.zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH)
			self.zed.retrieve_image(depth_map_img, sl.VIEW.DEPTH)

		depth_map = depth_map.get_data()

		if show:
			cv.imshow('Depth Map', depth_map_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Depth Map')

		if return_image:
			return depth_map_img
		else:
			return depth_map

	def point_cloud(self):
		"""Returns the point cloud of the image.

		Returns:
			point_cloud
				the coloured point cloud.
		"""
		point_cloud = sl.Mat()
		runtime_parameters = sl.RuntimeParameters()
		if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
			self.zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)

		return point_cloud.get_data()

	def object_detection(self, img=None, return_image=False, show=False, keep_showing=False):
		"""Uses a ML model (Yolov3) to detect objects in the picture.

		Parameters:
			img=None
				Image for detection.
				if None, the function will take the cached image or use a new image.
			show=False
				Bool to show if the user wants to see the object detection image.

		Returns:
			pred
				model output.
			pred_img
				image showing the predictions of the model.
		"""
		if img is None:
			img, _ = self.capture()

		pred_bbox = self.od_model.predict(img)

		if return_image:
			pred_img = self.od_model.show_on_image(img, pred_bbox, show, keep_showing)
			return pred_img
		else:
			return pred_bbox

	def semantic_segmentation(self, img=None, return_image=False, show=False, keep_showing=False):
		"""Uses a ML model (ICNet) to detect objects in the picture.

		Parameters:
			img=None
				Image for segmentation.
				if None, the function will take the cached image or use a new image.
			show=False
				Bool to show if the user wants to see the semantic segmentation image.

		Returns:
			pred
				model output.
			pred_img
				image showing the predictions of the model.
		"""
		if img is None:
			img, _ = self.capture()

		pred = self.ss_model.predict(img)

		if return_image:
			pred_img = self.ss_model.show_on_image(img, pred_bbox, show, keep_showing)
			return pred_img
		else:
			return pred

	def occupancy_grid(self, point_cloud=None, ss_pred=None, return_image=False, show=False, keep_showing=False):
		"""Uses RANSAC and other algorithms to compute the occupancy grid of the current frame.

		Parameters:
			depth_map=None
				depth map of current frame.
				if None, the function will compute the depth map of a newly captures frame.
			show=False
				Bool to show if the user wants to see the occupancy grid as an image.

		Returns:
			occ_grid
				occupancy grid.
		"""
		pass
	
	def _get_dist(bbox, point_cloud):
		"""Returns the distance of the object in the given point cloud from the given
		bounding box.

		Helper Function!
		"""
		x_min, y_min, x_max, y_max = bbox

		x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])

		cloud = np.array([[point_cloud.get_value(x,y)
						for x in range(x_min, x_max+1)] 
						for y in range(y_min, y_max+1)])

		box_dists = np.sqrt(cloud[:,:,0]*cloud[:,:,0]
						+ cloud[:,:,1]*cloud[:,:,1]
						+ cloud[:,:,2]*cloud[:,:,2])

		return np.min(box_dists)

	def distance_to_collision(self, od_bbox=None, point_cloud=None):
		"""Calculates the minimum distance to all detected objects.

		Parameters:
			od_bbox
				output of the OD model computed on the current frame
			depth_map
				depth map of the current frame

		Returns:
			min_distances
				the minimum distance for every detected object in the current frame
		"""
		if point_cloud is None:
			point_cloud = self.point_cloud()
		if od_bbox is None:
			od_bbox = self.object_detection()

		boxes, scores, classes, valid_detections = od_bbox
		x, y, z = point_cloud

		min_distances = []
		for i in range(valid_detections[0]):
			class_id = classes[0][i]
			if class_id in OD_USEFUL_CLASSES:
				bbox = boxes[0][i]
				min_distances.append(self._get_dist(bbox, point_cloud))

		return np.array(min_distances)


	# Add support for l_img, r_img in class_instance:
	# use 'q' to quit the loop
	def loop(self, l_img=True, r_img=False, depth_map=False, depth_map_img=False, point_cloud=False):
		while True:
			cache = ()
			_l_img, _r_img = self.capture()
			if l_img:
				cache = cache + (_l_img,)
			if r_img:
				cache = cache + (_r_img,)
			if depth_map:
				cache = cache + (self.depth_map(),)
			if depth_map_img:
				cache = cache + (self.depth_map(return_image=True),)
			if point_cloud:
				cache = cache + (self.point_cloud(),)
			yield cache
			# use 'q' to quit the loop
			if cv.waitKey(1) & 0xFF == ord('q'):
				raise StopIteration

# Unit Tests

if __name__ == '__main__':
	CV = ComputerVision()

	'''
	# Test SS and OD on College Data:
	SS_image_list = ['College_Test_{:02d}.jpeg'.format(n+1) for n in range(20)]
	print(SS_image_list)
	SS_image_dir = 'D:/Graduation Project/Computer Vision Notebooks/ss_model/data/input/'
	for img_name in SS_image_list:
		img_name = SS_image_dir + img_name
		img = cv.imread(img_name)
		CV.semantic_segmentation(img, show=True, keep_showing=True)
		CV.object_detection(img, show=True, keep_showing=False)
	#'''


	'''
	#Test OG and D2C on Course Data:
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

		img = cv.imread(img_dir)[:, :, ::-1]
		depth_map = np.loadtxt(depth_dir, delimiter=',', dtype=np.float64) * 1000.0
		seg_data = np.loadtxt(seg_dir, delimiter=',')
		od_data = od_bbox[i], od_scores[i], od_classes[i], od_valid_detections[i]

		print(i, ':', CV.distance_to_collision(od_data, depth_map))
		CV.occupancy_grid(depth_map, seg_data, show=True, keep_showing=False)
	#'''


	#'''
	# General Test:
	for cache in CV.loop(l_img=True, r_img=True, depth_map_img=True, point_cloud=True):
		l_img, r_img, depth_map_img, point_cloud = cache

		double_img = np.hstack((l_img, r_img))
		cv.imshow('Camera Inputs', double_img)
		cv.imshow('Depth Map', depth_map_img)

		# # Object Detection
		# od_bbox = CV.object_detection(l_img, show=True, keep_showing=True)

		# # Semantic Segmentation
		# ss_pred = CV.semantic_segmentation(l_img, show=True, keep_showing=True)

		# # Occupancy Grid
		# occ_grid = CV.occupancy_grid(point_cloud, ss_pred, show=True, keep_showing=True)

		# # Distance to Collision
		# min_dists = CV.distance_to_collision(od_data, point_cloud)
		# print(min_dists)

		# Press 'q' to stop ...
	#'''

	cv.destroyAllWindows()
