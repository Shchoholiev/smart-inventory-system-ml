import os
from flask import Flask
from scannable_codes.controller import scannable_codes

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = { 'png', 'jpg', 'jpeg', 'gif' }

@app.route('/health/liveness')
def liveness():
    return { 'status': 'Available' }

app.register_blueprint(scannable_codes)
    
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)