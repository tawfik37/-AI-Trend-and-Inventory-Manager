"""
Analytics service for calculating inventory metrics and statistics.
"""
from collections import defaultdict
from typing import List, Dict


def calculate_analytics(inventory_items, trending_products):
    """
    Calculate comprehensive analytics for visualization.

    Args:
        inventory_items: List of InventoryItem objects
        trending_products: List of trending product data

    Returns:
        Dictionary with analytics data
    """
    # Category breakdown
    category_data = defaultdict(lambda: {'count': 0, 'total_stock': 0, 'total_value': 0.0, 'total_revenue_potential': 0.0})
    warehouse_data = defaultdict(lambda: {'count': 0, 'total_stock': 0, 'total_value': 0.0})
    stock_health_data = {'healthy': 0, 'warning': 0, 'critical': 0, 'overstocked': 0}
    financial_metrics = {
        'total_inventory_value': 0.0,
        'total_revenue_potential': 0.0,
        'total_cost': 0.0,
        'potential_profit': 0.0,
        'average_margin': 0.0
    }

    # Process each item
    for item in inventory_items:
        # Category analytics
        cat = item.category
        category_data[cat]['count'] += 1
        category_data[cat]['total_stock'] += item.current_stock
        item_value = item.current_stock * item.cost_per_unit
        category_data[cat]['total_value'] += item_value
        revenue_potential = item.current_stock * item.selling_price
        category_data[cat]['total_revenue_potential'] += revenue_potential

        # Warehouse analytics
        wh = item.warehouse_location
        warehouse_data[wh]['count'] += 1
        warehouse_data[wh]['total_stock'] += item.current_stock
        warehouse_data[wh]['total_value'] += item_value

        # Stock health
        stock_ratio = item.current_stock / item.reorder_point if item.reorder_point > 0 else 0
        if item.current_stock <= item.reorder_point * 0.5:
            stock_health_data['critical'] += 1
        elif item.current_stock <= item.reorder_point:
            stock_health_data['warning'] += 1
        elif item.current_stock <= item.reorder_point * 2:
            stock_health_data['healthy'] += 1
        else:
            stock_health_data['overstocked'] += 1

        # Financial metrics
        financial_metrics['total_inventory_value'] += item_value
        financial_metrics['total_revenue_potential'] += revenue_potential
        financial_metrics['total_cost'] += item_value

    # Calculate average margin
    if financial_metrics['total_cost'] > 0:
        financial_metrics['potential_profit'] = financial_metrics['total_revenue_potential'] - financial_metrics['total_cost']
        financial_metrics['average_margin'] = (financial_metrics['potential_profit'] / financial_metrics['total_revenue_potential']) * 100 if financial_metrics['total_revenue_potential'] > 0 else 0

    # Stock levels by category (for bar chart)
    stock_by_category = []
    reorder_by_category = []
    categories_list = []
    for cat, data in sorted(category_data.items()):
        categories_list.append(cat)
        stock_by_category.append(data['total_stock'])
        # Calculate average reorder point for category
        avg_reorder = sum(item.reorder_point for item in inventory_items if item.category == cat) / max(1, data['count'])
        reorder_by_category.append(int(avg_reorder))

    # Trend status distribution
    trend_status_dist = defaultdict(int)
    for trend in trending_products:
        trend_status_dist[trend.get('status', 'Unknown')] += 1

    # Top products by value
    products_by_value = sorted(
        [
            {
                'name': item.product_name,
                'value': item.current_stock * item.cost_per_unit,
                'stock': item.current_stock,
                'category': item.category
            }
            for item in inventory_items
        ],
        key=lambda x: x['value'],
        reverse=True
    )[:10]

    # Top products by revenue potential
    products_by_revenue = sorted(
        [
            {
                'name': item.product_name,
                'revenue_potential': item.current_stock * item.selling_price,
                'stock': item.current_stock,
                'category': item.category
            }
            for item in inventory_items
        ],
        key=lambda x: x['revenue_potential'],
        reverse=True
    )[:10]

    return {
        'category_breakdown': {
            'categories': list(category_data.keys()),
            'counts': [category_data[cat]['count'] for cat in sorted(category_data.keys())],
            'total_stock': [category_data[cat]['total_stock'] for cat in sorted(category_data.keys())],
            'total_value': [float(category_data[cat]['total_value']) for cat in sorted(category_data.keys())],
            'revenue_potential': [float(category_data[cat]['total_revenue_potential']) for cat in sorted(category_data.keys())]
        },
        'warehouse_breakdown': {
            'warehouses': list(warehouse_data.keys()),
            'counts': [warehouse_data[wh]['count'] for wh in sorted(warehouse_data.keys())],
            'total_stock': [warehouse_data[wh]['total_stock'] for wh in sorted(warehouse_data.keys())],
            'total_value': [float(warehouse_data[wh]['total_value']) for wh in sorted(warehouse_data.keys())]
        },
        'stock_health': stock_health_data,
        'stock_by_category': {
            'categories': categories_list,
            'current_stock': stock_by_category,
            'reorder_points': reorder_by_category
        },
        'financial_metrics': financial_metrics,
        'trend_status_distribution': dict(trend_status_dist),
        'top_products_by_value': products_by_value[:10],
        'top_products_by_revenue': products_by_revenue[:10]
    }
