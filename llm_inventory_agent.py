"""
Component B: Inventory & Warehouse Management LLM Agent
Uses Large Language Model to generate actionable inventory recommendations
based on trend data, current inventory, and contextual factors.
"""
import json
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
        
        # Call Gemini API
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
            return f"Error generating recommendations: {str(e)}"
    
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

