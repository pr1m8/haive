# Universal Dry-Run System for Haive

This system provides safe dry-run capabilities for any command in the Haive project, making it easy to test operations before actually running them.

## 🚀 Quick Start

### For haive-dataflow absolute imports (what you need):

```bash
# Test what would be changed (DRY RUN)
poetry run task fix-imports-dataflow-dry

# Actually apply the changes
poetry run task fix-imports-dataflow
```

### Other useful commands:

```bash
# Lazy loading (safe deployment system)
poetry run task lazy-loading-dry          # Test lazy loading deployment
poetry run task lazy-loading-deploy       # Deploy lazy loading

# Code formatting
poetry run task format-dry                # Test formatting changes
poetry run task format                    # Apply formatting

# Import fixing for other packages
poetry run task fix-imports-core-dry       # Test core imports
poetry run task fix-imports-dry           # Test all imports
```

## 🛠️ How It Works

The system uses a universal wrapper (`dryrun_wrapper.py`) that:

1. **Analyzes commands** to understand what they might do
2. **Shows risk assessment** (🟢 LOW, 🟡 MEDIUM, 🔴 HIGH)
3. **Provides safe dry-run mode** via `DRY_RUN=1` environment variable
4. **Works with any command** - Python, shell, poetry, etc.

## 📋 Complete Task Reference

### Import Fixing Tasks

```bash
# haive-dataflow (what you need)
poetry run task fix-imports-dataflow-dry   # DRY RUN: Test absolute imports for haive-dataflow
poetry run task fix-imports-dataflow       # LIVE: Apply absolute imports to haive-dataflow

# Other packages
poetry run task fix-imports-core-dry       # DRY RUN: Test absolute imports for haive-core
poetry run task fix-imports-core           # LIVE: Apply absolute imports to haive-core
poetry run task fix-imports-dry            # DRY RUN: Test absolute imports for all packages
poetry run task fix-imports                # LIVE: Apply absolute imports to all packages
```

### Lazy Loading Tasks

```bash
poetry run task lazy-loading-dry           # DRY RUN: Test lazy loading deployment
poetry run task lazy-loading-test          # TEST ONLY: Check if deployment would be safe
poetry run task lazy-loading-deploy        # LIVE: Deploy lazy loading with full safety
poetry run task lazy-loading-models        # LIVE: Deploy lazy loading to models only
poetry run task lazy-loading-tools         # LIVE: Deploy lazy loading to tools only
poetry run task lazy-loading-agents        # LIVE: Deploy lazy loading to agents only
poetry run task lazy-loading-rollback      # Show available backups for rollback
poetry run task lazy-loading-preview       # DRY RUN: Preview generated lazy loading code
```

### Code Quality Tasks

```bash
poetry run task format-dry                 # DRY RUN: Test code formatting
poetry run task format                     # LIVE: Apply code formatting
poetry run task lint-fix-dry               # DRY RUN: Test linting fixes
poetry run task lint-fix                   # LIVE: Apply linting fixes
```

## 🔧 Direct Usage (Advanced)

### Basic Wrapper Usage

```bash
# Test any command safely
DRY_RUN=1 python scripts/maintenance/dryrun_wrapper.py -- <your-command>

# Execute the command for real
python scripts/maintenance/dryrun_wrapper.py -- <your-command>
```

### Examples

```bash
# Test import fixing on specific directory
DRY_RUN=1 python scripts/maintenance/dryrun_wrapper.py -- poetry run absolufy-imports packages/haive-dataflow/

# Test dangerous operations safely
DRY_RUN=1 python scripts/maintenance/dryrun_wrapper.py -- rm -rf some_folder

# Test complex commands
DRY_RUN=1 python scripts/maintenance/dryrun_wrapper.py -- poetry run python my_script.py --deploy --force
```

## 🎯 For haive-dataflow Absolute Imports (Your Use Case)

Here's exactly what you need for fixing absolute imports in haive-dataflow:

### Step 1: Test what would change (safe)

```bash
poetry run task fix-imports-dataflow-dry
```

This will show you:

- ✅ Command analysis and risk assessment
- 🔍 What `absolufy-imports` would do
- 📊 Files that would be modified
- ⚠️ Any potential issues

### Step 2: Apply the changes (when ready)

```bash
poetry run task fix-imports-dataflow
```

This will:

- 🚀 Execute the actual `absolufy-imports` command
- 📝 Convert relative imports to absolute imports
- ✅ Show exactly what was changed

### Step 3: Verify the results

```bash
# Check what changed
git diff

# Test that imports still work
poetry run python -c "import haive.dataflow; print('✅ Imports working')"

# Commit if satisfied
git add packages/haive-dataflow/
git commit -m "fix: convert relative imports to absolute imports in haive-dataflow"
```

## 🛡️ Safety Features

### Automatic Risk Assessment

The wrapper analyzes commands and shows:

- 🟢 **LOW RISK**: Read-only operations, analysis commands
- 🟡 **MEDIUM RISK**: File modifications, package changes
- 🔴 **HIGH RISK**: Potentially destructive operations

### Built-in Safety

- **DRY_RUN=1**: Always simulates, never executes
- **Analysis**: Shows what operations are detected
- **Command preview**: Shows exactly what would run
- **Working directory**: Shows where command runs

### Environment Variables

- `DRY_RUN=1`: Enable dry-run mode (safe simulation)
- `VERBOSE=1`: Enable verbose output for debugging

## 📚 Examples of Output

### Dry-Run Mode

```
🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍
🔍  DRY RUN MODE ACTIVE  🔍
🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍
Command: poetry run absolufy-imports packages/haive-dataflow/
Working Directory: /home/user/haive
Environment: DRY_RUN=True, VERBOSE=False
============================================================

📊 Command Analysis:
   Risk Level: 🟡 MEDIUM
   Detected: 📁 File Operations, 📦 Package Operations

[DRY RUN] Would execute: poetry run absolufy-imports packages/haive-dataflow/
[DRY RUN] Command execution skipped
```

### Live Mode

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
🚀  EXECUTING COMMAND   🚀
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
Command: poetry run absolufy-imports packages/haive-dataflow/
Working Directory: /home/user/haive
Environment: DRY_RUN=False, VERBOSE=False
============================================================

📊 Command Analysis:
   Risk Level: 🟡 MEDIUM
   Detected: 📁 File Operations, 📦 Package Operations

🚀 Executing: poetry run absolufy-imports packages/haive-dataflow/
[actual command output here]
```

## 🆘 Troubleshooting

### Command Not Found

If you get "command not found" errors:

```bash
# Make sure you're in the right directory
cd /path/to/haive/backend/haive/

# Make sure poetry is available
poetry --version

# Make sure the wrapper exists
ls scripts/maintenance/dryrun_wrapper.py
```

### Permission Issues

```bash
# Make wrapper executable
chmod +x scripts/maintenance/dryrun_wrapper.py
```

### Import Issues

```bash
# Test that absolufy-imports is available
poetry run absolufy-imports --help
```

## 💡 Tips

1. **Always test first**: Use the `-dry` version of tasks before running the real version
2. **Check git diff**: After running commands, check what changed with `git diff`
3. **Small batches**: Test on one package at a time for safety
4. **Use git branches**: Create a branch before making large changes
5. **Backup important work**: The system has backups, but manual backups are good too

## 🎓 Understanding the Tasks

Each task follows this pattern:

- **`task-name-dry`**: Safe testing mode (DRY_RUN=1)
- **`task-name`**: Actual execution mode
- **`task-name-rollback`**: Show backup/rollback options (where applicable)

This makes it easy to:

1. Test what would happen (`-dry`)
2. Apply changes (main task)
3. Rollback if needed (`-rollback`)

Perfect for collaborative development where you want to be extra careful! 🚀
