import cv2
from time import time

from od_model import ODModel, ODModelTiny

def test(yolo=True, yolo_tiny=False):
    if yolo:
        od_model = ODModel()
        img_shape = od_model.image_shape
    if yolo_tiny:
        od_model_tiny = ODModelTiny()
        img_shape = od_model_tiny.image_shape


    s = './computer_vision/test images/test02.jpeg'
    img = cv2.imread(s)
    img = cv2.resize(img, (720,360))


    t0 = time()
    if yolo:
        pred = od_model.predict(img)
    t1 = time()
    if yolo_tiny:
        pred_tiny = od_model_tiny.predict(img)
    t2 = time()


    if yolo:
        print()
        print('yolov3 time:      {:.2f} secs'.format(t1-t0))
        print('and predicted {} objects'.format(len(pred)))
    if yolo_tiny:
        print()
        print('yolov3_tiny time: {:.2f} secs'.format(t2-t1))
        print('and predicted {} objects'.format(len(pred_tiny)))


    # if yolo:
    #     print()
    #     print('output_format: (xmin, ymin, xmax, ymax, prob, class_id)')
    #     print(pred[:3])
    #     print(pred.shape)

    #     od_model.show_on_image(img, pred, show=True)
    # elif yolo_tiny:
    #     print('output_format: (xmin, ymin, xmax, ymax, prob, class_id)')
    #     print(pred_tiny[:3])
    #     print(pred_tiny.shape)

        od_model_tiny.show_on_image(img, pred_tiny, show=True)

if __name__ == "__main__":
    test(False, True)