from PIL import Image
import requests
import cv2
import urllib.request
import numpy as np
from datetime import datetime
import uuid
import configparser
import logging

config = configparser.RawConfigParser()
config.read('static/config/config.properties')


'''
	get image from url/path
'''
def get_image(url, type):
	try:
		isurl = 'false'
		if ('http://' in url) or ('https://' in url):
			isurl = 'true'
		# print("isurl=",isurl, " type="+type)
		# type=PIL
		if(isurl=='true' and type=='pil'):
			im = Image.open(requests.get(url, stream=True).raw)
		if(isurl=='false' and type=='pil'):
			im = Image.open(url)
		# type=cv2
		if(isurl=='false' and type=='cv2'):
			im = cv2.imread(url)
		if(isurl=='true' and type=='cv2'):
			req = urllib.request.urlopen(url)
			arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
			im = cv2.imdecode(arr, -1)

		# show image
		# if(type=='cv2'):
			# cv2.imshow("Image", im)
			# cv2.waitKey(0)
		# if(type=='pil'):
			# im.show()
		return im		
	except Exception as e:
		logging.debug("Exception@get_image="+str(e))

'''
	get image resolution
'''
def get_resolution(image):
  im = get_image(image, "cv2")
  h, w, c = im.shape
  return (h, w)

def get_uuid():
	now_1 = datetime.now()
	cur_datetime = now_1.strftime("%Y-%m-%d %H:%M")
	uid = uuid.uuid1()
	return cur_datetime, uid

'''
	get signatrue image dimensions from properties file
'''
def get_sign_img_dim():
	sign_height = config.get('signature', 'signature_height')
	sign_width = config.get('signature', 'signature_width')
	return sign_height, sign_width

'''
	get face image dimensions from properties file
'''
def get_face_img_dim():
	face_height = config.get('face', 'face_height')
	face_width = config.get('face', 'face_width')
	return face_height, face_width


# url = 'https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg'
#print(get_face_img_dim())
#print(get_sig_img_dim())	
#get_image(url, 'cv2')
