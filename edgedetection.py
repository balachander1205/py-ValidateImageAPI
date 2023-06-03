import cv2
import numpy as np

def edge_detection(imagePath):
	try:
		img = cv2.imread(imagePath)
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# laplacian = cv2.Laplacian(img,cv2.CV_64F)
		img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
		# print("laplacian=",(laplacian.mean()))
		# print("laplacian=",round(laplacian.var()))
		(T, threshInv) = cv2.threshold(img_blur, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
		sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
		sobelxy_arr = np.array(sobelxy)
		print(sobelxy_arr)
		cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
		cv2.waitKey(0)
		print("sobelxy=",(sobelxy.mean()))
		print("sobelxy=",round(sobelxy.var()))
		edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
		print("Canny\t=",(edges.mean()))
		print("Canny\t=",round(edges.var()))
		cv2.imshow('Canny Edge Detection', edges)
		cv2.waitKey(0)
	except Exception as e:
		raise e
		print(e)

imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/3113352803.jpg'
edge_detection(imagePath)