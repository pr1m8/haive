/**
 * Contextual Navigation for Furo Theme
 * 
 * Enhances navigation to show contextual view when on module pages
 */

(function() {
    'use strict';

    function getCurrentPackage() {
        const pathname = window.location.pathname;
        // Match new pattern like /api/haive/core/engine/base.html
        let match = pathname.match(/\/api\/haive\/([^\/]+)\//);
        if (match) {
            return match[1]; // Returns 'core', 'agents', etc.
        }
        // Fallback for generated paths
        match = pathname.match(/\/api\/generated\/(haive\.([^\.]+))/);
        return match ? match[2] : null;
    }

    function enhanceNavigation() {
        const currentPackage = getCurrentPackage();
        if (!currentPackage) return;

        // Collapse other packages, expand current package
        collapseOtherPackages(currentPackage);
        
        // Add visual indicators
        highlightCurrentPackage(currentPackage);
        
        // Add breadcrumb navigation
        addBreadcrumb(currentPackage);
    }

    function collapseOtherPackages(currentPackage) {
        // Map package names to their titles in new structure
        const packageMap = {
            'agents': 'Agents',
            'core': 'Core',
            'tools': 'Tools',
            'games': 'Games',
            'dataflow': 'Dataflow',
            'prebuilt': 'Prebuilt',
            'mcp': 'MCP'
        };

        // Find all package sections
        Object.entries(packageMap).forEach(([pkg, title]) => {
            const links = document.querySelectorAll('a.reference.internal');
            for (const link of links) {
                // Look for new structure pattern
                if ((link.textContent === `Haive ${title}` || link.textContent === title) && 
                    link.href.includes(`/haive/${pkg}/`)) {
                    const section = link.closest('li.has-children');
                    if (section) {
                        const checkbox = section.querySelector('input[type="checkbox"]');
                        if (checkbox) {
                            // Expand current package, collapse others
                            checkbox.checked = (pkg === currentPackage);
                        }
                    }
                    break;
                }
            }
        });
    }

    function highlightCurrentPackage(currentPackage) {
        const style = document.createElement('style');
        style.textContent = `
            /* Highlight current package section */
            .sidebar-tree .toctree-l2.current > a {
                font-weight: 600;
                color: var(--color-brand-primary);
            }
            
            /* Dim other package sections */
            .sidebar-tree .toctree-l2:not(.current) > a {
                opacity: 0.7;
            }
            
            /* Show current module prominently */
            .sidebar-tree .current-page > a {
                background-color: var(--color-api-background-hover);
                border-left: 3px solid var(--color-brand-primary);
                margin-left: -3px;
            }
        `;
        document.head.appendChild(style);
    }

    function addBreadcrumb(currentPackage) {
        const mainContent = document.querySelector('#furo-main-content');
        if (!mainContent) return;

        const breadcrumb = document.createElement('nav');
        breadcrumb.className = 'module-breadcrumb';
        breadcrumb.innerHTML = `
            <a href="../../index.html">API Reference</a>
            <span class="separator">›</span>
            <a href="../../haive/index.html">Haive</a>
            <span class="separator">›</span>
            <a href="../index.html">${capitalize(currentPackage)}</a>
            <span class="separator">›</span>
            <span class="current">${getCurrentModuleName()}</span>
        `;

        // Insert breadcrumb at the top of content
        mainContent.insertBefore(breadcrumb, mainContent.firstChild);

        // Add breadcrumb styles
        const style = document.createElement('style');
        style.textContent = `
            .module-breadcrumb {
                padding: 0.5rem 0;
                margin-bottom: 1rem;
                font-size: 0.875rem;
                color: var(--color-foreground-secondary);
                border-bottom: 1px solid var(--color-sidebar-background-border);
            }
            
            .module-breadcrumb a {
                color: var(--color-brand-primary);
                text-decoration: none;
            }
            
            .module-breadcrumb a:hover {
                text-decoration: underline;
            }
            
            .module-breadcrumb .separator {
                margin: 0 0.5rem;
                opacity: 0.5;
            }
            
            .module-breadcrumb .current {
                font-weight: 500;
                color: var(--color-foreground-primary);
            }
        `;
        document.head.appendChild(style);
    }

    function getCurrentModuleName() {
        const title = document.querySelector('h1');
        return title ? title.textContent : 'Module';
    }

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    function init() {
        // Only run on API module pages
        if (!window.location.pathname.includes('/api/haive/') && 
            !window.location.pathname.includes('/api/generated/')) {
            return;
        }

        enhanceNavigation();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();