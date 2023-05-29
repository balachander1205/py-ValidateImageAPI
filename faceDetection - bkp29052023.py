import face_recognition
from commons import get_image
import requests
from io import BytesIO
import logging
import cv2

imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_008.jpg'
# imagePath = 'https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg'

def is_face_valid(imagePath):
	try:
		isurl = 'false'
		if(len(str(imagePath)) == 0):
			return "NA"
		if ('http://' in imagePath) or ('https://' in imagePath):
			isurl = 'true'
		# print("is_face_valid:isurl=",isurl)
		logging.info("is_face_valid:isurl="+isurl)
		if(isurl=='true'):
			response = requests.get(imagePath)
			imagePath = BytesIO(response.content)

		image = face_recognition.load_image_file(imagePath)
		face_locations = face_recognition.face_locations(image)
		
		# for face_location in face_locations:
		#     top, right, bottom, left = face_location
		#     cv2.rectangle(image, (left-15, top-50), (right+15, bottom+15), (0, 255, 0), 1)
		# cv2.imshow("Image", image)
		# cv2.waitKey(0)
		
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

# is_face_valid(imagePath)
#do_validate_face(imagePath)