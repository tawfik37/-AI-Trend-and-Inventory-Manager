"""
Enhanced Main Application for AI Trend & Inventory Manager (ATIM)
Beautiful terminal output with colors, tables, and progress bars
"""
import sys
from datetime import datetime
from trend_analysis import TrendAnalyzer
from llm_inventory_agent import InventoryAgent
from config import CURRENT_SEASON
from inventory_data import InventoryManager

# Rich terminal library for beautiful output
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich.layout import Layout
from rich import box
from rich.text import Text

console = Console()


def get_shoe_keywords(inventory_items: list = None, use_inventory: bool = True, additional_keywords: list = None) -> list:
    """Get list of shoe-related keywords for trend analysis."""
    keywords = []
    
    if use_inventory:
        if inventory_items:
            items = inventory_items
        else:
            try:
                inventory_manager = InventoryManager()
                items = inventory_manager.get_all_inventory()
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load keywords from inventory: {e}[/yellow]")
                console.print("[yellow]   Using default keyword list instead...[/yellow]")
                items = None
        
        if items:
            for item in items:
                keyword = item.product_name.lower()
                keywords.append(keyword)
        else:
            keywords = [
                "chunky sneakers", "waterproof boots", "espadrilles",
                "ankle boots", "retro runners", "platform sandals",
                "minimalist running shoes", "suede boots", "canvas shoes",
                "running sneakers", "hiking boots", "dress shoes",
                "loafers", "high top sneakers", "slip on shoes"
            ]
    else:
        keywords = [
            "chunky sneakers", "waterproof boots", "espadrilles",
            "ankle boots", "retro runners", "platform sandals",
            "minimalist running shoes", "suede boots", "canvas shoes",
            "running sneakers", "hiking boots", "dress shoes",
            "loafers", "high top sneakers", "slip on shoes"
        ]
    
    if additional_keywords:
        for keyword in additional_keywords:
            if keyword.lower() not in [k.lower() for k in keywords]:
                keywords.append(keyword.lower())
    
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower not in seen:
            seen.add(keyword_lower)
            unique_keywords.append(keyword)
    
    return unique_keywords


def get_upcoming_holidays() -> list:
    """Get list of upcoming holidays/events."""
    return ["Labor Day", "Back to School", "Fall Fashion Week"]


def display_header():
    """Display beautiful header."""
    header_text = """
    ============================================================
    
          AI TREND & INVENTORY MANAGER (ATIM)
    
          Intelligent Inventory Optimization with AI
    
    ============================================================
    """
    console.print(header_text, style="bold cyan")
    console.print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
    console.print(f"Current Season: {CURRENT_SEASON}", style="dim")
    console.print()


def display_inventory_summary(inventory_summary):
    """Display inventory summary in a beautiful table."""
    table = Table(title="Inventory Overview", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="green")
    
    table.add_row("Total Products", str(inventory_summary['total_items']))
    table.add_row("Low Stock Items", f"[yellow]{inventory_summary['low_stock_items']}[/yellow]")
    table.add_row("Total Inventory Value", f"[green]${inventory_summary['total_inventory_value']:,.2f}[/green]")
    
    console.print(table)
    console.print()


def display_trending_products(trending_products):
    """Display trending products in a beautiful table."""
    if not trending_products:
        console.print("[yellow]No trending products found[/yellow]")
        return
    
    table = Table(
        title=f"Top {min(10, len(trending_products))} Trending Products",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("Rank", style="dim", width=6, justify="center")
    table.add_column("Product", style="cyan", no_wrap=False)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Confidence", justify="right", width=12)
    table.add_column("Velocity", justify="right", width=10)
    table.add_column("Strength", justify="right", width=10)
    
    for i, trend in enumerate(trending_products[:10], 1):
        # Color-code status
        status = trend['status']
        if status == "Rising":
            status_display = "[green]Rising[/green]"
        elif status == "Declining":
            status_display = "[red]Declining[/red]"
        elif status == "Peaking":
            status_display = "[yellow]Peaking[/yellow]"
        else:
            status_display = "[dim]Stable[/dim]"
        
        # Color-code velocity
        velocity = trend['velocity']
        if velocity > 5:
            velocity_str = f"[green]+{velocity:.1f}[/green]"
        elif velocity < -5:
            velocity_str = f"[red]{velocity:.1f}[/red]"
        else:
            velocity_str = f"[dim]{velocity:.1f}[/dim]"
        
        table.add_row(
            f"#{i}",
            trend['keyword'].title(),
            status_display,
            f"{trend['confidence']:.1f}",
            velocity_str,
            f"{trend['strength']:.1f}"
        )
    
    console.print(table)
    console.print()


def display_recommendations(recommendations):
    """Display AI recommendations in a beautiful panel."""
    # Convert recommendations to markdown for better formatting
    md = Markdown(recommendations)
    
    panel = Panel(
        md,
        title="AI-Powered Inventory Recommendations",
        border_style="green",
        box=box.DOUBLE,
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()


def display_low_stock_alerts(low_stock_items):
    """Display low stock alerts."""
    if not low_stock_items:
        console.print("[green]All items are above reorder point[/green]\n")
        return
    
    table = Table(
        title="Low Stock Alerts",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold yellow"
    )
    
    table.add_column("Product", style="yellow")
    table.add_column("Current Stock", justify="right", style="red")
    table.add_column("Reorder Point", justify="right", style="dim")
    table.add_column("Action Needed", style="bold red")
    
    for item in low_stock_items:
        urgency = "[red]URGENT[/red]" if item.current_stock < item.reorder_point * 0.5 else "[yellow]REORDER[/yellow]"
        table.add_row(
            item.product_name,
            str(item.current_stock),
            str(item.reorder_point),
            urgency
        )
    
    console.print(table)
    console.print()


def main():
    """Enhanced main application with beautiful output."""
    display_header()
    
    # Initialize components
    task1_desc = "Initializing Trend Analyzer..."
    console.print(f"[cyan]{task1_desc}[/cyan]")
    try:
        trend_analyzer = TrendAnalyzer()
    except ValueError as e:
        console.print(f"\n[bold red]Configuration Error:[/bold red] {e}")
        console.print("\n[yellow]Note:[/yellow] SerpAPI key is required for real trend data.")
        console.print("[dim]The system will use sample data instead.[/dim]")
        console.print("\nTo get real Google Trends data, add SERPAPI_KEY to your .env file")
        console.print("[dim]Get your key at: https://serpapi.com/manage-api-key[/dim]")
        sys.exit(1)
    
    task2_desc = "Loading Inventory Data..."
    console.print(f"[cyan]{task2_desc}[/cyan]")
    inventory_manager = InventoryManager()
    inventory_summary = inventory_manager.get_inventory_summary()
    inventory_items = inventory_manager.get_all_inventory()
    
    task3_desc = "Initializing AI Agent..."
    console.print(f"[cyan]{task3_desc}[/cyan]")
    try:
        inventory_agent = InventoryAgent()
    except ValueError as e:
        console.print(f"\n[bold red]ERROR:[/bold red] {e}")
        console.print("\n[yellow]Please create a .env file with your GEMINI_API_KEY:[/yellow]")
        console.print("[dim]GEMINI_API_KEY=your_api_key_here[/dim]")
        sys.exit(1)
    
    console.print()
    
    # Display inventory summary
    display_inventory_summary(inventory_summary)
    
    # Component A: Trend Analysis
    console.print(Panel.fit(
        "Analyzing Google Trends Data",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()
    
    keywords = get_shoe_keywords(inventory_items=inventory_items, use_inventory=True)
    console.print(f"[dim]> Total keywords available: {len(keywords)}[/dim]")
    
    max_keywords_to_analyze = 15
    if len(keywords) > max_keywords_to_analyze:
        console.print(f"[dim]> Analyzing first {max_keywords_to_analyze} keywords[/dim]")
    
    console.print()
    
    # Fetch trends with progress
    with console.status("[bold green]Fetching trend data from Google...", spinner="dots"):
        trending_products = trend_analyzer.get_high_confidence_trends(
            keywords,
            min_confidence=20.0,
            max_keywords=max_keywords_to_analyze
        )
    
    console.print()
    
    # Fallback to sample data if needed
    if not trending_products:
        console.print("[yellow]Warning: No trend data retrieved. Using sample data...[/yellow]\n")
        import random
        sample_keywords = keywords[:5]
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
                "confidence": confidence,
                "velocity": velocity,
                "strength": base_strength,
                "current_value": base_strength,
                "peak_value": base_strength * 1.2
            })
    
    # Display trending products
    display_trending_products(trending_products)
    
    # Component B: AI Recommendations
    console.print(Panel.fit(
        "Generating AI-Powered Recommendations",
        border_style="green",
        box=box.DOUBLE
    ))
    console.print()
    
    upcoming_holidays = get_upcoming_holidays()
    console.print(f"[dim]> Analyzing {len(trending_products)} trends[/dim]")
    console.print(f"[dim]> Season: {CURRENT_SEASON}[/dim]")
    console.print(f"[dim]> Events: {', '.join(upcoming_holidays)}[/dim]")
    console.print()
    
    with console.status("[bold green]AI is analyzing data...", spinner="dots"):
        recommendations = inventory_agent.generate_recommendations(
            trending_products,
            current_season=CURRENT_SEASON,
            upcoming_holidays=upcoming_holidays
        )
    
    console.print()
    
    # Display recommendations
    display_recommendations(recommendations)
    
    # Display low stock alerts
    low_stock_items = [
        item for item in inventory_manager.get_all_inventory()
        if item.current_stock <= item.reorder_point
    ]
    
    display_low_stock_alerts(low_stock_items)
    
    # Footer
    console.print(Panel.fit(
        "Analysis Complete\n\n"
        "Next Steps:\n"
        "  1. Review recommendations above\n"
        "  2. Adjust reorder quantities\n"
        "  3. Update warehouse locations\n"
        "  4. Schedule markdowns for declining items",
        title="Summary",
        border_style="cyan"
    ))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Analysis interrupted by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n\n[bold red]Error:[/bold red] {e}")
        import traceback
        console.print("[dim]" + traceback.format_exc() + "[/dim]")
        sys.exit(1)