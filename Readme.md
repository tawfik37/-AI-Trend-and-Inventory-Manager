# AI Trend & Inventory Manager (ATIM)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **An intelligent inventory management system that uses Google Trends and Google Gemini AI to optimize retail inventory decisions through predictive analytics and real-time trend analysis.**

## What is ATIM?

ATIM is a smart inventory management tool that helps retailers:
- **Analyze trends** - Automatically fetches Google Trends data for your products
- **Get AI recommendations** - Uses Google Gemini AI to suggest inventory actions
- **Optimize stock levels** - Identifies when to reorder, markdown, or adjust warehouse placement
- **Predict demand** - Spots rising, peaking, and declining trends before they impact sales

## Key Features

### 📊 Trend Analysis
- Real-time Google Trends data fetching via SerpAPI
- Automatic trend classification (Rising, Peaking, Declining, Stable)
- Trend velocity and strength analysis
- Confidence scoring and ranking

### 🤖 AI-Powered Recommendations
- Intelligent inventory recommendations using Google Gemini AI
- Context-aware suggestions (season, holidays, trends)
- Reorder point calculations
- Warehousing strategy suggestions
- Risk assessment and markdown recommendations

### 💻 Web Interface
- Upload CSV inventory files through a modern web interface
- Interactive data visualizations (charts and graphs)
- Sortable and filterable tables
- Export functionality for reports and data
- Real-time progress tracking
- Low stock alerts with suggested reorder quantities

### 📁 Inventory Management
- CSV-based inventory system
- Supports minimal (2 columns) or expanded (9 columns) formats
- Automatic category inference
- Pre-loaded with sample inventory data

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- SerpAPI key ([Get one here](https://serpapi.com/users/sign_up)) - Optional but recommended for real trend data
- Internet connection

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/omarsl255/-AI-Trend-and-Inventory-Manager.git
cd -AI-Trend-and-Inventory-Manager
```

#### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the project root directory:

```env
# Google Gemini API Configuration (Required)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# SerpAPI Configuration (Optional but recommended)
SERPAPI_KEY=your_serpapi_key_here
```

**Getting API Keys:**

1. **Google Gemini API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key" or "Get API Key"
   - Copy the key and paste it in your `.env` file

2. **SerpAPI Key (Optional):**
   - Visit [SerpAPI](https://serpapi.com/users/sign_up)
   - Sign up for a free account (100 free searches/month)
   - Go to your dashboard and copy your API key
   - Paste it in your `.env` file
   - **Note:** If you don't provide a SerpAPI key, the system will use sample trend data

#### 5. Verify Installation
```bash
python -c "from inventory_data import InventoryManager; im = InventoryManager(); print(f'Loaded {len(im.get_all_inventory())} items')"
```

## Usage

### Option 1: Web Interface (Recommended)

Run the Flask web application:

```bash
python app.py
```

Then open your browser and go to: `http://localhost:5000`

**Features:**
- Upload your inventory CSV file
- View interactive charts and visualizations
- See AI-powered recommendations
- Export reports and data
- Track low stock alerts

### Option 2: Command Line Interface

Run the main application:

```bash
python main.py
```

**Output includes:**
- Trend analysis for inventory products
- AI-generated inventory recommendations
- Low stock alerts
- Inventory summary and statistics

### Option 3: Individual Components

#### Trend Analysis Only
```bash
python trend_analysis.py
```
Analyzes trends for predefined keywords and displays trending products.

#### Inventory Agent Only
```bash
python llm_inventory_agent.py
```
Generates recommendations using sample trend data (requires Gemini API key).

## Project Structure

```
-AI-Trend-and-Inventory-Manager/
│
├── app.py                      # Flask web application
├── main.py                     # Command-line interface
├── trend_analysis.py           # Google Trends analysis (Component A)
├── llm_inventory_agent.py      # AI recommendations (Component B)
├── inventory_data.py           # Inventory data management
├── config.py                   # Configuration settings
├── format_utils.py             # CSV format utilities
├── report_generator.py         # HTML report generation
│
├── store_inventory.csv         # Sample inventory data
│
├── templates/
│   └── index.html              # Web interface template
│
├── uploads/                    # Uploaded CSV files (created automatically)
├── reports/                    # Generated reports (created automatically)
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this file)
│
├── Readme.md                   # This file
├── SETUP_GUIDE.md             # Detailed setup instructions
├── CSV_FORMAT.md              # CSV file format documentation
├── KEYWORDS_INFO.md           # Keywords management guide
└── APP_DOCUMENTATION.md       # Web app documentation
```

## How It Works

### Architecture Overview

```
┌──────────────────────┐         ┌──────────────────────┐
│  Component A:        │         │  Component B:        │
│  Trend Analysis      │────────▶│  LLM Inventory Agent │
│                      │         │                      │
│  • SerpAPI/Google    │         │  • Google Gemini AI  │
│    Trends API        │         │  • Recommendations   │
│  • Trend Velocity    │         │  • Risk Assessment   │
│  • Classification    │         │  • Context Awareness │
└──────────────────────┘         └──────────────────────┘
         │                                 │
         │                                 │
         ▼                                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Inventory CSV (store_inventory.csv)             │
│  • Products  • Stock Levels  • Categories  • Pricing        │
└─────────────────────────────────────────────────────────────┘
```

### Process Flow

1. **Load Inventory** - Reads product data from CSV file
2. **Extract Keywords** - Generates search keywords from product names
3. **Fetch Trends** - Retrieves Google Trends data via SerpAPI (or uses sample data)
4. **Analyze Trends** - Calculates trend velocity, strength, and status
5. **Generate Recommendations** - AI analyzes trends + inventory + context to suggest actions
6. **Display Results** - Shows recommendations, alerts, and visualizations

## CSV Inventory Format

The system supports two CSV formats:

### Minimal Format (2 columns - Required)
```csv
Shoe Description,Number of Items Left
Chunky Sneakers,150
Waterproof Boots,80
```

### Expanded Format (9 columns - Optional)
```csv
Shoe Description,Number of Items Left,Category,Reorder Point,Reorder Quantity,Lead Time (days),Warehouse Location,Cost Per Unit,Selling Price
Chunky Sneakers,150,Casual,100,200,10,Zone A,45.00,89.99
Waterproof Boots,80,Outdoor,50,150,14,Zone B,60.00,129.99
```

**Column Details:**
- `Shoe Description` (required) - Product name
- `Number of Items Left` (required) - Current stock level
- `Category` (optional) - Product category
- `Reorder Point` (optional) - Minimum stock level before reordering
- `Reorder Quantity` (optional) - Suggested order quantity
- `Lead Time (days)` (optional) - Days until new stock arrives
- `Warehouse Location` (optional) - Storage location
- `Cost Per Unit` (optional) - Purchase cost
- `Selling Price` (optional) - Retail price

See [CSV_FORMAT.md](CSV_FORMAT.md) for complete documentation.

## Configuration

### Environment Variables (.env file)

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# Optional (for real trend data)
SERPAPI_KEY=your_serpapi_key_here
```

### Configuration File (config.py)

Edit `config.py` to customize:

```python
# Google Trends Settings
TRENDS_GEO = "US"              # Geographic region
TRENDS_TIMEFRAME = "today 3-m" # Time range (last 3 months)

# Inventory Settings
DEFAULT_REORDER_POINT = 100      # Minimum stock level
DEFAULT_LEAD_TIME_DAYS = 14      # Average lead time
CURRENT_SEASON = "Late Summer"   # Current season
```

## Troubleshooting

### "Google Gemini API key is required"
- Create a `.env` file in the project root
- Add: `GEMINI_API_KEY=your_key_here`
- Ensure no extra spaces or quotes around the key

### "SerpAPI key is required" (Warning)
- This is optional - the system will use sample trend data if no key is provided
- To get real trend data, add `SERPAPI_KEY=your_key_here` to your `.env` file
- Get a free key at [SerpAPI](https://serpapi.com/users/sign_up)

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Rate limit reached" (Google Trends)
- SerpAPI has rate limits (100 free searches/month)
- The system automatically handles delays and retries
- Wait a few minutes and try again
- Consider upgrading your SerpAPI plan for more searches

### CSV file not loading
- Ensure CSV file is in the correct format (see [CSV_FORMAT.md](CSV_FORMAT.md))
- Check that required columns exist: "Shoe Description", "Number of Items Left"
- Verify CSV encoding is UTF-8
- Check for empty rows or invalid data

### Web interface not working
- Make sure Flask is installed: `pip install flask`
- Check that port 5000 is not in use
- Verify `templates/index.html` exists

## Example Use Cases

### Use Case 1: Late Summer Trend Analysis
**Scenario:** Late Summer, trending "Ankle Boots" and "Suede"

**ATIM Analysis:**
- Trend Analysis: Sharp spike in "Ankle Boot" and "Suede" searches
- Inventory Status: 120 units in stock, reorder point: 80

**AI Recommendation:**
> "Increase orders for suede ankle boots by 30% immediately. Current stock of 120 units may be insufficient given the sharp rise in search interest. Move lightweight canvas shoes to a low-priority warehouse location to make room for trending items."

### Use Case 2: Risk Assessment & Markdowns
**Scenario:** "Platform Sandals" trend sharply falling after peak

**ATIM Analysis:**
- Trend Analysis: Declining trend with negative velocity (-15.2)
- Inventory Status: 250 units in stock, well above reorder point

**AI Recommendation:**
> "Initiate a final clearance promotion on all 'Platform Sandals' within 7 days to clear Q3 stock and free up capital. The trend signal is rapidly decreasing, indicating declining consumer interest. Consider 30-40% markdown to accelerate clearance."

## Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup and installation instructions
- **[CSV_FORMAT.md](CSV_FORMAT.md)** - Complete CSV file format documentation
- **[KEYWORDS_INFO.md](KEYWORDS_INFO.md)** - Keywords management and customization guide
- **[APP_DOCUMENTATION.md](APP_DOCUMENTATION.md)** - Web application documentation

## Limitations

- ⚠️ SerpAPI has rate limits (100 free searches/month)
- ⚠️ Uses CSV-based inventory (not connected to real inventory systems)
- ⚠️ Requires Google Gemini API key (free tier available)
- ⚠️ Trend analysis based on search interest, not actual sales data
- ⚠️ Limited to single geographic region (configurable)

## Future Enhancements

- 🔄 Integration with real inventory management systems (ERP, WMS)
- 🔄 Historical sales data analysis and demand forecasting
- 🔄 Multi-region trend analysis
- 🔄 Automated reordering system integration
- 🔄 Real-time alerts and notifications
- 🔄 Machine learning models for demand forecasting
- 🔄 Integration with e-commerce platforms (Shopify, WooCommerce)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is a proof-of-concept for educational and demonstration purposes.

## Acknowledgments

- **Google Trends API** / **SerpAPI** for trend data
- **Google Gemini AI** for intelligent recommendations
- **pandas** for data processing
- **Flask** for web framework
- **Chart.js** for data visualizations

## Contact & Support

- **GitHub Repository**: [https://github.com/omarsl255/-AI-Trend-and-Inventory-Manager](https://github.com/omarsl255/-AI-Trend-and-Inventory-Manager)
- **Issues**: [Create an issue](https://github.com/omarsl255/-AI-Trend-and-Inventory-Manager/issues)

---

**Made with ❤️ for intelligent inventory management**

*Last updated: 2025*
