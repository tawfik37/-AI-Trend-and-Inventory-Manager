/**
 * Progress Tracker Component
 */
export default class ProgressTracker {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.steps = [];
        this.currentStep = 0;
    }

    init(steps) {
        this.steps = steps;
        this.render();
    }

    render() {
        const stepsHTML = this.steps.map((step, index) => `
            <div class="progress-step">
                <div class="step-circle" id="step${index + 1}">${index + 1}</div>
                <div class="step-label">${step}</div>
            </div>
        `).join('');

        this.container.innerHTML = `
            <div class="progress-steps">${stepsHTML}</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
        `;
    }

    update(stepIndex, message = '') {
        this.currentStep = stepIndex;
        
        // Update step circles
        this.steps.forEach((_, index) => {
            const circle = document.getElementById(`step${index + 1}`);
            if (index < stepIndex) {
                circle.classList.remove('active');
                circle.classList.add('completed');
            } else if (index === stepIndex) {
                circle.classList.add('active');
                circle.classList.remove('completed');
            } else {
                circle.classList.remove('active', 'completed');
            }
        });

        // Update progress bar
        const progress = ((stepIndex + 1) / this.steps.length) * 100;
        const fill = document.getElementById('progressFill');
        if (fill) fill.style.width = `${progress}%`;
    }
}