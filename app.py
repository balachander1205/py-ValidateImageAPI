import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from flask import Flask,render_template, request,json,Response
from crossdomain import crossdomain
import os
from waitress import serve
from imageUtils import process_image
from commons import get_uuid
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# logging config
handler = RotatingFileHandler('static/logs/middleware.log', maxBytes=1)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
handler.setFormatter(formatter)
logging.getLogger('').setLevel(logging.DEBUG)
logging.getLogger('').addHandler(handler)
# logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'Image validation Application'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

@app.route('/index')
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
    logging.info('/validateImage....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:UUID:="+str(uid)+" <<<-----<<")
    print(">>----->>> START:UUID:="+str(uid)+" <<<-----<<")
    data = json.loads(request.data)
    # REQUEST BODY
    id = data.get('id', '')
    print(data)
    image_file_path = data.get('imageFilePath', '')    
    img_type = data.get('fileType', '')
    app_id = data.get('appid', '') 

    data = process_image(image_file_path, img_type, app_id, id, uid, cur_datetime)
    logging.info(">>----->>> END:UUID:="+str(uid)+" <<<-----<<")
    print(">>----->>> END:UUID:="+str(uid)+" <<<-----<<")
    return Response(json.dumps(data),mimetype='application/json')

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)    
    logging.info('Started')
    print("Started Image validation server")
    print("Serving on http://0.0.0.0:5001")
    serve(app, host="0.0.0.0", port=5001)