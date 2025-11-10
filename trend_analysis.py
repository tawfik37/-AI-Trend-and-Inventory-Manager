"""
Component A: Trend Analysis and Prediction
Fetches real-time search interest data from Google Trends API
and analyzes trend velocity to identify rising, peaking, or declining trends.
"""
import pandas as pd
import numpy as np
from pytrends.request import TrendReq
import time
from typing import List, Dict, Tuple, Optional
import random
from config import TRENDS_GEO, TRENDS_TIMEFRAME


class TrendAnalyzer:
    """Analyzes Google Trends data to identify trending products."""
    
    def __init__(self, geo: str = TRENDS_GEO, timeframe: str = TRENDS_TIMEFRAME, max_keywords: int = 15):
        """
        Initialize the Trend Analyzer.
        
        Args:
            geo: Geographic region for trends (default: US)
            timeframe: Time range for trend analysis (default: last 3 months)
            max_keywords: Maximum number of keywords to process (default: 15 to avoid rate limits)
        """
        self.pytrends = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=0.1)
        self.geo = geo
        self.timeframe = timeframe
        self.max_keywords = max_keywords
        
    def fetch_trend_data(self, keywords: List[str], max_keywords: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """
        Fetch trend data for a list of keywords with improved rate limiting.
        
        Args:
            keywords: List of keywords to analyze
            max_keywords: Maximum number of keywords to process (uses self.max_keywords if None)
            
        Returns:
            Dictionary mapping keywords to their trend data
        """
        trend_data = {}
        max_kw = max_keywords or self.max_keywords
        
        # Limit number of keywords to avoid rate limits
        keywords_to_process = keywords[:max_kw] if len(keywords) > max_kw else keywords
        
        if len(keywords) > max_kw:
            print(f"   Limiting to first {max_kw} keywords to avoid API rate limits")
            print(f"   (Total keywords available: {len(keywords)})")
        
        # Process keywords one at a time with delays to avoid rate limiting
        for i, keyword in enumerate(keywords_to_process, 1):
            retries = 3
            retry_delay = 5  # Start with 5 seconds
            
            for attempt in range(retries):
                try:
                    # Create new TrendReq instance for each request to avoid connection issues
                    pytrends = TrendReq(hl='en-US', tz=360, retries=1, backoff_factor=0.1)
                    
                    # Process single keyword
                    pytrends.build_payload([keyword], geo=self.geo, timeframe=self.timeframe)
                    data = pytrends.interest_over_time()
                    
                    if not data.empty and keyword in data.columns:
                        trend_data[keyword] = data[[keyword]].copy()
                        print(f"   [{i}/{len(keywords_to_process)}] Successfully fetched: {keyword}")
                        break
                    else:
                        print(f"   [{i}/{len(keywords_to_process)}] No data available for: {keyword}")
                        break
                    
                except Exception as e:
                    error_str = str(e)
                    
                    # Check if it's a rate limit error (429)
                    if "429" in error_str or "rate limit" in error_str.lower() or "Too Many Requests" in error_str:
                        if attempt < retries - 1:
                            wait_time = retry_delay * (2 ** attempt) + random.uniform(1, 3)  # Exponential backoff with jitter
                            print(f"   Rate limit reached. Waiting {wait_time:.1f} seconds before retry {attempt + 1}/{retries}...")
                            time.sleep(wait_time)
                        else:
                            print(f"   Skipping '{keyword}': Rate limit exceeded after {retries} attempts")
                    else:
                        # Other errors - skip after first attempt
                        print(f"   Skipping '{keyword}': {error_str[:80]}")
                        break
            
            # Wait between keywords to avoid rate limiting
            if i < len(keywords_to_process):
                delay = random.uniform(3, 6)  # Random delay between 3-6 seconds
                time.sleep(delay)
        
        return trend_data
    
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
            max_keywords: Maximum number of keywords to process (uses self.max_keywords if None)
            
        Returns:
            List of dictionaries containing trend analysis results, ranked by confidence
        """
        max_kw = max_keywords or self.max_keywords
        keywords_to_process = keywords[:max_kw] if len(keywords) > max_kw else keywords
        
        print(f"Fetching trend data for {len(keywords_to_process)} keywords (out of {len(keywords)} total)...")
        trend_data = self.fetch_trend_data(keywords, max_keywords=max_kw)
        
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
            max_keywords: Maximum number of keywords to process (uses self.max_keywords if None)
            
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


if __name__ == "__main__":
    # Example usage
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
    
    print("Analyzing trends...")
    trends = analyzer.get_high_confidence_trends(shoe_keywords, min_confidence=20.0)
    
    print("\n=== HIGH-CONFIDENCE TRENDING PRODUCTS ===")
    for i, trend in enumerate(trends[:10], 1):
        print(f"\n{i}. {trend['keyword'].title()}")
        print(f"   Status: {trend['status']}")
        print(f"   Confidence: {trend['confidence']:.2f}")
        print(f"   Velocity: {trend['velocity']:.2f}")
        print(f"   Strength: {trend['strength']:.2f}")

