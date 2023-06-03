import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from commons import *

sepia_kernel = np.array([
    [0.272, 0.534, 0.131],
    [0.349, 0.686, 0.168],
    [0.393, 0.769, 0.189]])


# Calculate "sepia mask" using HSV color space; empirically set parameters
def sepia_mask(img):
    # img = get_image(img, 'pil')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sepia_lower = np.array([np.round( 30 / 2), np.round(0.10 * 255), np.round(0.10 * 255)])
    sepia_upper = np.array([np.round( 45 / 2), np.round(0.60 * 255), np.round(0.90 * 255)])
    return cv2.inRange(hsv, sepia_lower, sepia_upper)

def is_sepia(img):
    try:
        image_pil = get_image(img, 'pil')
        image = np.flip(np.array(image_pil), 2)
        sepia = cv2.transform(image, sepia_kernel)
        actual_perc = cv2.countNonZero(sepia_mask(image)) / np.prod(image.shape[:2])
        sepia_perc = cv2.countNonZero(sepia_mask(sepia)) / np.prod(sepia.shape[:2])
        print("ActualImage | Sepia mask=",actual_perc)
        print("ActualImage | Sepia mask=",round(actual_perc))
        print("Sepia Image | Sepia mask=",sepia_perc)
        print("Sepia Image | Sepia mask=",round(sepia_perc))
    except Exception as e:
        print(e)





# "Sepia kernel" for filtering; https://amin-ahmadi.com/2016/03/24/sepia-filter-opencv/

img = 'D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_003.jpg'
# Read image via Pillow; processing using OpenCV; sepia filtering
image_pil = get_image(img, 'pil')
image = np.flip(np.array(image_pil), 2)
sepia = cv2.transform(image, sepia_kernel)

# Outputs and sepia percentages
plt.figure(1, figsize=(9, 9))
plt.subplot(2, 2, 1), plt.imshow(np.flip(image, 2)), plt.title('Original image')
plt.subplot(2, 2, 2), plt.imshow(sepia_mask(image), cmap='gray')
perc = cv2.countNonZero(sepia_mask(image)) / np.prod(image.shape[:2])
print("original Image | Sepia mask=",perc)
print("original Image | Sepia mask=",round(perc))
plt.title('Sepia mask [' + str(perc) + ']')
plt.subplot(2, 2, 3), plt.imshow(np.flip(sepia, 2)), plt.title('Sepia filtered image')
plt.subplot(2, 2, 4), plt.imshow(sepia_mask(sepia), cmap='gray')
perc = cv2.countNonZero(sepia_mask(sepia)) / np.prod(sepia.shape[:2])
print("Sepia Image | Sepia mask=",perc)
print("Sepia Image | Sepia mask=",round(perc))
plt.title('Sepia mask [' + str(perc) + ']')
plt.tight_layout()
plt.show()