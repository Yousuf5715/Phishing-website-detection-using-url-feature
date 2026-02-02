import os
import argparse
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from feature_extraction import extract_features, FEATURE_NAMES


def train(data_csv: str, model_out: str, create_if_missing: bool = False):
    if not os.path.exists(data_csv):
        if create_if_missing:
            print(f"Data file '{data_csv}' not found — creating a starter CSV.")
            os.makedirs(os.path.dirname(data_csv), exist_ok=True)
            sample_path = os.path.join('data', 'sample_urls.csv')
            if os.path.exists(sample_path):
                import shutil
                shutil.copyfile(sample_path, data_csv)
                print(f"Copied sample data from '{sample_path}' to '{data_csv}'.")
            else:
                with open(data_csv, 'w', encoding='utf-8') as f:
                    f.write('url,label\nhttp://example.com,0\n')
                print(f"Created minimal CSV at '{data_csv}'.")
        else:
            raise FileNotFoundError(f"Data file '{data_csv}' not found. Provide a CSV with columns 'url,label' or run with --create-if-missing to create a starter file.")

    df = pd.read_csv(data_csv)
    if 'url' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'url' and 'label' columns (header: url,label). Use --create-if-missing to create a starter CSV if you don't have one.")

    X = df['url'].apply(lambda u: extract_features(u))
    X = list(X)
    X = pd.DataFrame(X, columns=FEATURE_NAMES)
    y = df['label'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    joblib.dump({'model': clf, 'features': FEATURE_NAMES}, model_out)
    print(f"Model saved to {model_out}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data/sample_urls.csv', help='CSV file with columns url,label')
    parser.add_argument('--out', default='models/model.joblib', help='Output path for trained model')
    parser.add_argument('--create-if-missing', action='store_true', help='Create a starter CSV at --data path if the file does not exist')
    args = parser.parse_args()
    train(args.data, args.out, create_if_missing=args.create_if_missing)
