/**
 * File Uploader Component
 */
export default class FileUploader {
    constructor(options = {}) {
        this.options = options;
        this.file = null;
        this.callbacks = {
            onSelect: options.onSelect || (() => {}),
            onUpload: options.onUpload || (() => {})
        };
    }

    init(uploadAreaId, fileInputId) {
        this.uploadArea = document.getElementById(uploadAreaId);
        this.fileInput = document.getElementById(fileInputId);

        // Click to upload
        this.uploadArea.addEventListener('click', () => this.fileInput.click());

        // File selected
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', () => this.handleDragLeave());
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.file = file;
            this.callbacks.onSelect(file);
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave() {
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.file = files[0];
            this.fileInput.files = files;
            this.callbacks.onSelect(files[0]);
        }
    }

    getFile() {
        return this.file;
    }
}