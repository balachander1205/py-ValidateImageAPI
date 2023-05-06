from imutils import paths
import logging
import argparse
import cv2
import os
from PIL import Image
import numpy as np
from numpy import asarray
from commons import get_image
import blur_detector

def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

'''
	check image blurness by applying laplacian transformation
'''
def do_blur_detection(imagePath):
	try:
		if(len(str(imagePath)) == 0):
			return "NA"
		image = get_image(imagePath, 'cv2')
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		fm = variance_of_laplacian(gray)
		text = "false"
		# if the focus measure is less than the supplied threshold,
		# then the image should be considered "blur"
		if fm < 100:
			text = "true"
		print("isblur=",text)
		return text
	except Exception as e:
		logging.debug("Xception@do_blur_detection="+str(e))

def blur_detection(image):
	try:
		img = cv2.imread(image, 0)
		blur_map = blur_detector.detectBlur(img, downsampling_factor=4, num_scales=4, scale_start=2, num_iterations_RF_filter=3)
		print(blur_map)
		cv2.imshow('ori_img', img)
		cv2.imshow('blur_map', blur_map)
		cv2.waitKey(0)
	except Exception as e:
		print(e)
		logging.debug("Xception@blur_detection="+str(e))

'''
	get file format i.e., jpeg/png/jpg etc..
'''
def get_file_format(imagePath):
	try:
		_file_format_ = "NA"
		if(len(str(imagePath)) == 0):
			_file_format_ = "NA"
		else:
			_format_ = os.path.splitext(imagePath)
			_file_format_ = _format_[1]
	except Exception as e:
		logging.debug("Xception@get_file_format="+str(e))
	return _file_format_

# image = 'D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_003.jpg'
#(do_blur_detection(image))
# blur_detection(image)