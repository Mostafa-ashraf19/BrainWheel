"""Computer Vision Module for Electrical Wheelchair Graduation Project 2020-2021.
Version 2.0

Written by:
	Pierre Nabil
	Panse Yasser
"""
# imports

import torch
import numpy as np
import cv2 as cv

try:
	from utils.general import (check_img_size, set_logging, non_max_suppression,
								scale_coords)
	from models.experimental import attempt_load
	from utils.datasets import letterbox
	from utils.plots import plot_one_box
except ModuleNotFoundError:
	from od_model.utils.general import (check_img_size, set_logging, non_max_suppression,
								scale_coords)
	from od_model.models.experimental import attempt_load
	from od_model.utils.datasets import letterbox
	from od_model.utils.plots import plot_one_box

# constants
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
half = device.type != 'cpu'

conf_thres = 0.25
iou_thres = 0.45
classes = None
agnostic_nms = False


# models
class ODModel:
	def __init__(self):
		self.model = attempt_load('./yolov3.pt', map_location=device)
		imgsz = check_img_size(640, s=self.model.stride.max())
		if half:
			self.model.half()
		self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
		self.colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in self.names]

		img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
		self.model(img.half() if half else img) if device.type != 'cpu' else None  # run once

	def predict(self, img):
		img0 = img

		img = letterbox(img, new_shape=640)[0]
		img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
		img = np.ascontiguousarray(img)
		img = torch.from_numpy(img).to(device)
		img = img.half() if half else img.float()
		if img.ndimension() == 3:
			img = img.unsqueeze(0)
		img /= 255.0

		pred_bbox = self.model(img, augment=False)[0]
		pred_bbox = non_max_suppression(pred_bbox, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)[0]

		gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
		if len(pred_bbox):
			# Rescale boxes from img_size to img0 size
			pred_bbox[:, :4] = scale_coords(img.shape[2:], pred_bbox[:, :4], img0.shape).round()

		return pred_bbox

	def show_on_image(self, img, pred_bbox, show=False, keep_showing=False):
		if len(pred_bbox):
			# Write results
			for *xyxy, conf, cls in reversed(pred_bbox):
				label = f'{self.names[int(cls)]} {conf:.2f}'
				plot_one_box(xyxy, img, label=label, color=self.colors[int(cls)], line_thickness=3)

		if show:
			cv.imshow('Object Detection', img)
			if not keep_showing:
				cv.waitKey(0)
				cv.destroyWindow('Object Detection')

		return img

	def _get_model_weights_file(self):
		return './yolov3.pt'

class ODModelTiny(ODModel):
	def _get_model_weights_file(self):
		return './yolov3-tiny.pt'


if __name__ == '__main__':
	od_model = ODModel()
	od_model_tiny = ODModelTiny()

	# for i in range(22):
	s = './img_test.jpeg'
	img = cv.imread(s)
	img = cv.resize(img, (640,320))

	pred = od_model.predict(img)
	# pred_tiny = od_model_tiny.predict(img)

	print(pred[:3])

	od_model.show_on_image(img, pred, show=True)
	# od_model_tiny.show_on_image(img, pred, show=True)