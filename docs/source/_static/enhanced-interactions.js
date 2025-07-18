/**
 * Enhanced Interactive Elements for Haive Documentation
 * Modern JavaScript functionality for better UX
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Haive Enhanced Documentation loaded');

    // Initialize all interactive components
    initializeCollapsibles();
    initializeTabs();
    initializeAnimations();
    initializeCodeCopyButtons();
    initializeSearchEnhancements();
    initializeNavigationEnhancements();
    initializeAgentCards();
    initializeGameCards();
    initializeThemeToggle();

    // Performance optimization - lazy load heavy content
    initializeLazyLoading();
});

/**
 * Collapsible Sections
 */
function initializeCollapsibles() {
    const collapsibles = document.querySelectorAll('.collapsible');
    
    collapsibles.forEach(collapsible => {
        const header = collapsible.querySelector('.collapsible-header');
        const content = collapsible.querySelector('.collapsible-content');
        
        if (header && content) {
            header.addEventListener('click', () => {
                const isExpanded = collapsible.classList.contains('expanded');
                
                // Close all other collapsibles in the same group
                const group = collapsible.closest('.collapsible-group');
                if (group) {
                    group.querySelectorAll('.collapsible.expanded').forEach(other => {
                        if (other !== collapsible) {
                            other.classList.remove('expanded');
                        }
                    });
                }
                
                // Toggle current collapsible
                collapsible.classList.toggle('expanded');
                
                // Smooth animation
                if (!isExpanded) {
                    content.style.display = 'block';
                    const height = content.scrollHeight;
                    content.style.height = '0';
                    content.style.overflow = 'hidden';
                    content.style.transition = 'height 0.3s ease';
                    
                    requestAnimationFrame(() => {
                        content.style.height = height + 'px';
                    });
                    
                    setTimeout(() => {
                        content.style.height = '';
                        content.style.overflow = '';
                        content.style.transition = '';
                    }, 300);
                } else {
                    content.style.height = content.scrollHeight + 'px';
                    content.style.overflow = 'hidden';
                    content.style.transition = 'height 0.3s ease';
                    
                    requestAnimationFrame(() => {
                        content.style.height = '0';
                    });
                    
                    setTimeout(() => {
                        content.style.display = 'none';
                        content.style.height = '';
                        content.style.overflow = '';
                        content.style.transition = '';
                    }, 300);
                }
            });
        }
    });
}

/**
 * Tab System
 */
function initializeTabs() {
    const tabContainers = document.querySelectorAll('.tabs');
    
    tabContainers.forEach(container => {
        const buttons = container.querySelectorAll('.tab-button');
        const contents = container.querySelectorAll('.tab-content');
        
        buttons.forEach((button, index) => {
            button.addEventListener('click', () => {
                // Remove active state from all buttons and contents
                buttons.forEach(btn => btn.classList.remove('active'));
                contents.forEach(content => content.classList.remove('active'));
                
                // Add active state to clicked button and corresponding content
                button.classList.add('active');
                if (contents[index]) {
                    contents[index].classList.add('active');
                }
                
                // Scroll into view if needed
                container.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'nearest' 
                });
            });
        });
    });
}

/**
 * Animation System
 */
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                
                // Stagger animations for child elements
                if (entry.target.classList.contains('stagger-animation')) {
                    const children = entry.target.children;
                    Array.from(children).forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('animate-fade-in-up');
                        }, index * 100);
                    });
                }
                
                animationObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatableElements = document.querySelectorAll(
        '.agent-card, .game-card, .section-nav, .collapsible, .tabs, .stagger-animation'
    );
    
    animatableElements.forEach(element => {
        animationObserver.observe(element);
    });
}

/**
 * Enhanced Code Copy Buttons
 */
function initializeCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('.highlight pre, .agent-code-content');
    
    codeBlocks.forEach(block => {
        // Skip if already has copy button
        if (block.parentNode.querySelector('.enhanced-copy-btn')) return;
        
        const copyButton = document.createElement('button');
        copyButton.className = 'enhanced-copy-btn';
        copyButton.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
        `;
        copyButton.title = 'Copy code to clipboard';
        
        copyButton.addEventListener('click', async () => {
            const code = block.textContent;
            
            try {
                await navigator.clipboard.writeText(code);
                
                // Success feedback
                copyButton.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20,6 9,17 4,12"></polyline>
                    </svg>
                    <span>Copied!</span>
                `;
                copyButton.classList.add('success');
                
                setTimeout(() => {
                    copyButton.innerHTML = `
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                        <span>Copy</span>
                    `;
                    copyButton.classList.remove('success');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy code:', err);
                copyButton.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="15" y1="9" x2="9" y2="15"></line>
                        <line x1="9" y1="9" x2="15" y2="15"></line>
                    </svg>
                    <span>Failed</span>
                `;
            }
        });
        
        // Position the button
        const container = block.parentNode;
        container.style.position = 'relative';
        container.appendChild(copyButton);
    });
}

/**
 * Search Enhancements
 */
function initializeSearchEnhancements() {
    const searchInput = document.querySelector('input[type="search"], #searchbox input');
    if (!searchInput) return;
    
    let searchTimeout;
    const searchResults = document.createElement('div');
    searchResults.className = 'enhanced-search-results';
    searchInput.parentNode.appendChild(searchResults);
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performEnhancedSearch(query, searchResults);
        }, 300);
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

/**
 * Navigation Enhancements
 */
function initializeNavigationEnhancements() {
    // Add smooth scrolling to all internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL without jumping
                history.pushState(null, null, href);
            }
        });
    });
    
    // Add breadcrumb enhancement
    enhanceBreadcrumbs();
    
    // Add section navigation
    addSectionNavigation();
}

/**
 * Agent Card Enhancements
 */
function initializeAgentCards() {
    const agentCards = document.querySelectorAll('.agent-card');
    
    agentCards.forEach(card => {
        // Add hover sound effect (optional)
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-4px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
        
        // Add click to expand functionality
        const expandButton = card.querySelector('.agent-expand-btn');
        if (expandButton) {
            expandButton.addEventListener('click', (e) => {
                e.preventDefault();
                toggleAgentDetails(card);
            });
        }
    });
}

/**
 * Game Card Enhancements
 */
function initializeGameCards() {
    const gameCards = document.querySelectorAll('.game-card');
    
    gameCards.forEach(card => {
        // Add parallax effect to game preview
        const preview = card.querySelector('.game-preview');
        if (preview) {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                preview.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            card.addEventListener('mouseleave', () => {
                preview.style.transform = '';
            });
        }
        
        // Add play button functionality
        const playButton = card.querySelector('.game-play-button');
        if (playButton) {
            playButton.addEventListener('click', (e) => {
                e.preventDefault();
                launchGame(card);
            });
        }
    });
}

/**
 * Theme Toggle
 */
function initializeThemeToggle() {
    // Add theme toggle button if it doesn't exist
    if (!document.querySelector('.theme-toggle')) {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = `
            <svg class="theme-icon-light" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"></circle>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
            </svg>
            <svg class="theme-icon-dark" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
        `;
        themeToggle.title = 'Toggle theme';
        
        // Add to header
        const header = document.querySelector('.sidebar-drawer') || document.body;
        header.appendChild(themeToggle);
        
        themeToggle.addEventListener('click', toggleTheme);
    }
}

/**
 * Lazy Loading
 */
function initializeLazyLoading() {
    const lazyElements = document.querySelectorAll('[data-lazy]');
    
    if ('IntersectionObserver' in window) {
        const lazyObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const src = element.dataset.lazy;
                    
                    if (element.tagName === 'IMG') {
                        element.src = src;
                    } else {
                        element.style.backgroundImage = `url(${src})`;
                    }
                    
                    element.classList.add('loaded');
                    lazyObserver.unobserve(element);
                }
            });
        });
        
        lazyElements.forEach(element => {
            lazyObserver.observe(element);
        });
    }
}

/**
 * Helper Functions
 */

function enhanceBreadcrumbs() {
    const breadcrumb = document.querySelector('.breadcrumb, nav[aria-label="breadcrumb"]');
    if (!breadcrumb) return;
    
    breadcrumb.classList.add('enhanced-breadcrumb');
    
    // Add separators if they don't exist
    const items = breadcrumb.querySelectorAll('a, span');
    items.forEach((item, index) => {
        if (index > 0 && index < items.length) {
            const separator = document.createElement('span');
            separator.className = 'enhanced-breadcrumb-separator';
            separator.textContent = '›';
            item.parentNode.insertBefore(separator, item);
        }
    });
}

function addSectionNavigation() {
    const headings = document.querySelectorAll('h2, h3');
    if (headings.length < 3) return;
    
    const nav = document.createElement('nav');
    nav.className = 'section-nav';
    nav.innerHTML = `
        <h3 class="section-nav-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9,22 9,12 15,12 15,22"></polyline>
            </svg>
            On this page
        </h3>
        <div class="section-nav-grid">
            ${Array.from(headings).map(heading => `
                <a href="#${heading.id}" class="section-nav-item">
                    <div class="section-nav-item-title">${heading.textContent}</div>
                    <div class="section-nav-item-desc">${heading.tagName}</div>
                </a>
            `).join('')}
        </div>
    `;
    
    // Insert after the first heading
    const firstHeading = document.querySelector('h1');
    if (firstHeading) {
        firstHeading.parentNode.insertBefore(nav, firstHeading.nextSibling);
    }
}

function toggleAgentDetails(card) {
    const details = card.querySelector('.agent-details');
    if (!details) return;
    
    card.classList.toggle('expanded');
    
    if (card.classList.contains('expanded')) {
        details.style.display = 'block';
        details.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
        details.style.display = 'none';
    }
}

function launchGame(card) {
    const gameUrl = card.dataset.gameUrl;
    const gameName = card.querySelector('.game-title').textContent;
    
    if (gameUrl) {
        // Open in new tab/window
        window.open(gameUrl, '_blank');
    } else {
        // Show modal or inline player
        showGameModal(gameName);
    }
}

function showGameModal(gameName) {
    const modal = document.createElement('div');
    modal.className = 'game-modal';
    modal.innerHTML = `
        <div class="game-modal-content">
            <div class="game-modal-header">
                <h3>${gameName}</h3>
                <button class="game-modal-close">&times;</button>
            </div>
            <div class="game-modal-body">
                <p>Game will be loaded here...</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal functionality
    const closeBtn = modal.querySelector('.game-modal-close');
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Add transition effect
    document.documentElement.style.transition = 'color 0.3s ease, background-color 0.3s ease';
    setTimeout(() => {
        document.documentElement.style.transition = '';
    }, 300);
}

function performEnhancedSearch(query, resultsContainer) {
    // Simple search implementation - in real use, this would connect to search API
    const searchableElements = document.querySelectorAll('h1, h2, h3, p, .agent-title, .game-title');
    const results = [];
    
    searchableElements.forEach(element => {
        const text = element.textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
            results.push({
                title: element.textContent,
                url: `#${element.id || ''}`,
                type: element.tagName.toLowerCase()
            });
        }
    });
    
    if (results.length > 0) {
        resultsContainer.innerHTML = results.slice(0, 5).map(result => `
            <a href="${result.url}" class="search-result-item">
                <div class="search-result-title">${result.title}</div>
                <div class="search-result-type">${result.type}</div>
            </a>
        `).join('');
        resultsContainer.style.display = 'block';
    } else {
        resultsContainer.innerHTML = '<div class="search-no-results">No results found</div>';
        resultsContainer.style.display = 'block';
    }
}

// Initialize theme on page load
(function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();