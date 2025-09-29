// Hospital Management System - Main JavaScript
// Modern UI interactions and utilities

document.addEventListener('DOMContentLoaded', function() {
    initializeComponents();
});

// Initialize all components
function initializeComponents() {
    initSidebarToggle();
    initAnimations();
    initFormEnhancements();
    initTableEnhancements();
    initTooltips();
    initDeleteConfirmations();
    initLoadingStates();
}

// Sidebar toggle for mobile
function initSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay d-md-none';
    
    if (sidebarToggle && sidebar) {
        // Add overlay
        document.body.appendChild(overlay);
        
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
            document.body.classList.toggle('sidebar-open');
        });
        
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
        });
        
        // Close sidebar when clicking nav links on mobile
        const sidebarLinks = sidebar.querySelectorAll('.nav-link');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 768) {
                    sidebar.classList.remove('show');
                    overlay.classList.remove('show');
                    document.body.classList.remove('sidebar-open');
                }
            });
        });
    }
}

// Animation utilities
function initAnimations() {
    // Fade in elements on page load
    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Hover animations for cards
    const cards = document.querySelectorAll('.card, .stat-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Form enhancements
function initFormEnhancements() {
    // Add floating labels effect
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        // Add focus/blur animations
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check if input has value on load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });
    
    // Add form validation styling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'danger');
            }
        });
    });
}

// Table enhancements
function initTableEnhancements() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        // Add search functionality if table has data-searchable attribute
        if (table.hasAttribute('data-searchable')) {
            addTableSearch(table);
        }
        
        // Add row hover effects
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'var(--gray-50)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    });
}

// Add search functionality to table
function addTableSearch(table) {
    const searchContainer = document.createElement('div');
    searchContainer.className = 'table-search mb-3';
    searchContainer.innerHTML = `
        <div class="input-group">
            <span class="input-group-text">
                <i class="fas fa-search"></i>
            </span>
            <input type="text" class="form-control" placeholder="Search table...">
        </div>
    `;
    
    table.parentNode.insertBefore(searchContainer, table);
    
    const searchInput = searchContainer.querySelector('input');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        new bootstrap.Tooltip(element);
    });
}

// Delete confirmations
function initDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 
                          'Are you sure you want to delete this item?';
            
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Loading states
function initLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                submitButton.disabled = true;
                
                // Re-enable button after 5 seconds (fallback)
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 5000);
            }
        });
    });
}

// Utility functions

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alerts') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Create alert container if it doesn't exist
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alerts';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Show loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.id = 'loading-overlay';
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(spinner);
}

// Hide loading spinner
function hideLoading() {
    const spinner = document.getElementById('loading-overlay');
    if (spinner) {
        spinner.remove();
    }
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Animate counting effect for numbers
function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// Date formatting utility
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Debounce function for search
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Add custom styles for overlay
const overlayStyles = `
    .sidebar-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }
    
    .sidebar-overlay.show {
        opacity: 1;
        visibility: visible;
    }
    
    .sidebar-open {
        overflow: hidden;
    }
    
    .table-search .input-group-text {
        background-color: var(--gray-50);
        border-right: none;
        color: var(--gray-500);
    }
    
    .table-search .form-control {
        border-left: none;
    }
    
    .table-search .form-control:focus {
        box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
    }
    
    .btn-loading {
        position: relative;
        color: transparent !important;
    }
    
    .btn-loading::after {
        content: "";
        position: absolute;
        width: 16px;
        height: 16px;
        top: 50%;
        left: 50%;
        margin-left: -8px;
        margin-top: -8px;
        border: 2px solid transparent;
        border-top-color: currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
`;

// Inject custom styles
const styleSheet = document.createElement('style');
styleSheet.textContent = overlayStyles;
document.head.appendChild(styleSheet);

// Export functions for use in other scripts
window.HospitalUI = {
    showAlert,
    showLoading,
    hideLoading,
    animateCounter,
    formatDate,
    formatNumber,
    debounce
};