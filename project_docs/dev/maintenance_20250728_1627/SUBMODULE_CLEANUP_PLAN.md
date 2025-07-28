# Submodule-Aware Cleanup Plan

**Date**: 2025-07-28 16:30  
**Purpose**: Package-by-package cleanup respecting git submodule structure  
**Approach**: Individual commits per submodule + root coordination commits

## 🎯 **SUBMODULE STRATEGY**

Since each package is a git submodule, we need to:
1. **Work inside each submodule directory**
2. **Commit changes within that submodule's git context**  
3. **Update parent repo with submodule reference updates**
4. **Coordinate between related submodules systematically**

---

## 📦 **PACKAGE-BY-PACKAGE EXECUTION**

### **Phase 1: haive-core (Foundation First)**

**Why First**: Core package, other packages depend on it

```bash
# Enter haive-core submodule
cd packages/haive-core/

# Check current state
git status && git diff
pwd  # Confirm: /packages/haive-core

# Create cleanup branch IN SUBMODULE
git checkout -b cleanup/organizational-fixes-20250728

# CLEANUP TASKS for haive-core:
# 1. Move project_docs content to root
mkdir -p ../../project_docs/haive-core/
mv project_docs/* ../../project_docs/haive-core/
rmdir project_docs/

# 2. Move misplaced tests from root to haive-core/tests/
cd ../../  # Back to root
mv test_*core*.py packages/haive-core/tests/ 2>/dev/null || true
mv test_*engine*.py packages/haive-core/tests/ 2>/dev/null || true
mv test_*graph*.py packages/haive-core/tests/ 2>/dev/null || true
mv test_*schema*.py packages/haive-core/tests/ 2>/dev/null || true

# 3. Back to haive-core submodule for commit
cd packages/haive-core/

# COMMIT IN SUBMODULE
git add .
git status  # Review changes
git commit -m "cleanup: organize haive-core project structure

- Moved project_docs content to root project_docs/haive-core/
- Relocated core-related tests from root to tests/
- Removed duplicate project_docs directory
- Maintains functionality while improving organization

Ref: maintenance_20250728_1627"

# Push submodule changes
git push -u origin cleanup/organizational-fixes-20250728

# Back to root to update submodule reference
cd ../../
git add packages/haive-core
git commit -m "update: haive-core submodule ref for organizational cleanup"
```

### **Phase 2: haive-agents (Major Cleanup)**

**Why Second**: Largest package with most scattered content

```bash
# Enter haive-agents submodule  
cd packages/haive-agents/

# Check current state
git status && git diff
pwd  # Confirm: /packages/haive-agents

# Create cleanup branch IN SUBMODULE
git checkout -b cleanup/organizational-fixes-20250728

# CLEANUP TASKS for haive-agents:
# 1. Move project_docs content to root
mkdir -p ../../project_docs/haive-agents/
mv project_docs/* ../../project_docs/haive-agents/
rmdir project_docs/

# 2. Move agent-related tests from root
cd ../../  # Back to root
mv test_*agent*.py packages/haive-agents/tests/ 2>/dev/null || true
mv test_*multi*.py packages/haive-agents/tests/ 2>/dev/null || true
mv test_*react*.py packages/haive-agents/tests/ 2>/dev/null || true
mv test_*simple*.py packages/haive-agents/tests/ 2>/dev/null || true
mv test_*enhanced*.py packages/haive-agents/tests/ 2>/dev/null || true
mv test_*supervisor*.py packages/haive-agents/tests/ 2>/dev/null || true
mv test_*coordination*.py packages/haive-agents/tests/ 2>/dev/null || true

# 3. Move agent-related examples to examples/
mkdir -p examples/agents/
mv *agent*.py examples/agents/ 2>/dev/null || true
mv *multi_agent*.py examples/agents/ 2>/dev/null || true
mv business_multi_agent_workflows.py examples/agents/ 2>/dev/null || true
mv complex_multi_agent_workflows.py examples/agents/ 2>/dev/null || true
mv advanced_multi_agent_patterns.py examples/agents/ 2>/dev/null || true

# 4. Back to haive-agents submodule for commit
cd packages/haive-agents/

# COMMIT IN SUBMODULE
git add .
git status  # Review changes
git commit -m "cleanup: organize haive-agents project structure

- Moved project_docs content to root project_docs/haive-agents/
- Relocated agent-related tests from root to tests/
- Moved agent examples to root examples/agents/
- Removed duplicate project_docs directory
- Consolidated scattered agent-related files

Ref: maintenance_20250728_1627"

# Push submodule changes
git push -u origin cleanup/organizational-fixes-20250728

# Back to root to update submodule reference
cd ../../
git add packages/haive-agents examples/
git commit -m "update: haive-agents submodule ref + examples reorganization"
```

### **Phase 3: haive-tools (Tools & Scripts)**

```bash
# Enter haive-tools submodule
cd packages/haive-tools/

# Create cleanup branch IN SUBMODULE
git checkout -b cleanup/organizational-fixes-20250728

# CLEANUP TASKS for haive-tools:
# 1. Move tool-related tests from root
cd ../../  # Back to root
mv test_*tool*.py packages/haive-tools/tests/ 2>/dev/null || true
mv test_*validation*.py packages/haive-tools/tests/ 2>/dev/null || true

# 2. Move tool examples
mkdir -p examples/tools/
mv *tool*.py examples/tools/ 2>/dev/null || true
mv enhanced_tool_management_demo.py examples/tools/ 2>/dev/null || true

# 3. Back to haive-tools submodule for commit
cd packages/haive-tools/

# COMMIT IN SUBMODULE
git add .
git commit -m "cleanup: organize haive-tools project structure

- Relocated tool-related tests from root to tests/
- Moved tool examples to root examples/tools/
- Consolidated scattered tool-related files

Ref: maintenance_20250728_1627"

# Push and update parent
git push -u origin cleanup/organizational-fixes-20250728
cd ../../
git add packages/haive-tools examples/
git commit -m "update: haive-tools submodule ref + tools examples"
```

### **Phase 4: haive-games**

```bash
# Enter haive-games submodule
cd packages/haive-games/

# Create cleanup branch IN SUBMODULE  
git checkout -b cleanup/organizational-fixes-20250728

# CLEANUP TASKS for haive-games:
# Move game-related content
cd ../../  # Back to root
mv test_*game*.py packages/haive-games/tests/ 2>/dev/null || true
mv *game*.py examples/games/ 2>/dev/null || true

# Back to submodule and commit
cd packages/haive-games/
git add .
git commit -m "cleanup: organize haive-games project structure

- Relocated game-related tests and examples
- Consolidated scattered game files

Ref: maintenance_20250728_1627"

git push -u origin cleanup/organizational-fixes-20250728
cd ../../
git add packages/haive-games examples/
git commit -m "update: haive-games submodule ref + games examples"
```

### **Phase 5: haive-mcp & haive-prebuilt**

```bash
# haive-mcp
cd packages/haive-mcp/
git checkout -b cleanup/organizational-fixes-20250728
cd ../../
mv test_*mcp*.py packages/haive-mcp/tests/ 2>/dev/null || true
cd packages/haive-mcp/
git add . && git commit -m "cleanup: organize haive-mcp structure"
git push -u origin cleanup/organizational-fixes-20250728

# haive-prebuilt  
cd ../haive-prebuilt/
git checkout -b cleanup/organizational-fixes-20250728
cd ../../
mv test_*prebuilt*.py packages/haive-prebuilt/tests/ 2>/dev/null || true
cd packages/haive-prebuilt/
git add . && git commit -m "cleanup: organize haive-prebuilt structure"
git push -u origin cleanup/organizational-fixes-20250728

# Update parent
cd ../../
git add packages/haive-mcp packages/haive-prebuilt
git commit -m "update: haive-mcp and haive-prebuilt submodule refs"
```

---

## 🧹 **ROOT DIRECTORY FINAL CLEANUP**

After all packages are cleaned, tackle root-only issues:

```bash
# ROOT CLEANUP (not in any submodule)
cd /home/will/Projects/haive/backend/haive

# Create root cleanup branch
git checkout -b cleanup/root-organization-20250728

# 1. Archive all analysis reports
mkdir -p project_docs/archive/reports/
mv AGENTS_ANALYSIS_REPORT.md project_docs/archive/reports/
mv CORE_ANALYSIS_REPORT.md project_docs/archive/reports/
mv POSTGRES_*.md project_docs/archive/reports/
mv SYNTAX_*.md project_docs/archive/reports/
mv MULTIAGENT_*.md project_docs/archive/reports/
mv ENHANCED_*.md project_docs/archive/reports/
mv STRUCTURED_*.md project_docs/archive/reports/
mv MEMORY_*.md project_docs/archive/reports/
mv TRUNK_*.md project_docs/archive/reports/
mv COMPREHENSIVE_*.md project_docs/archive/reports/
mv FOCUSED_*.md project_docs/archive/reports/
mv REMAINING_*.md project_docs/archive/reports/

# 2. Archive temp/debug files
mkdir -p project_docs/dev/temp/
mv agent_1_*.py project_docs/dev/temp/
mv agent_2_*.py project_docs/dev/temp/
mv batch_*.py project_docs/dev/temp/
mv categorize_*.py project_docs/dev/temp/
mv check_*.py project_docs/dev/temp/
mv debug_*.py project_docs/dev/temp/
mv final_*.py project_docs/dev/temp/
mv fix_*.py project_docs/dev/temp/
mv rescan_*.py project_docs/dev/temp/
mv scan_*.py project_docs/dev/temp/
mv split_*.py project_docs/dev/temp/

# 3. Archive temp data files
mkdir -p project_docs/dev/data/
mv *.json project_docs/dev/data/ 2>/dev/null || true
mv *.txt project_docs/dev/data/ 2>/dev/null || true
mv *.csv project_docs/dev/data/ 2>/dev/null || true

# 4. Organize remaining examples
mkdir -p examples/{quickstart,integrations,visualization}
mv example.py examples/quickstart/basic_usage.py 2>/dev/null || true
mv examples.py examples/quickstart/getting_started.py 2>/dev/null || true
mv plot_*.py examples/visualization/ 2>/dev/null || true
mv *integration*.py examples/integrations/ 2>/dev/null || true
mv *_example.py examples/integrations/ 2>/dev/null || true

# 5. Organize scripts
mkdir -p scripts/{maintenance,analysis,documentation,testing,automation}
# (This will need careful analysis of each script's purpose)

# COMMIT ROOT CHANGES
git add .
git status  # Review all changes
git commit -m "cleanup: massive root directory reorganization

- Archived 50+ analysis reports to project_docs/archive/reports/
- Moved 30+ temp/debug files to project_docs/dev/temp/
- Organized remaining examples into proper categories
- Consolidated data files to project_docs/dev/data/
- Prepared scripts for organization (next phase)

Ref: maintenance_20250728_1627"
```

---

## 📋 **COMMIT SEQUENCE SUMMARY**

### **Per-Submodule Commits**
```bash
# In each submodule:
packages/haive-core/.git     → "cleanup: organize haive-core project structure"
packages/haive-agents/.git   → "cleanup: organize haive-agents project structure" 
packages/haive-tools/.git    → "cleanup: organize haive-tools project structure"
packages/haive-games/.git    → "cleanup: organize haive-games project structure"
packages/haive-mcp/.git      → "cleanup: organize haive-mcp structure"
packages/haive-prebuilt/.git → "cleanup: organize haive-prebuilt structure"
```

### **Parent Repo Commits**
```bash
# In root .git:
"update: haive-core submodule ref for organizational cleanup"
"update: haive-agents submodule ref + examples reorganization"  
"update: haive-tools submodule ref + tools examples"
"update: haive-games submodule ref + games examples"
"update: haive-mcp and haive-prebuilt submodule refs"
"cleanup: massive root directory reorganization"
```

---

## ⚡ **EXECUTION COMMANDS**

### **Quick Execution Script**
```bash
#!/bin/bash
# submodule_cleanup.sh

echo "🧹 Starting submodule-aware cleanup..."

# Phase 1: haive-core
echo "📦 Cleaning haive-core..."
cd packages/haive-core/
git checkout -b cleanup/organizational-fixes-20250728
mkdir -p ../../project_docs/haive-core/
mv project_docs/* ../../project_docs/haive-core/ 2>/dev/null || true
rmdir project_docs/ 2>/dev/null || true
git add . && git commit -m "cleanup: organize haive-core project structure"
git push -u origin cleanup/organizational-fixes-20250728
cd ../../
git add packages/haive-core
git commit -m "update: haive-core submodule ref for organizational cleanup"

# Phase 2: haive-agents  
echo "📦 Cleaning haive-agents..."
cd packages/haive-agents/
git checkout -b cleanup/organizational-fixes-20250728
mkdir -p ../../project_docs/haive-agents/
mv project_docs/* ../../project_docs/haive-agents/ 2>/dev/null || true
rmdir project_docs/ 2>/dev/null || true
git add . && git commit -m "cleanup: organize haive-agents project structure"
git push -u origin cleanup/organizational-fixes-20250728
cd ../../
git add packages/haive-agents
git commit -m "update: haive-agents submodule ref for organizational cleanup"

# Phase 3: Root cleanup
echo "🏠 Cleaning root directory..."
mkdir -p project_docs/archive/reports/
mv *_REPORT.md *_ANALYSIS.md *_SUMMARY.md project_docs/archive/reports/ 2>/dev/null || true
mkdir -p project_docs/dev/temp/
mv *fix*.py *scan*.py *check*.py project_docs/dev/temp/ 2>/dev/null || true
git add .
git commit -m "cleanup: massive root directory reorganization"

echo "✅ Cleanup complete!"
```

---

## ✅ **VALIDATION STEPS**

After each phase:

```bash
# 1. Verify submodule functionality
cd packages/[package]/
poetry run python -c "import haive.[package]; print('✅ Import works')"

# 2. Verify parent repo submodule references
cd ../../
git submodule status
git status

# 3. Run tests to ensure no breakage
poetry run pytest packages/[package]/tests/ -v

# 4. Check for missing files
git status --porcelain
```

---

## 🎯 **SUCCESS CRITERIA**

### **Each Submodule After Cleanup**
- ✅ No duplicate project_docs directory
- ✅ All package-specific tests in tests/
- ✅ Clean package structure
- ✅ Functionality preserved
- ✅ Clean git history with descriptive commits

### **Root After Cleanup**  
- ✅ ≤10 files in root (only essentials)
- ✅ All reports archived
- ✅ All temp files organized
- ✅ Examples properly categorized
- ✅ Single project_docs/ directory

**This approach respects the submodule architecture while systematically cleaning each package and coordinating through the parent repository.**