import os
from flask import Flask
from flask_cors import CORS
from scannable_codes.controller import scannable_codes
import logging

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = { 'png', 'jpg', 'jpeg', 'gif' }

@app.route('/health/liveness')
def liveness():
    logging.info('liveness called')
    return { 'status': 'Available' }

app.register_blueprint(scannable_codes)

logging.basicConfig(level=logging.INFO)

logging.info('Creating upload folder')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
logging.info('Upload folder created')
    
if __name__ == '__main__':
    app.run(debug=True)