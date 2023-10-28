from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import cv2
from pyzbar.pyzbar import decode
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = { 'png', 'jpg', 'jpeg', 'gif' }

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def delete_file(file_path):
    os.remove(file_path)

@app.route('/health/liveness')
def liveness():
    return { 'status': 'Available' }

@app.route('/barcodes/decode', methods=['POST'])
def decode_image():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

