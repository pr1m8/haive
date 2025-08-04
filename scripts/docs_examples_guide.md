# Documentation Example Control Guide

This guide shows how to control example execution in documentation builds using nox sessions.

## 🚀 Quick Start

### For Development (Fast, No Examples)
```bash
# Ultra-fast development build
nox -s docs_dev

# Or the full name
nox -s docs_no_examples

# Or ultra-minimal (fastest possible)
nox -s docs_minimal_no_examples
```

### For Production (With Examples)
```bash
# Full production build with examples
nox -s docs_prod

# Or the full name  
nox -s docs_with_examples
```

### For Live Development
```bash
# Auto-rebuild on changes (no examples)
nox -s docs_live

# Or the full name
nox -s docs_autobuild_no_examples
```

## 📋 All Available Sessions

### Core Documentation Sessions

| Session | Examples | Profile | Use Case | Speed |
|---------|----------|---------|----------|--------|
| `docs_no_examples` | ❌ Disabled | Standard | Development | ⚡ Fast |
| `docs_with_examples` | ✅ Enabled | Full | Production | 🐌 Slow |
| `docs_minimal_no_examples` | ❌ Disabled | Minimal | Ultra-fast preview | ⚡⚡ Fastest |
| `docs_compare_examples` | Both | Both | Performance analysis | 📊 Analysis |

### Auto-Build Sessions

| Session | Examples | Port | Use Case |
|---------|----------|------|----------|
| `docs_autobuild` | ✅ Enabled | 8003 | Full live docs |
| `docs_autobuild_no_examples` | ❌ Disabled | 8004 | Fast live docs |

### Convenience Aliases

| Alias | Maps To | Description |
|-------|---------|-------------|
| `docs_dev` | `docs_no_examples` | Development build |
| `docs_prod` | `docs_with_examples` | Production build |
| `docs_fast_dev` | `docs_no_examples` | Fast development |  
| `docs_live` | `docs_autobuild_no_examples` | Live development |

## 🎯 Environment Variables

You can also control example execution manually with environment variables:

```bash
# Disable examples
SPHINX_DISABLE_EXAMPLES=1 nox -s docs

# Enable examples (default)
SPHINX_DISABLE_EXAMPLES=0 nox -s docs

# Control Sphinx profile
SPHINX_PROFILE=minimal nox -s docs      # Fastest
SPHINX_PROFILE=standard nox -s docs     # Balanced  
SPHINX_PROFILE=full nox -s docs         # Complete
```

## ⚡ Performance Comparison

Run this to see the performance difference:

```bash
nox -s docs_compare_examples
```

Expected results:
- **Without examples**: ~30-60 seconds
- **With examples**: ~5-15 minutes (depending on example complexity)
- **Speed improvement**: 5-10x faster without examples

## 🔧 Configuration Details

### What Gets Disabled

When `SPHINX_DISABLE_EXAMPLES=1`:

1. **Sphinx Gallery**: Completely removed from extensions
2. **Example Execution**: All code execution disabled
3. **Gallery Generation**: No auto_examples directory created
4. **Ignore Patterns**: Archive and example directories ignored

### What Still Works

Even with examples disabled:
- ✅ API documentation (AutoAPI)
- ✅ Docstring examples (non-executed)
- ✅ Code blocks in RST files
- ✅ All other Sphinx features

## 📊 Build Profiles

### Minimal Profile (`SPHINX_PROFILE=minimal`)
- Only core Sphinx extensions
- Fastest build time
- Basic documentation only

### Standard Profile (`SPHINX_PROFILE=standard`) 
- Common extensions (copybutton, design, etc.)
- Good balance of features vs speed
- Recommended for development

### Full Profile (`SPHINX_PROFILE=full`)
- All 80+ extensions loaded
- Complete feature set
- Used for production builds

## 🛠️ Development Workflow

### Daily Development
```bash
# Start live development server
nox -s docs_live

# Open http://localhost:8004
# Edit files and see instant rebuilds
```

### Before Committing
```bash
# Quick validation
nox -s docs_dev

# Check if it looks good
nox -s docs_serve
```

### CI/CD Pipeline
```bash
# Fast CI check
nox -s docs_no_examples

# Weekly full build
nox -s docs_with_examples
```

### Release Process
```bash
# Full production build
nox -s docs_prod

# Deploy to documentation server
```

## 🚨 Troubleshooting

### Build Hangs
If your build hangs, it's likely executing examples:
```bash
# Check if examples are enabled
echo $SPHINX_DISABLE_EXAMPLES

# Force disable examples
SPHINX_DISABLE_EXAMPLES=1 nox -s docs
```

### Memory Issues
If you get memory errors:
```bash
# Use minimal profile
nox -s docs_minimal_no_examples

# Or check memory usage
nox -s docs_monitor  # If available
```

### Port Conflicts
If auto-build fails with port errors:
```bash
# Kill existing processes
pkill -f sphinx-autobuild

# Use different session (different port)
nox -s docs_autobuild_no_examples  # Port 8004
nox -s docs_autobuild              # Port 8003
```

## 💡 Tips

1. **Use `docs_dev` for daily work** - It's fast and has everything you need
2. **Use `docs_live` for iterative writing** - Instant feedback on changes
3. **Use `docs_compare_examples` periodically** - Track performance improvements
4. **Reserve `docs_prod` for releases** - Only when you need complete docs
5. **Set up shell aliases** for even faster access:
   ```bash
   alias nd='nox -s docs_dev'
   alias nl='nox -s docs_live' 
   alias np='nox -s docs_prod'
   ```

## ✨ Advanced Usage

### Custom Environment Combinations
```bash
# Minimal build without examples (ultra-fast)
SPHINX_PROFILE=minimal SPHINX_DISABLE_EXAMPLES=1 nox -s docs

# Standard build with examples (balanced)
SPHINX_PROFILE=standard SPHINX_DISABLE_EXAMPLES=0 nox -s docs

# Full build without examples (feature-complete but fast)
SPHINX_PROFILE=full SPHINX_DISABLE_EXAMPLES=1 nox -s docs
```

### Build Specific Packages
```bash
# Build only core package docs (no examples)
SPHINX_PACKAGES=core nox -s docs_dev

# Build agents package with examples  
SPHINX_PACKAGES=agents nox -s docs_prod
```

This system gives you complete control over documentation build performance while maintaining flexibility for different use cases.