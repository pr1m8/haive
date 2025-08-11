"""Safe wrapper for viewcode extension that handles file access errors."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_viewcode_safe(app):
    """Setup viewcode with comprehensive error handling."""
    
    # Monkey-patch the problematic part of viewcode
    import sphinx.ext.viewcode as viewcode
    
    # Store original functions
    _original_get_module_filename = viewcode.get_module_filename if hasattr(viewcode, 'get_module_filename') else None
    _original_collect_pages = viewcode.collect_pages
    
    # Create a safer version of collect_pages
    def safe_collect_pages(app):
        """Safe version of collect_pages that handles all file errors."""
        try:
            for item in _original_collect_pages(app):
                yield item
        except IndexError as e:
            logger.warning(f"viewcode: Skipping file due to IndexError: {e}")
            # Continue without yielding anything for this file
        except Exception as e:
            logger.error(f"viewcode: Unexpected error in collect_pages: {e}")
            # Continue processing other files
    
    # Replace the function
    viewcode.collect_pages = safe_collect_pages
    
    # Also patch the file reading if needed
    if hasattr(viewcode, '_read_file'):
        _original_read_file = viewcode._read_file
        
        def safe_read_file(filename):
            """Safe file reading that checks file validity first."""
            try:
                path = Path(filename)
                if not path.exists():
                    logger.warning(f"viewcode: File not found: {filename}")
                    return []
                
                # Check if file has enough content
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) < 3:  # Files with too few lines cause issues
                        logger.warning(f"viewcode: File too short ({len(lines)} lines): {filename}")
                        return []
                    return lines
            except Exception as e:
                logger.warning(f"viewcode: Error reading file {filename}: {e}")
                return []
        
        viewcode._read_file = safe_read_file
    
    logger.info("✅ viewcode safety patches applied")


def should_skip_module(module_name):
    """Check if a module should be skipped by viewcode."""
    # List of patterns that cause issues
    problematic_patterns = [
        'prompts.py',
        'base/state.py',
        'base/engines.py',
        'base/state_manager.py', 
        'base/models.py',
        'base/player.py',
        'testing/base.py',
    ]
    
    for pattern in problematic_patterns:
        if module_name.endswith(pattern):
            return True
    
    return False