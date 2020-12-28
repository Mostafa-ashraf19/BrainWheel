"""Computer Vision Module for Electrical Wheelchair Graduation Project 2020-2021.

Written by:
	Pierre Nabil
	Panse Yasser
"""

#Imports
from typing import Any, Union, Tuple

import numpy as np
import cv2 as cv

import os
import glob

from od_model.predict import ObjectDetection as ODModel
# from od_model.predict import ObjectDetectionTiny as ODModel
from ss_model.predict import SSModel
from utils.utils import *


# Constants
L_CAM_NUM, R_CAM_NUM = 0, 1
IMG_WIDTH, IMG_HEIGHT = 640, 480
CHECKERBOARD_DIM = (11, 19)
CALIB_IMGS_DIR = './Checkerboard Images'

OD_USEFUL_CLASSES = [0, 1, 2, 3, 4, 6, 7, 8, 11, 14, 16, 17, 57, 58, 60, 61, 62, 63, 72, 73]


# VALUES TO TWEAK
#	Projection Matrix Constants
BASELINE = 0.15

#	Disparity Map Constants
NUM_DISPARITIES = 6*16	# multiple of 16
BLOCK_SIZE = 11
MIN_DISPARITY = 0		# should be zero (but can be >0)
WINDOW_SIZE = 6



class ComputerVision:
	"""Class for the entire Computer Vision Part of the Project.

	Can Create an Instance or work directly with the class functions.
	"""

	def __init__(self, calibrate=False, baseline=BASELINE, calib_imgs_dir=CALIB_IMGS_DIR):
		"""Constructor for the class.

		Creates 2 camera objects, calibrates the cameras, and fetches the ML models.

		Parameters:
			baseline=BASELINE
				Defines the horizontal distance between both cameras for calibration.
				Assumes no vertical or frontal distance.
			show_calibration=False
				Bool to show if the user wants to see the calibration process.
		"""
		self._l_cam = cv.VideoCapture(L_CAM_NUM)
		self._r_cam = cv.VideoCapture(R_CAM_NUM)

		self._l_cam.set(3, IMG_WIDTH)
		self._l_cam.set(4, IMG_HEIGHT)
		self._r_cam.set(3, IMG_WIDTH)
		self._r_cam.set(4, IMG_HEIGHT)

		if calibrate:
			self._set_proj_mat(baseline, calib_imgs_dir)
		else:
			proj_mats = np.load('projection_matricies.npz')
			self.l_proj_mat = proj_mats['l_proj_mat']
			self.r_proj_mat = proj_mats['r_proj_mat']

		self.l_img = None
		self.r_img = None

		self.od_model = ODModel((IMG_HEIGHT, IMG_WIDTH))
		self.ss_model = SSModel((IMG_HEIGHT, IMG_WIDTH))

	def _clear_img(self):
		"""Used to clear the current images in the cache.

		Private Function!
		"""
		self.l_img = None
		self.r_img = None

	# noinspection PyUnboundLocalVariable
	def _set_proj_mat(self, baseline=BASELINE, imgs_dir=CALIB_IMGS_DIR):
		"""Used to calibrate the cameras and create the projection matricies.

		Private Function!

		Parameters:
			baseline=BASELINE
				Defines the horizontal distance between both cameras for calibration.
				Assumes no vertical or frontal distance.
			show=False
				Bool to show if the user wants to see the calibration process.
		"""
		criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

		# Creating vector to store vectors of 3D points for each checkerboard image
		objpoints = []
		# Creating vector to store vectors of 2D points for each checkerboard image
		img_points = []

		# Defining the world coordinates for 3D points
		objp = np.zeros((1, CHECKERBOARD_DIM[0] * CHECKERBOARD_DIM[1], 3), np.float32)
		objp[0, :, :2] = np.mgrid[0:CHECKERBOARD_DIM[0], 0:CHECKERBOARD_DIM[1]].T.reshape(-1, 2)

		# Extracting path of individual image stored in a given directory
		images = glob.glob(os.path.join(imgs_dir, '*.jpg'))
		for f_name in images:
			current_img = cv.imread(f_name)
			gray = cv.cvtColor(current_img, cv.COLOR_BGR2GRAY)
			gray = cv.resize(gray, (IMG_HEIGHT, IMG_WIDTH))
			# Find the chess board corners
			# If desired number of corners are found in the image then ret = true
			ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD_DIM,
					cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

			# If desired number of corner are detected,
			# we refine the pixel coordinates and display
			# them on the images of checker board

			if ret:
				objpoints.append(objp)
				# refining pixel coordinates for given 2d points.
				corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

				img_points.append(corners2)

				# Draw and display the corners
				current_img = cv.drawChessboardCorners(current_img, CHECKERBOARD_DIM, corners2, ret)
	
			cv.imshow('Calibration Image', current_img)
			cv.waitKey(0)
		
		cv.destroyWindow('Calibration Image')

		# Performing camera calibration by
		# passing the value of known 3D points (objpoints)
		# and corresponding pixel coordinates of the
		# detected corners (img_points)

		_, intrinsic_mtx, *_ = cv.calibrateCamera(objpoints, img_points, gray.shape[::-1], None, None)

		# Initialize the left and right projection matrecies
		# and set the left camera as the origin and the right
		# camera as shifted by the baseline.

		self.l_proj_mat = np.zeros((3, 4))
		self.l_proj_mat[:, :3] = intrinsic_mtx
		self.r_proj_mat = self.l_proj_mat.copy()
		self.r_proj_mat[1, 3] = baseline

		np.savez('projection_matricies.npz', l_proj_mat=self.l_proj_mat, r_proj_mat=self.r_proj_mat)

	def _compute_left_disparity_map(self, l_img=None, r_img=None, show=False, keep_showing=False):
		"""Computes the disparity map relative to the left image.

		Private Function!

		Parameters:
			l_img=None
				left image.
				if None, the function will take the cached image or use a new image.
			r_img=None
				right image.
				if None, the function will take the cached image or use a new image.
			show=False
				Bool to show if the user wants to see the disparity map.

		Returns:
			disp_map
				The calculated disparity map.
		"""
		if l_img is None and r_img is None:
			# if there are no images as function args, get current images
			if self.l_img is None:
				l_img, r_img = self.capture()
				self._clear_img()
			else:
				l_img = self.l_img
				r_img = self.r_img
		elif l_img is None or r_img is None:
			# if only one image is provided, raise an error
			raise Exception('Only one image was provided, Required two.')

		#TODO: Review if this is neccessary
		l_img = cv.cvtColor(l_img, cv.COLOR_BGR2GRAY)
		r_img = cv.cvtColor(r_img, cv.COLOR_BGR2GRAY)

		matcher_SGBM = cv.StereoSGBM_create(
			minDisparity=MIN_DISPARITY,
			numDisparities=NUM_DISPARITIES,
			blockSize=BLOCK_SIZE,
			P1=8 * 3 * WINDOW_SIZE ** 2,
			P2=32 * 3 * WINDOW_SIZE ** 2,
			mode=cv.STEREO_SGBM_MODE_SGBM_3WAY
		)

		disp_map = matcher_SGBM.compute(l_img, r_img).astype(np.float32)/16

		if show:
			disp_map_img = disp_map.astype(np.uint8)
			disp_map_img = 255 - disp_map_img
			disp_map_img = cv.applyColorMap(disp_map_img, cv.COLORMAP_JET)
			cv.imshow('Disparity Map', disp_map_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Disparity Map')

		return disp_map

	def _xyz_from_depth(self, depth_map):
		"""Used to calculate the x, y and z coordinates from a given depth map.

		Private Function!

		Parameters:
			depth_map
				depth map to extract the coordinates from.

		Returns:
			x, y, z
				The calculated coordinates of every point in the disparity map.
		"""
		h, w = depth_map.shape
		# noinspection PyTypeChecker
		c_u, c_v, f = self.l_proj_mat[0, 2], self.l_proj_mat[1, 2], self.l_proj_mat[0, 0]

		x = np.zeros((h, w))
		y = np.zeros((h, w))
		z = depth_map

		for i in range(h):
			y[i, :] = ((i + 1 - c_v) * depth_map[i, :]) / f

		for j in range(w):
			x[:, j] = ((j + 1 - c_u) * depth_map[:, j]) / f

		return x, y, z

	def _get_free_space(self, ground_mask, depth_map):
		"""Computes the Occupancy Grid from the ground mask and depth map.

		Private Function!

		Parameters:
			ground_mask
				ground mask from the SS of the current frame
			depth_map
				depth map of the current frame

		Returns:
			occ_grid
				the Occupancy Grid of the current frame
		"""
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

	def capture(self, show=False, keep_showing=False):
		"""Fetches left and right images from cameras and places them in the cache.
		
		Parameters:
			show=False
				Bool to show if the user wants to see the left and right images.

		Returns:
			left and right images fetched.
		"""
		while True:
			l_success, self.l_img = self._l_cam.read()
			r_success, self.r_img = self._r_cam.read()
			break

		if not (l_success and r_success):
			raise Exception('Cannot get next frame from cameras.')

		# self.l_img = cv.cvtColor(self.l_img, cv.COLOR_BGR2RGB)
		# self.r_img = cv.cvtColor(self.r_img, cv.COLOR_BGR2RGB)

		if show:
			double_img = np.hstack((self.l_img, self.r_img))
			cv.imshow('Camera Inputs', double_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Camera Inputs')

		return self.l_img, self.r_img

	def compute_depth_map(self, l_img=None, r_img=None, show=False, show_disp=False, keep_showing=False):
		"""Computes the depth map of the image.

		(No Need to use compute_left_disparity_map() first)

		Parameters:
			l_img=None
				left image.
				if None, the function will take the cached image or use a new image.
			r_img=None
				right image.
				if None, the function will take the cached image or use a new image.
			show=False
				Bool to show if the user wants to see the depth map.

		Returns:
			depth_map
				The calculated depth map.
		"""
		if l_img is None and r_img is None:
			# if there are no images as function args, get current images
			if self.l_img is None:
				l_img, r_img = self.capture()
				self._clear_img()
			else:
				l_img = self.l_img
				r_img = self.r_img
		elif l_img is None or r_img is None:
			# if only one image is provided, raise an error
			raise Exception('Only one image was provided, Required two.')

		disp_map = self._compute_left_disparity_map(l_img, r_img, show_disp, keep_showing)

		k_left, r_left, t_left, *_ = cv.decomposeProjectionMatrix(self.l_proj_mat)
		k_right, r_right, t_right, *_ = cv.decomposeProjectionMatrix(self.r_proj_mat)

		t_left  = t_left  / t_left[3]
		t_right = t_right / t_right[3]

		# focal length
		f = k_left[0, 0]
		# get baseline
		b = t_left[1] - t_right[1]
		# Replace all instances of 0 or -ve disparity with a small minimum value (to avoid div by 0 or -ve values)
		disp_map[disp_map <= 0] = 0.1

		# Initialize the depth map to match the size of the disparity map
		depth_map = np.ones(disp_map.shape, np.single)
		depth_map[:] = f * b / disp_map[:]

		if show:
			depth_map_img = depth_map.astype(np.uint8)
			depth_map_img = cv.applyColorMap(depth_map_img, cv.COLORMAP_JET)
			cv.imshow('Depth Map', depth_map_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Depth Map')

		return depth_map

	def object_detection(self, img=None, show=False, keep_showing=False):
		"""Uses a ML model (Yolov4) to detect objects in the picture.

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
			# if there are no images as function args, get current images
			if self.l_img is None:
				img, _ = self.capture()
				self._clear_img()
			else:
				img = self.l_img

		boxes, scores, classes, valid_detections = self.od_model.predict(img)
		pred_bbox = boxes, scores, classes, valid_detections
		pred_img = self.od_model.show(img, pred_bbox, show)

		if not keep_showing:
			cv.waitKey(0)
			cv.destroyWindow('Object Detection')

		return pred_bbox, pred_img

	def semantic_segmentation(self, img=None, show=False, keep_showing=False):
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
			# if there are no images as function args, get current images
			if self.l_img is None:
				img, _ = self.capture()
				self._clear_img()
			else:
				img = self.l_img

		pred, seg_img = self.ss_model.predict(img)

		if show:
			self.ss_model.show(img, seg_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Semantic Segmentation')

		return pred, seg_img

	def occupancy_grid(self, depth_map=None, segmentation=None, show=False, keep_showing=False):
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
		# Get depth_map and segmentation
		if depth_map is None and segmentation is None:
			l_img, r_img = self.capture()
			depth_map = self.compute_depth_map(l_img, r_img)
			segmentation = self.semantic_segmentation(l_img)
			self._clear_img()
		else:
			if depth_map is None:
				depth_map = self.compute_depth_map()
			if segmentation is None:
				segmentation = self.semantic_segmentation()

		# Get Ground Mask from segmentation
		x, y, z = self._xyz_from_depth(depth_map)

		road_mask = np.zeros(segmentation.shape)
		road_mask[segmentation == 0] = 1 # road_class_id = 0
		# road_mask[segmentation == 1] = 1 # side_walk_class_id = 1

		x, y, z = x[road_mask == 1], y[road_mask == 1], z[road_mask == 1]
		xyz_ground = np.stack((x, y, z))

		p_final = ransac_plane_fit(xyz_ground)
		dist = np.abs(dist_to_plane(p_final, x, y, z))

		ground_mask = np.zeros(dist.shape)
		ground_mask[dist < 0.1] = 1
		ground_mask[dist > 0.1] = 0

		occ_grid = self._get_free_space(ground_mask, depth_map)

		if show:
			occ_grid_img = np.flip(occ_grid, axis=1)
			cv.imshow('Occupancy Grid', occ_grid_img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Occupancy Grid')

		return occ_grid

	def distance_to_collision(self, od_data=None, depth_map=None):
		"""Calculates the minimum distance to all detected objects.

		Parameters:
			od_data
				output of the OD model computed on the current frame
			depth_map
				depth map of the current frame

		Returns:
			min_distances
				the minimum distance for every detected object in the current frame
		"""
		# Get depth_map and object_detection_data
		if depth_map is None and od_data is None:
			l_img, r_img = self.capture()
			depth_map = self.compute_depth_map(l_img, r_img)
			od_data = self.object_detection(l_img)
			self._clear_img()
		else:
			if depth_map is None:
				depth_map = self.compute_depth_map()
			if od_data is None:
				od_data = self.object_detection()

		x, y, z = self._xyz_from_depth(depth_map)
		boxes, scores, classes, valid_detections = od_data

		min_distances = []
		for i in range(valid_detections[0]):
			class_id = classes[0][i]
			if class_id in OD_USEFUL_CLASSES:
				x_min, y_min, x_max, y_max = boxes[0][i]
				x_min = int(x_min)
				y_min = int(y_min)
				x_max = int(x_max)
				y_max = int(y_max)

				box_x = x[y_min:y_max, x_min:x_max]
				box_y = y[y_min:y_max, x_min:x_max]
				box_z = z[y_min:y_max, x_min:x_max]

				box_distances = np.sqrt(box_x**2 + box_y**2 + box_z**2)

				min_distances.append(np.min(box_distances))

		return np.array(min_distances)

	# Add support for l_img, r_img in class_instance:
	# use 'q' to quit the loop
	def __iter__(self):
		return self

	def __next__(self):
		if cv.waitKey(1) & 0xFF == ord('q'):
			raise StopIteration
		return self.capture()


if __name__ == '__main__':
	CV = ComputerVision()

	#'''
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


	'''
	# General Test:
	for l_img, r_img in CV:
		double_img = np.hstack((l_img, r_img))
		cv.imshow('Camera Inputs', double_img)

		# Computing Disparity and Deapth Maps
		depth_map = CV.compute_depth_map(l_img, r_img, show=True, show_disp=True, keep_showing=True)

		# Object Detection
		od_data, od_img = CV.object_detection(l_img, show=True, keep_showing=True)

		# Semantic Segmentation
		seg_data, seg_img = CV.semantic_segmentation(l_img, show=True, keep_showing=True)

		# Occupancy Grid
		occ_grid = CV.occupancy_grid(depth_map, seg_data, show=True, keep_showing=True)

		# Distance to Collision
		min_dists = CV.distance_to_collision(od_data, depth_map)

		# Press 'q' to stop
	#'''

	cv.destroyAllWindows()
