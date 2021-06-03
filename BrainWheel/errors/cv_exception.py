""" Exceptions module for Computer Vision Class.
"""
from .base import BrainWheelException

class CVException(BrainWheelException):
	pass

class CameraNotConnectedError(CVException):
	def __init__(self, err):
		self.err = str(err)
	def __str__(self):
		return f'ZED camera is not connected. "{self.err}"'

class NoImageError(CVException):
	def __str__(self):
		return 'Must add an image to the function to use this feature.'
