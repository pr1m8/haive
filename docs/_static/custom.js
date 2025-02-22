// Custom JavaScript for Haive documentation

// Add copy buttons to code blocks
document.addEventListener('DOMContentLoaded', function() {
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach(function(codeBlock) {
        if (!codeBlock.querySelector('.copybutton')) {
            const button = document.createElement('button');
            button.className = 'copybutton';
            button.textContent = 'Copy';
            
            button.addEventListener('click', function() {
                const code = codeBlock.querySelector('code') ? 
                    codeBlock.querySelector('code').textContent :
                    codeBlock.textContent;
                
                navigator.clipboard.writeText(code.trim()).then(function() {
                    button.textContent = 'Copied!';
                    setTimeout(function() {
                        button.textContent = 'Copy';
                    }, 2000);
                }, function() {
                    button.textContent = 'Error!';
                });
            });
            
            codeBlock.appendChild(button);
        }
    });
});

// Add collapsible sections
document.addEventListener('DOMContentLoaded', function() {
    const collapsibleSections = document.querySelectorAll('.collapsible');
    
    collapsibleSections.forEach(function(section) {
        const header = section.querySelector('h2, h3, h4, h5, h6');
        if (header) {
            header.style.cursor = 'pointer';
            const content = document.createElement('div');
            content.className = 'collapsible-content';
            
            // Move all content after the header into the collapsible div
            let nextElement = header.nextElementSibling;
            while (nextElement) {
                const temp = nextElement.nextElementSibling;
                content.appendChild(nextElement);
                nextElement = temp;
            }
            
            section.appendChild(content);
            
            // Add click handler to toggle visibility
            header.addEventListener('click', function() {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
            });
        }
    });
});
