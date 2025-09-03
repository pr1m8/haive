# Issues Organization - Haive Framework

**Purpose**: Comprehensive organization of all identified issues by subject matter and date
**Created**: 2025-07-21
**Status**: Manual organization only - NO automated fixes applied

## 🚨 CRITICAL WARNING

**NEVER USE comprehensive_dev_fix.py** - This type of automated fixing script caused the July 20 disaster that broke the entire codebase.

## 📂 Organization Structure

Issues are organized by:

1. **Subject Matter** (primary categorization)
2. **Date** (secondary organization within each subject)

### Subject Categories

- **`compilation/`** - Syntax errors, import errors, pycompile failures
- **`documentation/`** - Missing docstrings, type hints, documentation issues
- **`architecture/`** - Design issues, schema problems, pattern violations
- **`testing/`** - Test failures, coverage issues, testing patterns
- **`imports/`** - Import path issues, circular imports, module structure
- **`infrastructure/`** - Build issues, CI/CD, environment problems

### Date Organization

Within each subject, issues are organized by date:

- **`2025-07-20/`** - Issues from the parse error disaster
- **`2025-07-21/`** - Issues identified in recovery analysis
- **`ongoing/`** - Long-term architectural issues

## 🎯 Current Priority

**Phase 1**: Fix 59 compilation errors identified in 2025-07-21 analysis

- Focus on haive-prebuilt (31 files) and haive-agents (26 files)
- Manual fixes only, no automation
- Test each fix individually

## 📋 Issue References

All issues reference back to source analysis:

- `/tmp/pycompile_errors.log` - Detailed compilation errors
- `/tmp/documentation_audit.log` - Documentation issues
- `RECOVERY_PLAN.md` - Overall recovery strategy
- Memory index entries for specific problem types

---

**Safety Protocol**: All fixes must be manual and tested individually. NO automated scripts.
