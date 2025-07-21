# Priority 1: Import Format Fixes

**Status**: Ready for Implementation  
**Assigned**: Available for immediate work  
**Target**: Complete within 1 day  

## Immediate Action Required

Fix 5 files with invalid import format: `from haive-prebuilt.src.haive.prebuilt.module`

## Quick Fix Command

```bash
# Navigate to project root
cd /home/will/Projects/haive/backend/haive

# Fix invalid import patterns
find packages/haive-prebuilt -name "*.py" -exec sed -i 's/from haive-prebuilt\.src\.haive/from haive/g' {} \;

# Verify fixes
poetry run python -c "
import py_compile
files = [
    'packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py',
    'packages/haive-prebuilt/src/haive/prebuilt/tldr2/engines.py', 
    'packages/haive-prebuilt/src/haive/prebuilt/tldr2/agent.py'
]
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print(f'✅ {f}')
    except:
        print(f'❌ {f}')
"
```

## Expected Result

All 5 files should compile successfully, reducing total compilation errors from 59 to 54.

## Next Priority

After completing this fix, move to [URLs in Code fixes](../by_date/2025-01-21/urls_in_code_syntax_errors.md).