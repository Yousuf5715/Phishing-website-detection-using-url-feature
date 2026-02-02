import os
import joblib
from flask import Flask, request, jsonify, send_from_directory
from feature_extraction import extract_features, FEATURE_NAMES

MODEL_PATH = os.path.join('models', 'model.joblib')

app = Flask(__name__, static_folder='../web', static_url_path='')

_model_bundle = None


def load_model():
    global _model_bundle
    if _model_bundle is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train first using src/train_model.py")
        _model_bundle = joblib.load(MODEL_PATH)
    return _model_bundle


@app.route('/')
def index():
    return send_from_directory(os.path.join(os.getcwd(), 'web'), 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing "url" in JSON body'}), 400

    try:
        model_bundle = load_model()
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 503

    clf = model_bundle['model']

    feats = extract_features(url)
    proba = None
    try:
        proba_arr = clf.predict_proba([feats])[0]
        proba = float(max(proba_arr))
    except Exception:
        proba = None

    try:
        pred = int(clf.predict([feats])[0])
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'detail': str(e)}), 500

    return jsonify({'url': url, 'prediction': int(pred), 'probability': proba})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
