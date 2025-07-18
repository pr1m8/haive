/**
 * Showcase Interactions for Haive Documentation
 * Enhanced interactivity for agent and game showcases
 */

(function() {
    'use strict';

    // === UTILITY FUNCTIONS === //
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // === SHOWCASE TABS === //
    
    function initializeShowcaseTabs() {
        const tabGroups = document.querySelectorAll('.showcase-tabs');
        
        tabGroups.forEach(tabGroup => {
            const tabs = tabGroup.querySelectorAll('.showcase-tab');
            const contents = tabGroup.parentElement.querySelectorAll('.showcase-content');
            
            tabs.forEach((tab, index) => {
                tab.addEventListener('click', () => {
                    // Remove active class from all tabs and contents
                    tabs.forEach(t => t.classList.remove('active'));
                    contents.forEach(c => c.classList.remove('active'));
                    
                    // Add active class to clicked tab and corresponding content
                    tab.classList.add('active');
                    if (contents[index]) {
                        contents[index].classList.add('active');
                    }
                });
            });
            
            // Activate first tab by default
            if (tabs.length > 0 && contents.length > 0) {
                tabs[0].classList.add('active');
                contents[0].classList.add('active');
            }
        });
    }

    // === CARD INTERACTIONS === //
    
    function initializeCardInteractions() {
        const cards = document.querySelectorAll('.showcase-card, .agent-card, .game-card');
        
        cards.forEach(card => {
            // Add hover effects
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-2px)';
                card.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.15)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
            });
            
            // Add click analytics
            card.addEventListener('click', (e) => {
                const cardType = card.className.split(' ')[0];
                const cardTitle = card.querySelector('.agent-title, .game-title')?.textContent || 'Unknown';
                
                // Track interaction (implement analytics as needed)
                console.log(`Card interaction: ${cardType} - ${cardTitle}`);
            });
        });
    }

    // === SEARCH FUNCTIONALITY === //
    
    function initializeShowcaseSearch() {
        // Create search input if it doesn't exist
        const showcaseContainer = document.querySelector('.agent-showcase, .games-showcase');
        if (!showcaseContainer) return;
        
        const searchContainer = document.createElement('div');
        searchContainer.className = 'showcase-search-container';
        searchContainer.innerHTML = `
            <div class="showcase-search-wrapper">
                <input type="text" class="showcase-search-input" placeholder="🔍 Search agents, games, or features...">
                <button class="showcase-search-clear" style="display: none;">×</button>
            </div>
            <div class="showcase-search-results"></div>
        `;
        
        showcaseContainer.parentElement.insertBefore(searchContainer, showcaseContainer);
        
        const searchInput = searchContainer.querySelector('.showcase-search-input');
        const clearButton = searchContainer.querySelector('.showcase-search-clear');
        const resultsContainer = searchContainer.querySelector('.showcase-search-results');
        
        // Search functionality
        const performSearch = debounce((query) => {
            const cards = document.querySelectorAll('.agent-card, .game-card');
            const results = [];
            
            if (query.length < 2) {
                // Show all cards
                cards.forEach(card => {
                    card.style.display = 'block';
                    card.classList.remove('search-highlight');
                });
                resultsContainer.innerHTML = '';
                clearButton.style.display = 'none';
                return;
            }
            
            clearButton.style.display = 'block';
            
            cards.forEach(card => {
                const title = card.querySelector('.agent-title, .game-title')?.textContent || '';
                const description = card.querySelector('.agent-description, .game-description')?.textContent || '';
                const features = Array.from(card.querySelectorAll('.agent-features li, .game-feature'))
                    .map(el => el.textContent).join(' ');
                
                const searchContent = `${title} ${description} ${features}`.toLowerCase();
                const queryLower = query.toLowerCase();
                
                if (searchContent.includes(queryLower)) {
                    card.style.display = 'block';
                    card.classList.add('search-highlight');
                    results.push({
                        title,
                        description: description.substring(0, 100) + '...',
                        card
                    });
                } else {
                    card.style.display = 'none';
                    card.classList.remove('search-highlight');
                }
            });
            
            // Show results count
            resultsContainer.innerHTML = `
                <div class="search-results-count">
                    Found ${results.length} result${results.length !== 1 ? 's' : ''} for "${query}"
                </div>
            `;
        }, 300);
        
        searchInput.addEventListener('input', (e) => {
            performSearch(e.target.value);
        });
        
        clearButton.addEventListener('click', () => {
            searchInput.value = '';
            performSearch('');
        });
    }

    // === PERFORMANCE MONITORING === //
    
    function initializePerformanceMonitoring() {
        const performanceBadges = document.querySelectorAll('.performance-badge');
        
        performanceBadges.forEach(badge => {
            // Add click handler to show detailed metrics
            badge.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Create modal or tooltip with detailed performance info
                const modal = document.createElement('div');
                modal.className = 'performance-modal';
                modal.innerHTML = `
                    <div class="performance-modal-content">
                        <h3>Performance Metrics</h3>
                        <div class="performance-details">
                            <p><strong>Response Time:</strong> < 2 seconds</p>
                            <p><strong>Memory Usage:</strong> Optimized</p>
                            <p><strong>Accuracy:</strong> 95%+</p>
                            <p><strong>Scalability:</strong> High</p>
                        </div>
                        <button class="close-modal">Close</button>
                    </div>
                `;
                
                document.body.appendChild(modal);
                
                // Close modal functionality
                modal.querySelector('.close-modal').addEventListener('click', () => {
                    document.body.removeChild(modal);
                });
                
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        document.body.removeChild(modal);
                    }
                });
            });
        });
    }

    // === COPY CODE FUNCTIONALITY === //
    
    function initializeCopyCode() {
        const codeBlocks = document.querySelectorAll('.highlight');
        
        codeBlocks.forEach(block => {
            // Add copy button
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-code-btn';
            copyButton.innerHTML = '📋 Copy';
            copyButton.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 0.8rem;
                cursor: pointer;
                z-index: 10;
                transition: all 0.3s ease;
            `;
            
            block.style.position = 'relative';
            block.appendChild(copyButton);
            
            copyButton.addEventListener('click', async () => {
                const codeText = block.querySelector('code')?.textContent || '';
                
                try {
                    await navigator.clipboard.writeText(codeText);
                    copyButton.innerHTML = '✅ Copied!';
                    copyButton.style.background = 'rgba(40, 167, 69, 0.8)';
                    
                    setTimeout(() => {
                        copyButton.innerHTML = '📋 Copy';
                        copyButton.style.background = 'rgba(0, 0, 0, 0.7)';
                    }, 2000);
                } catch (err) {
                    copyButton.innerHTML = '❌ Error';
                    copyButton.style.background = 'rgba(220, 53, 69, 0.8)';
                    
                    setTimeout(() => {
                        copyButton.innerHTML = '📋 Copy';
                        copyButton.style.background = 'rgba(0, 0, 0, 0.7)';
                    }, 2000);
                }
            });
        });
    }

    // === LAZY LOADING === //
    
    function initializeLazyLoading() {
        const cards = document.querySelectorAll('.showcase-card, .agent-card, .game-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('loaded');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });
        
        cards.forEach(card => {
            card.classList.add('loading');
            observer.observe(card);
        });
    }

    // === SMOOTH SCROLLING === //
    
    function initializeSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // === THEME AWARE UPDATES === //
    
    function initializeThemeAwareUpdates() {
        const themeObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                    // Update theme-specific elements
                    updateThemeSpecificElements();
                }
            });
        });
        
        themeObserver.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme']
        });
    }
    
    function updateThemeSpecificElements() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        
        // Update performance badges
        const performanceBadges = document.querySelectorAll('.performance-badge');
        performanceBadges.forEach(badge => {
            badge.style.background = isDark 
                ? 'linear-gradient(135deg, #38a169, #2d7d52)'
                : 'linear-gradient(135deg, #28a745, #20c997)';
        });
        
        // Update search highlights
        const searchHighlights = document.querySelectorAll('.search-highlight');
        searchHighlights.forEach(highlight => {
            highlight.style.outline = isDark 
                ? '2px solid #4da6ff'
                : '2px solid #0066cc';
        });
    }

    // === ACCESSIBILITY ENHANCEMENTS === //
    
    function initializeAccessibilityEnhancements() {
        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Close any open modals
                const modals = document.querySelectorAll('.performance-modal');
                modals.forEach(modal => {
                    if (modal.parentElement) {
                        modal.parentElement.removeChild(modal);
                    }
                });
            }
            
            if (e.key === 'Tab') {
                // Ensure focus indicators are visible
                document.body.classList.add('keyboard-navigation');
            }
        });
        
        // Remove keyboard navigation class on mouse use
        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
        
        // Add ARIA labels
        const cards = document.querySelectorAll('.agent-card, .game-card');
        cards.forEach(card => {
            const title = card.querySelector('.agent-title, .game-title')?.textContent;
            if (title) {
                card.setAttribute('aria-label', `${title} showcase card`);
                card.setAttribute('role', 'article');
            }
        });
    }

    // === INITIALIZATION === //
    
    function initialize() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initialize);
            return;
        }
        
        // Initialize all features
        initializeShowcaseTabs();
        initializeCardInteractions();
        initializeShowcaseSearch();
        initializePerformanceMonitoring();
        initializeCopyCode();
        initializeLazyLoading();
        initializeSmoothScrolling();
        initializeThemeAwareUpdates();
        initializeAccessibilityEnhancements();
        
        // Add loading complete class
        document.body.classList.add('showcase-loaded');
        
        console.log('🚀 Haive Showcase interactions initialized');
    }

    // === CSS INJECTION === //
    
    function injectAdditionalCSS() {
        const style = document.createElement('style');
        style.textContent = `
            .showcase-search-container {
                margin: 2rem 0;
            }
            
            .showcase-search-wrapper {
                position: relative;
                max-width: 400px;
                margin: 0 auto;
            }
            
            .showcase-search-input {
                width: 100%;
                padding: 0.75rem 1rem;
                border: 2px solid #e1e4e8;
                border-radius: 8px;
                font-size: 1rem;
                transition: all 0.3s ease;
            }
            
            .showcase-search-input:focus {
                outline: none;
                border-color: #0066cc;
                box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
            }
            
            .showcase-search-clear {
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: #666;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .showcase-search-clear:hover {
                background: rgba(0, 0, 0, 0.1);
            }
            
            .search-results-count {
                text-align: center;
                margin: 1rem 0;
                color: #666;
                font-size: 0.9rem;
            }
            
            .search-highlight {
                outline: 2px solid #0066cc;
                outline-offset: 2px;
            }
            
            .performance-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            
            .performance-modal-content {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                max-width: 400px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
            }
            
            [data-theme="dark"] .performance-modal-content {
                background: #2d3748;
                color: #e2e8f0;
            }
            
            .performance-details p {
                margin: 0.5rem 0;
            }
            
            .close-modal {
                background: #0066cc;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 1rem;
            }
            
            .close-modal:hover {
                background: #0056b3;
            }
            
            .loading {
                opacity: 0.7;
            }
            
            .loaded {
                opacity: 1;
                transition: opacity 0.3s ease;
            }
            
            .keyboard-navigation *:focus {
                outline: 2px solid #0066cc !important;
                outline-offset: 2px !important;
            }
            
            .copy-code-btn:hover {
                background: rgba(0, 0, 0, 0.9) !important;
            }
        `;
        
        document.head.appendChild(style);
    }

    // Start initialization
    injectAdditionalCSS();
    initialize();

})();