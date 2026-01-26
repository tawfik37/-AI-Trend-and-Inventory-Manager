"""
Flask Web Application for ATIM
Upload CSV inventory files and get AI-powered recommendations
"""
from flask import Flask
from flask.json.provider import DefaultJSONProvider
import os
import numpy as np

from api.routes import register_routes


# Custom JSON encoder to handle numpy types
class NumpyJSONProvider(DefaultJSONProvider):
    """Custom JSON provider that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# Check if templates folder exists, if not use current directory
project_root = os.path.dirname(os.path.dirname(__file__))
template_folder = os.path.join(project_root, 'templates') if os.path.exists(os.path.join(project_root, 'templates')) else '.'

app = Flask(__name__, template_folder=template_folder)
app.json = NumpyJSONProvider(app)  # Use custom JSON encoder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register all routes
register_routes(app)


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 ATIM Web Application Starting...")
    print("=" * 70)
    print(f"\n📂 Template folder: {template_folder}")
    print(f"📂 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("\n📱 Open your browser and go to:")
    print("   → http://localhost:5000")
    print("\n⌨️  Press Ctrl+C to stop the server\n")
    print("=" * 70)

    app.run(debug=True, host='0.0.0.0', port=5000)
