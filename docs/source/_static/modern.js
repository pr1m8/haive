/**
 * Modern Haive Documentation JavaScript
 * Clean, minimal, and performance-focused enhancements
 */

(function() {
  'use strict';

  // ==========================================================================
  // Utilities
  // ==========================================================================
  
  const utils = {
    // Debounce function for performance
    debounce: (func, wait) => {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    // Query selector with error handling
    $: (selector, context = document) => context.querySelector(selector),
    $$: (selector, context = document) => Array.from(context.querySelectorAll(selector)),

    // Add class with error handling
    addClass: (element, className) => {
      if (element && element.classList) {
        element.classList.add(className);
      }
    },

    // Remove class with error handling  
    removeClass: (element, className) => {
      if (element && element.classList) {
        element.classList.remove(className);
      }
    }
  };

  // ==========================================================================
  // Smooth Scrolling for Anchor Links
  // ==========================================================================
  
  function initSmoothScrolling() {
    utils.$$('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        
        // Skip empty or placeholder anchors
        if (!href || href === '#' || href === '#top') return;
        
        const target = utils.$(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
          
          // Update URL without triggering scroll
          if (history.pushState) {
            history.pushState(null, null, href);
          }
        }
      });
    });
  }

  // ==========================================================================
  // Enhanced Copy Button Feedback
  // ==========================================================================
  
  function enhanceCopyButtons() {
    utils.$$('.copybtn').forEach(button => {
      button.addEventListener('click', function() {
        const originalText = this.textContent.trim();
        const originalIcon = this.innerHTML;
        
        // Show success state
        this.textContent = '✓ Copied!';
        this.style.background = '#10b981';
        this.style.color = 'white';
        
        // Reset after 2 seconds
        setTimeout(() => {
          this.innerHTML = originalIcon;
          this.style.background = '';
          this.style.color = '';
        }, 2000);
      });
    });
  }

  // ==========================================================================
  // Reading Progress Indicator
  // ==========================================================================
  
  function initProgressIndicator() {
    // Create progress bar
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 3px;
      background: linear-gradient(90deg, var(--color-brand-primary), var(--color-brand-content));
      transition: width 0.2s ease;
      z-index: var(--z-fixed);
      pointer-events: none;
    `;
    
    document.body.appendChild(progressBar);
    
    // Update progress on scroll
    const updateProgress = utils.debounce(() => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      const scrolled = window.pageYOffset;
      const progress = Math.min((scrolled / documentHeight) * 100, 100);
      
      progressBar.style.width = `${progress}%`;
    }, 10);
    
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress(); // Initial call
  }

  // ==========================================================================
  // Search Enhancement with Keyboard Shortcuts
  // ==========================================================================
  
  function initSearchEnhancement() {
    // Keyboard shortcut for search (Ctrl/Cmd + K)
    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = utils.$('input[type="search"]') || utils.$('.search-input');
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }
      
      // Escape to blur search
      if (e.key === 'Escape') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.type === 'search') {
          activeElement.blur();
        }
      }
    });
  }

  // ==========================================================================
  // Auto-hide Elements on Scroll
  // ==========================================================================
  
  function initScrollHide() {
    let lastScrollY = window.pageYOffset;
    let ticking = false;
    
    const updateScrollDirection = () => {
      const scrollY = window.pageYOffset;
      const scrollingDown = scrollY > lastScrollY;
      const scrollingUp = scrollY < lastScrollY;
      
      // Add classes for CSS to use
      if (scrollingDown && scrollY > 100) {
        document.body.classList.add('scrolling-down');
        document.body.classList.remove('scrolling-up');
      } else if (scrollingUp) {
        document.body.classList.add('scrolling-up');
        document.body.classList.remove('scrolling-down');
      }
      
      lastScrollY = scrollY;
      ticking = false;
    };
    
    const requestScrollUpdate = () => {
      if (!ticking) {
        requestAnimationFrame(updateScrollDirection);
        ticking = true;
      }
    };
    
    window.addEventListener('scroll', requestScrollUpdate, { passive: true });
  }

  // ==========================================================================
  // Table of Contents Enhancement
  // ==========================================================================
  
  function initTocEnhancement() {
    const toc = utils.$('.toc-tree') || utils.$('.page-toc');
    if (!toc) return;
    
    // Add smooth scrolling to TOC links
    utils.$$('a', toc).forEach(link => {
      link.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href && href.startsWith('#')) {
          const target = utils.$(href);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        }
      });
    });
  }

  // ==========================================================================
  // Code Block Enhancements
  // ==========================================================================
  
  function initCodeBlockEnhancements() {
    utils.$$('.highlight').forEach(codeBlock => {
      // Add language label if available
      const langMatch = codeBlock.className.match(/highlight-(\w+)/);
      if (langMatch) {
        const lang = langMatch[1];
        const label = document.createElement('div');
        label.textContent = lang.toUpperCase();
        label.style.cssText = `
          position: absolute;
          top: 0.5rem;
          right: 0.5rem;
          font-size: 0.75rem;
          font-weight: 600;
          color: var(--color-foreground-secondary);
          background: var(--color-background-secondary);
          padding: 0.25rem 0.5rem;
          border-radius: var(--radius-sm);
          opacity: 0.7;
        `;
        
        codeBlock.style.position = 'relative';
        codeBlock.appendChild(label);
      }
    });
  }

  // ==========================================================================
  // Image Lazy Loading and Enhancement
  // ==========================================================================
  
  function initImageEnhancements() {
    // Add loading="lazy" to images
    utils.$$('img').forEach(img => {
      if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
      
      // Add error handling
      img.addEventListener('error', function() {
        this.style.display = 'none';
      });
    });
  }

  // ==========================================================================
  // Performance Monitoring
  // ==========================================================================
  
  function logPerformanceMetrics() {
    if ('performance' in window && 'getEntriesByType' in performance) {
      window.addEventListener('load', () => {
        setTimeout(() => {
          const navigation = performance.getEntriesByType('navigation')[0];
          if (navigation) {
            console.log('📊 Page Performance:', {
              'DOM Content Loaded': `${Math.round(navigation.domContentLoadedEventEnd)}ms`,
              'Load Complete': `${Math.round(navigation.loadEventEnd)}ms`,
              'First Paint': 'Check DevTools for detailed metrics'
            });
          }
        }, 1000);
      });
    }
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================
  
  function init() {
    // Check if DOM is already loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }
    
    try {
      // Initialize all features
      initSmoothScrolling();
      enhanceCopyButtons();
      initProgressIndicator();
      initSearchEnhancement();
      initScrollHide();
      initTocEnhancement();
      initCodeBlockEnhancements();
      initImageEnhancements();
      
      // Development helpers
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        logPerformanceMetrics();
      }
      
      // Console welcome message
      console.log(
        '%c🤖 Haive Documentation',
        'font-size: 18px; font-weight: bold; color: #0f62fe;'
      );
      console.log(
        '%cBuild powerful AI agents with Haive! Visit: https://github.com/will-astley/haive',
        'font-size: 12px; color: #525252;'
      );
      
    } catch (error) {
      console.warn('Documentation enhancement error:', error);
    }
  }

  // Start initialization
  init();

})();