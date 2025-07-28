# TODO List - Documentation Improvements

**Date**: 2025-07-27
**Purpose**: Consolidated action items from documentation analysis
**Priority**: Continue improving documentation coverage

## 🚀 **HIGH PRIORITY TODOs**

### 1. **Update Ignore Patterns for CLI Documentation** ⭐⭐⭐

- **Task**: Make ignore patterns more specific to allow valuable CLIs
- **Files to Document**:
  - `packages/haive-mcp/src/haive/mcp/cli.py` - MCP server management
  - `packages/haive-agents/src/haive/agents/research/open_perplexity/cli.py` - Research automation
- **Implementation**:

  ```python
  # Current (too broad):
  "**/cli.py",

  # Change to (more specific):
  "**/test*/cli.py",
  "**/debug*/cli.py",
  "**/example*/cli.py",
  ```

- **Impact**: Essential user-facing CLI documentation

### 2. **Add Sphinx-Gallery Configuration** ⭐⭐⭐

- **Task**: Configure sphinx-gallery for excellent examples
- **Add to conf.py**:
  ```python
  sphinx_gallery_conf = {
      'examples_dirs': '../packages/haive-agents/examples',
      'gallery_dirs': 'auto_examples/agents',
      'filename_pattern': '/.*_example\.py$',
      'ignore_pattern': r'__init__\.py|test_.*\.py',
      'download_all_examples': False,
      'plot_gallery': True,
      'abort_on_example_error': False,
      'run_stale_examples': False,
  }
  ```
- **Impact**: 30+ high-quality examples with visual output

### 3. **Fix CSS Issues** ⭐⭐⭐

- **Task**: Fix code blocks and right-pushed formatting
- **Current Issue**: CSS causing layout problems
- **Files**: Check `_static/` CSS customizations
- **Impact**: Better documentation readability

## 📝 **MEDIUM PRIORITY TODOs**

### 4. **Test Selective File Inclusion**

- **Task**: Remove specific files from ignore list one by one
- **Process**:
  1. Remove one file pattern from autoapi_ignore
  2. Test build for errors
  3. Evaluate documentation quality
  4. Repeat for high-value files
- **Candidates**: Entry point main.py files for deployment docs

### 5. **Complete HTML Build Verification**

- **Task**: Verify final HTML output once build completes
- **Check**:
  - HTML file count
  - Navigation structure
  - Cross-references working
  - Search functionality
- **Next**: Deploy to test server for review

### 6. **Test Documentation Screenshots**

- **Task**: Run playwright screenshot script
- **Purpose**: Verify visual documentation quality
- **Script**: Check for existing screenshot automation

## 🔧 **LOW PRIORITY TODOs**

### 7. **Fix Additional Sphinx Extensions**

- **Task**: Review sphinx_tabs and other extension configurations
- **Current**: Some extensions may need configuration
- **Impact**: Enhanced documentation features

### 8. **Review 'Unknown type: placeholder' Warnings**

- **Task**: Investigate and fix type annotation warnings
- **Count**: Multiple warnings in build output
- **Impact**: Cleaner build output

## 📊 **Implementation Strategy**

### Phase 1: Quick Wins (Do First)

1. ✅ Fix sphinx-gallery import (DONE)
2. Update CLI ignore patterns
3. Add basic sphinx-gallery config
4. Test build with changes

### Phase 2: Enhanced Coverage (Do Next)

1. Remove examples from ignore list selectively
2. Test more main.py files for documentation
3. Fix CSS issues for better appearance
4. Verify HTML build completeness

### Phase 3: Polish (Do Later)

1. Configure additional extensions
2. Fix type annotation warnings
3. Optimize build performance
4. Add custom styling

## 🎯 **Expected Outcomes**

### Documentation Coverage

- **Current**: 1,877 RST files (core functionality)
- **After CLIs**: +2 essential user interfaces
- **After Examples**: +30-50 executable examples
- **After Main.py**: +5-10 deployment guides
- **Total Potential**: 1,900+ documented items

### User Experience

- **CLI Documentation**: Clear command-line usage
- **Example Gallery**: Visual learning with code + output
- **Deployment Guides**: Server setup documentation
- **Complete Coverage**: Minimal documentation gaps

## 🔗 **Reference Documents**

### Analysis Files

- `project_docs/documentation_fix/CLI_FILES_AUDIT.md` - CLI analysis
- `project_docs/documentation_fix/EXAMPLES_SPHINX_GALLERY_ANALYSIS.md` - Examples analysis
- `project_docs/documentation_fix/IGNORED_FILES_ANALYSIS.md` - Complete ignore analysis
- `project_docs/documentation_fix/SPHINX_GALLERY_ISSUE.md` - Extension fix guide

### Configuration

- `docs/source/conf.py` - Current configuration to update
- `project_docs/documentation_fix/AUTOAPI_RESOLUTION.md` - Technical solutions

## 📅 **Suggested Timeline**

### Immediate (Today/Tomorrow)

- Update ignore patterns for CLIs
- Add sphinx-gallery configuration
- Test build with changes

### Short Term (This Week)

- Fix CSS issues
- Complete HTML build verification
- Test selective file inclusion

### Medium Term (Next Week)

- Polish documentation appearance
- Fix remaining warnings
- Deploy updated documentation

## ✅ **Success Criteria**

1. **MCP CLI documented** - Users can find CLI usage
2. **Research CLI documented** - Research workflows clear
3. **Example gallery working** - Visual examples available
4. **CSS issues fixed** - Professional appearance
5. **Build clean** - Minimal warnings
6. **HTML complete** - Full navigation working

---

**Next Action**: Update conf.py ignore patterns to be more specific for CLI files
