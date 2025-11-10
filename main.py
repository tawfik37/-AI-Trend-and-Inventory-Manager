"""
Main application for AI Trend & Inventory Manager (ATIM)
Integrates Component A (Trend Analysis) and Component B (LLM Inventory Agent)
"""
import sys
from datetime import datetime
from trend_analysis import TrendAnalyzer
from llm_inventory_agent import InventoryAgent
from config import CURRENT_SEASON
from inventory_data import InventoryManager


def get_shoe_keywords(inventory_items: list = None, use_inventory: bool = True, additional_keywords: list = None) -> list:
    """
    Get list of shoe-related keywords for trend analysis.
    
    Args:
        inventory_items: Optional list of InventoryItem objects (to avoid reloading)
        use_inventory: If True, generate keywords from inventory CSV (default: True)
        additional_keywords: Optional list of additional keywords to include
    
    Returns:
        List of keywords for trend analysis
    """
    keywords = []
    
    if use_inventory:
        # Generate keywords from inventory CSV
        if inventory_items:
            # Use provided inventory items
            items = inventory_items
        else:
            # Load inventory items
            try:
                inventory_manager = InventoryManager()
                items = inventory_manager.get_all_inventory()
            except Exception as e:
                print(f"   Warning: Could not load keywords from inventory: {e}")
                print("   Using default keyword list instead...")
                items = None
        
        if items:
            # Convert product names to lowercase keywords
            for item in items:
                # Use product name as keyword (convert to lowercase)
                keyword = item.product_name.lower()
                keywords.append(keyword)
        else:
            # Fallback to default keywords
            keywords = [
                "chunky sneakers",
                "waterproof boots",
                "espadrilles",
                "ankle boots",
                "retro runners",
                "platform sandals",
                "minimalist running shoes",
                "suede boots",
                "canvas shoes",
                "running sneakers",
                "hiking boots",
                "dress shoes",
                "loafers",
                "high top sneakers",
                "slip on shoes"
            ]
    else:
        # Use default manual keyword list
        keywords = [
            "chunky sneakers",
            "waterproof boots",
            "espadrilles",
            "ankle boots",
            "retro runners",
            "platform sandals",
            "minimalist running shoes",
            "suede boots",
            "canvas shoes",
            "running sneakers",
            "hiking boots",
            "dress shoes",
            "loafers",
            "high top sneakers",
            "slip on shoes"
        ]
    
    # Add additional keywords if provided
    if additional_keywords:
        for keyword in additional_keywords:
            if keyword.lower() not in [k.lower() for k in keywords]:
                keywords.append(keyword.lower())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower not in seen:
            seen.add(keyword_lower)
            unique_keywords.append(keyword)
    
    return unique_keywords


def get_upcoming_holidays() -> list:
    """Get list of upcoming holidays/events (can be made dynamic)."""
    # This can be enhanced to automatically detect upcoming holidays
    return ["Labor Day", "Back to School", "Fall Fashion Week"]


def main():
    """Main application function."""
    print("=" * 70)
    print("AI TREND & INVENTORY MANAGER (ATIM)")
    print("=" * 70)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current Season: {CURRENT_SEASON}")
    print("=" * 70)
    
    # Initialize components
    print("\n[1/3] Initializing Trend Analyzer...")
    trend_analyzer = TrendAnalyzer()
    
    print("[2/3] Initializing Inventory Manager...")
    inventory_manager = InventoryManager()
    inventory_summary = inventory_manager.get_inventory_summary()
    inventory_items = inventory_manager.get_all_inventory()
    
    print(f"   - Total Items: {inventory_summary['total_items']}")
    print(f"   - Low Stock Items: {inventory_summary['low_stock_items']}")
    print(f"   - Total Inventory Value: ${inventory_summary['total_inventory_value']:,.2f}")
    
    print("[3/3] Initializing LLM Inventory Agent...")
    try:
        inventory_agent = InventoryAgent()
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("\nPlease create a .env file with your GEMINI_API_KEY:")
        print("GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Step 1: Analyze Trends (Component A)
    print("\n" + "=" * 70)
    print("COMPONENT A: TREND ANALYSIS")
    print("=" * 70)
    
    # Get keywords from inventory CSV (default) or use manual list
    # Pass inventory_items to avoid reloading the CSV
    # You can also add additional keywords: get_shoe_keywords(inventory_items=inventory_items, additional_keywords=["new trend"])
    keywords = get_shoe_keywords(inventory_items=inventory_items, use_inventory=True)
    print(f"\nTotal keywords available: {len(keywords)}")
    
    # Show sample of keywords being analyzed
    if len(keywords) > 10:
        print(f"   Sample keywords: {', '.join(keywords[:10])}...")
        print(f"   (Showing first 10 of {len(keywords)} total keywords)")
    else:
        print(f"   Keywords: {', '.join(keywords)}")
    
    # Limit keywords to avoid rate limits (Google Trends has strict rate limiting)
    max_keywords_to_analyze = 15
    if len(keywords) > max_keywords_to_analyze:
        print(f"\n   Note: Analyzing first {max_keywords_to_analyze} keywords to avoid API rate limits.")
        print(f"   To analyze all {len(keywords)} keywords, run multiple times or increase delays in trend_analysis.py")
    
    trending_products = trend_analyzer.get_high_confidence_trends(
        keywords,
        min_confidence=20.0,
        max_keywords=max_keywords_to_analyze
    )
    
    # If no trends found due to rate limiting, create sample data for demonstration
    if not trending_products:
        print("\nWarning: No trend data retrieved (likely due to API rate limits).")
        print("Creating sample trend data for demonstration purposes...")
        
        # Create sample trends based on inventory items
        sample_keywords = keywords[:5]  # Use first 5 keywords
        trending_products = []
        import random
        
        for keyword in sample_keywords:
            # Find matching inventory item
            matching_item = None
            for item in inventory_items:
                if keyword.lower() in item.product_name.lower():
                    matching_item = item
                    break
            
            # Generate sample trend data
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
                "confidence": confidence,
                "velocity": velocity,
                "strength": base_strength,
                "current_value": base_strength,
                "peak_value": base_strength * 1.2
            })
        
        print(f"   Generated {len(trending_products)} sample trends for demonstration")
    
    if trending_products:
        print(f"\nFound {len(trending_products)} trending products:")
        print("\nTop Trending Products:")
        for i, trend in enumerate(trending_products[:5], 1):
            print(f"  {i}. {trend['keyword'].title()}")
            print(f"     Status: {trend['status']} | Confidence: {trend['confidence']:.2f}")
            print(f"     Velocity: {trend['velocity']:.2f} | Strength: {trend['strength']:.2f}")
    else:
        print("\nNo trending products found. Using minimal sample data...")
        trending_products = [{
            "keyword": keywords[0] if keywords else "sample product",
            "status": "Rising",
            "confidence": 45.0,
            "velocity": 12.3,
            "strength": 68.2,
            "current_value": 68.2,
            "peak_value": 80.0
        }]
    
    # Step 2: Generate Inventory Recommendations (Component B)
    print("\n" + "=" * 70)
    print("COMPONENT B: INVENTORY MANAGEMENT RECOMMENDATIONS")
    print("=" * 70)
    
    upcoming_holidays = get_upcoming_holidays()
    print(f"\nGenerating recommendations based on:")
    print(f"  - {len(trending_products)} trending products")
    print(f"  - Current season: {CURRENT_SEASON}")
    print(f"  - Upcoming events: {', '.join(upcoming_holidays)}")
    
    recommendations = inventory_agent.generate_recommendations(
        trending_products,
        current_season=CURRENT_SEASON,
        upcoming_holidays=upcoming_holidays
    )
    
    print("\n" + "-" * 70)
    print("RECOMMENDATIONS:")
    print("-" * 70)
    print(recommendations)
    print("-" * 70)
    
    # Step 3: Display Inventory Status
    print("\n" + "=" * 70)
    print("CURRENT INVENTORY STATUS")
    print("=" * 70)
    
    low_stock_items = [
        item for item in inventory_manager.get_all_inventory()
        if item.current_stock <= item.reorder_point
    ]
    
    if low_stock_items:
        print("\n⚠️  LOW STOCK ALERT:")
        for item in low_stock_items:
            print(f"  - {item.product_name}: {item.current_stock} units "
                  f"(Reorder Point: {item.reorder_point})")
    else:
        print("\n✓ All items are above reorder point")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Review the recommendations above")
    print("2. Adjust reorder quantities based on trend analysis")
    print("3. Update warehouse locations for trending items")
    print("4. Schedule markdowns for declining items")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

