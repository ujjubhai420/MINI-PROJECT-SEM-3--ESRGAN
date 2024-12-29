from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import torch
import cv2
import numpy as np
from esrgan_model import ESRGAN
import os.path as osp
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads/'
RESULTS_FOLDER = 'static/results/'


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)


MODEL_PATH = 'model/RRDB_ESRGAN_x4.pth'  
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
esrgan = ESRGAN(MODEL_PATH)

def get_image_details(image_path):
    img = cv2.imread(image_path)
    dimensions = f"{img.shape[1]}x{img.shape[0]}"  # width x height
    size = os.path.getsize(image_path) / 1024  # KB
    return dimensions, round(size, 2)


@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the image upload and enhancement
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

   
    filename = secure_filename(image_file.filename)
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(original_path)

    
    img = cv2.imread(original_path, cv2.IMREAD_COLOR)
    img = img.astype(np.float32) / 255.0
    img = img.transpose((2, 0, 1))
    img_LR = torch.from_numpy(img[None]).float().to(device)

    with torch.no_grad():
        output = esrgan.enhance_image(original_path)  

    
    enhanced_filename = 'enhanced_' + filename
    enhanced_path = os.path.join(RESULTS_FOLDER, enhanced_filename)
    cv2.imwrite(enhanced_path, output)

    # Get details for both images
    original_dimensions, original_size = get_image_details(original_path)
    enhanced_dimensions, enhanced_size = get_image_details(enhanced_path)

    # Return the paths of the original and enhanced images, along with their details
    return jsonify({
        'originalImageUrl': original_path,
        'enhancedImageUrl': enhanced_path,
        'originalDimensionsData': original_dimensions,
        'enhancedDimensionsData': enhanced_dimensions,
        'originalSizeData': original_size,
        'enhancedSizeData': enhanced_size
    })

if __name__ == '__main__':
    app.run(debug=True)
