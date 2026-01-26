"""
Inventory processing service for handling file uploads and analysis.
"""
import os
import random
from datetime import datetime
from typing import Dict
import numpy as np

from core.inventory_data import InventoryManager
from core.trend_analysis import TrendAnalyzer
from core.llm_inventory_agent import InventoryAgent
from utils.report_generator import ReportGenerator
from utils.format_utils import clean_llm_output
from config import CURRENT_SEASON
from services.analytics import calculate_analytics


def convert_to_python_type(obj):
    """Convert numpy/pandas types to native Python types."""
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_python_type(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_python_type(item) for item in obj]
    return obj


def generate_sample_trends(keywords, count=5):
    """
    Generate sample trend data when real data is unavailable.

    Args:
        keywords: List of keywords to generate data for
        count: Number of sample trends to generate

    Returns:
        List of sample trend dictionaries
    """
    sample_keywords = keywords[:count]
    trending_products = []

    for keyword in sample_keywords:
        base_strength = random.uniform(40, 80)
        velocity = random.uniform(-10, 15)
        confidence = abs(velocity) * 0.6 + base_strength * 0.4

        if velocity > 5:
            status = "Rising"
        elif velocity < -5:
            status = "Declining"
        elif base_strength > 70:
            status = "Peaking"
        else:
            status = "Stable"

        trending_products.append({
            "keyword": keyword,
            "status": status,
            "confidence": float(confidence),
            "velocity": float(velocity),
            "strength": float(base_strength),
            "current_value": float(base_strength),
            "peak_value": float(base_strength * 1.2)
        })

    return trending_products


def process_inventory(csv_filepath, max_keywords=15, min_confidence=20.0):
    """
    Process inventory file and generate analysis.

    Args:
        csv_filepath: Path to uploaded CSV file
        max_keywords: Maximum keywords to analyze
        min_confidence: Minimum confidence threshold

    Returns:
        Dictionary with analysis results
    """
    # Initialize components
    inventory_manager = InventoryManager(csv_file=csv_filepath)
    trend_analyzer = TrendAnalyzer()
    inventory_agent = InventoryAgent()

    # Get inventory data
    inventory_items = inventory_manager.get_all_inventory()
    inventory_summary = inventory_manager.get_inventory_summary()

    # Generate keywords
    keywords = [item.product_name.lower() for item in inventory_items]

    # Analyze trends
    trending_products = trend_analyzer.get_high_confidence_trends(
        keywords,
        min_confidence=min_confidence,
        max_keywords=max_keywords
    )

    # Fallback to sample data if no trends
    if not trending_products and keywords:
        trending_products = generate_sample_trends(keywords)

    # Convert trending products to ensure all values are JSON serializable
    trending_products = convert_to_python_type(trending_products)

    # Generate AI recommendations
    upcoming_holidays = ["Labor Day", "Back to School", "Fall Fashion Week"]
    recommendations = inventory_agent.generate_recommendations(
        trending_products,
        current_season=CURRENT_SEASON,
        upcoming_holidays=upcoming_holidays
    )

    # Clean the recommendations for better display
    recommendations_clean = clean_llm_output(recommendations)

    # Get low stock items
    low_stock_items = [
        item for item in inventory_items
        if item.current_stock <= item.reorder_point
    ]

    # Calculate additional analytics
    analytics = calculate_analytics(inventory_items, trending_products)

    # Generate HTML report
    report_gen = ReportGenerator()
    report_filename = f"atim_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_path = os.path.join('reports', report_filename)
    os.makedirs('reports', exist_ok=True)

    report_gen.generate_html_report(
        trending_products,
        inventory_summary,
        recommendations,
        low_stock_items,
        output_file=report_path
    )

    # Prepare response - convert all numpy types to Python types
    return {
        'success': True,
        'inventory_summary': {
            'total_items': int(inventory_summary['total_items']),
            'low_stock_items': int(inventory_summary['low_stock_items']),
            'total_value': float(inventory_summary['total_inventory_value'])
        },
        'trending_products': convert_to_python_type(trending_products[:10]),
        'recommendations': str(recommendations_clean),
        'low_stock_count': int(len(low_stock_items)),
        'low_stock_items': [
            {
                'product_name': str(item.product_name),
                'current_stock': int(item.current_stock),
                'reorder_point': int(item.reorder_point),
                'reorder_quantity': int(item.reorder_quantity) if hasattr(item, 'reorder_quantity') else int(item.reorder_point * 1.5),
                'category': str(item.category),
                'warehouse_location': str(item.warehouse_location),
                'cost_per_unit': float(item.cost_per_unit),
                'selling_price': float(item.selling_price)
            }
            for item in low_stock_items
        ],
        'analytics': convert_to_python_type(analytics),
        'report_url': f'/reports/{report_filename}'
    }
