from flask import Flask, request, jsonify
from flask_cors import CORS
import pydicom
from PIL import Image
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return 'Health check ok!'

# the following RESTful API  is a singular endpoint that 
# allows a user to save a DICOM file while returning any DICOM 
# header attribute based on the DICOM Tag as a query parameter
# and the dicom file converted into a png file
@app.route('/save_file', methods=['POST'])
def save_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    tag = request.args.get('tag')
    if tag is None:
        return jsonify({'error': 'No DICOM Tag provided'}), 400

    file = request.files['file']

    try:
        dicom_data = pydicom.dcmread(file)
    except ValueError:
        return jsonify({'error': 'Unable read file'}), 400

    attribute_value = dicom_data.get(tag)
    
    dicom_data.save_as(file.filename)

    # converting dicom file into png
    try:
        image_array = dicom_data.pixel_array.astype(float)
    except ValueError:
        return jsonify({'error': 'Unable to convert to pixel data'}), 400
    rescaled_image = (np.maximum(image_array, 0) / image_array.max()) * 255.0
    rescaled_image = np.uint8(rescaled_image)
    final_image = Image.fromarray(rescaled_image)
    buffered = BytesIO()
    final_image.save(buffered, format='PNG')
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    
    response = {
        'attribute_value': str(attribute_value or ''),
        'dicom_image': encoded_image,
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=False)