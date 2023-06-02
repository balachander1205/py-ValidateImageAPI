from PIL import Image, ImageSequence
import requests
import cv2
import urllib.request
import numpy as np
from datetime import datetime
import uuid
import configparser
import logging
import urllib.request as ur
import extcolors
from colormap import rgb2hex
import pandas as pd
from PIL.ExifTags import TAGS

config = configparser.RawConfigParser()
config.read('static/config/config.properties')


def get_gif_img(url, im):
	im = Image.open(requests.get(url, stream=True).raw)
	print(im)
	im = np.array([np.array(im.copy().convert('RGB').getdata(),dtype=np.uint8).reshape(im.size[1],im.size[0],3) for im in ImageSequence.Iterator(im)])
	im = im[0]
	return im

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
			req = ur.urlopen(url)
			arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
			im = cv2.imdecode(arr, -1)
			if(im is None):
				im = get_gif_img(url, im)

		# show image
		# if(type=='cv2'):
			# cv2.imshow("Image", im)
			# cv2.waitKey(0)
		# if(type=='pil'):
			# im.show()
		return im		
	except Exception as e:
		print(e)
		logging.debug("Exception@get_image="+str(e))

def get_img_meta_data(image):
	is_meta_data = True
	try:
		im = get_image(image, "pil")
		exifdata = im.getexif()
		if(len(exifdata)==0):
			is_meta_data = False
		return is_meta_data
		# looping through all the tags present in exifdata
		# for tagid in exifdata:
			# tagname = TAGS.get(tagid, tagid)
			# value = exifdata.get(tagid)
			# if isinstance(value, bytes):
				# data = value.decode()
			# print(f"{tagname}: {value}")
	except Exception as e:
		print(e)
		logging.debug("Exception@get_img_meta_data="+str(e))

'''
	get image resolution
'''
def get_resolution(image):
	try:
		im = get_image(image, "cv2")
		get_img_meta_data(image)
		if(len(im.shape)<=2):
			print("get_resolution=2")
			h,w = im.shape
		if(len(im.shape)>2):
			print("get_resolution>2")
			h, w, c = im.shape
	except Exception as e:
		print(e)
		logging.debug("Exception:get_resolution="+str(e))		
	return (h, w)

def get_dpi(image):
	try:
		img = get_image(image, 'pil')
		print("dpi=",img.info['dpi'])
		return img.info['dpi']
	except Exception as e:
		raise e
		print(e)

def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]    
    # df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    list_color = list(df_color_up)
    list_precent = [int(i) for i in list(df_percent)]
    # text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color, list_precent)]
    text_c = [str(round(p*100/sum(list_precent),1)) for c, p in zip(list_color, list_precent)]
    df = pd.DataFrame(zip(df_color_up, df_percent, text_c), columns = ['c_code','pixels','percent'])
    print(df)
    return list(text_c), list(df['c_code'])

def get_colors(image):
	try:
	  img = get_image(image, "pil")
	  colors = extcolors.extract_from_image(img)
	  data_frame, c_code = color_to_df(colors)
	  return data_frame, c_code
	except Exception as e:
		print(e)
		logging.debug("Exception:get_colors="+str(e))

'''
checking image for black and white
'''
def is_binary_image(image):
	is_binary_image = False
	try:
		colors, c_code = get_colors(image)
		if len(c_code)==2:
			print("Image is black & white")
			is_binary_image = True
			# if(("#FFF".lower() in c_code[0].lower() or "#000".lower() in c_code[0].lower())
				# and ("#FFF".lower() in c_code[1].lower() or "#000".lower() in c_code[1].lower())):
				# print("Image is black & white")
				# is_binary_image = True
		logging.info("is_binary_image="+str(is_binary_image))
		return is_binary_image
	except Exception as e:
		print("Exception:is_binary_image=",e)
		logging.debug("Exception|is_binary_image="+str(e))
		return is_binary_image


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

def get_brightness(img_path):
	img = get_image(img_path, "cv2")
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	return hsv[...,2].mean()

# url = 'https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg'
#print(get_face_img_dim())
#print(get_sig_img_dim())	
#get_image(url, 'cv2')
