# 🚨 URGENT: Documentation Source Directory Cleanup Plan

**Current State**: **DISASTER** - 612MB, 4,482 files
**Target State**: ~50MB, <200 files (clean source-only documentation)

## 📊 Current Problem Analysis

```bash
Size Breakdown:
- logs/              521MB  (!!!) - Giant debug logs
- reference/         28MB   - Generated API content
- api/               26MB   - Generated API content  
- examples/          24MB   - Generated notebooks/zips
- auto_examples/     8.7MB  - Generated examples
- Other              4.3MB  - Source content

File Count Breakdown:
- 331 Jupyter notebooks (.ipynb)
- 373 zip files (generated downloads)
- 97 Python files (belong in packages/)
- 21 log files (debug artifacts)
- Multiple CSS/JS backups and duplicates
```

## 🎯 Cleanup Strategy

### Phase 1: Emergency Cleanup (IMMEDIATE)
```bash
# Remove the 541MB debug log
rm docs/source/logs/autoapi_debug.log

# Remove all generated content
rm -rf docs/source/logs/
rm -rf docs/source/auto_examples/
rm -rf docs/source/examples/
rm -rf docs/source/reference/
rm -rf docs/source/generated/
rm -rf docs/source/discovered_readmes/

# Remove backup directories
rm -rf docs/source/_static/backup/
rm -rf docs/source/_static/backup_cleanup/
rm -rf docs/source/_static/archive/

# Remove vault logs and other debug files
rm docs/source/vault_cli_*.log
rm docs/source/poker_game.log
rm docs/source/dynamic_graph.log
```

### Phase 2: Clean Source Structure
```
docs/source/
├── index.rst                 # Main index
├── conf.py                   # Single config file
├── _static/                  # Static assets (cleaned)
│   ├── enhanced-docs.css     # Main styles
│   ├── custom.js            # Main scripts
│   └── images/              # Essential images only
├── _templates/              # RST templates (cleaned)
│   ├── autoapi/            # AutoAPI templates
│   └── autosummary/        # Autosummary templates
├── agents/                  # Agent documentation
│   ├── index.rst
│   └── demos/              # Demo RST files only
├── games/                   # Game documentation  
├── tools/                   # Tool documentation
├── guides/                  # User guides
├── mcp/                     # MCP documentation
└── conf_modules/           # Modular config (if kept)
```

### Phase 3: Move Generated Content (Build Time)
```
docs/build/                  # All generated content goes here
├── html/                   # Built HTML
├── api/                    # Generated API docs
├── examples/               # Generated examples
└── _static/               # Compiled static assets
```

## 🚀 Implementation Plan

### Step 1: Backup Current State
```bash
# Create backup of current source (just in case)
cp -r docs/source docs/source_backup_disaster_$(date +%Y%m%d)
```

### Step 2: Nuclear Cleanup
```bash
# Remove all generated/temporary content
find docs/source -name "*.log" -delete
find docs/source -name "*.ipynb" -delete  
find docs/source -name "*.zip" -delete
find docs/source -name "*.py" -not -path "*/conf_modules/*" -not -name "conf*.py" -delete
rm -rf docs/source/logs/
rm -rf docs/source/auto_examples/
rm -rf docs/source/examples/
rm -rf docs/source/reference/  
rm -rf docs/source/generated/
rm -rf docs/source/discovered_readmes/
rm -rf docs/source/_static/backup*/
```

### Step 3: Clean Static Assets
```bash
# Keep only essential CSS/JS
cd docs/source/_static/
find . -name "*.css" -not -name "enhanced-docs.css" -delete
find . -name "*.js" -not -name "custom.js" -not -name "*toc*" -delete
```

### Step 4: Update .gitignore
```gitignore
# Generated documentation content
docs/build/
docs/source/auto_examples/
docs/source/examples/
docs/source/reference/
docs/source/generated/
docs/source/logs/
docs/source/_static/backup*/
docs/source/vault_cli_*.log
docs/source/*.log

# Generated files
docs/source/**/*.ipynb
docs/source/**/*.zip
!docs/source/conf_modules/
```

### Step 5: Fix Build Process
- Configure AutoAPI to generate into docs/build/api/ not docs/source/api/
- Configure examples to generate into docs/build/examples/
- Move all logs to docs/build/logs/
- Clean conf.py to use build directory for generated content

## 📈 Expected Results

**Before**: 612MB, 4,482 files
**After**: ~50MB, <200 files  

**Build Impact**:
- Faster builds (no processing thousands of generated files)
- Cleaner git history (no generated content commits)
- Easier navigation and maintenance
- Proper separation of source vs build artifacts

## ⚠️ Risks

1. **Lost customizations**: Some generated examples might have manual edits
2. **Broken links**: Internal links to generated content need updating
3. **Build script changes**: Need to update AutoAPI and example generation configs

## 🎯 Success Criteria

- [ ] Source directory under 100MB
- [ ] Less than 500 files in source
- [ ] All generated content in build/ directory
- [ ] Documentation builds successfully
- [ ] All links work correctly
- [ ] Git repository size reduced significantly

---

**RECOMMENDATION**: Execute Phase 1 (Emergency Cleanup) immediately to remove the 541MB log file and get the repository back to a reasonable size.