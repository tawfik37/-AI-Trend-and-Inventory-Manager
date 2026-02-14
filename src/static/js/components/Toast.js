/**
 * Toast Notification Component
 */

export default class Toast {
    constructor() {
        this.container = this.createContainer();
    }

    createContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} animate-slideUp`;
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <span class="toast-content">${message}</span>
            <button class="toast-close" aria-label="Close">×</button>
        `;
        
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.onclick = () => this.remove(toast);
        
        this.container.appendChild(toast);
        
        if (duration > 0) {
            setTimeout(() => this.remove(toast), duration);
        }
        
        return toast;
    }

    remove(toast) {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }

    success(message) {
        return this.show(message, 'success');
    }

    error(message) {
        return this.show(message, 'error');
    }

    warning(message) {
        return this.show(message, 'warning');
    }

    info(message) {
        return this.show(message, 'info');
    }
}