from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import cv2
import io
import os
from PIL import Image
from processing import detect_water_and_contours

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

    # Save processed image for download
    os.makedirs('output', exist_ok=True)
    cv2.imwrite('output/processed.png', contour_img)

    _, img_encoded = cv2.imencode('.png', contour_img)
    return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/png')

@app.route('/download')
def download_image():
    file_path = 'output/processed.png'
    if not os.path.exists(file_path):
        return jsonify({'error': 'Processed image not found.'}), 404
    return send_file(file_path, mimetype='image/png', as_attachment=True)

@app.route('/histogram')
def histogram():
    mask_path = 'output/mask.png'
    if not os.path.exists(mask_path):
        return jsonify({'error': 'Mask image not found.'}), 404
    mask = cv2.imread(mask_path, 0)
    hist = cv2.calcHist([mask], [0], None, [256], [0, 256]).flatten().tolist()
    return jsonify(hist)

@app.route('/edges')
def get_edges():
    img_path = 'output/processed.png'
    if not os.path.exists(img_path):
        return jsonify({'error': 'Processed image not found.'}), 404
    img = cv2.imread(img_path)
    edges = cv2.Canny(img, 100, 200)
    edge_path = 'output/edges.png'
    cv2.imwrite(edge_path, edges)
    return send_file(edge_path, mimetype='image/png')

@app.route('/processed')
def processed_image():
    file_path = 'output/processed.png'
    if not os.path.exists(file_path):
        return jsonify({'error': 'Processed image not found.'}), 404
    return send_file(file_path, mimetype='image/png')

@app.route('/stats', methods=['POST'])
def stats():
    file = request.files['image']
    hsv_values = request.form

    img = Image.open(file.stream).convert("RGB")
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    lower = np.array([int(hsv_values['h_min']), int(hsv_values['s_min']), int(hsv_values['v_min'])])
    upper = np.array([int(hsv_values['h_max']), int(hsv_values['s_max']), int(hsv_values['v_max'])])

    water_only, contour_img, water_pixels, percentage, _ = detect_water_and_contours(img_cv, (lower, upper))
    total_pixels = img_cv.shape[0] * img_cv.shape[1]
    stats = {
        'total_pixels': int(total_pixels),
        'water_pixels': int(water_pixels),
        'water_percentage': float(percentage)
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
