/**
 * State Management
 */
class State {
    constructor() {
        this.data = {
            currentFile: null,
            analysisResults: null,
            isLoading: false,
            error: null
        };
        this.listeners = [];
    }

    get(key) {
        return this.data[key];
    }

    set(key, value) {
        this.data[key] = value;
        this.notify();
    }

    update(updates) {
        Object.assign(this.data, updates);
        this.notify();
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.data));
    }
}

export default new State();