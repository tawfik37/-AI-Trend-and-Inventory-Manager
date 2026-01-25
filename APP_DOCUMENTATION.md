# Flask Web Application Documentation (app.py)

## Overview

`app.py` is a Flask-based web application that provides a user-friendly web interface for the AI Trend & Inventory Manager (ATIM) system. It allows users to upload CSV inventory files and receive AI-powered inventory recommendations through a web browser.

## Features

- **CSV File Upload**: Upload inventory CSV files through a web interface
- **Real-time Analysis**: Process inventory data and generate trend analysis
- **AI Recommendations**: Get AI-powered inventory management recommendations
- **HTML Reports**: Generate downloadable HTML reports
- **RESTful API**: JSON API endpoints for programmatic access
- **Health Check**: Health monitoring endpoint

## Architecture

### Components Used

- **Flask**: Web framework for handling HTTP requests
- **InventoryManager**: Manages inventory data from CSV files
- **TrendAnalyzer**: Analyzes Google Trends data
- **InventoryAgent**: Generates AI-powered recommendations using Gemini
- **ReportGenerator**: Creates HTML reports

### File Structure

```
app.py
├── Flask Application Setup
├── Custom JSON Encoder (NumpyJSONProvider)
├── File Upload Handler
├── Inventory Processing Function
├── Report Download Endpoint
└── Health Check Endpoint
```

## API Endpoints

### 1. `GET /`
**Description**: Home page with file upload form

**Response**: Renders `index.html` template

**Usage**:
```bash
# Open in browser
http://localhost:5000
```

---

### 2. `POST /upload`
**Description**: Handle CSV file upload and process inventory

**Request**:
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): CSV file to upload
  - `max_keywords` (optional): Maximum keywords to analyze (default: 15)
  - `min_confidence` (optional): Minimum confidence threshold (default: 20.0)

**Response**:
```json
{
  "success": true,
  "inventory_summary": {
    "total_items": 59,
    "low_stock_items": 0,
    "total_value": 284370.00
  },
  "trending_products": [
    {
      "keyword": "chunky sneakers",
      "status": "Rising",
      "confidence": 45.5,
      "velocity": 12.3,
      "strength": 68.2
    }
  ],
  "recommendations": "AI-generated recommendations text...",
  "low_stock_count": 5,
  "low_stock_items": [
    {
      "product_name": "Golf Shoes",
      "current_stock": 35,
      "reorder_point": 25
    }
  ],
  "report_url": "/reports/atim_report_20250120_120000.html"
}
```

**Error Responses**:
- `400 Bad Request`: Missing file, invalid file type, or empty filename
- `500 Internal Server Error`: Processing error with traceback

**Example cURL**:
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@inventory.csv" \
  -F "max_keywords=15" \
  -F "min_confidence=20.0"
```

---

### 3. `GET /reports/<filename>`
**Description**: Download or view generated HTML report

**Parameters**:
- `filename`: Name of the report file (e.g., `atim_report_20250120_120000.html`)

**Response**: HTML file (served as `text/html`)

**Usage**:
```bash
# Open in browser
http://localhost:5000/reports/atim_report_20250120_120000.html
```

---

### 4. `GET /health`
**Description**: Health check endpoint for monitoring

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T12:00:00"
}
```

**Usage**:
```bash
curl http://localhost:5000/health
```

## Configuration

### Application Settings

```python
app.config['UPLOAD_FOLDER'] = 'uploads'          # Directory for uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv'}       # Allowed file extensions
```

### Directories Created

- `uploads/`: Stores uploaded CSV files (with timestamp prefix)
- `reports/`: Stores generated HTML reports
- `templates/`: Contains HTML templates (if exists)

## Key Functions

### `allowed_file(filename)`
**Purpose**: Validate file extension

**Parameters**:
- `filename`: Name of the uploaded file

**Returns**: `True` if file extension is `.csv`, `False` otherwise

---

### `process_inventory(csv_filepath, max_keywords=15, min_confidence=20.0)`
**Purpose**: Core processing function that analyzes inventory and generates recommendations

**Parameters**:
- `csv_filepath`: Path to uploaded CSV file
- `max_keywords`: Maximum number of keywords to analyze (default: 15)
- `min_confidence`: Minimum confidence threshold for trends (default: 20.0)

**Returns**: Dictionary containing:
- `success`: Boolean indicating success
- `inventory_summary`: Summary statistics
- `trending_products`: List of trending products
- `recommendations`: AI-generated recommendations
- `low_stock_items`: Items below reorder point
- `report_url`: URL to generated HTML report

**Process Flow**:
1. Load inventory from CSV file
2. Extract keywords from product names
3. Analyze trends using TrendAnalyzer
4. Generate AI recommendations using InventoryAgent
5. Identify low stock items
6. Generate HTML report
7. Return JSON response

---

### `convert_to_python_type(obj)`
**Purpose**: Convert numpy/pandas types to native Python types for JSON serialization

**Parameters**:
- `obj`: Object to convert (can be dict, list, numpy types, etc.)

**Returns**: Object with all numpy types converted to Python native types

**Handles**:
- `np.integer`, `np.int64` → `int`
- `np.floating`, `np.float64` → `float`
- `np.ndarray` → `list`
- Recursively processes dicts and lists

---

### `NumpyJSONProvider`
**Purpose**: Custom JSON encoder class to handle numpy types in Flask responses

**Usage**: Automatically registered with Flask app to handle numpy serialization

## File Upload Process

1. **Validation**: Check if file is present, not empty, and has `.csv` extension
2. **Security**: Use `secure_filename()` to sanitize filename
3. **Storage**: Save with timestamp prefix: `YYYYMMDD_HHMMSS_originalname.csv`
4. **Processing**: Pass to `process_inventory()` function
5. **Response**: Return JSON with analysis results

## Error Handling

### Client Errors (400)
- No file provided
- No file selected
- Invalid file type (non-CSV)

### Server Errors (500)
- Processing exceptions
- Includes full traceback in response for debugging

## Dependencies

### Required Packages
```python
flask                    # Web framework
werkzeug                 # File handling utilities
numpy                    # Numerical operations
```

### Internal Dependencies
```python
inventory_data           # InventoryManager class
trend_analysis           # TrendAnalyzer class
llm_inventory_agent      # InventoryAgent class
report_generator         # ReportGenerator class
format_utils             # clean_llm_output function
config                   # CURRENT_SEASON constant
```

## Running the Application

### Basic Usage
```bash
python app.py
```

### Default Configuration
- **Host**: `0.0.0.0` (accessible from all network interfaces)
- **Port**: `5000`
- **Debug Mode**: Enabled

### Access the Application
```
http://localhost:5000
```

### Stop the Server
Press `Ctrl+C` in the terminal

## Example Workflow

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Open browser** and navigate to `http://localhost:5000`

3. **Upload CSV file** through the web interface:
   - Select your inventory CSV file
   - Optionally set `max_keywords` and `min_confidence`
   - Click "Upload and Analyze"

4. **View results**:
   - See inventory summary
   - Review trending products
   - Read AI recommendations
   - Check low stock alerts
   - Download HTML report

5. **Download report**:
   - Click on the report URL
   - Save the HTML file for offline viewing

## CSV File Format

The application accepts CSV files in the format supported by `InventoryManager`. See `CSV_FORMAT.md` for detailed format specifications.

**Minimum Required Columns**:
- `Shoe Description` (or `product_name`)
- `Number of Items Left` (or `current_stock`)

**Extended Format** (optional):
- Category
- Reorder Point
- Reorder Quantity
- Lead Time (days)
- Warehouse Location
- Cost Per Unit
- Selling Price

## Security Considerations

1. **File Validation**: Only CSV files are accepted
2. **Filename Sanitization**: Uses `secure_filename()` to prevent path traversal
3. **File Size Limit**: 16MB maximum file size
4. **Error Handling**: Errors don't expose sensitive system information

## Troubleshooting

### Issue: Template not found
**Solution**: Ensure `templates/index.html` exists, or the app will use current directory

### Issue: Upload folder permission errors
**Solution**: Ensure write permissions for the `uploads/` directory

### Issue: JSON serialization errors
**Solution**: The custom `NumpyJSONProvider` should handle this automatically

### Issue: API quota exceeded
**Solution**: The system will automatically retry and fall back to rule-based recommendations

## Integration with Other Components

### InventoryManager
- Loads inventory from uploaded CSV
- Provides inventory summary and item lists

### TrendAnalyzer
- Analyzes trends for product keywords
- Falls back to sample data if SerpAPI key not available

### InventoryAgent
- Generates AI recommendations using Gemini API
- Includes retry logic for quota errors
- Falls back to rule-based recommendations if API fails

### ReportGenerator
- Creates formatted HTML reports
- Includes all analysis results and recommendations

## Future Enhancements

Potential improvements:
- User authentication
- Multiple file format support (Excel, JSON)
- Real-time progress updates via WebSockets
- Export to PDF format
- Historical analysis tracking
- Dashboard with charts and graphs
- API key management interface

## License

Part of the ATIM (AI Trend & Inventory Manager) project.

---

**Last Updated**: 2025-01-20
**Version**: 1.0
