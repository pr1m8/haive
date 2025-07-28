# Documentation Fix Quick Reference

## 🚨 Current State

- **Errors**: 6,802
- **Warnings**: 2,407
- **HTML Files**: 13 (should be 500+)
- **Main Issue**: Sphinx/AutoAPI can't handle namespace packages

## 🎯 Three Options

### Option A: Fix Sphinx

```bash
git checkout -b docs/sphinx-incremental-fix-2025
# Start with PHASE_1_MINIMAL.md
```

- **Time**: 2-3 weeks
- **Success**: 60%

### Option B: MkDocs

```bash
git checkout -b docs/mkdocs-poc-2025
pip install mkdocs-material mkdocstrings[python]
mkdocs new .
```

- **Time**: 3-4 weeks
- **Success**: 85%

### Option C: Hybrid (Recommended)

```bash
# Do both, then choose
git checkout -b docs/hybrid-comparison-2025
```

- **Time**: 4-6 weeks
- **Success**: 90%

## 📋 Key Documents

1. **[MASTER_PLAN.md](./MASTER_PLAN.md)** - Start here
2. **[DECISION_TREE.md](./DECISION_TREE.md)** - Help choosing
3. **[GIT_WORKFLOW.md](./GIT_WORKFLOW.md)** - Version control

## 🔧 Quick Fixes

### Fix Import Errors

```python
# In conf.py
for package in packages:
    sys.path.insert(0, f"{package}/src")
```

### Fix CSS Width

```css
:root {
  --sidebar-width: 19rem; /* Not 30.5rem */
}
```

### Aggressive Ignores

```python
autoapi_ignore = [
    "**/test*",
    "**/supervisor/**",
    "**/examples/**",
]
```

## 📊 Success Metrics

| Metric     | Current | Target |
| ---------- | ------- | ------ |
| Errors     | 6,802   | 0      |
| Warnings   | 2,407   | <100   |
| HTML Files | 13      | 500+   |
| Build Time | ???     | <2 min |

## 🚀 Next Actions

1. **Review** [MASTER_PLAN.md](./MASTER_PLAN.md)
2. **Decide** using [DECISION_TREE.md](./DECISION_TREE.md)
3. **Execute** with [GIT_WORKFLOW.md](./GIT_WORKFLOW.md)

## 💡 Key Insight

**Sphinx wasn't designed for namespaced monorepos**. We're either:

- Fighting the tool (Fix Sphinx)
- Using the right tool (MkDocs)
- Hedging our bets (Hybrid)

---

_When in doubt, choose Hybrid approach_
