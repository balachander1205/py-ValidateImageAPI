import face_recognition
from commons import get_image
import requests
from io import BytesIO
import logging
import cv2
import numpy as np

# imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_004.jpg'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG23/116371708041978.jpg&filePath=basePath'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG62/314868719111993.jpg&filePath=basePath'
# imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/IMG-20230520-WA0001.jpg'

eye_cascade = cv2.CascadeClassifier('static/haarcascade_eye.xml')

def validate_face_alignment(image, face_locations):
	angle = 0
	try:
		print("validate_face_alignment")
		for face_location in face_locations:
			# [x,y,w,h]
		    top, right, bottom, left = face_location
		    image = image[top-50:bottom+15, left-15:right+15]		    
		    # cv2.rectangle(image, (left-15, top-50), (right+15, bottom+15), (0, 255, 0), 1)
		    eyes = eye_cascade.detectMultiScale(image)
		    listarray1 = []
		    listarray2 = []
		    count = 0
		    leftEyeCenter = 0
		    rightEyeCenter = 0		    
		    # print("Eyes length=",len(eyes))
		    for (ex,ey,ew,eh) in eyes:
		    	cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
		    	eye_centerX = (ex+(ex+ew))/2
		    	eye_centerY = (ey+(ey+eh))/2
		    	if(count==0):
		    		listarray1.append([eye_centerX, eye_centerY])
		    		nparray1 = np.array(listarray1)
		    		leftEyeCenter = nparray1.mean(axis=0).astype("int")
		    	if(count==1):
		    		listarray2.append([eye_centerX, eye_centerY])
		    		nparray2 = np.array(listarray2)
		    		rightEyeCenter = nparray2.mean(axis=0).astype("int")
		    		dY = rightEyeCenter[1] - leftEyeCenter[1]
		    		dX = rightEyeCenter[0] - leftEyeCenter[0]
		    		# print("actual angle=",np.degrees(np.arctan2(dY, dX)))
		    		angle = np.degrees(np.arctan2(dY, dX)) - 180
		    		# print("angle=",angle)
		    		count=0
		    	count+=1
		    	# cv2.line(image, (int(eye_centerX), int(eye_centerY)), (int(eye_centerX), int(eye_centerY)), (0,255,255), 1)
		# cv2.imshow("Image", image)
		# cv2.waitKey(0)
		return angle
	except Exception as e:
		print("Exception:validate_face_alignment=",str(e))

def is_face_valid(imagePath):
	try:
		isurl = 'false'	
		if(len(str(imagePath)) == 0):
			return "NA"
		if ('http://' in imagePath) or ('https://' in imagePath):
			isurl = 'true'
		# print("is_face_valid:isurl=",isurl)
		logging.info("face:face:is_face_valid:isurl="+isurl)
		if(isurl=='true'):
			response = requests.get(imagePath)
			imagePath = BytesIO(response.content)

		image = face_recognition.load_image_file(imagePath)
		face_locations = face_recognition.face_locations(image)
		
		# for face_location in face_locations:
			# [x,y,w,h]
		    # top, right, bottom, left = face_location		    
		    # cv2.rectangle(image, (left-15, top-50), (right+15, bottom+15), (0, 255, 0), 1)
		    # eyes = eye_cascade.detectMultiScale(image)
		    # for (ex,ey,ew,eh) in eyes:
		    	# cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
		# cv2.imshow("Image", image)
		# cv2.waitKey(0)		
		print("face:Face Locations=",face_locations)
		logging.info("Face Locations="+str(face_locations))
		is_valid_face = 'false'
		if(len(face_locations)==1):
			# angle = validate_face_alignment(image, face_locations)
			# print("Face angle=",str(angle))
			is_valid_face = 'true'
		if(len(face_locations)==2):
			is_valid_face = 'false'
		print("face:is_valid_face=",is_valid_face)
		logging.info("is_face_valid="+is_valid_face)
		return is_valid_face
	except Exception as e:
		logging.debug("Xception:is_face_valid="+e)	

# is_face_valid(imagePath)
#do_validate_face(imagePath)