from flask import Flask, request, jsonify
import os
import random
import string
from datetime import datetime
from flask_cors import CORS
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate_random_suffix(length=6):
    """Generate a random string suffix"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

@app.route('/save-drawing', methods=['POST'])
def save_drawing():
    try:
        data = request.json
        
        # Get filename and path from request
        filename = data.get('filename', 'drawing')
        relative_path = data.get('path', '.')
        image_data = data.get('image', '')  # Base64 encoded image
        
        # Remove data:image/png;base64, prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
            
        # Generate random suffix
        suffix = generate_random_suffix()
        
        # Ensure filename has .png extension
        if not filename.lower().endswith('.png'):
            filename = f"{filename}.png"
            
        # Add random suffix before extension
        filename_parts = filename.rsplit('.', 1)
        filename_with_suffix = f"{filename_parts[0]}_{suffix}.{filename_parts[1]}"
        
        # Create full path
        full_path = os.path.join(relative_path, filename_with_suffix)
        directory = os.path.dirname(full_path)
        
        # Ensure directory exists
        if directory:
            ensure_directory(directory)
            
        # Decode and save image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image.save(full_path, 'PNG')
        
        return jsonify({
            'success': True,
            'filename': filename_with_suffix,
            'path': full_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)