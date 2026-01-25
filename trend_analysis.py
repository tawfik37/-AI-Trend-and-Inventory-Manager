"""
Component A: Trend Analysis and Prediction (SerpAPI Version)
Fetches real-time search interest data from Google Trends via SerpAPI
and analyzes trend velocity to identify rising, peaking, or declining trends.
"""
import pandas as pd
import numpy as np
from serpapi import GoogleSearch
import time
from typing import List, Dict, Optional
import random
from config import TRENDS_GEO, TRENDS_TIMEFRAME, SERPAPI_KEY


class TrendAnalyzer:
    """Analyzes Google Trends data to identify trending products using SerpAPI."""
    
    def __init__(self, geo: str = TRENDS_GEO, timeframe: str = TRENDS_TIMEFRAME, max_keywords: int = 15):
        """
        Initialize the Trend Analyzer with SerpAPI.
        
        Args:
            geo: Geographic region for trends (default: US)
            timeframe: Time range for trend analysis (default: last 3 months)
            max_keywords: Maximum number of keywords to process (default: 15)
        """
        self.api_key = SERPAPI_KEY
        self.has_api_key = bool(SERPAPI_KEY)
        self.geo = geo
        self.timeframe = timeframe
        self.max_keywords = max_keywords
        
        if not self.has_api_key:
            print("Warning: No SerpAPI key found. Running in demo mode with sample data.")
            print("   To use real Google Trends data, add SERPAPI_KEY to your .env file")
            print("   Get your key at: https://serpapi.com/manage-api-key")
        
    def fetch_trend_data(self, keywords: List[str], max_keywords: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """
        Fetch trend data for a list of keywords using SerpAPI.
        
        Args:
            keywords: List of keywords to analyze
            max_keywords: Maximum number of keywords to process
            
        Returns:
            Dictionary mapping keywords to their trend data
        """
        # If no API key, return empty dict (will use sample data in analyze_trends)
        if not self.has_api_key:
            return {}
        
        trend_data = {}
        max_kw = max_keywords or self.max_keywords
        
        # Limit number of keywords
        keywords_to_process = keywords[:max_kw] if len(keywords) > max_kw else keywords
        
        if len(keywords) > max_kw:
            print(f"   Limiting to first {max_kw} keywords to optimize API usage")
            print(f"   (Total keywords available: {len(keywords)})")
        
        # Process keywords one at a time
        for i, keyword in enumerate(keywords_to_process, 1):
            try:
                # Build SerpAPI request
                params = {
                    "engine": "google_trends",
                    "q": keyword,
                    "date": self.timeframe,
                    "data_type": "TIMESERIES",
                    "geo": self.geo if self.geo != "US" else "",
                    "api_key": self.api_key
                }
                
                search = GoogleSearch(params)
                results = search.get_dict()
                
                # Check for errors
                if "error" in results:
                    print(f"   [{i}/{len(keywords_to_process)}] Error for '{keyword}': {results['error']}")
                    continue
                
                # Extract timeline data
                if "interest_over_time" in results:
                    timeline = results["interest_over_time"]["timeline_data"]
                    
                    # Convert to pandas DataFrame
                    dates = []
                    values = []
                    
                    for entry in timeline:
                        dates.append(entry["date"])
                        # Get the extracted_value which is always an integer
                        values.append(entry["values"][0]["extracted_value"])
                    
                    df = pd.DataFrame({
                        "date": dates,
                        keyword: values
                    })
                    
                    # Set date as index
                    df.set_index("date", inplace=True)
                    
                    trend_data[keyword] = df[[keyword]].copy()
                    print(f"   [{i}/{len(keywords_to_process)}] ✓ Fetched: {keyword}")
                else:
                    print(f"   [{i}/{len(keywords_to_process)}] No data for: {keyword}")
                
                # Small delay between requests (SerpAPI handles rate limiting well)
                if i < len(keywords_to_process):
                    time.sleep(0.5)  # 500ms delay
                    
            except Exception as e:
                print(f"   [{i}/{len(keywords_to_process)}] Failed '{keyword}': {str(e)[:80]}")
                continue
        
        return trend_data
    
    def fetch_related_queries(self, keyword: str) -> Dict:
        """
        Fetch related queries for a keyword to discover trending variations.
        
        Args:
            keyword: Base keyword to analyze
            
        Returns:
            Dictionary with rising and top related queries
        """
        if not self.has_api_key:
            return {"rising": [], "top": []}
        
        try:
            params = {
                "engine": "google_trends",
                "q": keyword,
                "date": self.timeframe,
                "data_type": "RELATED_QUERIES",
                "geo": self.geo if self.geo != "US" else "",
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "related_queries" in results:
                return results["related_queries"]
            else:
                return {"rising": [], "top": []}
                
        except Exception as e:
            print(f"   Error fetching related queries for '{keyword}': {str(e)[:80]}")
            return {"rising": [], "top": []}
    
    def calculate_trend_velocity(self, trend_series: pd.Series) -> float:
        """
        Calculate the velocity (rate of change) of a trend.
        
        Args:
            trend_series: Time series of trend values
            
        Returns:
            Trend velocity (positive = rising, negative = declining)
        """
        if len(trend_series) < 2:
            return 0.0
        
        # Calculate percentage change over the time period
        recent_values = trend_series.tail(4).values  # Last 4 weeks
        if len(recent_values) < 2:
            return 0.0
        
        # Calculate average rate of change
        changes = np.diff(recent_values)
        velocity = np.mean(changes) if len(changes) > 0 else 0.0
        
        return velocity
    
    def calculate_trend_strength(self, trend_series: pd.Series) -> float:
        """
        Calculate the overall strength (average value) of a trend.
        
        Args:
            trend_series: Time series of trend values
            
        Returns:
            Average trend strength (0-100)
        """
        return trend_series.mean() if not trend_series.empty else 0.0
    
    def classify_trend_status(self, velocity: float, strength: float) -> str:
        """
        Classify a trend as rising, peaking, or declining.
        
        Args:
            velocity: Trend velocity
            strength: Trend strength
            
        Returns:
            Trend status classification
        """
        if velocity > 5:
            return "Rising"
        elif velocity < -5:
            return "Declining"
        elif strength > 70:
            return "Peaking"
        else:
            return "Stable"
    
    def analyze_trends(self, keywords: List[str], max_keywords: Optional[int] = None) -> List[Dict]:
        """
        Analyze trends for a list of keywords and return ranked results.
        
        Args:
            keywords: List of keywords to analyze
            max_keywords: Maximum number of keywords to process
            
        Returns:
            List of dictionaries containing trend analysis results, ranked by confidence
        """
        max_kw = max_keywords or self.max_keywords
        keywords_to_process = keywords[:max_kw] if len(keywords) > max_kw else keywords
        
        print(f"Fetching trend data for {len(keywords_to_process)} keywords (out of {len(keywords)} total)...")
        trend_data = self.fetch_trend_data(keywords, max_keywords=max_kw)
        
        # If no API key or no data, generate sample data
        if not trend_data:
            print("   Using sample data (demo mode - add SERPAPI_KEY for real data)")
            results = []
            for keyword in keywords_to_process:
                # Generate realistic sample trend data
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
                
                results.append({
                    "keyword": keyword,
                    "velocity": velocity,
                    "strength": base_strength,
                    "status": status,
                    "confidence": confidence,
                    "current_value": base_strength,
                    "peak_value": base_strength * 1.2
                })
            
            # Rank by confidence (descending)
            results.sort(key=lambda x: x["confidence"], reverse=True)
            return results
        
        results = []
        
        for keyword, data in trend_data.items():
            if data.empty:
                continue
            
            trend_series = data[keyword]
            velocity = self.calculate_trend_velocity(trend_series)
            strength = self.calculate_trend_strength(trend_series)
            status = self.classify_trend_status(velocity, strength)
            
            # Calculate confidence score (higher is better)
            # Combines velocity and strength
            confidence = abs(velocity) * 0.6 + strength * 0.4
            
            results.append({
                "keyword": keyword,
                "velocity": velocity,
                "strength": strength,
                "status": status,
                "confidence": confidence,
                "current_value": trend_series.iloc[-1] if not trend_series.empty else 0,
                "peak_value": trend_series.max() if not trend_series.empty else 0
            })
        
        # Rank by confidence (descending)
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        return results
    
    def get_high_confidence_trends(self, keywords: List[str], min_confidence: float = 30.0, max_keywords: Optional[int] = None) -> List[Dict]:
        """
        Get only high-confidence trending products.
        
        Args:
            keywords: List of keywords to analyze
            min_confidence: Minimum confidence score threshold
            max_keywords: Maximum number of keywords to process
            
        Returns:
            Filtered list of high-confidence trends
        """
        all_trends = self.analyze_trends(keywords, max_keywords=max_keywords)
        
        # If no trends found, return all trends (even low confidence) to provide some data
        high_confidence = [trend for trend in all_trends if trend["confidence"] >= min_confidence]
        
        if not high_confidence and all_trends:
            print(f"   No trends with confidence >= {min_confidence}, returning all {len(all_trends)} trends found")
            return all_trends
        
        return high_confidence
    
    def get_inventory_specific_trends(self, base_keyword: str, inventory_items: List[str]) -> Dict:
        """
        Get trends for specific inventory items related to a base keyword.
        Useful for finding which exact products are trending.
        
        Args:
            base_keyword: Base category (e.g., "Nike Shoes")
            inventory_items: List of specific products in your inventory
            
        Returns:
            Dictionary with rising and top products
        """
        print(f"\nFinding specific trends for: {base_keyword}")
        related = self.fetch_related_queries(base_keyword)
        
        # Match related queries with inventory items
        rising_matches = []
        top_matches = []
        
        for item in inventory_items:
            item_lower = item.lower()
            
            # Check rising queries
            for query in related.get("rising", []):
                if item_lower in query["query"].lower() or query["query"].lower() in item_lower:
                    rising_matches.append({
                        "inventory_item": item,
                        "search_query": query["query"],
                        "growth": query["value"],
                        "growth_value": query["extracted_value"]
                    })
            
            # Check top queries
            for query in related.get("top", []):
                if item_lower in query["query"].lower() or query["query"].lower() in item_lower:
                    top_matches.append({
                        "inventory_item": item,
                        "search_query": query["query"],
                        "popularity": query["extracted_value"]
                    })
        
        return {
            "base_keyword": base_keyword,
            "rising_in_inventory": rising_matches,
            "top_in_inventory": top_matches,
            "all_rising": related.get("rising", [])[:10],
            "all_top": related.get("top", [])[:10]
        }


if __name__ == "__main__":
    # Example usage
    try:
        analyzer = TrendAnalyzer()
        
        # Sample shoe-related keywords
        shoe_keywords = [
            "chunky sneakers",
            "waterproof boots",
            "espadrilles",
            "ankle boots",
            "retro runners",
            "platform sandals",
            "minimalist running shoes",
            "suede boots",
            "canvas shoes",
            "running sneakers"
        ]
        
        print("Analyzing trends using SerpAPI...")
        trends = analyzer.get_high_confidence_trends(shoe_keywords, min_confidence=20.0)
        
        print("\n=== HIGH-CONFIDENCE TRENDING PRODUCTS ===")
        for i, trend in enumerate(trends[:10], 1):
            print(f"\n{i}. {trend['keyword'].title()}")
            print(f"   Status: {trend['status']}")
            print(f"   Confidence: {trend['confidence']:.2f}")
            print(f"   Velocity: {trend['velocity']:.2f}")
            print(f"   Strength: {trend['strength']:.2f}")
            
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("Please add SERPAPI_KEY to your .env file")