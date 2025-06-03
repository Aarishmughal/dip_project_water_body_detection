from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import cv2
import io
from PIL import Image
from processing import detect_water_and_contours
from flask import send_file

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_image():
    file = request.files['image']
    hsv_values = request.form

    img = Image.open(file.stream).convert("RGB")
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    lower = np.array([int(hsv_values['h_min']), int(hsv_values['s_min']), int(hsv_values['v_min'])])
    upper = np.array([int(hsv_values['h_max']), int(hsv_values['s_max']), int(hsv_values['v_max'])])

    water_only, contour_img, water_pixels, percentage, _ = detect_water_and_contours(img_cv, (lower, upper))

    _, img_encoded = cv2.imencode('.png', contour_img)
    return send_file(io.BytesIO(img_encoded), mimetype='image/png')

@app.route('/download')
def download_image():
    return send_file('output/processed.png', mimetype='image/png', as_attachment=True)

@app.route('/stats', methods=['POST'])

@app.route('/histogram')
def histogram():
    mask = cv2.imread('output/mask.png', 0)  # Your binarized water mask
    hist = cv2.calcHist([mask], [0], None, [256], [0, 256]).flatten().tolist()
    return jsonify(hist)

def pixel_stats():
    # Add similar logic if needed
    pass

if __name__ == '__main__':
    app.run(debug=True)
