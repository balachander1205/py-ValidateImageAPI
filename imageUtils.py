import logging
from flask import Flask,render_template, request,json,Response
from blurDetection import do_blur_detection
from faceDetection import is_face_valid
from binarizeImage import binarize
from signature_extractor import signature_extractor
import os
from urllib.request import urlopen
from commons import *
import configparser
from checkfullscan import is_full_scan
from getimagemetadata import *
from numpy import asarray

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

def validate_image_url(image_file_path):
	try:
		is_valid_url = False
		image_formats = ("image/png", "image/jpg", "image/jpeg")
		site = urlopen(image_file_path)
		meta = site.info()  # get header of the http request
		if meta["content-type"] in image_formats:  # check if the content-type is a image
			is_valid_url = True
	except Exception as e:
		logging.debug(e)
	return is_valid_url

def validate_input_file(image_file_path):
	try:
		isurl = False
		isfile = False
		msg = ''
		if ('http://' in image_file_path) or ('https://' in image_file_path):
			isurl = True
			isfile = validate_image_url(image_file_path)
		else:
			isfile = os.path.exists(image_file_path)
		logging.info("validate_input_file:isfile="+str(isfile)+ " isurl="+str(isurl))
		if(isurl==False and isfile==False):
			msg = 'File not found / invalid file'
		# print("isfile=",isfile, " isurl=",isurl)
		logging.info("validate_input_file2:isfile="+str(isfile)+ " isurl="+str(isurl))
	except Exception as e:
		logging.debug(e)
	return isfile, msg

def process_image(image_file_path, img_type, app_id, id, uid, cur_datetime):
	try:
		logging.info('process_image:image_file_path='+image_file_path+" img_type="+img_type)
		is_valid_file, msg = validate_input_file(image_file_path)
		if(is_valid_file):
			remarks = ""
			isblur1 = do_blur_detection(image_file_path)		
			# validate image background
			# validate_bg_img1 = binarize(image_file_path, img_type)
			isvalidimage = "false"
			# face
			if(img_type=="face"):
				# validate face
				validate_face1 = is_face_valid(image_file_path)		
				isvalidimage, remarks = validate_face_params(image_file_path, isblur1, validate_face1)
				print("face:_isblur1_=",isblur1," isvalidface=",isvalidimage," remarks=",remarks)
				logging.info("face:_isblur1_="+isblur1+" isvalidface="+isvalidimage+" remarks="+remarks)
			# signature		
			if(img_type=="sign"):
				isvalidimage, remarks = validate_sign_params(image_file_path, isblur1)
				print("sign:_isblur1_=",isblur1," isvalidsign=",isvalidimage," remarks=",remarks)
				logging.info("sign:_isblur1_="+isblur1+" isvalidsign="+isvalidimage+" remarks="+remarks)
			
			data = {
			'status':'OK',
			'imagefile':image_file_path,
			'createdatetime':cur_datetime,
			'candidate_id':id,
			'appid':app_id,            
			'reference_id': uid,
			'image_type': img_type,
			'isblur': isblur1,
			'isvalidimage': isvalidimage,
			'remarks':remarks
			}
		else:
			data = {
			'status':'ERROR',
			'imagefile':image_file_path,
			'createdatetime':cur_datetime,
			'candidate_id':id,
			'appid':app_id,            
			'reference_id': uid,
			'image_type': img_type,
			'isblur':'false',
			'isvalidimage':'false',
			'remarks': ("Invalid Image" if(img_type=="face") else "Invalid Signature")
			}
		return data		
	except Exception as e:
		logging.debug("process_image:Exception="+e)
		return {
			'status':'ERROR',
			'imagefile':image_file_path,
			'createdatetime':cur_datetime,
			'candidate_id':id,
			'appid':app_id,            
			'reference_id': uid,
			'image_type': img_type,
			'isblur':'false',
			'isvalidimage':'false',
			'remarks': str(e)
			}

def validate_face_params(image_file_path, isblur1, validate_face1):
	isvalidimage = "false"
	remarks = ""
	face_h, face_w = get_face_img_dim()
	face_hi, face_wi = get_resolution(image_file_path)
	print("face:Actual face Dim=",face_hi, face_wi)
	print("face:Required face Dim=",face_h, face_w)
	logging.info("Actual face Dim=height="+str(face_hi)+ " width="+str(face_wi))
	logging.info("Required face Dim=height="+str(face_h)+ " width="+str(face_w))
	try:
		# brightness = get_brightness(image_file_path)
		isbinaryimage = is_binary_image(image_file_path)
		# is_meta_data = get_img_meta_data(image_file_path)
		# print("brightness=",brightness)
		print("face:isbinaryimage=",isbinaryimage)
		# print("face:is_meta_data=",is_meta_data)
		brightness_threshold = int(config.get('image', 'brightness_threshold'))
		# if(int(brightness)>brightness_threshold):
			# isblur1 = "true"
		# Blur Image
		if(isblur1=="true"):
			print("face:if1....")
			isvalidimage = "false"
			remarks = config.get('face', 'blur_image')
			return isvalidimage, remarks
		if(isblur1=="false" and isbinaryimage==True):
			print("face:if2....")
			isvalidimage = "false"
			remarks = config.get('face', 'invalid_image')
			return isvalidimage, remarks
		# Invalid Image
		if(validate_face1=="false" and isblur1=="false"):
			print("face:if3....")
			isvalidimage = "false"
			remarks = config.get('face', 'invalid_image')
			return isvalidimage, remarks
		if(validate_face1=="true" and isblur1=="false" and isbinaryimage==False):
			print("face:if4....")
			isfullscan = is_full_scan(image_file_path, "face")			
			print("face:isfullscan=",isfullscan)
			if(isfullscan==True):
				if((len(str(face_hi))<=3) and (len(str(face_hi))<=3)):
					print("face:if5....")
					isvalidimage = "true"
					remarks = config.get('face', 'valid_image')
					return isvalidimage, remarks
				else:
					print("face:if5.1....")
					isvalidimage = "false"
					remarks = config.get('face', 'full_scan_image')
					return isvalidimage, remarks
			if(isfullscan==False):
				print("face:if6....")
				isvalidimage = "true"
				remarks = config.get('face', 'valid_image')
				return isvalidimage, remarks
			# Valid Image
			# if(((int(face_hi) <= int(face_h)) and (int(face_wi) <= int(face_w))) and isfullscan==False):
				# isvalidimage = "true"
				# remarks = config.get('face', 'valid_image')
			# Full Scan Image
			# elif(((int(face_hi) >= int(face_h)) or (int(face_wi) >= int(face_w))) and isfullscan==True):
				# isvalidimage = "false"
				# remarks = config.get('face', 'full_scan_image')
		print("validate_face_params::remarks=",remarks)
		return isvalidimage, remarks
	except Exception as e:
		logging.debug("Xception:validate_face_params="+e)

def validate_sign_params(image_file_path, isblur1):
	isvalidimage = "false"
	remarks = ""
	sign_h, sign_w = get_sign_img_dim()
	sign_hi, sign_wi = get_resolution(image_file_path)
	print("sign:Actual sign Dim=height::width=",sign_hi, sign_wi)
	print("sign:Requir sign Dim=height::width=",sign_h, sign_w)
	logging.info("sign:Actual sign Dim=height="+str(sign_hi)+ " width="+str(sign_wi))
	logging.info("sign:Requir sign Dim=height="+str(sign_h)+ " width="+str(sign_w))
	try:
		if(isblur1=="true"):
			isvalidimage = "false"
			remarks = config.get('signature', 'blur_sign')
			return isvalidimage, remarks
		if(isblur1=="false"):
			signature, average = signature_extractor(image_file_path)
			isfullscan = is_full_scan(image_file_path, "sign")
			# is_meta_data = get_img_meta_data(image_file_path)
			# img = binarize(image_file_path, "sign")
			# numpydata = asarray(img)
			# cv2.imshow("Image", numpydata)
			# cv2.waitKey(0)
			print("sign:isfullscan=",isfullscan)
			# print("sign:is_meta_data=",is_meta_data)
			# if(is_meta_data==False):
				# print("sign:if1...")
				# isvalidimage = "false"
				# remarks = config.get('signature', 'invalid_sign')
				# return isvalidimage, remarks
			if(int(sign_wi)<=int(sign_hi) and isfullscan==True):
				print("sign:if1...")
				isvalidimage = "false"
				remarks = config.get('signature', 'full_scan_sign')
				return isvalidimage, remarks
			if((int(signature)>0 or int(average)>0) and isfullscan==True):
				if(((int(sign_hi) <= int(sign_h)) and (int(sign_wi) <= int(sign_w)))):
					print("sign:if2...")
					isvalidimage = "true"
					remarks = config.get('signature', 'valid_sign')
					return isvalidimage, remarks
				else:
					print("sign:if2.1...")
					isvalidimage = "false"
					remarks = config.get('signature', 'full_scan_sign')
					return isvalidimage, remarks
			if((int(signature)>0 or int(average)>0) and isfullscan==False):
				print("sign:if3...")
				if(int(sign_wi)<=int(sign_hi)):
					print("sign:if4...")
					isvalidimage = "false"
					remarks = config.get('signature', 'invalid_sign')
					return isvalidimage, remarks
				else:
					print("sign:if5...")
					isvalidimage = "true"
					remarks = config.get('signature', 'valid_sign')
					return isvalidimage, remarks
				
			# image height <= width which means landscape
			# if(int(sign_hi)<=int(sign_wi)):
				# signature, average = signature_extractor(image_file_path)
				# isfullscan = is_full_scan(image_file_path)				
				# if((int(signature)>0 or int(average)>0) and ((int(sign_hi) <= int(sign_h)) and (int(sign_wi) <= int(sign_w)))):
					# isvalidimage = "true"
					# remarks = config.get('signature', 'valid_sign')
				# elif((int(signature)<=0 or int(average)<=0) and ((int(sign_hi) <= int(sign_h)) and (int(sign_wi) <= int(sign_w)))):
					# isvalidimage = "false"
					# remarks = config.get('signature', 'invalid_sign')
				# elif(((int(sign_hi) >= int(sign_h)) or (int(sign_wi) >= int(sign_w)))):
					# isvalidimage = "false"
					# remarks = config.get('signature', 'full_scan_sign')
			# image width <= height which means portrait
			if(int(sign_wi)<=int(sign_hi)):
				isvalidimage = "false"
				remarks = config.get('signature', 'invalid_sign')
				return isvalidimage, remarks
		print("sign:remarks=",remarks)
		return isvalidimage, remarks
	except Exception as e:
		print(e)
		logging.debug("Xception:validate_sign_params="+e)