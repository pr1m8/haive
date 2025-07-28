# Implementation Plan - Documentation Fix

**Created**: 2025-01-27
**Based on**: Analysis of current issues and docs/fix-documentation-20250121 branch

## Executive Summary

We have:

- 6,802 errors in current build
- 2,407 warnings
- Only 13 HTML files generated
- CSS layout issues (sidebar too wide)
- A previous attempt (docs branch) that made progress but still has issues

## Recommended Implementation Order

### Week 1: Foundation

#### Day 1: Setup and Baseline

1. **Create working branch**

   ```bash
   git checkout -b docs/incremental-fix-2025
   ```

2. **Implement Phase 1**
   - Use [PHASE_1_MINIMAL.md](./PHASE_1_MINIMAL.md)
   - Get baseline metrics
   - Verify Furo works correctly

3. **Document baseline**
   - Update [PROGRESS_LOG.md](./PROGRESS_LOG.md)
   - Screenshot clean layout
   - Record build time

#### Day 2: Core Package

1. **Implement Phase 2**
   - Add haive-core only
   - Use ignore patterns from docs branch
   - Fix import issues

2. **Track errors**
   - Use [ERROR_PATTERNS.md](./ERROR_PATTERNS.md)
   - Document new patterns
   - Update ignore list

#### Day 3: Fix Core Issues

1. **Resolve remaining core errors**
   - Target < 100 errors
   - Fix critical imports
   - Update [COMMON_FIXES.md](./COMMON_FIXES.md)

### Week 2: Scale Up

#### Day 4: Add Agents Package

1. **Copy ignore patterns from docs branch**
   - Especially supervisor directory
   - Problem files identified

2. **Test incremental build**
   - Monitor error count
   - Adjust ignores as needed

#### Day 5: CSS and Layout

1. **Implement CSS fixes**
   - Use single CSS file
   - Follow [CSS_ISSUES.md](./CSS_ISSUES.md)
   - Test responsive design

#### Day 6-7: Remaining Packages

1. **Add packages one by one**
   - haive-tools
   - haive-games
   - haive-dataflow
   - haive-mcp

2. **Fix package-specific issues**
   - Update ignore patterns
   - Document in [PROGRESS_LOG.md](./PROGRESS_LOG.md)

### Week 3: Polish

1. **Optimize build**
   - Enable caching
   - Parallel builds
   - Reduce warnings to < 100

2. **Documentation**
   - Update all guides
   - Create troubleshooting guide
   - Document final configuration

## Key Files to Create/Modify

### Configuration Files

1. `docs/source/conf_incremental.py` - Our clean configuration
2. `docs/source/_static/furo-haive.css` - Minimal CSS
3. `docs/source/_templates/autoapi/` - If needed for path fixes

### Documentation

1. Update this entire `documentation_fix/` directory
2. Create `TROUBLESHOOTING.md` with solutions
3. Update main project documentation

## Success Metrics

### Phase Targets

| Phase   | Errors | Warnings | HTML Files | Build Time |
| ------- | ------ | -------- | ---------- | ---------- |
| Current | 6,802  | 2,407    | 13         | ?          |
| Phase 1 | 0      | <10      | 5          | <10s       |
| Phase 2 | <500   | <200     | 50+        | <30s       |
| Phase 3 | <100   | <500     | 200+       | <60s       |
| Phase 4 | <50    | <300     | 400+       | <90s       |
| Final   | 0      | <100     | 500+       | <120s      |

## Risk Mitigation

1. **Backup Strategy**
   - Commit after each successful phase
   - Tag working configurations
   - Keep rollback points

2. **Testing Protocol**
   - Build after each change
   - Visual inspection of output
   - Check cross-references work

3. **Communication**
   - Update team on progress
   - Document blockers immediately
   - Share lessons learned

## Tools and Commands

### Build Commands

```bash
# Clean build
rm -rf docs/build && sphinx-build -b html docs/source docs/build/html

# Verbose build
sphinx-build -vvv -b html docs/source docs/build/html 2>&1 | tee build.log

# Check errors
grep -c "ERROR\|WARNING" build.log
```

### Analysis Commands

```bash
# Find problem files
grep "Failed to import" build.log | sort | uniq -c | sort -nr

# Check HTML output
find docs/build/html -name "*.html" | wc -l

# Test imports
python -c "import sys; sys.path.insert(0, 'packages/haive-core/src'); from haive.core import *"
```

## Next Immediate Steps

1. **Review all documentation in this directory**
2. **Get approval for implementation plan**
3. **Create working branch**
4. **Start Phase 1**

## References

- [BUILD_ANALYSIS.md](./BUILD_ANALYSIS.md) - Current state analysis
- [BUILD_STRATEGY.md](./BUILD_STRATEGY.md) - Incremental approach
- [AUTOAPI_STRATEGY.md](./AUTOAPI_STRATEGY.md) - Namespace package handling
- [CSS_ISSUES.md](./CSS_ISSUES.md) - Layout fixes
- [DOCS_BRANCH_ANALYSIS.md](./DOCS_BRANCH_ANALYSIS.md) - Lessons from previous attempt
- [ERROR_PATTERNS.md](./ERROR_PATTERNS.md) - Common issues
- [COMMON_FIXES.md](./COMMON_FIXES.md) - Quick solutions
