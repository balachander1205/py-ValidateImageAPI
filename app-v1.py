import logging
from flask import Flask,render_template, request,json,Response
from crossdomain import crossdomain
from blurDetection import do_blur_detection, get_file_format
from faceDetection import do_validate_face
from faceDetection import is_face_valid
from binarizeImage import binarize, get_resolution
import os
from waitress import serve
from commons import get_uuid

app = Flask(__name__)

@app.route('/')
@crossdomain(origin='*')
def index():
    return 'Welcome to image validation Application!'

@app.route('/home')
@crossdomain(origin='*')
def home():
    return render_template('index.html')

@app.route('/validateImage', methods=['POST'])    
@crossdomain(origin='*')
def validateImage():
    logging.info('Started image validation....')
    data = json.loads(request.data)

    id = data.get('id', '')
    print(data)
    image_file_path = data.get('imageFilePath', '')    
    sign_file_path = data.get('signFilePath', '')
    app_id = data.get('appid', '') 

    cur_datetime, uid = get_uuid()   
        
    isblur1 = do_blur_detection(image_file_path)
    isblur2 = do_blur_detection(sign_file_path)

    format1 = get_file_format(image_file_path)
    format2 = get_file_format(sign_file_path)

    # validate face
    validate_face1 = is_face_valid(image_file_path)

    # validate image background
    validate_bg_img1 = binarize(image_file_path, "face")
    validate_bg_img2 = binarize(sign_file_path, "sign")

    # image resolution
    img_res1 = get_resolution(image_file_path)
    img_res2 = get_resolution(sign_file_path)

    isvalidface1 = "false"
    isvalidface2 = "false"
    if(isblur1=="false" and validate_face1=="true"):
        isvalidface1 = "true"
    print("_isblur1_="+isblur1+" isvalidface="+isvalidface1)

    image1_data = {
            'type': 'face_image',
            'isblur': isblur1,
            'isvalidface': isvalidface1,
            'format' : format1,
            'isvalidbg': validate_bg_img1,
            'resolution': img_res1
            }
    image2_data = {
            'type': 'signature',
            'isblur': isblur2,
            'isvalidsign': validate_bg_img2,
            'format' : format2,
            'resolution': img_res2
            }
    data = {
            'status':'OK',
            'createdatetime':cur_datetime,
            'id':id,
            'appid':app_id,
            'image1': image1_data,
            'image2': image2_data,
            'uid': uid
            }
    return Response(json.dumps(data),mimetype='application/json')

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)    
    logging.info('Started')
    #app.run(host='127.0.0.1', port=5001,debug=True, threaded=True)
    serve(app, host="127.0.0.1", port=5001)
