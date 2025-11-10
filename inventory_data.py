"""
Inventory data management for shoe retailer.
Loads inventory data from CSV file and provides inventory management functions.
"""
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import json
import os
import pandas as pd
from config import DEFAULT_REORDER_POINT, DEFAULT_LEAD_TIME_DAYS


@dataclass
class InventoryItem:
    """Represents a single inventory item."""
    product_name: str
    category: str
    current_stock: int
    reorder_point: int
    reorder_quantity: int
    lead_time_days: int
    warehouse_location: str
    cost_per_unit: float
    selling_price: float


class InventoryManager:
    """Manages inventory data for the retailer."""
    
    def __init__(self, csv_file: str = "store_inventory.csv"):
        """
        Initialize inventory manager by loading data from CSV file.
        
        Args:
            csv_file: Path to the CSV file containing inventory data
        """
        self.csv_file = csv_file
        self.inventory = self._load_inventory_from_csv()
    
    def _infer_category(self, product_name: str) -> str:
        """
        Infer product category from product name.
        
        Args:
            product_name: Name of the product
            
        Returns:
            Inferred category
        """
        name_lower = product_name.lower()
        
        # Category mapping based on keywords (order matters - check specific first)
        if "waterproof" in name_lower or "hiking" in name_lower:
            return "Outdoor"
        elif any(word in name_lower for word in ["boot"]):
            if "winter" in name_lower:
                return "Outdoor"
            return "Fall/Winter"
        elif any(word in name_lower for word in ["sandal", "espadrille"]):
            return "Summer"
        elif any(word in name_lower for word in ["running", "runner", "athletic", "training"]):
            return "Athletic"
        elif any(word in name_lower for word in ["dress", "formal", "loafer"]):
            return "Formal"
        elif any(word in name_lower for word in ["chunky", "casual", "canvas", "slip"]):
            return "Casual"
        elif "sneaker" in name_lower:
            # Distinguish between casual and athletic sneakers
            if any(word in name_lower for word in ["running", "athletic", "training"]):
                return "Athletic"
            return "Casual"
        else:
            return "General"
    
    def _calculate_defaults(self, current_stock: int, category: str) -> Dict:
        """
        Calculate default values for inventory fields based on stock level and category.
        
        Args:
            current_stock: Current stock level
            category: Product category
            
        Returns:
            Dictionary with default values
        """
        # Calculate reorder point (typically 60-70% of current stock, minimum 50)
        reorder_point = max(50, int(current_stock * 0.65))
        
        # Calculate reorder quantity (typically 1.5x current stock, rounded)
        reorder_quantity = max(100, int(current_stock * 1.5))
        
        # Lead time varies by category
        lead_time_map = {
            "Outdoor": 21,
            "Fall/Winter": 16,
            "Athletic": 12,
            "Summer": 10,
            "Formal": 14,
            "Casual": 10,
            "General": DEFAULT_LEAD_TIME_DAYS
        }
        lead_time_days = lead_time_map.get(category, DEFAULT_LEAD_TIME_DAYS)
        
        # Warehouse location based on category
        warehouse_map = {
            "Outdoor": "Zone B",
            "Fall/Winter": "Zone B",
            "Athletic": "Zone A",
            "Summer": "Zone C",
            "Formal": "Zone B",
            "Casual": "Zone A",
            "General": "Zone A"
        }
        warehouse_location = warehouse_map.get(category, "Zone A")
        
        # Estimate cost and selling price based on category and stock level
        # Higher stock often means lower cost items
        base_cost_map = {
            "Outdoor": 65.00,
            "Fall/Winter": 55.00,
            "Athletic": 45.00,
            "Summer": 25.00,
            "Formal": 75.00,
            "Casual": 30.00,
            "General": 40.00
        }
        cost_per_unit = base_cost_map.get(category, 40.00)
        
        # Adjust cost slightly based on stock (higher stock = potentially lower cost)
        if current_stock > 200:
            cost_per_unit *= 0.9
        elif current_stock < 80:
            cost_per_unit *= 1.1
        
        # Selling price is typically 2x cost (markup)
        selling_price = cost_per_unit * 2.0
        
        return {
            "reorder_point": reorder_point,
            "reorder_quantity": reorder_quantity,
            "lead_time_days": lead_time_days,
            "warehouse_location": warehouse_location,
            "cost_per_unit": round(cost_per_unit, 2),
            "selling_price": round(selling_price, 2)
        }
    
    def _load_inventory_from_csv(self) -> List[InventoryItem]:
        """
        Load inventory data from CSV file.
        
        Returns:
            List of InventoryItem objects
        """
        # Check if CSV file exists
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(
                f"Inventory CSV file '{self.csv_file}' not found. "
                f"Please ensure the file exists in the current directory."
            )
        
        try:
            # Read CSV file
            df = pd.read_csv(self.csv_file)
            
            # Validate required columns
            required_columns = ["Shoe Description", "Number of Items Left"]
            if not all(col in df.columns for col in required_columns):
                raise ValueError(
                    f"CSV file must contain columns: {required_columns}. "
                    f"Found columns: {list(df.columns)}"
                )
            
            # Optional columns (will use defaults if not present)
            optional_columns = {
                "Category": "category",
                "Reorder Point": "reorder_point",
                "Reorder Quantity": "reorder_quantity",
                "Lead Time (days)": "lead_time_days",
                "Warehouse Location": "warehouse_location",
                "Cost Per Unit": "cost_per_unit",
                "Selling Price": "selling_price"
            }
            
            # Convert to InventoryItem objects
            inventory_items = []
            for _, row in df.iterrows():
                product_name = str(row["Shoe Description"]).strip()
                current_stock = int(row["Number of Items Left"])
                
                # Skip empty rows
                if not product_name or pd.isna(current_stock):
                    continue
                
                # Get category from CSV or infer it
                if "Category" in df.columns and not pd.isna(row.get("Category")):
                    category = str(row["Category"]).strip()
                else:
                    category = self._infer_category(product_name)
                
                # Calculate defaults (will be overridden by CSV values if present)
                defaults = self._calculate_defaults(current_stock, category)
                
                # Use CSV values if available, otherwise use defaults
                reorder_point = int(row["Reorder Point"]) if "Reorder Point" in df.columns and not pd.isna(row.get("Reorder Point")) else defaults["reorder_point"]
                reorder_quantity = int(row["Reorder Quantity"]) if "Reorder Quantity" in df.columns and not pd.isna(row.get("Reorder Quantity")) else defaults["reorder_quantity"]
                lead_time_days = int(row["Lead Time (days)"]) if "Lead Time (days)" in df.columns and not pd.isna(row.get("Lead Time (days)")) else defaults["lead_time_days"]
                warehouse_location = str(row["Warehouse Location"]).strip() if "Warehouse Location" in df.columns and not pd.isna(row.get("Warehouse Location")) else defaults["warehouse_location"]
                cost_per_unit = float(row["Cost Per Unit"]) if "Cost Per Unit" in df.columns and not pd.isna(row.get("Cost Per Unit")) else defaults["cost_per_unit"]
                selling_price = float(row["Selling Price"]) if "Selling Price" in df.columns and not pd.isna(row.get("Selling Price")) else defaults["selling_price"]
                
                # Create InventoryItem
                item = InventoryItem(
                    product_name=product_name,
                    category=category,
                    current_stock=current_stock,
                    reorder_point=reorder_point,
                    reorder_quantity=reorder_quantity,
                    lead_time_days=lead_time_days,
                    warehouse_location=warehouse_location,
                    cost_per_unit=round(cost_per_unit, 2),
                    selling_price=round(selling_price, 2)
                )
                inventory_items.append(item)
            
            if not inventory_items:
                raise ValueError("No valid inventory items found in CSV file.")
            
            return inventory_items
            
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file '{self.csv_file}' is empty.")
        except Exception as e:
            raise RuntimeError(f"Error loading inventory from CSV: {str(e)}")
    
    def get_inventory_by_keyword(self, keyword: str) -> List[InventoryItem]:
        """
        Find inventory items matching a keyword.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching inventory items
        """
        keyword_lower = keyword.lower()
        matches = []
        
        for item in self.inventory:
            if keyword_lower in item.product_name.lower() or keyword_lower in item.category.lower():
                matches.append(item)
        
        return matches
    
    def get_all_inventory(self) -> List[InventoryItem]:
        """Get all inventory items."""
        return self.inventory
    
    def get_inventory_summary(self) -> Dict:
        """Get a summary of current inventory status."""
        total_items = len(self.inventory)
        low_stock_items = [item for item in self.inventory if item.current_stock <= item.reorder_point]
        total_value = sum(item.current_stock * item.cost_per_unit for item in self.inventory)
        
        return {
            "total_items": total_items,
            "low_stock_items": len(low_stock_items),
            "total_inventory_value": total_value,
            "items": [
                {
                    "product_name": item.product_name,
                    "current_stock": item.current_stock,
                    "reorder_point": item.reorder_point,
                    "status": "Low Stock" if item.current_stock <= item.reorder_point else "Adequate"
                }
                for item in self.inventory
            ]
        }
    
    def update_stock(self, product_name: str, new_stock: int, save_to_csv: bool = True) -> bool:
        """
        Update stock level for a product and optionally save to CSV.
        
        Args:
            product_name: Name of the product
            new_stock: New stock level
            save_to_csv: Whether to save changes back to CSV file (default: True)
            
        Returns:
            True if update was successful, False otherwise
        """
        for item in self.inventory:
            if item.product_name.lower() == product_name.lower():
                item.current_stock = new_stock
                if save_to_csv:
                    self._save_to_csv()
                return True
        return False
    
    def _save_to_csv(self):
        """Save current inventory back to CSV file with all columns."""
        try:
            # Create DataFrame from current inventory with all columns
            data = {
                "Shoe Description": [item.product_name for item in self.inventory],
                "Number of Items Left": [item.current_stock for item in self.inventory],
                "Category": [item.category for item in self.inventory],
                "Reorder Point": [item.reorder_point for item in self.inventory],
                "Reorder Quantity": [item.reorder_quantity for item in self.inventory],
                "Lead Time (days)": [item.lead_time_days for item in self.inventory],
                "Warehouse Location": [item.warehouse_location for item in self.inventory],
                "Cost Per Unit": [item.cost_per_unit for item in self.inventory],
                "Selling Price": [item.selling_price for item in self.inventory]
            }
            df = pd.DataFrame(data)
            
            # Save to CSV
            df.to_csv(self.csv_file, index=False)
        except Exception as e:
            print(f"Warning: Could not save inventory to CSV: {str(e)}")
    
    def reload_inventory(self):
        """Reload inventory from CSV file."""
        self.inventory = self._load_inventory_from_csv()
    
    def to_dict(self) -> List[Dict]:
        """Convert inventory to dictionary format for LLM processing."""
        return [
            {
                "product_name": item.product_name,
                "category": item.category,
                "current_stock": item.current_stock,
                "reorder_point": item.reorder_point,
                "reorder_quantity": item.reorder_quantity,
                "lead_time_days": item.lead_time_days,
                "warehouse_location": item.warehouse_location,
                "cost_per_unit": item.cost_per_unit,
                "selling_price": item.selling_price
            }
            for item in self.inventory
        ]

