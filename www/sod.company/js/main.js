// Sod.Company - Main JavaScript

// Form submission handling
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('leadForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Let form submit normally to PHP handler
            // Add any validation here if needed
            const phone = document.getElementById('phone');
            if (phone && phone.value) {
                // Basic phone validation
                const phoneNum = phone.value.replace(/\D/g, '');
                if (phoneNum.length < 10) {
                    e.preventDefault();
                    alert('Please enter a valid phone number');
                    return false;
                }
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // Mobile menu toggle (if needed)
    const mobileToggle = document.querySelector('.mobile-toggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            document.querySelector('.nav-links').classList.toggle('active');
        });
    }
});

// Google Analytics event tracking
function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
}

// Track phone clicks
document.querySelectorAll('a[href^="tel:"]').forEach(link => {
    link.addEventListener('click', function() {
        trackEvent('Contact', 'Phone Click', this.href);
    });
});

// Track form submissions
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        trackEvent('Lead', 'Form Submit', window.location.pathname);
    });
});
