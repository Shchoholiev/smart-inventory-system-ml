from flask import current_app, Blueprint, Response, request, jsonify
from werkzeug.utils import secure_filename
import cv2
from pyzbar.pyzbar import decode
import os
import qrcode
from io import BytesIO
import logging

scannable_codes = Blueprint('scannable_codes', __name__, url_prefix='/scannable-codes')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def delete_file(file_path):
    logging.info('Deleting file')
    os.remove(file_path)

def generate_qr_code(data):
    logging.info('Generating QR code')

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer)
    binary_image = buffer.getvalue()

    logging.info('QR code generated')
    
    return binary_image

@scannable_codes.route('/decode', methods=['POST'])
def decode_image():
    logging.info('decode_image called')

    if 'file' not in request.files:
        logging.warning('No file part in request')
        return jsonify(error='No file part'), 400
    
    file = request.files['file']
    if file.filename == '':
        logging.warning('No selected file')
        return jsonify(error='No selected file'), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        logging.info(f'Saving file to {file_path}')
        file.save(file_path)
        
        logging.info('Reading and processing image')
        image = cv2.imread(file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray_image)
        
        logging.info('Preparing response data')
        response_data = [
            {
                'type': 'QRCODE' if obj.type == 'QRCODE' else 'BARCODE',
                'data': obj.data.decode('utf-8')
            } for obj in decoded_objects
        ]

        delete_file(file_path)

        logging.info('Returning response')
        return jsonify(response_data)
    
    logging.error('Invalid file')
    return jsonify(error='Invalid file'), 400

@scannable_codes.route('/generate', methods=['POST'])
def generate_scannable_code():
    logging.info('Generating scannable code')

    data = request.json.get('data')
    code_type = request.json.get('type')
    
    if not data:
        logging.error('No data provided')
        return jsonify(error='No data provided'), 400
    
    if code_type == 'QRCode':
        binary_image = generate_qr_code(data)
        return Response(binary_image, mimetype='image/png')
    elif code_type == 'Barcode':
        logging.error('Barcode generation not implemented')
        return jsonify(error='Barcode generation not implemented'), 501
    else:
        logging.error('Invalid code type')
        return jsonify(error='Invalid code type'), 400
