/**
 * API Module
 * Handles all HTTP requests to the backend
 */

class API {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
    }

    /**
     * Upload inventory file and get analysis
     */
    async uploadInventory(formData, onProgress) {
        try {
            const response = await fetch(`${this.baseURL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Upload failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Health check
     */
    async healthCheck() {
        const response = await fetch(`${this.baseURL}/health`);
        return await response.json();
    }
}

export default new API();