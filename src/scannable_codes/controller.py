from flask import current_app, Blueprint, Response, request, jsonify
from werkzeug.utils import secure_filename
import cv2
from pyzbar.pyzbar import decode
import os
import qrcode
from io import BytesIO

scannable_codes = Blueprint('scannable_codes', __name__, url_prefix='/scannable-codes')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def delete_file(file_path):
    os.remove(file_path)

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer)
    binary_image = buffer.getvalue()
    
    return binary_image

@scannable_codes.route('/decode', methods=['POST'])
def decode_image():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        image = cv2.imread(file_path)
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Decode the barcode/QR code
        decoded_objects = decode(gray_image)
        
        response_data = [
            {
                'type': 'QRCODE' if obj.type == 'QRCODE' else 'BARCODE', 
                'data': obj.data.decode('utf-8')
            } for obj in decoded_objects
        ]

        delete_file(file_path)

        return jsonify(decoded_objects=response_data)
    
    return jsonify(error='Invalid file'), 400

@scannable_codes.route('/generate', methods=['POST'])
def generate_scannable_code():
    data = request.json.get('data')
    code_type = request.json.get('type')
    
    if not data:
        return jsonify(error='No data provided'), 400
    
    if code_type == 'QRCode':
        binary_image = generate_qr_code(data)
        return Response(binary_image, mimetype='image/png')
    elif code_type == 'Barcode':
        return jsonify(error='Barcode generation not implemented'), 501
    else:
        return jsonify(error='Invalid code type'), 400
