# Documentation Backup Methodology

## 🎯 Backup Strategy

### 1. Archive Directory Structure

```
docs/
├── source/              # Active documentation
└── _archives/           # Backup archives
    ├── conf_backups/    # Configuration file backups
    ├── logs/            # Log files
    ├── scripts/         # Orphaned scripts
    └── analysis/        # Analysis documents
```

### 2. Backup Naming Convention

- **Config files**: `conf_backups/conf_{type}_{date}.py`
- **Log files**: `logs/{year}/{month}/`
- **Scripts**: `scripts/{purpose}/`
- **Analysis**: `analysis/{topic}/`

### 3. Retention Policy

- **Config backups**: Keep latest 3 versions
- **Logs**: Archive by month, keep 3 months
- **Scripts**: Archive permanently if functional
- **Analysis**: Keep if still relevant

## 📋 Implementation Script

```python
#!/usr/bin/env python3
"""Archive and clean up docs/source directory."""

import os
import shutil
from datetime import datetime
from pathlib import Path

# Paths
SOURCE_DIR = Path("docs/source")
ARCHIVE_DIR = Path("docs/_archives")

# Create archive structure
def create_archive_structure():
    dirs = [
        ARCHIVE_DIR / "conf_backups",
        ARCHIVE_DIR / "logs" / datetime.now().strftime("%Y/%m"),
        ARCHIVE_DIR / "scripts",
        ARCHIVE_DIR / "analysis"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

# Archive files by category
def archive_files():
    # Config backups
    for conf_file in SOURCE_DIR.glob("conf*.py"):
        if conf_file.name != "conf.py":
            shutil.move(conf_file, ARCHIVE_DIR / "conf_backups" / conf_file.name)

    # Log files
    for log_file in SOURCE_DIR.glob("*.log"):
        shutil.move(log_file, ARCHIVE_DIR / "logs" / datetime.now().strftime("%Y/%m") / log_file.name)

    # Scripts
    scripts = ["generate_package_docs.py", "restructure_navigation.py",
               "test_conf_extensions.py", "test_memory_management.py",
               "update_sidebar_structure.py", "toc_control_example.py"]
    for script in scripts:
        if (SOURCE_DIR / script).exists():
            shutil.move(SOURCE_DIR / script, ARCHIVE_DIR / "scripts" / script)

    # Analysis docs
    analysis_docs = ["CONF_MODULARIZATION_PLAN.md", "DOCUMENTATION_ANALYSIS.md",
                     "NAVIGATION_STRUCTURE.md", "RST_TEMPLATE_UPDATE_GUIDE.md",
                     "documentation_enhancement_plan.md"]
    for doc in analysis_docs:
        if (SOURCE_DIR / doc).exists():
            shutil.move(SOURCE_DIR / doc, ARCHIVE_DIR / "analysis" / doc)

if __name__ == "__main__":
    create_archive_structure()
    archive_files()
    print("✅ Archival complete!")
```

## 🔄 Maintenance Procedures

### Daily

- No action needed

### Weekly

- Review and archive new log files
- Check for new orphaned scripts

### Monthly

- Clean up old logs (>3 months)
- Review config backup retention

### Quarterly

- Review analysis documents for relevance
- Archive outdated documentation

## 📝 .gitignore Entries

```gitignore
# Documentation backups and archives
docs/_archives/
docs/source/*.log
docs/source/conf_*.py
docs/source/*_backup*
docs/source/test_*.py
```
