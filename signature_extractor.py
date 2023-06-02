import cv2
# import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np
from commons import get_image

def signature_extractor(image):
    the_biggest_component = 0
    average = 0.0
    try:
        # read the input image
        img = get_image(image, 'cv2')
        img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
        # connected component analysis by scikit-learn framework
        blobs = img > img.mean()
        blobs_labels = measure.label(blobs, background=1)
        image_label_overlay = label2rgb(blobs_labels, image=img)
        # fig, ax = plt.subplots(figsize=(10, 6))
        '''
        # plot the connected components (for debugging)
        ax.imshow(image_label_overlay)
        ax.set_axis_off()
        plt.tight_layout()
        plt.show()
        '''        
        total_area = 0
        counter = 0        
        for region in regionprops(blobs_labels):
            if (region.area > 5):
                total_area = total_area + region.area
                counter = counter + 1
            # take regions with large enough areas
            if (region.area >= 5):
                if (region.area > the_biggest_component):
                    the_biggest_component = region.area
        average = (total_area/counter)
        print("sign:biggest_component: " + str(the_biggest_component))
        print("sign:average: " + str(round(average, 2)))
        return the_biggest_component, round(average, 2)      
    except Exception as e:
        print("Exception:signature_extractor=",e)
        return the_biggest_component, round(average, 2)


# image = "D:/Projects/signature_extractor-master/inputs/3113347090.jpg"
# print(signature_extractor(image))
        
