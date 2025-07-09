# Automatic Source Tracking for Everything

Want to see where EVERY log and print comes from in ALL your Python scripts? Here's how!

## 🚀 Quick Setup (Choose One)

### Option 1: Shell Alias (Easiest)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias python='python -m haive.core.logging.auto_wrapper'
```

Now every time you run `python`, you'll have source tracking!

### Option 2: Auto-Import (For Haive Projects)

Just import haive.core and it's automatic:

```python
import haive.core  # Source tracking enabled automatically!

# Now all your logs show sources
import logging
logging.info("This will show where it comes from")
```

### Option 3: Environment Variable

Add to your shell profile:

```bash
export HAIVE_AUTO_LOGGING=1
```

### Option 4: Python Startup File

Create `~/.pythonrc`:

```python
try:
    from haive.core.logging.quick_setup import setup_development_logging
    setup_development_logging()
except ImportError:
    pass
```

Then add to shell profile:

```bash
export PYTHONSTARTUP=~/.pythonrc
```

## 📊 What You'll See

Instead of:

```
INFO: Processing request
Starting task...
ERROR: Task failed
```

You'll see:

```
[14:32:15] INFO     myapp.service | process_request() in service.py:45
    Processing request

[PRINT from myapp.worker.start_task():67] Starting task...

[14:32:16] ERROR    myapp.service | handle_error() in service.py:89
    Task failed
```

## 🛠️ Advanced Options

### Run Any Script with Tracking

```bash
python -m haive.core.logging.auto_wrapper any_script.py
```

### Create Custom Aliases

```bash
# Track everything
alias pytrack='python -m haive.core.logging.auto_wrapper'

# Track with debug mode
alias pydebug='python -c "from haive.core.logging.quick_setup import i_want_to_see_everything; i_want_to_see_everything()" && python'
```

### Jupyter/IPython Setup

Add to `~/.ipython/profile_default/startup/00-logging.py`:

```python
try:
    from haive.core.logging.quick_setup import setup_development_logging
    setup_development_logging()
    print("📍 Source tracking enabled in IPython!")
except ImportError:
    pass
```

## 🎯 Use Cases

### Debugging Unknown Errors

```python
from haive.core.logging.quick_setup import where_is_this_coming_from
where_is_this_coming_from("connection refused")
# Now run your code - matching messages will be highlighted!
```

### Development Mode

```python
from haive.core.logging.quick_setup import setup_development_logging
setup_development_logging()  # Perfect balance of info
```

### Maximum Visibility

```python
from haive.core.logging.quick_setup import i_want_to_see_everything
i_want_to_see_everything()  # See EVERYTHING
```

## 🔧 Troubleshooting

### Too Much Output?

```python
from haive.core.logging.quick_setup import just_show_my_code
just_show_my_code()  # Hide library noise
```

### Need Specific Modules?

```python
from haive.core.logging.quick_setup import track_specific_modules
track_specific_modules(['myapp', 'haive.core'])
```

### Turn It Off

```python
from haive.core.logging.quick_setup import debug_off
debug_off()
```

## 💡 Pro Tips

1. **Performance**: Source tracking has minimal overhead
2. **Thread-safe**: Works in multi-threaded applications
3. **Compatible**: Works with existing logging configuration
4. **Persistent**: Settings can be saved with `logging_control.save_config()`

## 🚨 One-Time Setup Script

Run this to set everything up:

```bash
curl -sSL https://raw.githubusercontent.com/YourOrg/haive/main/scripts/enable_auto_logging.sh | bash
```

Or manually:

```bash
cd packages/haive-core
chmod +x scripts/enable_auto_logging.sh
./scripts/enable_auto_logging.sh
```

Now you'll always know where every log and print comes from! 🎉
