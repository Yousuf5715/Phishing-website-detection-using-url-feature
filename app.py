import os
import sys

# Ensure `src` directory is importable for deployment platforms that don't treat it as a package
ROOT = os.path.dirname(__file__)
SRC_PATH = os.path.join(ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from predict_api import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
