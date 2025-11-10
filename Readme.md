# [cite_start]Project: AI Trend & Inventory Manager (ATIM) [cite: 1]

## 1. Executive Summary

[cite_start]The AI Trend & Inventory Manager (ATIM) is a proof-of-concept tool using predictive analytics and Generative AI to optimize retail inventory[cite: 3]. [cite_start]It addresses inventory management challenges by correlating real-time public interest from Google Trends with operational stock levels[cite: 4]. [cite_start]The primary use case focuses on a shoe retailer, guiding purchasing and warehousing strategies based on emerging trends[cite: 5].

## 2. Problem Statement

[cite_start]Traditional inventory management often relies on historical data and manual intuition[cite: 7], leading to:

* [cite_start]**Missed Opportunities:** Slowness in capitalizing on emerging trends[cite: 8].
* [cite_start]**Waste and Markdowns:** Overstocking items with declining popularity[cite: 9].
* [cite_start]**Operational Friction:** A gap between market intelligence and actionable inventory adjustments[cite: 10].

## 3. Proposed Solution: ATIM Architecture

[cite_start]The tool has two main Al-driven components[cite: 12]:

### [cite_start]A. Trend Analysis and Prediction (Component A) [cite: 13]

* [cite_start]**Function:** Automatically fetches real-time search interest data from the Google Trends API for relevant keywords (e.g., "chunky sneakers," "waterproof boots")[cite: 14].
* [cite_start]**Mechanism:** Analyzes search interest velocity and volume to identify rising, peaking, or declining trends[cite: 15].
* [cite_start]**Output:** Generates a ranked list of "High-Confidence Trending Products"[cite: 16].

### [cite_start]B. Inventory & Warehouse Management (Component B) [cite: 17]

* [cite_start]**Function:** Serves as a dynamic consulting agent for logistics and stocking[cite: 18].
* [cite_start]**Inputs:** The LLM is fed[cite: 19]:
    1.  [cite_start]The Trending Product List from Component A[cite: 20].
    2.  [cite_start]The retailer's Current Inventory Data[cite: 21].
    3.  [cite_start]Contextual Factors (e.g., current season)[cite: 21].
* [cite_start]**Output:** Generates actionable, natural language recommendations [cite: 22][cite_start], such as reorder suggestions [cite: 25][cite_start], warehousing strategy [cite: 26][cite_start], and risk assessment[cite: 27].

## 4. Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
- Internet connection for Google Trends API

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd Retal
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   - Create a `.env` file in the project root
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Optionally specify the model:
     ```
     GEMINI_MODEL=gemini-2.0-flash
     ```

## 5. Usage

### Running the Complete ATIM System

Run the main application to execute both components:

```bash
python main.py
```

This will:
1. Analyze Google Trends for shoe-related keywords (Component A)
2. Generate inventory recommendations using LLM (Component B)
3. Display current inventory status and alerts

### Running Individual Components

#### Component A: Trend Analysis Only

```bash
python trend_analysis.py
```

This will analyze trends for predefined shoe keywords and display high-confidence trending products.

#### Component B: Inventory Agent Only

```bash
python llm_inventory_agent.py
```

This will generate recommendations using sample trend data (requires Google Gemini API key).

## 6. Project Structure

```
Retal/
├── main.py                  # Main application (integrates both components)
├── trend_analysis.py        # Component A: Google Trends analysis
├── llm_inventory_agent.py   # Component B: LLM-based inventory recommendations
├── inventory_data.py        # Inventory data management
├── config.py                # Configuration settings
├── store_inventory.csv      # Inventory data (CSV file with 59 products)
├── requirements.txt         # Python dependencies
├── CSV_FORMAT.md           # CSV file format documentation
├── SETUP_GUIDE.md          # Setup instructions
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore file
└── Readme.md               # This file
```

## 7. Scripts Overview

### `main.py`
Main application that integrates both components. Executes the complete ATIM workflow:
- Fetches and analyzes Google Trends data
- Generates LLM-powered inventory recommendations
- Displays inventory status and alerts

### `trend_analysis.py`
Implements Component A. Features:
- Connects to Google Trends API via `pytrends`
- Analyzes trend velocity and strength for keywords
- Classifies trends as Rising, Peaking, Declining, or Stable
- Ranks products by confidence score
- Returns high-confidence trending products

### `llm_inventory_agent.py`
Implements Component B. Features:
- Uses Google Gemini API to generate recommendations
- Combines trend data with inventory data
- Considers contextual factors (season, holidays)
- Generates actionable recommendations for:
  - Reorder suggestions
  - Warehousing strategy
  - Risk assessment
  - Priority actions

### `inventory_data.py`
Manages inventory data:
- Loads inventory from CSV file (`store_inventory.csv`)
- Supports both minimal (2 columns) and expanded (9 columns) CSV formats
- Automatically infers missing data (category, reorder points, pricing)
- Functions to query and update inventory
- Inventory summary generation
- Auto-saves changes back to CSV file

### `config.py`
Configuration settings:
- API keys and model configuration
- Google Trends settings (geo, timeframe)
- Inventory defaults
- Season mapping

## 8. Example Use Cases

### Use Case 1: Late Summer Trend Analysis

**Scenario**: Late Summer, trending "Ankle Boots" and "Suede"

**ATIM Output**:
- Trend Analysis shows sharp spike in "Ankle Boot" and "Suede" searches
- LLM Recommendation: "Increase orders for suede ankle boots by 30% immediately. Move lightweight canvas shoes to a low-priority warehouse location."

### Use Case 2: Sustained Trend Management

**Scenario**: High interest in '90s-style "Retro Runners"

**ATIM Output**:
- Google Trends shows sustained, high interest
- LLM Recommendation: "Establish a minimum reorder point of 500 units for top 3 'Retro Runner' styles across all sizes to prevent stockouts."

### Use Case 3: Risk Assessment

**Scenario**: "Platform Sandals" trend sharply falling after peak

**ATIM Output**:
- Trend Analysis identifies declining trend
- LLM Recommendation: "Initiate a final clearance promotion on all 'Platform Sandals' within 7 days to clear Q3 stock and free up capital."

## 9. Configuration

### Google Trends Settings

Edit `config.py` to customize:
- `TRENDS_GEO`: Geographic region (default: "US")
- `TRENDS_TIMEFRAME`: Time range (default: "today 3-m" for last 3 months)

### Inventory Settings

Edit `config.py` to customize:
- `DEFAULT_REORDER_POINT`: Minimum stock level (default: 100)
- `DEFAULT_LEAD_TIME_DAYS`: Average lead time (default: 14 days)
- `CURRENT_SEASON`: Current season (default: "Late Summer")

### Google Gemini Settings

Edit `.env` file:
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL`: Model to use (default: "gemini-2.0-flash", alternatives: "gemini-2.5-flash", "gemini-2.5-pro" for more capability)

## 10. Customization

### Adding New Keywords

Edit the `get_shoe_keywords()` function in `main.py` to add more keywords for trend analysis.

### Modifying Inventory Data

Edit the `store_inventory.csv` file directly to add or modify inventory items. The CSV supports:
- **Minimal format**: Just "Shoe Description" and "Number of Items Left" (system will infer other fields)
- **Expanded format**: All 9 columns including Category, Reorder Point, Cost, Price, etc.

See `CSV_FORMAT.md` for detailed documentation on the CSV file format.

### Adjusting Trend Confidence Threshold

Modify the `min_confidence` parameter in `main.py`:
```python
trending_products = trend_analyzer.get_high_confidence_trends(
    keywords,
    min_confidence=30.0  # Adjust this value
)
```

## 11. Limitations & Future Enhancements

### Current Limitations

- Uses sample/mock inventory data (not connected to real inventory systems)
- Google Trends API has rate limits
- Requires Google Gemini API key (free tier available with usage limits)
- Trend analysis is based on search interest, not actual sales data

### Future Enhancements

- Integration with real inventory management systems
- Historical sales data analysis
- Multi-region trend analysis
- Automated reordering system integration
- Real-time alerts and notifications
- Web dashboard interface
- Machine learning models for demand forecasting
- Integration with e-commerce platforms

## 12. Troubleshooting

### Common Issues

**Issue**: "Google Gemini API key is required"
- **Solution**: Create a `.env` file with your `GEMINI_API_KEY`

**Issue**: "Error fetching trends"
- **Solution**: Check internet connection and wait a few seconds (rate limiting)

**Issue**: "No trends found"
- **Solution**: Lower the `min_confidence` threshold or check keyword relevance

**Issue**: Import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## 13. AI and Management Relevance

This project demonstrates core AI concepts applied to management:

1. **Predictive Sourcing**: Using public data (Google Trends) as a leading indicator for demand forecasting
2. **Agile Logistics**: Enabling warehouse teams to rapidly adjust stock positioning based on real-time market shifts
3. **Decision Augmentation**: The LLM acts as an expert consultant, translating complex data into clear, human-readable business strategy

## 14. License

This is a proof-of-concept project for educational and demonstration purposes.

## 15. Contact & Support

For questions or issues, please refer to the project documentation or create an issue in the project repository.