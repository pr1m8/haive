"""Monkey patch for viewcode to fix IndexError on line 331."""

import logging

logger = logging.getLogger(__name__)


def apply_viewcode_monkey_patch():
    """Apply monkey patch to viewcode.collect_pages to handle IndexError."""
    try:
        from sphinx.ext import viewcode
        
        # Store the original function
        _original_collect_pages = viewcode.collect_pages
        
        def patched_collect_pages(app):
            """Patched collect_pages that wraps the generator to catch IndexError."""
            # We need to catch the error in the specific place where it occurs
            # The error happens when viewcode tries to access lines[start]
            
            env = app.builder.env
            if not hasattr(env, '_viewcode_modules'):
                return
                
            # Get the modules
            modules = env._viewcode_modules
            
            # Filter out modules that might cause issues
            safe_modules = {}
            for modname, entry in modules.items():
                try:
                    # Check if this module has problematic characteristics
                    if entry and len(entry) > 1:
                        analyzer = entry[1]
                        if analyzer and hasattr(analyzer, 'code') and analyzer.code:
                            # Check if code has at least a few lines
                            lines = analyzer.code.splitlines()
                            if len(lines) > 2:  # Need at least 3 lines to be safe
                                safe_modules[modname] = entry
                            else:
                                logger.warning(f"Skipping module with too few lines: {modname}")
                        else:
                            safe_modules[modname] = entry
                    else:
                        safe_modules[modname] = entry
                except Exception as e:
                    logger.warning(f"Error checking module {modname}: {e}")
                    # Skip problematic modules
                    continue
            
            # Temporarily replace the modules
            original_modules = env._viewcode_modules
            env._viewcode_modules = safe_modules
            
            try:
                # Call the original function with filtered modules
                yield from _original_collect_pages(app)
            finally:
                # Restore original modules
                env._viewcode_modules = original_modules
        
        # Replace the function
        viewcode.collect_pages = patched_collect_pages
        logger.info("✅ Applied viewcode IndexError monkey patch")
        
    except Exception as e:
        logger.error(f"Failed to apply viewcode patch: {e}")
        raise