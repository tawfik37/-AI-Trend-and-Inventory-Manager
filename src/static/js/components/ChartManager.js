/**
 * Chart Manager Component
 */
export default class ChartManager {
    constructor() {
        this.charts = {};
    }

    create(canvasId, config) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        // Create new chart
        this.charts[canvasId] = new Chart(ctx, config);
        return this.charts[canvasId];
    }

    destroy(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }

    destroyAll() {
        Object.keys(this.charts).forEach(id => this.destroy(id));
    }
}