from PIL import Image
from PIL.ExifTags import TAGS
import sys
from commons import *

# imagename = "D:/Projects/py-ValidateImageAPI/static/images/IMG-20230520-WA0004.jpg"

def get_img_meta_data(imagename):
    try:
        image = get_image(imagename, "pil")
        # extract other basic metadata
        info_dict = {
            "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
        }

        # for label,value in info_dict.items():
            # print(f"{label:25}: {value}")
            
        # extract EXIF data
        exifdata = image.getexif()

        # iterating over all EXIF data fields
        for tag_id in exifdata:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                try:
                    data = data.decode()
                except Exception as e:
                    print(e)                
            print(f"{tag:25}: {data}")
        return info_dict
    except Exception as e:
        print(e)

# get_img_meta_data(imagename)