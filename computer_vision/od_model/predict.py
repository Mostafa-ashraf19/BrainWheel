# Imports
import numpy as np
import cv2
import torch.backends.cudnn as cudnn
import torch.onnx

from .easydet.model import Darknet
from .easydet.utils import (select_device, load_darknet_weights,
                            non_max_suppression, plot_one_box)

# Arguments:

class args:
    # cfg = "cfgs/yolov3.cfg"
    # names = "data/coco.names"
    # weights = "weights/yolov3.pth"
    image_size = 608
    confidence_threshold = 0.3
    iou_threshold = 0.6
    device = ""     # device id (i.e. 0 or 0,1) or cpu. (default="")
    classes = None
    agnostic_nms = False

    config_dir = "computer_vision/od_model/"

# Constants:

CLASS_NAMES = [
	'person', 			'bicycle', 		'car', 			'motorcycle', 	'airplane', 
	'bus', 				'train', 		'truck', 		'boat', 		'traffic light', 
	'fire hydrant',		'stop sign', 	'parking meter','bench', 		'bird',
	'cat', 				'dog', 			'horse', 		'sheep', 		'cow',
	'elephant', 		'bear', 		'zebra', 		'giraffe', 		'backpack', 
	'umbrella', 		'handbag', 		'tie', 			'suitcase', 	'frisbee', 
	'skis', 			'snowboard', 	'sports ball', 	'kite', 		'baseball bat', 
	'baseball glove',	'skateboard',	'surfboard', 	'tennis racket','bottle', 
	'wine glass', 		'cup', 			'fork', 		'knife', 		'spoon', 
	'bowl', 			'banana', 		'apple', 		'sandwich', 	'orange', 
	'broccoli', 		'carrot', 		'hot dog', 		'pizza', 		'donut', 
	'cake', 			'chair', 		'couch', 		'potted plant',	'bed', 
	'dining table', 	'toilet', 		'tv', 			'laptop', 		'mouse', 
	'remote', 			'keyboard', 	'cell phone', 	'microwave', 	'oven', 
	'toaster', 			'sink', 		'refrigerator', 'book', 		'clock', 
	'vase', 			'scissors', 	'teddy bear', 	'hair drier',	'toothbrush'
]

CLASS_COLORS = [
	(220, 20, 60), (119, 11, 32), (  0,  0,142), (  0,  0,230), (  0,  0,  0),
	(  0, 60,100), (  0, 80,100), (  0,  0, 70), (  0,  0,  0), (250,170, 30),
	(  0,  0,  0), (220,220,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
	(  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0), (  0,  0,  0)
]

USEFUL_CLASSES = [
	0 ,  1,  2,  3,  4,	 5,  6,  
	7 ,  9,	10,	11, 12, 13, 15, 
	16,	24, 26, 28, 56, 57,	58,
	59,	60, 61, 68,	69, 72, 75
]

# Class

class ODModel:
    def __init__(self):
        self.device = select_device(args.device)
        self.image_shape = (args.image_size, args.image_size)
        
        self.model = Darknet(self._get_config(), args.image_size)
        load_darknet_weights(self.model, self._get_weights())
        self.model.to(self.device)
        self.model.eval()
        if self.device.type != "cpu":
            self.model(torch.zeros((1, 3, args.image_size, args.image_size), device=self.device))

    def predict(self, img):
        input_img_shape = img.shape
        img = cv2.resize(img, self.image_shape)
        image = torch.from_numpy(img).to(self.device)
        image = image.float() / 255.0

        if image.ndimension() == 3:     # add (m, ...)
            image = image.unsqueeze(0)
        if image.shape[1] != 3:         # (m, c, h, w) instad of (m, h, w, c)
            image = np.transpose(image, (0,3,1,2))

        pred_bbox = self.model(image)[0]

        pred_bbox = non_max_suppression(pred_bbox, args.confidence_threshold, args.iou_threshold,
                                      multi_label=False, classes=args.classes,
                                      agnostic=args.agnostic_nms)

        pred_bbox = self._fix_bbox(pred_bbox, input_img_shape)
        return pred_bbox

    def show_on_image(self, img, pred_bbox, show=False, keep_showing=False):
        for *xyxy, confidence, class_id in pred_bbox:
            if class_id in USEFUL_CLASSES:
                label = f"{CLASS_NAMES[int(class_id)]} {confidence * 100:.2f}%"
                plot_one_box(xyxy, img, label=label, color=CLASS_COLORS[int(class_id)])

        if show:
            cv2.imshow('Object Detection', img)
            if not keep_showing:
                cv2.waitKey(0)
                cv2.destroyWindow('Object Detection')
        return img

    def _fix_bbox(self, pred_bbox, input_img_shape):
        pred_bbox = pred_bbox[0]
        
        height_ratio = input_img_shape[0] / self.image_shape[0]
        width_ratio  = input_img_shape[1] / self.image_shape[1]

        pred_bbox[:, 0] *= width_ratio  # x_min
        pred_bbox[:, 1] *= height_ratio # y_min
        pred_bbox[:, 2] *= width_ratio  # x_max
        pred_bbox[:, 3] *= height_ratio # y_max

        return pred_bbox



    def _get_weights(self):
        return args.config_dir + "weights/yolov3.weights"

    def _get_config(self):
        return args.config_dir + "cfgs/yolov3.cfg"


class ODModelTiny(ODModel):
    def _get_weights(self):
        return args.config_dir + "weights/yolov3-tiny.weights"

    def _get_config(self):
        return args.config_dir + "cfgs/yolov3-tiny.cfg"


class ODModelSPP(ODModel):
    def _get_weights(self):
        return args.config_dir + "weights/yolov3-spp.weights"

    def _get_config(self):
        return args.config_dir + "cfgs/yolov3-spp.cfg"