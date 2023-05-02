import face_recognition
from commons import get_image
import requests
from io import BytesIO
import logging

imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_003.jpg'

def is_face_valid(imagePath):
	try:
		isurl = 'false'
		if(len(str(imagePath)) == 0):
			return "NA"
		if ('http://' in imagePath) or ('https://' in imagePath):
			isurl = 'true'
		print("is_face_valid:isurl=",isurl)
		logging.info("is_face_valid:isurl="+isurl)
		if(isurl=='true'):
			response = requests.get(imagePath)
			imagePath = BytesIO(response.content)

		image = face_recognition.load_image_file(imagePath)
		face_locations = face_recognition.face_locations(image)
		print("Face Locations=",face_locations)
		logging.info("Face Locations="+str(face_locations))
		is_valid_face = 'false'
		if(len(face_locations)>0):
			is_valid_face = 'true'
		print("is_valid_face=",is_valid_face)
		logging.info("is_face_valid="+is_valid_face)
		return is_valid_face
	except Exception as e:
		logging.debug("Xception:is_face_valid="+e)	

#is_face_valid(imagePath)
#do_validate_face(imagePath)