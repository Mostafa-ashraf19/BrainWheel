"""Computer Vision Module for Electrical Wheelchair Graduation Project 2020-2021.
Version 3.0

Written by:
	Pierre Nabil
	Panse Yasser
"""
# imports

import numpy as np
import cv2
import pyzed.sl as sl

from errors import CameraNotConnectedError

# from od_model import ODModel
from od_model import ODModelTiny as ODModel
# from ss_model import SSModel

# Constants

ZED_IMG_RESOLUTION = sl.RESOLUTION.HD720
ZED_CAM_FPS = 30
ZED_COORDINATE_UNITS = sl.UNIT.CENTIMETER
ZED_DEPTH_MODE = sl.DEPTH_MODE.PERFORMANCE

D2C_THRESHOLD = 73

# Main Class

class ComputerVision:
	def __init__(self):
		# zed camera
		self.zed = sl.Camera()

		init_params = sl.InitParameters()
		init_params.camera_resolution = ZED_IMG_RESOLUTION
		init_params.camera_fps = ZED_CAM_FPS
		init_params.coordinate_units = ZED_COORDINATE_UNITS
		init_params.depth_mode = ZED_DEPTH_MODE

		err = self.zed.open(init_params)
		if err != sl.ERROR_CODE.SUCCESS:
			raise CameraNotConnectedError()

		# machine learning models
		self.od_model = ODModel()
		# self.ss_model = SSModel()

	def __del__(self):
		self.zed.close()

	def loop(self, *, l_img=True, r_img=False, depth_map=False, depth_map_img=False, point_cloud=False):
		runtime_parameters = sl.RuntimeParameters()

		while True:
			cache = []
			if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
				if l_img:
					_l_img = sl.Mat()
					self.zed.retrieve_image(_l_img, sl.VIEW.LEFT)
					cache.append(_l_img.get_data())

				if r_img:
					_r_img = sl.Mat()
					self.zed.retrieve_image(_r_img, sl.VIEW.RIGHT)
					cache.append(_r_img.get_data())

				if depth_map:
					_depth_map = sl.Mat()
					self.zed.retrieve_measure(_depth_map, sl.MEASURE.DEPTH)
					cache.append(_depth_map.get_data())		

				if depth_map_img:
					_depth_map_img = sl.Mat()
					self.zed.retrieve_image(_depth_map_img, sl.VIEW.DEPTH)
					cache.append(_depth_map_img.get_data())

				if point_cloud:
					_point_cloud = sl.Mat()
					self.zed.retrieve_measure(_point_cloud, sl.MEASURE.XYZRGBA)
					cache.append(_point_cloud.get_data())

			if cache:
				yield cache
			else:
				raise StopIteration
			# use 'q' to quit the loop
			if cv2.waitKey(1) & 0xFF == ord('q'):
				raise StopIteration

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
		gen = self.loop(l_img=True, r_img=True)
		l_img, r_img = next(gen)

		if show:
			double_img = np.hstack((l_img, r_img))
			cv2.imshow('Camera Inputs', double_img)
			if not keep_showing:
				cv2.waitKey(0)
				cv2.destroyWindow('Camera Inputs')

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
		gen = self.loop(depth_map=True, depth_map_img=True)
		depth_map, depth_map_img = next(gen)

		if show:
			cv2.imshow('Depth Map', depth_map_img)
			if not keep_showing:
				cv2.waitKey(0)
				cv2.destroyWindow('Depth Map')

		if return_image:
			return depth_map, depth_map_img
		else:
			return depth_map

	def point_cloud(self):
		"""Returns the point cloud of the image.

		Returns:
			point_cloud
				the coloured point cloud.
		"""
		gen = self.loop(point_cloud=True)
		point_cloud = next(gen)
		return point_cloud

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
		#TODO: Check that this function works with ZED camera
		pass
	
	def _get_dist(bbox, point_cloud):
		"""Returns the distance of the object in the given point cloud from the given
		bounding box.

		Helper Function!
		"""
		#TODO: Check that this function works with ZED camera
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
		#TODO: Check that this function works with ZED camera
		if point_cloud is None:
			point_cloud = self.point_cloud()
		if od_bbox is None:
			od_bbox = self.object_detection()

		boxes = od_bbox[:, :4]
		scores = od_bbox[:, 4]
		classes = od_bbox[:, 5]
		valid_detections = len(od_bbox)

		min_distances = []
		for i in range(valid_detections):
			class_id = classes[i]
			if class_id in OD_USEFUL_CLASSES:
				bbox = boxes[i]
				min_distances.append(self._get_dist(bbox, point_cloud))

		return np.array(min_distances)

	def show_distance_to_collision(self, img, od_bbox, min_dists, show=False, keep_showing=False):
		"""Shows the minimum distance to all detected objects in an image.

		Parameters:
			img
				left image from the camera
			od_bbox
				output of the OD model computed on the current frame
			min_dists
				output of the distance_to_collision function
			show

		Returns:
			img
				modified image after adding bounding boxes
		"""
		d2c_img = img.copy()

		for (*xyxy, conf, class_id), dist in reversed(zip(od_bbox, min_dists)):
				if class_id in USEFUL_CLASSES:
					label = '{}: {:.2f} cm'.format(CLASS_NAMES[int(class_id)], dist)
					plot_one_box(xyxy, d2c_img, label=label, color=CLASS_COLORS[int(class_id)], line_thickness=LINE_THICKNESS)
		
		if show:
			cv2.imshow('Distance To Collision', d2c_img)
			if not keep_showing:
				cv2.waitKey(0)
				cv2.destroyWindow('Distance To Collision')

		return d2c_img

	def is_close_to_collision(self, min_dists=None, thres=D2C_THRESHOLD):
		if min_dists is None:
			min_dists = self.distance_to_collision()

		min_dist = min_dists[np.isfinite(min_dists)].min()
		return (min_dist < D2C_THRESHOLD)

	def is_close_to_collision_simple(self, depth_map=None, thres=D2C_THRESHOLD, return_min_dist=False):
		if depth_map is None:
			depth_map = self.depth_map()

		img_h, img_w = depth_map.shape
		third_img_h = img_h // 3
		quart_img_w = img_w // 4

		window = depth_map[:-quart_img_h, third_img_w:-third_img_w]
		min_dist = window[np.isfinite(window)].min()
		
		is_close = min_dist < D2C_THRESHOLD
		if return_min_dist:
			return min_dist, is_close
		else:
			return is_close
