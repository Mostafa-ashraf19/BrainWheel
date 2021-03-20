""" Exceptions module for Computer Vision Class.
"""

class CVException(Exception):
	pass

class CameraNotConnectedError(CVException):
	def __str__(self):
		return 'ZED camera is not connected.'
