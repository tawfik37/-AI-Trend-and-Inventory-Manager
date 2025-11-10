# Google Trends Keywords - Location and Usage

## Where Keywords Are Defined

### Primary Location: `main.py`
The keywords for Google Trends analysis are generated in the `get_shoe_keywords()` function in `main.py` (lines 13-102).

## Current Implementation

### Automatic Keyword Generation (Default)
**Status**: ✅ **ACTIVE** - Keywords are automatically generated from your inventory CSV file

The system now automatically generates keywords from all products in `store_inventory.csv`. This means:
- **59 keywords** are generated from your 59 inventory items
- Keywords match your actual inventory products
- No manual maintenance needed - keywords update automatically when you add/remove products from the CSV

### Manual Keyword List (Fallback)
If you want to use a manual list instead, you can set `use_inventory=False`:

```python
keywords = get_shoe_keywords(use_inventory=False)
```

This will use the default 15 keywords:
- chunky sneakers
- waterproof boots
- espadrilles
- ankle boots
- retro runners
- platform sandals
- minimalist running shoes
- suede boots
- canvas shoes
- running sneakers
- hiking boots
- dress shoes
- loafers
- high top sneakers
- slip on shoes

## How It Works

1. **Inventory-Based (Default)**:
   - Loads all products from `store_inventory.csv`
   - Converts product names to lowercase keywords
   - Uses all 59 products as keywords for trend analysis

2. **Manual Override**:
   - Set `use_inventory=False` to use the manual keyword list
   - Or modify the manual list in `get_shoe_keywords()` function

3. **Additional Keywords**:
   - You can add extra keywords without modifying the function:
   ```python
   keywords = get_shoe_keywords(
       inventory_items=inventory_items,
       additional_keywords=["new trend", "emerging style"]
   )
   ```

## Current Keywords (59 total)

Generated from your inventory CSV:
1. chunky sneakers
2. waterproof boots
3. espadrilles
4. ankle boots
5. retro runners
6. platform sandals
7. minimalist running shoes
8. suede boots
9. canvas shoes
10. running sneakers
11. high top sneakers
12. loafers
13. dress shoes
14. hiking boots
15. slip on shoes
16. winter boots
17. cross training shoes
18. athletic sneakers
19. casual sneakers
20. formal dress shoes
21. basketball shoes
22. tennis shoes
23. walking shoes
24. climbing shoes
25. work boots
26. chelsea boots
27. oxford shoes
28. boat shoes
29. flip flops
30. wedge sandals
31. moccasins
32. slippers
33. ballet flats
34. mary janes
35. ankle strap heels
36. combat boots
37. trail running shoes
38. soccer cleats
39. baseball cleats
40. golf shoes
41. yoga shoes
42. pilates shoes
43. cycling shoes
44. skateboarding shoes
45. vans style sneakers
46. converse style sneakers
47. timberland style boots
48. ugg style boots
49. doc martens style boots
50. hunter style boots
51. wingtips
52. monk straps
53. brogues
54. derby shoes
55. gladiator sandals
56. espadrille wedges
57. slide sandals
58. water shoes
59. beach sandals

## Customization Options

### Option 1: Use Manual Keywords Only
Edit `main.py` line 150:
```python
keywords = get_shoe_keywords(use_inventory=False)
```

### Option 2: Add Additional Keywords
Edit `main.py` line 150:
```python
keywords = get_shoe_keywords(
    inventory_items=inventory_items,
    additional_keywords=["new trend", "another keyword"]
)
```

### Option 3: Modify Manual Keyword List
Edit the `get_shoe_keywords()` function in `main.py` (lines 68-85) to change the default manual keywords.

### Option 4: Filter Inventory Keywords
You can modify `get_shoe_keywords()` to filter which inventory items become keywords (e.g., only high-stock items, only certain categories, etc.)

## Benefits of Automatic Keyword Generation

✅ **Always Up-to-Date**: Keywords automatically match your inventory
✅ **No Manual Maintenance**: Add products to CSV, keywords update automatically
✅ **Comprehensive Coverage**: All 59 products are analyzed for trends
✅ **Accurate Matching**: Trends are analyzed for products you actually stock

## Notes

- Google Trends API has rate limits, so analyzing 59 keywords may take some time
- The system processes keywords in batches of 5 to avoid rate limiting
- You can reduce the number of keywords by filtering the inventory items before passing to `get_shoe_keywords()`
- Keywords are converted to lowercase for consistency

## Testing

To test keyword generation:
```python
from main import get_shoe_keywords
from inventory_data import InventoryManager

im = InventoryManager()
items = im.get_all_inventory()
keywords = get_shoe_keywords(inventory_items=items, use_inventory=True)
print(f"Generated {len(keywords)} keywords: {keywords}")
```

