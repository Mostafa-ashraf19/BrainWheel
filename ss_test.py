import cv2
from time import time

from BrainWheel.computer_vision.ss_model import SSModel, SSModelTiny


def test(big_model=True, tiny_model=False):
	if big_model:
		ss_model = SSModel()
	if tiny_model:
		ss_model_tiny = SSModelTiny()

	s = './BrainWheel/computer_vision/test images/ test02.jpeg'
	img = cv2.imread(s)
	print(img.shape)

	t0 = time()
	if big_model:
		pred = ss_model.predict(img)
	t1 = time()
	if tiny_model:
		pred_tiny = ss_model_tiny.predict(img)
	t2 = time()

	if big_model:
		print()
		print('model time:      {:.2f} secs'.format(t1-t0))
		ss_model.show_on_image(img, pred, show=True)
	if tiny_model:
		print()
		print('tiny model time: {:.2f} secs'.format(t2-t1))
		ss_model_tiny.show_on_image(img, pred_tiny, show=True)


if __name__ == "__main__":
	test(False, True)