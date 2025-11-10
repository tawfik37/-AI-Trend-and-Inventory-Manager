# Inventory CSV File Format

## Overview
The `store_inventory.csv` file is the primary data source for the ATIM inventory management system. The CSV supports both minimal (2 columns) and expanded (9 columns) formats.

## CSV Columns

### Required Columns
1. **Shoe Description** - Name of the shoe product
2. **Number of Items Left** - Current stock quantity

### Optional Columns (with defaults if omitted)
3. **Category** - Product category (Athletic, Casual, Outdoor, Summer, Fall/Winter, Formal, General)
4. **Reorder Point** - Minimum stock level before reordering
5. **Reorder Quantity** - Quantity to order when reorder point is reached
6. **Lead Time (days)** - Number of days for delivery
7. **Warehouse Location** - Storage location (Zone A, Zone B, Zone C)
8. **Cost Per Unit** - Cost price per unit
9. **Selling Price** - Retail selling price per unit

## CSV Format Examples

### Minimal Format (2 columns)
```csv
Shoe Description,Number of Items Left
Chunky Sneakers,150
Waterproof Boots,80
```

### Expanded Format (9 columns) - Recommended
```csv
Shoe Description,Number of Items Left,Category,Reorder Point,Reorder Quantity,Lead Time (days),Warehouse Location,Cost Per Unit,Selling Price
Chunky Sneakers,150,Casual,100,200,10,Zone A,45.00,89.99
Waterproof Boots,80,Outdoor,50,150,21,Zone B,65.00,129.99
```

## Default Behavior

If optional columns are not provided, the system will:
- **Category**: Automatically infer from product name
- **Reorder Point**: Calculate as 65% of current stock (minimum 50)
- **Reorder Quantity**: Calculate as 1.5x current stock (minimum 100)
- **Lead Time (days)**: Assign based on category (10-21 days)
- **Warehouse Location**: Assign based on category
- **Cost Per Unit**: Estimate based on category and stock level
- **Selling Price**: Calculate as 2x cost per unit (markup)

## Category Inference Rules

The system automatically infers categories from product names:
- **Athletic**: running, athletic, training, runner, basketball, tennis, etc.
- **Casual**: chunky, casual, canvas, slip-on, skateboarding, etc.
- **Outdoor**: waterproof, hiking, winter boots, climbing, work boots, etc.
- **Fall/Winter**: boots (non-outdoor), ankle boots, suede boots, etc.
- **Summer**: sandals, espadrilles, flip flops, beach sandals, etc.
- **Formal**: dress, formal, loafers, oxford, wingtips, etc.
- **General**: Fallback category for unmatched items

## Current Inventory Statistics

- **Total Items**: 59 products
- **Categories**: 
  - Athletic: 14 items
  - Casual: 12 items
  - Formal: 11 items
  - Summer: 9 items
  - Outdoor: 8 items
  - Fall/Winter: 5 items
- **Total Inventory Value**: $284,370.00

## Usage Tips

1. **Adding New Products**: Add a new row with at minimum "Shoe Description" and "Number of Items Left"
2. **Updating Stock**: Edit the "Number of Items Left" column directly in the CSV
3. **Bulk Updates**: Use Excel or any CSV editor to modify multiple items at once
4. **Data Integrity**: The system validates data on load and will report errors if required columns are missing
5. **Auto-Save**: When using `update_stock()` in code, changes are automatically saved back to CSV

## File Location
`store_inventory.csv` in the project root directory

