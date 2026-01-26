"""
Flask route handlers for the ATIM web application.
"""
import os
import traceback
from datetime import datetime
from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from services.inventory_service import process_inventory


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def register_routes(app):
    """
    Register all routes with the Flask app.

    Args:
        app: Flask application instance
    """

    @app.route('/')
    def index():
        """Home page with upload form."""
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Handle file upload and process inventory."""
        try:
            # Check if file is present
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400

            file = request.files['file']

            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
                return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            saved_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(filepath)

            # Get analysis parameters
            max_keywords = int(request.form.get('max_keywords', 15))
            min_confidence = float(request.form.get('min_confidence', 20.0))

            # Process the file
            result = process_inventory(filepath, max_keywords, min_confidence)

            return jsonify(result)

        except Exception as e:
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500

    @app.route('/reports/<filename>')
    def download_report(filename):
        """Download generated report."""
        return send_file(
            os.path.join('reports', filename),
            as_attachment=False,
            mimetype='text/html'
        )

    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
