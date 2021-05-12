import numpy as np
import cv2
import json
from time import time
import torch
import tarfile
import boto3
import sagemaker
from sagemaker.utils import name_from_base
from sagemaker.pytorch.model import PyTorchModel
from sagemaker.predictor import Predictor

from od_model.easydet.model import Darknet
from od_model.easydet.utils import (select_device, load_darknet_weights,
                                non_max_suppression, plot_one_box)

from od_model.predict import args, ODModel, ODModelTiny

def compress(tiny=False):
    # Import Model
    image_shape = [1, 3, args.image_size, args.image_size]
    ModelClass = ODModelTiny if tiny else ODModel
    model = Darknet(ModelClass._get_config(None), args.image_size)
    load_darknet_weights(model, ModelClass._get_weights(None))

    trace = torch.jit.trace(model.float().eval(), torch.zeros(image_shape).float())
    trace.save("model.pth")

    with tarfile.open("model.tar.gz", "w:gz") as f:
        f.add("model.pth")

    # Upload Model Archive to S3
    role = sagemaker.get_execution_role()
    sess = sagemaker.Session()
    region = sess.boto_region_name
    bucket = sess.default_bucket()

    name = "YoloV3-Tiny-Neo" if tiny else "YoloV3-Neo"
    compilation_job_name = name_from_base(name)
    prefix = compilation_job_name + "/model"

    model_path = sess.upload_data(path="model.tar.gz", key_prefix=prefix)

    data_shape = '{"input0":' + str(image_shape) + '}'
    target_device = "jetson_nano"
    framework = "PYTORCH"
    framework_version = torch.__version__[:3]
    compiled_model_path = "s3://{}/{}/output".format(bucket, compilation_job_name)
    entry_point = "yolov3_tiny.py" if tiny else "yolov3.py"

    # Create a PyTorch SageMaker Model
    sagemaker_model = PyTorchModel(
        model_data=model_path,
        predictor_cls=Predictor,
        framework_version=framework_version,
        role=role,
        sagemaker_session=sess,
        entry_point=entry_point,
        source_dir="code",
        py_version="py3",
        env={"MMS_DEFAULT_RESPONSE_TIMEOUT": "500"},
    )

    # Deploy the model
    predictor = compiled_model.deploy(initial_instance_count=1, instance_type="ml.c5.9xlarge")
    return predictor, sess

def delete_endpoint(predictor, sess):
    sess.delete_endpoint(predictor.endpoint_name)

def predict_test_image_on_model(predictor, image):
    input_img_shape = image.shape
    image = cv2.resize(image, (args.image_shape, args.image_shape)) / 255

    if image.ndim == 3:     # add (m, ...)
        image = np.expand_dims(image, 0)
    if image.shape[1] != 3:         # (m, c, h, w) instad of (m, h, w, c)
        image = np.transpose(image, (0,3,1,2))

    image = bytearray(image)

    response = predictor.predict(image)
    pred_bbox = json.loads(response.decode)
    print(pred_bbox)

    pred_bbox = non_max_suppression(pred_bbox, args.confidence_threshold, args.iou_threshold,
                                    multi_label=False, classes=args.classes,
                                    agnostic=args.agnostic_nms)

    pred_bbox = ODModel._fix_bbox(None, pred_bbox, input_img_shape)
    return pred_bbox


def test(predictor):
    s = './computer_vision/test images/test02.jpeg'
    img = cv2.imread(s)

    t0 = time()
    pred = predict_test_image_on_model(predictor, img)
    t1 = time()

    print()
    print('yolov3 time:      {:.2f} secs'.format(t1-t0))
    print('and predicted {} objects'.format(len(pred)))

if __name__ == "__main__":
    predictor, sess = compress(tiny=False)
    test(predictor)
    delete_endpoint(predictor, sess)
