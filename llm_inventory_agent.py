"""
Component B: Inventory & Warehouse Management LLM Agent
Uses Large Language Model to generate actionable inventory recommendations
based on trend data, current inventory, and contextual factors.
"""
import json
import time
from typing import List, Dict
from datetime import datetime
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, CURRENT_SEASON
from inventory_data import InventoryManager


class InventoryAgent:
    """LLM-based inventory management agent."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the Inventory Agent.
        
        Args:
            api_key: Google Gemini API key (defaults to config)
            model: Gemini model to use (defaults to config)
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or GEMINI_MODEL
        
        if not self.api_key:
            raise ValueError("Google Gemini API key is required. Set GEMINI_API_KEY in .env file or pass as parameter.")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
        self.inventory_manager = InventoryManager()
    
    def generate_recommendations(
        self,
        trending_products: List[Dict],
        current_season: str = None,
        upcoming_holidays: List[str] = None
    ) -> str:
        """
        Generate actionable inventory recommendations using LLM.
        
        Args:
            trending_products: List of trending products from Component A
            current_season: Current season (defaults to config)
            upcoming_holidays: List of upcoming holidays/events
            
        Returns:
            Natural language recommendations
        """
        current_season = current_season or CURRENT_SEASON
        upcoming_holidays = upcoming_holidays or []
        
        # Get inventory data
        inventory_data = self.inventory_manager.to_dict()
        inventory_summary = self.inventory_manager.get_inventory_summary()
        
        # Prepare prompt with system instructions
        system_instruction = "You are an expert inventory management consultant for a shoe retailer. " \
                           "You analyze market trends, inventory levels, and business context to provide " \
                           "actionable recommendations for inventory management, reordering, warehousing, " \
                           "and risk assessment. Your recommendations should be clear, specific, and " \
                           "prioritized by business impact."
        
        user_prompt = self._build_prompt(
            trending_products,
            inventory_data,
            inventory_summary,
            current_season,
            upcoming_holidays
        )
        
        # Combine system instruction and user prompt for Gemini
        full_prompt = f"{system_instruction}\n\n{user_prompt}"
        
        # Call Gemini API with retry logic
        max_retries = 3
        retry_delay = 1  # Start with 1 second
        
        for attempt in range(max_retries):
            try:
                # Generate content with configuration parameters
                # The generation_config can be passed as a dictionary
                response = self.client.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 2048,
                    }
                )
                
                recommendations = response.text
                return recommendations
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a quota error
                if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                    if attempt < max_retries - 1:
                        # Extract retry delay from error if available
                        if "retry in" in error_str.lower():
                            try:
                                # Try to extract the delay (in seconds or milliseconds)
                                import re
                                delay_match = re.search(r'retry in ([\d.]+)\s*(ms|s)?', error_str, re.IGNORECASE)
                                if delay_match:
                                    delay = float(delay_match.group(1))
                                    unit = delay_match.group(2) or "s"
                                    if unit.lower() == "ms":
                                        delay = delay / 1000.0
                                    retry_delay = max(delay, 1)  # At least 1 second
                            except:
                                retry_delay = min(retry_delay * 2, 60)  # Exponential backoff, max 60s
                        
                        print(f"   Quota exceeded. Retrying in {retry_delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        # Final attempt failed - return helpful error message
                        return self._generate_fallback_recommendations(
                            trending_products,
                            inventory_data,
                            inventory_summary,
                            current_season,
                            upcoming_holidays
                        )
                else:
                    # Other errors - return error message
                    return f"Error generating recommendations: {str(e)}"
        
        # Should not reach here, but just in case
        return self._generate_fallback_recommendations(
            trending_products,
            inventory_data,
            inventory_summary,
            current_season,
            upcoming_holidays
        )
    
    def _build_prompt(
        self,
        trending_products: List[Dict],
        inventory_data: List[Dict],
        inventory_summary: Dict,
        current_season: str,
        upcoming_holidays: List[str]
    ) -> str:
        """
        Build the prompt for the LLM.
        
        Args:
            trending_products: Trending products data
            inventory_data: Current inventory data
            inventory_summary: Inventory summary
            current_season: Current season
            upcoming_holidays: Upcoming holidays
            
        Returns:
            Formatted prompt string
        """
        # Format trending products
        trends_text = "\n".join([
            f"- {t['keyword'].title()}: Status={t['status']}, "
            f"Confidence={t['confidence']:.2f}, Velocity={t['velocity']:.2f}, "
            f"Strength={t['strength']:.2f}"
            for t in trending_products[:10]  # Top 10 trends
        ])
        
        # Format inventory data
        inventory_text = "\n".join([
            f"- {item['product_name']}: Stock={item['current_stock']}, "
            f"Reorder Point={item['reorder_point']}, "
            f"Reorder Qty={item['reorder_quantity']}, "
            f"Lead Time={item['lead_time_days']} days, "
            f"Location={item['warehouse_location']}"
            for item in inventory_data
        ])
        
        prompt = f"""
Analyze the following data and provide actionable inventory management recommendations for a shoe retailer.

## TRENDING PRODUCTS (from Google Trends Analysis)
{trends_text}

## CURRENT INVENTORY STATUS
Total Items: {inventory_summary['total_items']}
Low Stock Items: {inventory_summary['low_stock_items']}
Total Inventory Value: ${inventory_summary['total_inventory_value']:,.2f}

### Detailed Inventory:
{inventory_text}

## CONTEXTUAL FACTORS
- Current Season: {current_season}
- Upcoming Holidays/Events: {', '.join(upcoming_holidays) if upcoming_holidays else 'None specified'}

## YOUR TASK
Provide comprehensive, actionable recommendations in the following format:

### 1. REORDER SUGGESTIONS
- Identify products that need immediate reordering based on trending status and current stock levels
- Specify exact reorder quantities and reasoning
- Consider lead times and seasonal factors

### 2. WAREHOUSING STRATEGY
- Recommend warehouse location adjustments for trending items
- Suggest prioritization of high-velocity items
- Identify items that should be moved to high-access zones

### 3. RISK ASSESSMENT
- Flag items at risk of overstocking (declining trends with high inventory)
- Identify items that may need markdowns or clearance promotions
- Highlight potential stockout risks

### 4. PRIORITY ACTIONS
- List top 3-5 immediate actions with specific details
- Include quantitative recommendations where possible (e.g., "Increase reorder by 40%")

Be specific, actionable, and prioritize by business impact. Use natural language that a retail manager can immediately act upon.
"""
        
        return prompt
    
    def _generate_fallback_recommendations(
        self,
        trending_products: List[Dict],
        inventory_data: List[Dict],
        inventory_summary: Dict,
        current_season: str,
        upcoming_holidays: List[str]
    ) -> str:
        """
        Generate basic recommendations when API quota is exceeded.
        Provides rule-based recommendations as a fallback.
        """
        recommendations = []
        recommendations.append("## AI-Powered Inventory Recommendations")
        recommendations.append("\n**Note:** Gemini API quota exceeded. Showing rule-based recommendations.\n")
        recommendations.append("To get AI-powered recommendations, please wait for quota reset or upgrade your API plan.\n")
        
        # REORDER SUGGESTIONS
        recommendations.append("### 1. REORDER SUGGESTIONS\n")
        reorder_items = []
        for item in inventory_data:
            if item['current_stock'] <= item['reorder_point']:
                reorder_items.append(item)
        
        # Match with trending products
        for trend in trending_products[:5]:  # Top 5 trends
            keyword = trend['keyword'].lower()
            for item in inventory_data:
                if keyword in item['product_name'].lower():
                    if trend['status'] == 'Rising' and item['current_stock'] < item['reorder_point'] * 1.5:
                        recommendations.append(f"- **{item['product_name']}**: Increase reorder by 30-50% (Trending: {trend['status']}, Stock: {item['current_stock']})")
                    elif trend['status'] == 'Peaking' and item['current_stock'] < item['reorder_point'] * 2:
                        recommendations.append(f"- **{item['product_name']}**: Increase reorder by 50-75% (Peaking trend, Stock: {item['current_stock']})")
        
        if not reorder_items:
            recommendations.append("- No immediate reorders needed based on current stock levels.")
        
        # RISK ASSESSMENT
        recommendations.append("\n### 2. RISK ASSESSMENT\n")
        declining_items = []
        for trend in trending_products:
            if trend['status'] == 'Declining':
                keyword = trend['keyword'].lower()
                for item in inventory_data:
                    if keyword in item['product_name'].lower() and item['current_stock'] > item['reorder_point'] * 1.5:
                        declining_items.append((item, trend))
        
        if declining_items:
            recommendations.append("Items at risk of overstocking:")
            for item, trend in declining_items[:3]:
                recommendations.append(f"- **{item['product_name']}**: Consider markdowns (Declining trend, High stock: {item['current_stock']})")
        else:
            recommendations.append("- No significant overstocking risks identified.")
        
        # PRIORITY ACTIONS
        recommendations.append("\n### 3. PRIORITY ACTIONS\n")
        recommendations.append("1. Monitor trending products and adjust inventory levels accordingly")
        recommendations.append("2. Review low stock items and place reorders as needed")
        recommendations.append("3. Consider promotional strategies for declining trend items")
        recommendations.append("4. Update warehouse locations for high-velocity trending items")
        
        recommendations.append(f"\n---\n*Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        recommendations.append(f"*Season: {current_season}*")
        recommendations.append(f"*Total Inventory Value: ${inventory_summary['total_inventory_value']:,.2f}*")
        
        return "\n".join(recommendations)
    
    def get_detailed_recommendations(
        self,
        trending_products: List[Dict],
        current_season: str = None,
        upcoming_holidays: List[str] = None
    ) -> Dict:
        """
        Get detailed recommendations with structured output.
        
        Args:
            trending_products: List of trending products
            current_season: Current season
            upcoming_holidays: Upcoming holidays
            
        Returns:
            Dictionary with recommendations and metadata
        """
        recommendations_text = self.generate_recommendations(
            trending_products,
            current_season,
            upcoming_holidays
        )
        
        return {
            "recommendations": recommendations_text,
            "trending_products_count": len(trending_products),
            "season": current_season or CURRENT_SEASON,
            "timestamp": str(datetime.now())
        }


if __name__ == "__main__":
    # Example usage
    try:
        agent = InventoryAgent()
        
        # Sample trending products (would normally come from Component A)
        sample_trends = [
            {
                "keyword": "ankle boots",
                "status": "Rising",
                "confidence": 45.5,
                "velocity": 12.3,
                "strength": 68.2
            },
            {
                "keyword": "retro runners",
                "status": "Peaking",
                "confidence": 52.1,
                "velocity": 8.7,
                "strength": 75.4
            },
            {
                "keyword": "platform sandals",
                "status": "Declining",
                "confidence": 38.9,
                "velocity": -15.2,
                "strength": 45.6
            }
        ]
        
        print("Generating inventory recommendations...")
        recommendations = agent.generate_recommendations(
            sample_trends,
            current_season="Late Summer",
            upcoming_holidays=["Labor Day", "Back to School"]
        )
        
        print("\n=== INVENTORY RECOMMENDATIONS ===")
        print(recommendations)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set GEMINI_API_KEY in your .env file.")

