#import libraries
import PIL
from PIL import Image
import numpy as np
from numpy import asarray
import cv2
from commons import get_image

image = 'D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_003.jpg'

def get_resolution(image):
  im = cv2.imread(image)
  h, w, c = im.shape
  return (h, w)


def binarize(img, type):
  is_valid_img = "true"
  try:
    img = get_image(img, 'pil')
    #initialize threshold
    thresh=100
    #convert image to greyscale
    img=img.convert('L')
    width,height=img.size
    #traverse through pixels 
    for x in range(width):
      for y in range(height):
        #if intensity less than threshold, assign white
        if img.getpixel((x,y)) < thresh:
          img.putpixel((x,y),0)
        #if intensity > threshold, assign black 
        else:
          img.putpixel((x,y),255)
    numpydata = asarray(img)
    number_of_white_pix = np.sum(numpydata == 255)
    number_of_black_pix = np.sum(numpydata == 0)
    print("number_of_white_pix=",number_of_white_pix)
    print("number_of_black_pix=",number_of_black_pix)
    print(number_of_white_pix- number_of_black_pix)
    if((type=="face") and (number_of_white_pix > number_of_black_pix)):
      diff = number_of_white_pix- number_of_black_pix
      if((diff > number_of_black_pix) and (diff < number_of_white_pix)):
        is_valid_img = "false"
    print("is_valid_img=",is_valid_img)
    # img.show()   
  except Exception as e:
    print("Exception@binarize=",e)
  return is_valid_img
  

#bin_image=binarize(image, "face")