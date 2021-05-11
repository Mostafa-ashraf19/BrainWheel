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

from errors import CameraNotConnectedError, NoImageError

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

	def loop(self, *, l_img=True, r_img=False, depth_map=False, depth_map_img=False, point_cloud=False,
					od_bbox=False, od_img=False, ss_pred=False, ss_img=False,
					dist_to_col=False, dist_to_col_img=False,
					is_close=False, min_dist=False, is_close_simple=False, min_dist_simple=False):
		is_c = is_close or min_dist
		is_c_s = is_close_simple or min_dist_simple
		d2c = dist_to_col or dist_to_col_img 		or is_c
		od = od_bbox or od_img						or d2c
		ss = ss_pred or ss_img
		
		runtime_parameters = sl.RuntimeParameters()

		while True:
			cache = []
			if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
				if l_img or od or ss or d2c:
					_l_img = sl.Mat()
					self.zed.retrieve_image(_l_img, sl.VIEW.LEFT)
					if l_img:
						cache.append(_l_img.get_data())

				if r_img:
					_r_img = sl.Mat()
					self.zed.retrieve_image(_r_img, sl.VIEW.RIGHT)
					cache.append(_r_img.get_data())

				if depth_map or is_c_s:
					_depth_map = sl.Mat()
					self.zed.retrieve_measure(_depth_map, sl.MEASURE.DEPTH)
					cache.append(_depth_map.get_data())		

				if depth_map_img:
					_depth_map_img = sl.Mat()
					self.zed.retrieve_image(_depth_map_img, sl.VIEW.DEPTH)
					cache.append(_depth_map_img.get_data())

				if point_cloud or d2c:
					_point_cloud = sl.Mat()
					self.zed.retrieve_measure(_point_cloud, sl.MEASURE.XYZRGBA)
					if point_cloud:
						cache.append(_point_cloud.get_data())

				if od:
					_od_bbox = self.object_detection(img=_l_img, return_image=od_img)
					if od_img:
						_od_bbox, _od_img = _od_bbox
					if od_bbox:
						cache.append(_od_bbox)
					if od_img:
						cache.append(_od_img)

				if ss:
					_ss_pred = self.semantic_segmentation(img=_l_img, return_image=ss_img)
					if ss_img:
						_ss_pred, _ss_img = _ss_pred
					if ss_pred:
						cache.append(_ss_pred)
					if ss_img:
						cache.append(_ss_img)

				if d2c:
					_dist_to_col = self.distance_to_collision(_od_bbox, _point_cloud, _l_img, return_image=dist_to_col_img)
					if dist_to_col_img:
						_dist_to_col, _dist_to_col_img = _dist_to_col
					if dist_to_col:
						cache.append(_dist_to_col)
					if dist_to_col_img:
						cache.append(_dist_to_col_img)

				if is_c:
					_is_close = self.is_close_to_collision(_od_bbox, _dist_to_col, return_min_dist=min_dist)
					if min_dist:
						_is_close, _min_dist = _is_close
					if is_close:
						cache.append(_is_close)
					if min_dist:
						cache.append(_min_dist)

				if is_c_s:
					_is_close = self.is_close_to_collision_simple(_depth_map, return_min_dist=min_dist_simple)
					if min_dist_simple:
						_is_close, _min_dist = _is_close
					if is_close_simple:
						cache.append(_is_close)
					if min_dist_simple:
						cache.append(_min_dist)

			if cache:
				yield cache
			else:
				raise StopIteration
			# use 'q' to quit the loop
			if cv2.waitKey(1) & 0xFF == ord('q'):
				raise StopIteration

	def capture(self, *, show=False, keep_showing=False):
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

	def depth_map(self, *, return_image=False, show=False, keep_showing=False):
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

	def object_detection(self, img=None, *, return_image=False, show=False, keep_showing=False):
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

		if show or return_image:
			pred_img = self.od_model.show_on_image(img, pred_bbox, show, keep_showing)

		if return_image:
			return pred_bbox, pred_img
		else:
			return pred_bbox

	def semantic_segmentation(self, img=None, *, return_image=False, show=False, keep_showing=False):
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

		if show or return_image:
			pred_img = self.ss_model.show_on_image(img, pred_bbox, show, keep_showing)

		if return_image:
			return pred, pred_img
		else:
			return pred

	def occupancy_grid(self, point_cloud=None, ss_pred=None, *, return_image=False, show=False, keep_showing=False):
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
	
	def _get_dist(self, bbox, point_cloud):
		"""Returns the distance of the object in the given point cloud from the given
		bounding box.

		Helper Function!
		"""
		x_min, y_min, x_max, y_max = map(int, bbox)

		cloud = np.array([[point_cloud.get_value(x,y)
						for x in range(x_min, x_max+1)] 
						for y in range(y_min, y_max+1)])

		# Eucledian Distance
		box_dists = np.sqrt(cloud[:,:,0]*cloud[:,:,0] + cloud[:,:,1]*cloud[:,:,1] + cloud[:,:,2]*cloud[:,:,2])

		return np.min(box_dists)

	def distance_to_collision(self, od_bbox=None, point_cloud=None, image=None, *, return_image=False, show=False, keep_showing=False):
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

		boxes = od_bbox[:, :4]
		# scores = od_bbox[:, 4]
		# classes = od_bbox[:, 5]
		# valid_detections = len(od_bbox)

		min_dists = np.array([self._get_dist(bbox, point_cloud) for bbox in boxes])

		if show or return_image:
			if image is None:
				raise NoImageError
			dists_img = self.od_model._show_min_dists_on_image(image, od_bbox, min_dists, show=show, keep_showing=keep_showing)

		if return_image:
			return min_dists, dists_img
		else:
			return min_dists

	def _window(self, get_lims=False):
		img_h, img_w = self.od_model.img_shape
		h_llim = 0
		w_llim = img_w // 3
		h_ulim = img_h - (img_h // 4)
		w_ulim = 1- wllim

		if get_lims:
			return (h_llim, h_ulim), (w_llim, w_ulim)

		window = slice(h_llim, h_ulim), slice(w_llim, w_ulim)
		return window

	def is_close_to_collision_simple(self, depth_map=None, *, return_min_dist=False, thres=D2C_THRESHOLD):
		if depth_map is None:
			depth_map = self.depth_map()

		min_dist = depth_map[self._window()].min()
		is_close = min_dist < D2C_THRESHOLD

		if return_min_dist:
			return is_close, min_dist
		else:
			return is_close

	def _boxes_in_window(self, od_bbox):
		(h_llim, h_ulim), (w_llim, w_ulim) = self._window(get_lims=True)
		xmin = od_bbox[:, 0]
		# ymin = od_bbox[:, 1]
		xmax = od_bbox[:, 2]
		ymax = od_bbox[:, 3]

		in_window = (x_min > w_llim  &  xmax < w_ulim  &  ymax < h_ulim)
		print(in_window.shape) # (n)
		return in_window

	def is_close_to_collision(self, od_bbox=None, min_dists=None, *, return_min_dist=False, thres=D2C_THRESHOLD):
		if od_bbox is None:
			od_bbox = self.object_detection()
		if min_dists is None:
			point_cloud = self.point_cloud()
			min_dists = self.distance_to_collision(od_bbox=od_bbox, point_cloud=point_cloud)

		min_dists = min_dists[self._boxes_in_window(od_bbox)]

		min_dist = min_dists[np.isfinite(min_dists)].min()
		is_close = min_dist < D2C_THRESHOLD

		if return_min_dist:
			return is_close, min_dist
		else:
			return is_close

	