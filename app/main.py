from flask import Flask, request, jsonify
from PIL import Image
import io

from app.torch_utils import transform_image, get_prediction

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    # xxx.png
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.data.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})
        try:
            img_bytes = file.read()
            tensor = transform_image(Image.open(io.BytesIO(img_bytes)))
            prediction = get_prediction(tensor)
            return jsonify(prediction)
        except Exception as e:
            return jsonify({'error': f'{e}'})
