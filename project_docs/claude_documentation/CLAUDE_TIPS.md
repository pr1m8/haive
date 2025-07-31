# Claude Code Tips and Workarounds

## Timeout Limitations

Claude Code has a hardcoded timeout of approximately 2 minutes for command execution. This can be problematic for long-running operations like documentation builds, tests, or installations.

### Workarounds for Long-Running Commands

#### 1. Background Execution with nohup

```bash
# Run command in background and save output
nohup poetry run nox -s docs > docs_build.log 2>&1 &

# Check the process
ps aux | grep nox

# Monitor the output
tail -f docs_build.log
```

#### 2. Using screen (if available)

```bash
# Create a new screen session
screen -S docs_build

# Run your command
poetry run nox -s docs

# Detach with Ctrl+A then D
# Reattach later with:
screen -r docs_build
```

#### 3. Using tmux (if available)

```bash
# Create new tmux session
tmux new -s docs_build

# Run your command
poetry run nox -s docs

# Detach with Ctrl+B then D
# Reattach with:
tmux attach -t docs_build
```

#### 4. Split Long Operations

For documentation builds specifically:

```bash
# Clean first (quick)
poetry run nox -s docs_clean

# Install dependencies separately
poetry install --only docs

# Then build
poetry run sphinx-build -b html docs/source docs/build/html
```

#### 5. Check Existing Builds

Often you can skip rebuilding entirely:

```bash
# Serve existing docs without rebuilding
cd docs/build/html && python -m http.server 8000
```

## Known Issues

- GitHub issues tracking timeout problems: #424, #2489, #743
- No current way to configure timeout via settings
- Affects all long-running operations (builds, tests, large installs)

## Best Practices

1. **Always save output** when running long commands:

   ```bash
   command > output.log 2>&1 &
   ```

2. **Check if rebuild is necessary** before starting:

   ```bash
   ls -la docs/build/html/
   ```

3. **Monitor background processes**:

   ```bash
   # Check if still running
   ps aux | grep [p]rocess_name

   # Check exit status
   echo $?
   ```

4. **Use poetry's verbose mode** for better progress tracking:
   ```bash
   poetry install -vvv
   ```

## Documentation-Specific Tips

### Quick Serve Without Rebuild

```bash
# If docs already built
cd docs/build/html && python -m http.server 8000

# Or use the nox session if available
poetry run nox -s docs_view
```

### Background Documentation Build

```bash
# Start build in background
nohup poetry run nox -s docs > docs_build_$(date +%Y%m%d_%H%M%S).log 2>&1 &

# Get the process ID
echo $!

# Monitor progress
tail -f docs_build_*.log
```

### Check Build Status

```bash
# See if sphinx-build is still running
pgrep -f sphinx-build

# Check last modified times
find docs/build -name "*.html" -mmin -5 | wc -l
```

## When to Use Background Execution

Use background execution for:

- Documentation builds (usually 3-5+ minutes)
- Full test suites
- Large dependency installations
- Database migrations
- Data processing scripts

Don't use for:

- Quick commands (< 30 seconds)
- Commands that need interactive input
- Commands where you need immediate error feedback
