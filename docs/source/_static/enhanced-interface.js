/**
 * Enhanced Interface JavaScript for Haive Documentation
 * Provides dynamic sidebar navigation, smooth interactions, and progressive enhancement
 */

(function() {
    'use strict';

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeEnhancedSidebar();
        initializeAPICardInteractions();
        initializeCodeBlockEnhancements();
        initializeSearchEnhancements();
        initializeAccessibility();
        initializeProgressiveEnhancement();
    });

    /**
     * Enhanced Sidebar Navigation
     */
    function initializeEnhancedSidebar() {
        const sidebar = document.querySelector('.sidebar-drawer');
        if (!sidebar) return;

        // Add sidebar brand if it doesn't exist
        addSidebarBrand(sidebar);
        
        // Enhance navigation tree
        enhanceNavigationTree();
        
        // Add section icons based on content
        addSectionIcons();
        
        // Add collapsible behavior
        addCollapsibleSections();
    }

    function addSidebarBrand(sidebar) {
        const existingBrand = sidebar.querySelector('.sidebar-brand');
        if (existingBrand) return;

        const brand = document.createElement('div');
        brand.className = 'sidebar-brand';
        brand.innerHTML = `
            <h1 class="brand-title">🤖 Haive</h1>
            <p class="brand-subtitle">AI Agent Framework</p>
        `;
        
        const firstChild = sidebar.firstElementChild;
        if (firstChild) {
            sidebar.insertBefore(brand, firstChild);
        } else {
            sidebar.appendChild(brand);
        }
    }

    function enhanceNavigationTree() {
        const navLinks = document.querySelectorAll('.toctree-wrapper .toctree-l1 > a');
        
        navLinks.forEach(link => {
            // Add hover effects and animations
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(4px)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
            });
            
            // Add click animations
            link.addEventListener('click', function(e) {
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }

    function addSectionIcons() {
        const sections = {
            'agents': '🤖',
            'tools': '🔧', 
            'games': '🎮',
            'core': '⚙️',
            'api': '📚',
            'guides': '📖',
            'mcp': '🔌',
            'dataflow': '🌊'
        };

        Object.keys(sections).forEach(section => {
            const links = document.querySelectorAll(`a[href*="${section}"]`);
            links.forEach(link => {
                if (link.closest('.toctree-l1')) {
                    link.parentElement.setAttribute('data-section', section);
                }
            });
        });
    }

    function addCollapsibleSections() {
        const mainSections = document.querySelectorAll('.toctree-wrapper .toctree-l1');
        
        mainSections.forEach(section => {
            const link = section.querySelector('a');
            const subsections = section.querySelectorAll('.toctree-l2');
            
            if (subsections.length > 0) {
                // Add expand/collapse indicator
                const indicator = document.createElement('span');
                indicator.className = 'expand-indicator';
                indicator.innerHTML = '▼';
                indicator.style.marginLeft = 'auto';
                indicator.style.fontSize = '0.8rem';
                indicator.style.transition = 'transform 0.3s ease';
                
                link.appendChild(indicator);
                
                // Add click handler for toggling
                link.addEventListener('click', function(e) {
                    if (e.target === indicator || e.target === link) {
                        e.preventDefault();
                        toggleSection(section, indicator);
                    }
                });
            }
        });
    }

    function toggleSection(section, indicator) {
        const subsections = section.querySelectorAll('.toctree-l2');
        const isExpanded = section.classList.contains('expanded');
        
        if (isExpanded) {
            // Collapse
            section.classList.remove('expanded');
            indicator.style.transform = 'rotate(0deg)';
            subsections.forEach(sub => {
                sub.style.maxHeight = '0';
                sub.style.opacity = '0';
                sub.style.overflow = 'hidden';
            });
        } else {
            // Expand
            section.classList.add('expanded');
            indicator.style.transform = 'rotate(180deg)';
            subsections.forEach(sub => {
                sub.style.maxHeight = 'none';
                sub.style.opacity = '1';
                sub.style.overflow = 'visible';
            });
        }
    }

    /**
     * API Card Interactions
     */
    function initializeAPICardInteractions() {
        const apiCards = document.querySelectorAll('.api-card');
        
        apiCards.forEach(card => {
            // Add intersection observer for animations
            observeCardVisibility(card);
            
            // Enhanced hover effects
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-6px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
            
            // Click animation for links
            const link = card.querySelector('.api-card-link');
            if (link) {
                link.addEventListener('click', function(e) {
                    // Add ripple effect
                    createRippleEffect(this, e);
                });
            }
        });
    }

    function observeCardVisibility(card) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                } else {
                    entry.target.style.opacity = '0';
                    entry.target.style.transform = 'translateY(20px)';
                }
            });
        }, { threshold: 0.1 });

        // Set initial state
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        observer.observe(card);
    }

    function createRippleEffect(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        // Add CSS for ripple effect
        if (!document.querySelector('#ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                .ripple {
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.6);
                    transform: scale(0);
                    animation: ripple-animation 0.6s linear;
                    pointer-events: none;
                }
                @keyframes ripple-animation {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    /**
     * Code Block Enhancements
     */
    function initializeCodeBlockEnhancements() {
        const codeBlocks = document.querySelectorAll('.highlight');
        
        codeBlocks.forEach(block => {
            // Add copy button if it doesn't exist
            addCopyButton(block);
            
            // Add language label
            addLanguageLabel(block);
            
            // Add line numbers if needed
            enhanceLineNumbers(block);
        });
    }

    function addCopyButton(codeBlock) {
        if (codeBlock.querySelector('.copy-button')) return;
        
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.innerHTML = '📋';
        button.title = 'Copy to clipboard';
        button.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            color: white;
            padding: 0.25rem 0.5rem;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
            z-index: 10;
        `;
        
        button.addEventListener('click', function() {
            const code = codeBlock.querySelector('pre').textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.innerHTML = '✅';
                button.title = 'Copied!';
                setTimeout(() => {
                    button.innerHTML = '📋';
                    button.title = 'Copy to clipboard';
                }, 2000);
            });
        });
        
        button.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(255, 255, 255, 0.2)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255, 255, 255, 0.1)';
        });
        
        codeBlock.style.position = 'relative';
        codeBlock.appendChild(button);
    }

    function addLanguageLabel(codeBlock) {
        const classes = codeBlock.className.split(' ');
        const langClass = classes.find(cls => cls.startsWith('language-') || cls.startsWith('highlight-'));
        
        if (langClass && !codeBlock.querySelector('.language-label')) {
            const lang = langClass.replace(/^(language-|highlight-)/, '').toUpperCase();
            const label = document.createElement('span');
            label.className = 'language-label';
            label.textContent = lang;
            label.style.cssText = `
                position: absolute;
                top: 0.5rem;
                left: 0.5rem;
                background: var(--haive-gradient-main);
                color: white;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.7rem;
                font-weight: bold;
                z-index: 10;
            `;
            
            codeBlock.appendChild(label);
        }
    }

    function enhanceLineNumbers(codeBlock) {
        const pre = codeBlock.querySelector('pre');
        if (!pre || pre.querySelector('.line-numbers')) return;
        
        const lines = pre.textContent.split('\n').length - 1;
        if (lines > 5) {
            // Add line numbers for longer code blocks
            const lineNumbers = document.createElement('div');
            lineNumbers.className = 'line-numbers';
            lineNumbers.style.cssText = `
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 2.5rem;
                background: rgba(0, 0, 0, 0.1);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
                padding: 1rem 0.5rem;
                font-family: var(--font-family-mono);
                font-size: 0.8rem;
                line-height: 1.7;
                color: rgba(255, 255, 255, 0.5);
                user-select: none;
            `;
            
            for (let i = 1; i <= lines; i++) {
                const lineNum = document.createElement('div');
                lineNum.textContent = i;
                lineNumbers.appendChild(lineNum);
            }
            
            codeBlock.appendChild(lineNumbers);
            pre.style.paddingLeft = '3rem';
        }
    }

    /**
     * Search Enhancements
     */
    function initializeSearchEnhancements() {
        const searchInput = document.querySelector('input[type="search"], .search input');
        if (!searchInput) return;
        
        // Add enhanced search functionality
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                enhancedSearch(this.value);
            }, 300);
        });
        
        // Add search suggestions
        addSearchSuggestions(searchInput);
    }

    function enhancedSearch(query) {
        if (!query || query.length < 2) return;
        
        // Highlight matching navigation items
        const navLinks = document.querySelectorAll('.toctree-wrapper a');
        navLinks.forEach(link => {
            const text = link.textContent.toLowerCase();
            if (text.includes(query.toLowerCase())) {
                link.style.background = 'rgba(102, 126, 234, 0.2)';
                link.style.fontWeight = 'bold';
            } else {
                link.style.background = '';
                link.style.fontWeight = '';
            }
        });
    }

    function addSearchSuggestions(searchInput) {
        const suggestions = [
            'SimpleAgent', 'ReactAgent', 'RAG', 'Multi-agent',
            'Tools', 'Games', 'Core Engine', 'MCP',
            'Configuration', 'Examples', 'API Reference'
        ];
        
        const datalist = document.createElement('datalist');
        datalist.id = 'search-suggestions';
        
        suggestions.forEach(suggestion => {
            const option = document.createElement('option');
            option.value = suggestion;
            datalist.appendChild(option);
        });
        
        searchInput.setAttribute('list', 'search-suggestions');
        searchInput.parentNode.appendChild(datalist);
    }

    /**
     * Accessibility Enhancements
     */
    function initializeAccessibility() {
        // Add skip links
        addSkipLinks();
        
        // Enhance keyboard navigation
        enhanceKeyboardNavigation();
        
        // Add ARIA labels
        addAriaLabels();
        
        // Respect reduced motion preferences
        respectReducedMotion();
    }

    function addSkipLinks() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--haive-primary);
            color: white;
            padding: 8px;
            border-radius: 4px;
            text-decoration: none;
            z-index: 1000;
            transition: top 0.3s;
        `;
        
        skipLink.addEventListener('focus', function() {
            this.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', function() {
            this.style.top = '-40px';
        });
        
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Add main content landmark if it doesn't exist
        const mainContent = document.querySelector('main, .main-content, [role="main"]');
        if (mainContent && !mainContent.id) {
            mainContent.id = 'main-content';
        }
    }

    function enhanceKeyboardNavigation() {
        // Add focus visible styles
        const style = document.createElement('style');
        style.textContent = `
            .js-focus-visible :focus:not(.focus-visible) {
                outline: none;
            }
            .focus-visible {
                outline: 2px solid var(--haive-primary);
                outline-offset: 2px;
            }
        `;
        document.head.appendChild(style);
        
        // Add keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Alt + S to focus search
            if (e.altKey && e.key === 's') {
                e.preventDefault();
                const searchInput = document.querySelector('input[type="search"]');
                if (searchInput) searchInput.focus();
            }
            
            // Alt + N to focus navigation
            if (e.altKey && e.key === 'n') {
                e.preventDefault();
                const firstNavLink = document.querySelector('.toctree-wrapper a');
                if (firstNavLink) firstNavLink.focus();
            }
        });
    }

    function addAriaLabels() {
        // Add labels to interactive elements
        const apiCards = document.querySelectorAll('.api-card');
        apiCards.forEach((card, index) => {
            const title = card.querySelector('.api-card-title');
            if (title) {
                card.setAttribute('aria-labelledby', `api-card-${index}`);
                title.id = `api-card-${index}`;
            }
        });
        
        // Add navigation landmarks
        const sidebar = document.querySelector('.sidebar-drawer');
        if (sidebar) {
            sidebar.setAttribute('role', 'navigation');
            sidebar.setAttribute('aria-label', 'Main navigation');
        }
    }

    function respectReducedMotion() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            const style = document.createElement('style');
            style.textContent = `
                * {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                }
            `;
            document.head.appendChild(style);
        }
    }

    /**
     * Progressive Enhancement
     */
    function initializeProgressiveEnhancement() {
        // Add CSS custom properties support detection
        if (CSS.supports('color', 'var(--test)')) {
            document.documentElement.classList.add('supports-custom-properties');
        }
        
        // Add Intersection Observer support
        if ('IntersectionObserver' in window) {
            document.documentElement.classList.add('supports-intersection-observer');
        }
        
        // Add focus-visible polyfill class
        document.documentElement.classList.add('js-focus-visible');
        
        // Lazy load images if Intersection Observer is supported
        if ('IntersectionObserver' in window) {
            lazyLoadImages();
        }
    }

    function lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }

    // Expose utilities globally for console debugging
    window.HaiveDocUtils = {
        toggleSection: toggleSection,
        createRippleEffect: createRippleEffect,
        enhancedSearch: enhancedSearch
    };

})();