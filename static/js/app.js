/**
 * Plant Care Pro - Main JavaScript Application
 * Handles UI interactions, form validations, and dynamic content
 */

'use strict';

// Global App Object
const PlantCareApp = {
    // Initialize the application
    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupFormValidations();
    },

    // Setup global event listeners
    setupEventListeners() {
        // Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Bootstrap popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });

        // Auto-hide alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    },

    // Initialize various components
    initializeComponents() {
        this.initFileUpload();
        this.initChatInterface();
        this.initWeatherInterface();
        this.initProgressBars();
    },

    // Setup form validations
    setupFormValidations() {
        // Bootstrap form validation
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });

        // Custom validations
        this.setupCustomValidations();
    },

    // Custom form validations
    setupCustomValidations() {
        // Password strength indicator
        const passwordInputs = document.querySelectorAll('input[type="password"]');
        passwordInputs.forEach(input => {
            input.addEventListener('input', this.checkPasswordStrength);
        });

        // Email validation
        const emailInputs = document.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.addEventListener('blur', this.validateEmail);
        });
    },

    // File upload functionality
    initFileUpload() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('file');
        const imagePreview = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImg');
        const analyzeBtn = document.getElementById('analyzeBtn');

        if (!uploadArea || !fileInput) return;

        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-primary');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-primary');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-primary');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0], fileInput, imagePreview, previewImg, analyzeBtn);
            }
        });

        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // File input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileSelect(e.target.files[0], fileInput, imagePreview, previewImg, analyzeBtn);
            }
        });
    },

    // Handle file selection
    handleFileSelect(file, fileInput, imagePreview, previewImg, analyzeBtn) {
        // Validate file type
        const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            this.showNotification('Please select a valid image file (PNG, JPG, JPEG, GIF)', 'error');
            return;
        }

        // Validate file size (16MB max)
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showNotification('File size must be less than 16MB', 'error');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.classList.remove('d-none');
            if (analyzeBtn) {
                analyzeBtn.disabled = false;
            }
        };
        reader.readAsDataURL(file);
    },

    // Chat interface initialization
    initChatInterface() {
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const chatForm = document.getElementById('chatForm');
        const quickQuestions = document.querySelectorAll('.quick-question');

        if (!chatMessages) return;

        // Auto-scroll to bottom
        this.scrollToBottom = () => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        // Initial scroll
        this.scrollToBottom();

        // Quick questions
        quickQuestions.forEach(button => {
            button.addEventListener('click', () => {
                const question = button.getAttribute('data-question');
                if (messageInput) {
                    messageInput.value = question;
                    messageInput.focus();
                }
            });
        });

        // Form submission
        if (chatForm) {
            chatForm.addEventListener('submit', () => {
                const sendBtn = document.getElementById('sendBtn');
                if (sendBtn && messageInput.value.trim()) {
                    sendBtn.disabled = true;
                    sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                }
            });
        }

        // Enter key handling
        if (messageInput) {
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    chatForm.submit();
                }
            });
        }
    },

    // Weather interface initialization
    initWeatherInterface() {
        const weatherForm = document.querySelector('form[method="POST"]');
        if (!weatherForm) return;

        weatherForm.addEventListener('submit', () => {
            const submitBtn = weatherForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
            }
        });
    },

    // Initialize progress bars with animation
    initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const width = progressBar.style.width;
                    progressBar.style.width = '0%';
                    
                    setTimeout(() => {
                        progressBar.style.width = width;
                    }, 100);
                }
            });
        });

        progressBars.forEach(bar => {
            observer.observe(bar);
        });
    },

    // Password strength checker
    checkPasswordStrength(event) {
        const password = event.target.value;
        const strengthIndicator = document.getElementById('passwordStrength');
        
        if (!strengthIndicator) return;

        let strength = 0;
        let strengthText = '';
        let strengthClass = '';

        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;

        switch (strength) {
            case 0:
            case 1:
                strengthText = 'Very Weak';
                strengthClass = 'text-danger';
                break;
            case 2:
                strengthText = 'Weak';
                strengthClass = 'text-warning';
                break;
            case 3:
                strengthText = 'Fair';
                strengthClass = 'text-info';
                break;
            case 4:
                strengthText = 'Good';
                strengthClass = 'text-success';
                break;
            case 5:
                strengthText = 'Strong';
                strengthClass = 'text-success fw-bold';
                break;
        }

        strengthIndicator.textContent = strengthText;
        strengthIndicator.className = strengthClass;
    },

    // Email validation
    validateEmail(event) {
        const email = event.target.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (email && !emailRegex.test(email)) {
            event.target.setCustomValidity('Please enter a valid email address');
        } else {
            event.target.setCustomValidity('');
        }
    },

    // Show notification
    showNotification(message, type = 'info') {
        const alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
        const iconClass = type === 'error' ? 'fa-exclamation-triangle' : 
                         type === 'success' ? 'fa-check-circle' : 'fa-info-circle';

        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                <i class="fas ${iconClass} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        // Find or create alert container
        let alertContainer = document.querySelector('.alert-container');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.className = 'alert-container container mt-3';
            const main = document.querySelector('main');
            if (main) {
                main.insertBefore(alertContainer, main.firstChild);
            }
        }

        alertContainer.insertAdjacentHTML('beforeend', alertHtml);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            const alert = alertContainer.lastElementChild;
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    },

    // Utility: Format file size
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Utility: Copy to clipboard
    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success');
            }).catch(() => {
                this.fallbackCopyToClipboard(text);
            });
        } else {
            this.fallbackCopyToClipboard(text);
        }
    },

    // Fallback copy method
    fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showNotification('Copied to clipboard!', 'success');
        } catch (err) {
            this.showNotification('Failed to copy to clipboard', 'error');
        }
        
        document.body.removeChild(textArea);
    },

    // Loading state management
    showLoading(element, text = 'Loading...') {
        if (element) {
            element.disabled = true;
            element.innerHTML = `<i class="fas fa-spinner fa-spin me-1"></i>${text}`;
        }
    },

    hideLoading(element, originalText) {
        if (element) {
            element.disabled = false;
            element.innerHTML = originalText;
        }
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    PlantCareApp.init();
});

// Service Worker registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export for global access
window.PlantCareApp = PlantCareApp;
