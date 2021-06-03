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

from ..errors import CameraNotConnectedError, NoImageError
from .occupancy_grid import ransac_plane_fit, abs_dist_to_plane, get_free_space

# from .od_model import ODModel
# from .od_model import ODModelTiny as ODModel
# from .ss_model import SSModel

# Constants

ZED_IMG_RESOLUTION = sl.RESOLUTION.HD720
ZED_CAM_FPS = 30
ZED_COORDINATE_UNITS = sl.UNIT.CENTIMETER
ZED_DEPTH_MODE = sl.DEPTH_MODE.PERFORMANCE

D2C_THRESHOLD = 73
#D2C_THRESHOLD = 150

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
			raise CameraNotConnectedError(err)

		# machine learning models
		# self.od_model = ODModel()
		# self.ss_model = SSModel()

	def __del__(self):
		self.zed.close()

	def loop(self, *, l_img=False, r_img=False, depth_map=False, depth_map_img=False, point_cloud=False,
					od_bbox=False, od_img=False, ss_pred=False, ss_img=False,
					dist_to_col=False, dist_to_col_img=False,
					is_close=False, min_dist=False, is_close_simple=False, min_dist_simple=False):
		"""Main generator function for the ComputerVision class.
		
		Preforms all prerequisite functions to return any and all required data from the CV module.
		May also be used in for loops as follows:
		```python
		CV = ComputerVision()
		for cache in CV.loop(data1=True, data2=True, ..., dataN=True):
			data1, data2, ..., dataN = cache
			# use data1 to dataN directly ...
		```

		Order of returned Parameters:
			- l_img
			- r_img
			- depth_map
			- depth_map_img
			- point_cloud
			- od_bbox
			- od_img
			- ss_pred
			- ss_img
			- dist_to_col (aka: min_dists)
			- dist_to_col_img
			- is_close
			- min_dist
			- is_close_simple
			- min_dist_simple
		
		Parameterss:
			all parameters are bools that if set to true, will be returned in the order described above
			(not in the order of being called!)
		Returns:
			all parameters that have been set to True.
		"""
		is_c = is_close or min_dist
		is_c_s = is_close_simple or min_dist_simple
		d2c = dist_to_col or dist_to_col_img or is_c
		od = od_bbox or od_img or d2c
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
					if depth_map:
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
					_od_bbox = self.object_detection(_l_img, return_image=od_img)
					if od_img:
						_od_bbox, _od_img = _od_bbox
					if od_bbox:
						cache.append(_od_bbox)
					if od_img:
						cache.append(_od_img)

				if ss:
					_ss_pred = self.semantic_segmentation(_l_img, return_image=ss_img)
					if ss_img:
						_ss_pred, _ss_img = _ss_pred
					if ss_pred:
						cache.append(_ss_pred)
					if ss_img:
						cache.append(_ss_img)

				if d2c:
					_dist_to_col = self.distance_to_collision(_od_bbox, _point_cloud, image=_l_img, return_image=dist_to_col_img)
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
			return_img=False
				if True, the function will also return an image of the depth map.
				else, the function will return the depth map only (without the image).

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
		"""Uses a ML model (Yolov3-Tiny) to detect objects in the picture.

		Parameters:
			img=None
				Image for detection.
				if None, the function will use a new image.
			return_img=False
				if True, the function will also return the image of the OD model's prediction.
				else, the function will return the model prediction only (without the image).
			show=False
				Bool to show if the user wants to see the object detection image.
			keep_showing=False
				Bool to define whether the user wants to continue with the code while
				keeping the show window. If False, the code execution will stop until
				the window is closed.

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
				Image for detection.
				if None, the function will use a new image.
			return_img=False
				if True, the function will also return the image of the SS model's prediction.
				else, the function will return the model prediction only (without the image).
			show=False
				Bool to show if the user wants to see the semantic segmentation image.
			keep_showing=False
				Bool to define whether the user wants to continue with the code while
				keeping the show window. If False, the code execution will stop until
				the window is closed.

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
		if point_cloud is None or ss_pred is None:
			gen = self.loop(point_cloud=True, ss_pred=True)
			point_cloud, ss_pred = next(gen)
		
		x, y, z = ... # get coordinates from point cloud

		road_mask = np.zeros(ss_pred.shape)
		road_mask[ss_pred == 0] = 1 # Check that road class id == 0
		# road_mask[ss_pred == 1] = 1 # Check that sidewalk class id == 1

		x, y, z = x[road_mask == 1], y[road_mask == 1], z[road_mask == 1]
		xyz_ground = np.stack((x,y,z))

		p_final = ransac_plane_fit(xyz_ground)
		dist = abs_dist_to_plane(p_final, x, y, z)

		ground_mask = np.zeros(dist.shape)
		ground_mask[dist < 0.1] = 1

		occ_grid = get_free_space(ground_mask, point_cloud)
		occ_grid_img = np.flip(occ_grid, axis=1)

		if show:
			cv2.imshow('Occupancy Grid', occ_grid_img)
			if not keep_showing:
				cv2.waitKey(0)
				cv2.destroyWindow('Occupancy Grid')

		if return_image:
			return occ_grid, occ_grid_img
		else:
			return occ_grid

	
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

	def distance_to_collision(self, od_bbox=None, point_cloud=None, *, image=None, return_image=False, show=False, keep_showing=False):
		"""Calculates the minimum distance to all detected objects.

		Parameters:
			od_bbox
				output of the OD model computed on the current frame.
			point_cloud
				point_cloud of the frontal view of the camera.
			image
				the current image which is used for showing the prediction on the image.
			return_img=False
				if True, the function will also return an image showing the distance to each object.
				else, the function will return the minimum distances only (without the image).
			show=False
				Bool to show if the user wants to see the distance to collision image.
			keep_showing=False
				Bool to define whether the user wants to continue with the code while
				keeping the show window. If False, the code execution will stop until
				the window is closed.

		Returns:
			min_dists
				the minimum distance for every detected object in the current frame
			dists_img
				the image showing the minimum distance to each object
		"""
		if point_cloud is None or od_bbox is None:
			gen = self.loop(point_cloud=True, od_bbox=True)
			point_cloud, od_bbox = next(gen)

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
		"""Returns a window slice object for the image where objects must be detected.

		Helper Function!
		"""
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
		"""Checks if the camera is close to collsion.

		Parameters:
			depth_map=None
				depth map of current frame.
				if None, the function will compute the depth map of a newly captures frame.

			return_min_dist=False
				if True, the function will also return the minimum distance to the closest object.
				else, the function will return the boolian value only.
			thres
				defines a threshold for detecting whether the object is "close" or "not close".

		Returns:
			is_close
				a boolean to show whether the distance to the closest object is less than
				the given threshold
			min_dist
				the minimum distance to the closest object.
		"""
		if depth_map is None:
			depth_map = self.depth_map()
		depth_map = depth_map.get_data()

		# min_dist = depth_map[self._window()].min()
		min_dist = depth_map[np.isfinite(depth_map)].min()
		is_close = min_dist < D2C_THRESHOLD

		if return_min_dist:
			return is_close, min_dist
		else:
			return is_close

	def _boxes_in_window(self, od_bbox):
		"""Return a boolean vector that shows for each bounding box in od_bbox, if it is in the window or not.
		
		Helper Function!
		"""
		(h_llim, h_ulim), (w_llim, w_ulim) = self._window(get_lims=True)
		xmin = od_bbox[:, 0]
		# ymin = od_bbox[:, 1]
		xmax = od_bbox[:, 2]
		# ymax = od_bbox[:, 3]

		in_window = (xmax > w_llim  &  xmin < w_ulim)
		print(in_window.shape) # (n)
		return in_window

	def is_close_to_collision(self, od_bbox=None, min_dists=None, *, return_min_dist=False, thres=D2C_THRESHOLD):
		"""Checks if the camera is close to collsion.

		Parameters:
			od_bbox
				output of the OD model computed on the current frame.
			min_dists
				the minimum distance to each object in od_bbox.

			return_min_dist=False
				if True, the function will also return the minimum distance to the closest object.
				else, the function will return the boolian value only.
			thres
				defines a threshold for detecting whether the object is "close" or "not close".

		Returns:
			is_close
				a boolean to show whether the distance to the closest object is less than
				the given threshold
			min_dist
				the minimum distance to the closest object.
		"""
		if od_bbox is None or min_dists is None:
			gen = self.loop(od_bbox=True, dist_to_col=True)
			od_bbox, dist_to_col = next(gen)

		min_dists = min_dists[self._boxes_in_window(od_bbox)]

		min_dist = min_dists[np.isfinite(min_dists)].min()
		is_close = min_dist < D2C_THRESHOLD

		if return_min_dist:
			return is_close, min_dist
		else:
			return is_close

	