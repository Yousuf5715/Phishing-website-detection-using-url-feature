import os
import sys
import json
import joblib
import pandas as pd

# Make src importable
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from feature_extraction import extract_features, FEATURE_NAMES

MODEL_PATH = os.path.join(ROOT, 'models', 'model.joblib')


def _load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train and commit models/model.joblib or set up model download.")
    return joblib.load(MODEL_PATH)


# Vercel Python serverless function entrypoint
def handler(request):
    try:
        payload = None
        if hasattr(request, 'json'):
            payload = request.json
        else:
            try:
                payload = json.loads(request.body)
            except Exception:
                payload = {}

        url = None
        if isinstance(payload, dict):
            url = payload.get('url')

        if not url:
            return ({'error': 'Missing "url" in request body'}, 400)

        try:
            bundle = _load_model()
        except FileNotFoundError as e:
            return ({'error': str(e)}, 503)

        clf = bundle['model']

        feats = extract_features(url)
        X = pd.DataFrame([feats], columns=FEATURE_NAMES)

        proba = None
        try:
            proba = float(max(clf.predict_proba(X)[0]))
        except Exception:
            proba = None

        try:
            pred = int(clf.predict(X)[0])
        except Exception as e:
            return ({'error': 'Prediction failed', 'detail': str(e)}, 500)

        return ({'url': url, 'prediction': pred, 'probability': proba}, 200)

    except Exception as exc:
        return ({'error': 'Internal server error', 'detail': str(exc)}, 500)
