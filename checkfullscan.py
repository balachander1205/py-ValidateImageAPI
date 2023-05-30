from commons import get_sign_img_dim, get_face_img_dim, get_resolution, get_colors
import logging
import configparser

config = configparser.RawConfigParser()
config.read('static/config/config.properties')

def is_full_scan(image_file_path, type):
	remarks = False
	fullscan_start = int(config.get('fullscan', 'fullscan_start'))
	fullscan_end = int(config.get('fullscan', 'fullscan_end'))
	try:
		colors = get_colors(image_file_path)
		print("colors=",colors)
		if(type=="face"):
			if len(colors)==0:
				remarks = True
			if len(colors)>0:
				if(int(float(colors[0]))==fullscan_end or (fullscan_start <= int(float(colors[0])) <=fullscan_end)):
					remarks = True
		if(type=="sign"):
			if (len(colors)==0 or (len(colors)==1 and int(float(colors[0]))==fullscan_end)):
				remarks = True
			if len(colors)>0:
				if(int(float(colors[0]))==fullscan_end or (fullscan_start <= int(float(colors[0])) <=fullscan_end)):
					remarks = True
		return remarks			
	except Exception as e:
		print("Exception:is_full_scan=",e)
		logging.debug("Exception:is_full_scan="+str(e))
		return remarks

# imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/IMG-20230520-WA0002.jpg'
# imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/349207615081997.jpg'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG23/116371708041978.jpg&filePath=basePath'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG62/314868719111993.jpg&filePath=basePath'
# imagePath = 'D:/Projects/py-ValidateImageAPI/static/images/IMG-20230520-WA0001.jpg'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG69/349984905081983.jpg&filePath=basePath'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG34/173838008041984.jpg&filePath=basePath'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG70/350249805101990.jpg&filePath=basePath'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/PHOTO/PHOTO_JPG69/346516924032002.jpg&filePath=basePath'
# imagePath = 'https://tspsconetimereg.tspsc.gov.in/preview.tspsc?fileName=Documents/JPG/SIGN/SIGN_JPG62266/3113348450.jpg&filePath=basePath'
# is_full_scan(imagePath)
	