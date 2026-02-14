/**
 * ATIM - Main Application Entry Point
 * Beautiful, modular inventory management interface
 */

import API from './core/api.js';
import State from './core/state.js';
import { formatNumber, formatCurrency } from './core/utils.js';
import Toast from './components/Toast.js';
import ProgressTracker from './components/ProgressTracker.js';
import FileUploader from './components/FileUploader.js';
import ChartManager from './components/ChartManager.js';

class ATIMApp {
    constructor() {
        this.toast = new Toast();
        this.progressTracker = null;
        this.fileUploader = null;
        this.chartManager = new ChartManager();
        this.currentData = null;
    }

    async init() {
        console.log('🚀 ATIM Application Starting...');
        
        // Initialize Progress Tracker
        this.progressTracker = new ProgressTracker('progressContainer');
        this.progressTracker.init([
            'Uploading',
            'Loading Inventory',
            'Analyzing Trends',
            'AI Analysis',
            'Finalizing'
        ]);

        // Initialize File Uploader
        this.fileUploader = new FileUploader({
            onSelect: (file) => this.handleFileSelect(file),
            onUpload: (data) => this.handleUploadComplete(data)
        });
        this.fileUploader.init('uploadArea', 'fileInput');

        // Setup form submission
        const form = document.getElementById('uploadForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));

        console.log('✅ Application initialized');
    }

    handleFileSelect(file) {
        const uploadText = document.querySelector('.upload-text');
        if (uploadText) {
            uploadText.textContent = `Selected: ${file.name}`;
        }
        
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
        }

        this.toast.info(`File selected: ${file.name}`);
    }

    async handleSubmit(e) {
        e.preventDefault();

        // Show loading state
        this.showLoading();

        // Get form data
        const formData = new FormData(e.target);

        try {
            // Step 1: Uploading
            this.progressTracker.update(0, 'Uploading file...');
            await this.delay(300);

            // Step 2: Loading
            this.progressTracker.update(1, 'Loading inventory...');
            await this.delay(300);

            // Make API call
            const data = await API.uploadInventory(formData);

            // Step 3: Analyzing
            this.progressTracker.update(2, 'Analyzing trends...');
            await this.delay(500);

            // Step 4: AI Analysis
            this.progressTracker.update(3, 'Generating recommendations...');
            await this.delay(500);

            // Step 5: Complete
            this.progressTracker.update(4, 'Complete!');
            await this.delay(300);

            // Show results
            this.showResults(data);
            this.toast.success('Analysis complete!');

        } catch (error) {
            this.hideLoading();
            this.showError(error.message);
            this.toast.error(`Error: ${error.message}`);
        }
    }

    showLoading() {
        document.getElementById('uploadCard').style.display = 'none';
        document.getElementById('loading').classList.add('active');
        document.getElementById('results').classList.remove('active');
    }

    hideLoading() {
        document.getElementById('loading').classList.remove('active');
        document.getElementById('uploadCard').style.display = 'block';
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.classList.add('active');
    }

    showResults(data) {
        this.currentData = data;
        
        // Hide loading, show results
        document.getElementById('loading').classList.remove('active');
        document.getElementById('results').classList.add('active');

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Render all sections
        this.renderStats(data);
        this.renderTrendsTable(data.trending_products);
        this.renderLowStockTable(data.low_stock_items);
        this.renderActionItems(data.low_stock_items, data.trending_products);
        this.renderRecommendations(data.recommendations);
        
        // Render charts if analytics available
        if (data.analytics) {
            this.renderCharts(data.analytics);
        }

        // Set report download link
        if (data.report_url) {
            document.getElementById('downloadReport').href = data.report_url;
        }
    }

    renderActionItems(lowStockItems, trendingProducts) {
        const container = document.getElementById('actionItems');
        const actions = [];

        // Generate actions from low stock items
        if (lowStockItems && lowStockItems.length > 0) {
            lowStockItems.forEach(item => {
                const isUrgent = item.current_stock < item.reorder_point * 0.5;
                actions.push({
                    text: `Reorder ${item.product_name}`,
                    meta: `Current: ${item.current_stock} | Reorder: ${item.reorder_point}`,
                    badge: isUrgent ? 'URGENT' : 'REORDER',
                    badgeClass: isUrgent ? 'badge-urgent' : 'badge-warning',
                    completed: false
                });
            });
        }

        // Generate actions from trending products
        if (trendingProducts && trendingProducts.length > 0) {
            const topTrending = trendingProducts.slice(0, 2);
            topTrending.forEach(product => {
                if (product.velocity > 10) {
                    actions.push({
                        text: `Review pricing for ${this.capitalize(product.keyword)}`,
                        meta: `Velocity: +${product.velocity.toFixed(1)} | Confidence: ${product.confidence.toFixed(1)}`,
                        badge: 'REVIEW',
                        badgeClass: 'badge-warning',
                        completed: false
                    });
                }
            });
        }

        // Limit to top 5 actions
        const topActions = actions.slice(0, 5);

        if (topActions.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--color-text-light); padding: var(--space-8);">No actions required at this time ✓</p>';
            return;
        }

        let html = '';
        topActions.forEach((action, idx) => {
            html += `
                <div class="action-card" onclick="toggleActionItem(this)" style="animation: fadeIn 0.5s ease-out ${idx * 0.1}s backwards;">
                    <div class="action-checkbox"></div>
                    <div class="action-content">
                        <div class="action-text">${action.text}</div>
                        <div class="action-meta">${action.meta}</div>
                    </div>
                    <span class="action-badge ${action.badgeClass}">${action.badge}</span>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    renderStats(data) {
        const statsGrid = document.getElementById('statsGrid');
        statsGrid.innerHTML = `
            <div class="stat-card animate-scaleIn">
                <div class="stat-icon coral">📦</div>
                <div class="stat-label">Total Products</div>
                <div class="stat-value">${formatNumber(data.inventory_summary.total_items)}</div>
                <span class="stat-trend">↗ Active inventory</span>
            </div>
            <div class="stat-card animate-scaleIn" style="animation-delay: 0.1s">
                <div class="stat-icon amber">⚠️</div>
                <div class="stat-label">Low Stock Alerts</div>
                <div class="stat-value">${data.inventory_summary.low_stock_items}</div>
                <span class="stat-trend">Needs attention</span>
            </div>
            <div class="stat-card animate-scaleIn" style="animation-delay: 0.2s">
                <div class="stat-icon teal">💰</div>
                <div class="stat-label">Inventory Value</div>
                <div class="stat-value">${formatCurrency(data.inventory_summary.total_value)}</div>
                <span class="stat-trend">↗ Total value</span>
            </div>
            <div class="stat-card animate-scaleIn" style="animation-delay: 0.3s">
                <div class="stat-icon purple">📈</div>
                <div class="stat-label">Trending Items</div>
                <div class="stat-value">${data.trending_products.length}</div>
                <span class="stat-trend">↗ Rising demand</span>
            </div>
        `;
    }

    renderTrendsTable(trends) {
        const table = document.getElementById('trendsTable');
        let html = `
            <thead>
                <tr>
                    <th>Rank</th>
                    <th class="sortable">Product</th>
                    <th class="sortable">Status</th>
                    <th class="sortable">Confidence</th>
                    <th class="sortable">Velocity</th>
                </tr>
            </thead>
            <tbody>
        `;

        trends.forEach((trend, idx) => {
            const statusClass = `status-${trend.status.toLowerCase()}`;
            html += `
                <tr class="animate-fadeIn" style="animation-delay: ${idx * 0.05}s">
                    <td>#${idx + 1}</td>
                    <td>${this.capitalize(trend.keyword)}</td>
                    <td class="${statusClass}">${trend.status}</td>
                    <td>${trend.confidence.toFixed(1)}</td>
                    <td>${trend.velocity > 0 ? '+' : ''}${trend.velocity.toFixed(1)}</td>
                </tr>
            `;
        });

        html += '</tbody>';
        table.innerHTML = html;
    }

    renderLowStockTable(items) {
        const table = document.getElementById('lowStockTable');
        
        if (!items || items.length === 0) {
            table.innerHTML = `
                <tbody>
                    <tr>
                        <td colspan="4" class="text-center p-lg">
                            <div class="table-empty">
                                <div class="table-empty-icon">✅</div>
                                <div>All items are above reorder point</div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            `;
            return;
        }

        let html = `
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Current Stock</th>
                    <th>Reorder Point</th>
                    <th>Reorder Quantity</th>
                </tr>
            </thead>
            <tbody>
        `;

        items.forEach((item, idx) => {
            const isUrgent = item.current_stock < item.reorder_point * 0.5;
            html += `
                <tr class="${isUrgent ? 'urgent-row' : ''} animate-fadeIn" style="animation-delay: ${idx * 0.05}s">
                    <td><strong>${item.product_name}</strong></td>
                    <td style="color: ${isUrgent ? 'var(--color-error)' : 'var(--color-warning)'}; font-weight: bold;">${item.current_stock}</td>
                    <td>${item.reorder_point}</td>
                    <td style="color: var(--color-success); font-weight: bold;">${item.reorder_quantity}</td>
                </tr>
            `;
        });

        html += '</tbody>';
        table.innerHTML = html;
    }

    renderRecommendations(text) {
        const div = document.getElementById('recommendationsDiv');
        div.innerHTML = this.formatMarkdown(text);
    }

    renderCharts(analytics) {
        // Stock Health Overview chart
        if (analytics.stock_health || this.currentData) {
            const lowStockCount = this.currentData.low_stock_items?.length || 0;
            const totalItems = this.currentData.inventory_summary?.total_items || 0;
            const healthyStock = totalItems - lowStockCount;

            this.chartManager.create('stockHealthChart', {
                type: 'doughnut',
                data: {
                    labels: ['Healthy Stock', 'Low Stock'],
                    datasets: [{
                        data: [healthyStock, lowStockCount],
                        backgroundColor: ['#10b981', '#f59e0b'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: { size: 14 }
                            }
                        }
                    }
                }
            });
        }

        // Category distribution chart
        if (analytics.category_breakdown) {
            this.chartManager.create('categoryChart', {
                type: 'doughnut',
                data: {
                    labels: analytics.category_breakdown.categories,
                    datasets: [{
                        data: analytics.category_breakdown.counts,
                        backgroundColor: [
                            '#667eea', '#764ba2', '#f093fb', '#4facfe',
                            '#00f2fe', '#43e97b', '#fa709a', '#fee140'
                        ],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: { size: 14 }
                            }
                        }
                    }
                }
            });
        }
    }

    formatMarkdown(text) {
        // Simple markdown formatting
        return text
            .replace(/### (.*)/g, '<h3>$1</h3>')
            .replace(/## (.*)/g, '<h2>$1</h2>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
    }

    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new ATIMApp();
    app.init();
});

// Global function for action item toggle
window.toggleActionItem = function(card) {
    const checkbox = card.querySelector('.action-checkbox');
    const isCompleted = card.classList.contains('completed');
    
    if (isCompleted) {
        card.classList.remove('completed');
        checkbox.classList.remove('checked');
    } else {
        card.classList.add('completed');
        checkbox.classList.add('checked');
    }
};
