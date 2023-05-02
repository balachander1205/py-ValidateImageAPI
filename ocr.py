from PIL import Image
from pytesseract import *
import numpy as np
import cv2

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'

filename = "D:/Projects/py-ValidateImageAPI/static/images/detecting_blur_result_006.jpg"
image = np.array(Image.open(filename))
text = pytesseract.image_to_string(image)
results = pytesseract.image_to_data(image, output_type=Output.DICT)
print(results)
for i in range(0, len(results['text'])):
   x = results['left'][i]
   y = results['top'][i]

   w = results['width'][i]
   h = results['height'][i]

   text = results['text'][i]
   conf = int(results['conf'][i])

   if conf > 70:
       text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
       print(text)
       cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
       cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
cv2.imshow("Image",image)
cv2.waitKey(0)

## Ref : https://nanonets.com/blog/ocr-with-tesseract/
