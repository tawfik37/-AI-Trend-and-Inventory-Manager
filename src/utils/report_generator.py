"""
HTML Report Generator for ATIM
Creates beautiful HTML reports with interactive charts
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from typing import List, Dict
import json


class ReportGenerator:
    """Generates beautiful HTML reports with charts."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_html_report(
        self,
        trending_products: List[Dict],
        inventory_summary: Dict,
        recommendations: str,
        low_stock_items: List,
        output_file: str = "atim_report.html"
    ) -> str:
        """
        Generate complete HTML report.
        
        Args:
            trending_products: List of trending products
            inventory_summary: Inventory summary dict
            recommendations: AI recommendations text
            low_stock_items: List of low stock items
            output_file: Output HTML filename
            
        Returns:
            Path to generated HTML file
        """
        # Create charts
        trends_chart = self._create_trends_chart(trending_products)
        inventory_chart = self._create_inventory_chart(inventory_summary)
        velocity_chart = self._create_velocity_chart(trending_products)
        
        # Build HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATIM Report - {self.timestamp}</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .chart-container {{
            margin: 30px 0;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .recommendations {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            line-height: 1.8;
        }}
        
        .recommendations h3 {{
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .recommendations ul {{
            margin-left: 20px;
        }}
        
        .recommendations li {{
            margin-bottom: 10px;
        }}
        
        .alert-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .alert-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .alert-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .alert-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .urgent {{
            color: #dc3545;
            font-weight: bold;
        }}
        
        .warning {{
            color: #ffc107;
            font-weight: bold;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Trend & Inventory Manager</h1>
            <p>Intelligent Inventory Analysis Report</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: {self.timestamp}</p>
        </div>
        
        <div class="content">
            <!-- Executive Summary -->
            <div class="section">
                <h2 class="section-title">📊 Executive Summary</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Products</h3>
                        <div class="value">{inventory_summary['total_items']}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Low Stock Alerts</h3>
                        <div class="value">{inventory_summary['low_stock_items']}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Inventory Value</h3>
                        <div class="value">${inventory_summary['total_inventory_value']:,.0f}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Trending Products</h3>
                        <div class="value">{len(trending_products)}</div>
                    </div>
                </div>
            </div>
            
            <!-- Trend Analysis Charts -->
            <div class="section">
                <h2 class="section-title">📈 Trend Analysis</h2>
                
                <div class="chart-container">
                    <h3 style="margin-bottom: 15px;">Top Trending Products by Confidence</h3>
                    <div id="trends-chart"></div>
                </div>
                
                <div class="chart-container">
                    <h3 style="margin-bottom: 15px;">Trend Velocity Analysis</h3>
                    <div id="velocity-chart"></div>
                </div>
            </div>
            
            <!-- AI Recommendations -->
            <div class="section">
                <h2 class="section-title">🤖 AI-Powered Recommendations</h2>
                <div class="recommendations">
                    {self._format_recommendations_html(recommendations)}
                </div>
            </div>
            
            <!-- Low Stock Alerts -->
            <div class="section">
                <h2 class="section-title">⚠️ Low Stock Alerts</h2>
                {self._create_low_stock_table_html(low_stock_items)}
            </div>
            
            <!-- Inventory Overview -->
            <div class="section">
                <h2 class="section-title">📦 Inventory Distribution</h2>
                <div class="chart-container">
                    <div id="inventory-chart"></div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>AI Trend & Inventory Manager (ATIM) | Powered by Google Gemini AI & SerpAPI</p>
            <p style="margin-top: 5px;">Report generated on {self.timestamp}</p>
        </div>
    </div>
    
    <script>
        // Trends Chart
        {trends_chart}
        
        // Velocity Chart
        {velocity_chart}
        
        // Inventory Chart
        {inventory_chart}
    </script>
</body>
</html>
"""
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_file
    
    def _create_trends_chart(self, trending_products: List[Dict]) -> str:
        """Create trends bar chart."""
        if not trending_products:
            return ""
        
        # Prepare data
        products = [t['keyword'].title() for t in trending_products[:10]]
        confidence = [t['confidence'] for t in trending_products[:10]]
        colors = []
        
        for t in trending_products[:10]:
            if t['status'] == 'Rising':
                colors.append('#28a745')  # Green
            elif t['status'] == 'Declining':
                colors.append('#dc3545')  # Red
            elif t['status'] == 'Peaking':
                colors.append('#ffc107')  # Yellow
            else:
                colors.append('#6c757d')  # Gray
        
        fig = go.Figure(data=[
            go.Bar(
                x=confidence,
                y=products,
                orientation='h',
                marker=dict(color=colors),
                text=[f"{c:.1f}" for c in confidence],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            xaxis_title="Confidence Score",
            yaxis_title="Product",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white'
        )
        
        return f"Plotly.newPlot('trends-chart', {fig.to_json()});"
    
    def _create_velocity_chart(self, trending_products: List[Dict]) -> str:
        """Create velocity scatter chart."""
        if not trending_products:
            return ""
        
        # Prepare data
        products = [t['keyword'].title() for t in trending_products[:10]]
        velocity = [t['velocity'] for t in trending_products[:10]]
        strength = [t['strength'] for t in trending_products[:10]]
        
        colors = ['green' if v > 0 else 'red' for v in velocity]
        
        fig = go.Figure(data=[
            go.Scatter(
                x=velocity,
                y=strength,
                mode='markers+text',
                marker=dict(
                    size=[abs(v)*3 + 10 for v in velocity],
                    color=colors,
                    opacity=0.6,
                    line=dict(width=2, color='white')
                ),
                text=products,
                textposition='top center',
                textfont=dict(size=10)
            )
        ])
        
        fig.update_layout(
            xaxis_title="Velocity (Rate of Change)",
            yaxis_title="Strength (Average Interest)",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            shapes=[
                # Add quadrant lines
                dict(type='line', x0=0, y0=0, x1=0, y1=100, line=dict(color='gray', dash='dash')),
            ]
        )
        
        return f"Plotly.newPlot('velocity-chart', {fig.to_json()});"
    
    def _create_inventory_chart(self, inventory_summary: Dict) -> str:
        """Create inventory distribution pie chart."""
        # This would need category breakdown from inventory
        # For now, create a simple placeholder
        fig = go.Figure(data=[
            go.Pie(
                labels=['In Stock', 'Low Stock'],
                values=[
                    inventory_summary['total_items'] - inventory_summary['low_stock_items'],
                    inventory_summary['low_stock_items']
                ],
                marker=dict(colors=['#28a745', '#ffc107']),
                hole=0.4
            )
        ])
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True
        )
        
        return f"Plotly.newPlot('inventory-chart', {fig.to_json()});"
    
    def _format_recommendations_html(self, recommendations: str) -> str:
        """Format recommendations text as HTML."""
        # Simple markdown-like formatting
        lines = recommendations.split('\n')
        html_lines = []
        
        for line in lines:
            if line.startswith('###'):
                html_lines.append(f"<h3>{line.replace('###', '').strip()}</h3>")
            elif line.startswith('##'):
                html_lines.append(f"<h3>{line.replace('##', '').strip()}</h3>")
            elif line.startswith('-'):
                if not html_lines or not html_lines[-1].startswith('<ul>'):
                    html_lines.append('<ul>')
                html_lines.append(f"<li>{line[1:].strip()}</li>")
            else:
                if html_lines and html_lines[-1].startswith('<ul>'):
                    html_lines.append('</ul>')
                if line.strip():
                    html_lines.append(f"<p>{line}</p>")
        
        return '\n'.join(html_lines)
    
    def _create_low_stock_table_html(self, low_stock_items: List) -> str:
        """Create HTML table for low stock items."""
        if not low_stock_items:
            return '<p style="color: #28a745; font-weight: bold;">✅ All items are above reorder point!</p>'
        
        rows = []
        for item in low_stock_items:
            urgency_class = 'urgent' if item.current_stock < item.reorder_point * 0.5 else 'warning'
            urgency_text = '🔴 URGENT' if item.current_stock < item.reorder_point * 0.5 else '🟡 REORDER'
            
            rows.append(f"""
                <tr>
                    <td>{item.product_name}</td>
                    <td>{item.current_stock}</td>
                    <td>{item.reorder_point}</td>
                    <td class="{urgency_class}">{urgency_text}</td>
                </tr>
            """)
        
        return f"""
        <table class="alert-table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Current Stock</th>
                    <th>Reorder Point</th>
                    <th>Action Required</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """