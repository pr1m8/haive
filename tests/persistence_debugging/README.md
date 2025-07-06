# PostgreSQL Persistence Debugging

## Directory Structure

### utilities/

Utility scripts for viewing database content and debugging:

- `view_*.py` - View various database tables and content
- `check_*.py` - Check system status and configuration
- `decode_*.py` - Decode binary data (msgpack, etc)

### tests/

Test scripts for verifying functionality:

- `test_*.py` - Various test scenarios
- `verify_*.py` - Verification scripts

### analysis/

Analysis and data extraction scripts:

- `conversation_status_summary.py` - Analyze conversation status
- `extract_conversation_outputs.py` - Extract conversation data

### results/

Test results and output files (JSON, logs)

### state_history/

Agent state history files

## Key Fixes Applied

1. **Prepared Statement Conflicts**: Fixed by setting `prepare_threshold=None`
2. **Connection Manager**: Updated to disable prepared statements
3. **Persistence Mixin**: Fixed to handle `persistence=True`
4. **Unique App Names**: Each agent gets unique PostgreSQL app name

## Usage

```bash
# Run a test
python tests/test_all_agents_comprehensive.py

# View errors
python utilities/view_conversation_errors.py

# Check system status
python utilities/check_db.py
```
