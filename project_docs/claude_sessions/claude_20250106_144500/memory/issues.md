# Issues Encountered and Solutions

## Issue: Autosummary Module Misdetection
**Root Cause**: Autosummary with `:recursive:` flag treats `haive.core.engine` as an attribute of `haive.core` instead of recognizing it as a standalone module.

**Symptoms**:
- Generated files contained `.. autodata:: engine` 
- URLs like `/api/generated/haive.core.persistence.html` showed minimal content
- No classes, functions, or submodules displayed
- Only stub documentation visible

**Debug Process**:
1. Confirmed modules are importable: ✅ `import haive.core.engine` works
2. Confirmed modules have content: ✅ `dir(haive.core.engine)` shows classes
3. Tested manual `automodule`: ✅ Shows full documentation
4. Identified autosummary as the problem

**Solution**: Replace autosummary with manual `automodule` directives
- **Implementation**: Create manual module pages in `/api/modules/`
- **Result**: Full module documentation with all classes and functions
- **Verification**: Manual pages show complete content

## Issue: Gallery Links Pointing to Broken Pages
**Root Cause**: Gallery cards were linking to autosummary-generated pages that had minimal content.

**Solution**: Update gallery links to point to manual module pages
- **Before**: `:link: generated/haive.core.engine`
- **After**: `:link: modules/haive.core.engine`

## Issue: Template Not Applied Correctly
**Root Cause**: Even with enhanced template, autosummary was not using `automodule` directive.

**Investigation**: Template was correct, but autosummary object detection was wrong
**Solution**: Bypass autosummary entirely with manual approach

## Performance Notes
- Manual `automodule` directives build quickly
- No import errors or dependency issues
- Documentation shows immediately in build output
- Scales well to additional modules