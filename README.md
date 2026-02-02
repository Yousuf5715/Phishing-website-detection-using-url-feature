# URL-based Phishing Detector (Minimal)

This small project extracts URL-based features, trains a RandomForest classifier, and exposes a Flask API + minimal web UI for prediction.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# then
pip install -r requirements.txt
python -m tldextract
```

2. Train a model using the sample data (or provide your own CSV with `url,label` columns):

```bash
python src/train_model.py --data data/sample_urls.csv --out models/model.joblib
```

The training script will automatically create a starter CSV if the `--data` path does not exist. If you do NOT want this behavior, pass `--no-create-if-missing`.

Examples:

```bash
# create starter CSV automatically and train
python src/train_model.py --data data/my_urls.csv --out models/model.joblib

# don't auto-create, fail if data is missing
python src/train_model.py --data data/my_urls.csv --no-create-if-missing --out models/model.joblib
```

3. Run the API and open the web UI at http://localhost:5000

```bash
python src/predict_api.py
```

Files
- src/feature_extraction.py: URL feature extractor and feature names
- src/train_model.py: training script that saves `models/model.joblib`
- src/predict_api.py: Flask app with `/predict` endpoint and simple web UI at `/`
- web/index.html: minimal UI to test predictions
- data/sample_urls.csv: small example dataset
- requirements.txt: Python deps

Notes
- This is a minimal example using only URL textual features. Real-world phishing detection benefits from additional signals (WHOIS, hosting info, TLS certificate, page content, blacklists, heuristics, etc.).
- Improve the dataset size and labeling for production use.
