# smart-inventory-system-ml  
A Python-based system for reading and generating scannable codes such as barcodes and QR codes, built with Flask and containerized using Docker.

## Table of Contents  
- [Features](#features)  
- [Stack](#stack)  
- [Installation](#installation)  
  - [Prerequisites](#prerequisites)  
  - [Setup Instructions](#setup-instructions)  
- [Configuration](#configuration)

## Features  
- Decode barcodes and QR codes from uploaded images.  
- Generate QR codes from provided data.  
- Health check endpoint for system liveness status.  
- Logging for tracking requests and operations.  
- Containerized with Docker for easy deployment and development.

## Stack  
- Python 3.11  
- Flask 3.0  
- Flask-CORS  
- Gunicorn WSGI HTTP Server  
- OpenCV (opencv-python-headless) for image processing  
- Pyzbar for barcode and QR code decoding  
- qrcode for QR code generation  
- Docker for containerization  

## Installation  

### Prerequisites  
- Python 3.11  
- Docker (for containerized deployment)  
- pip package manager  

### Setup Instructions  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Shchoholiev/smart-inventory-system-ml.git
   cd smart-inventory-system-ml
   ```

2. **Create a virtual environment and activate it (optional but recommended)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application locally**  
   ```bash
   python src/app.py
   ```
   The Flask app will start on [http://localhost:5000](http://localhost:5000)

5. **Running with Docker**  
   Build the Docker image:  
   ```bash
   docker build -t smartinventorysystemml:latest .
   ```  
   Run the container:  
   ```bash
   docker run -p 5000:5000 smartinventorysystemml:latest
   ```  

## Configuration  
- The app uses environment variables and Flask configurations inside `src/app.py`:  

  - `UPLOAD_FOLDER`: Directory where uploaded files are stored. Default is `uploads/`.  
  - `ALLOWED_EXTENSIONS`: Set of allowed image file extensions for uploads (`png`, `jpg`, `jpeg`, `gif`).  

- These can be adjusted by modifying the Flask app’s config dictionary or overriding via environment variables if extended.

- The Docker setup exposes port `5000`.  

- CORS is enabled to allow cross-origin requests.

- Logs are emitted to standard output with INFO level detailing key operations such as decoding, QR code generation, and file handling.
