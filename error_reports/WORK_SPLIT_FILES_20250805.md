# Work Split by Files - Import Error Fixes

## Total Critical Files: 288
- haive-agents: 268 files
- haive-mcp: 11 files  
- haive-games: 4 files
- haive-prebuilt: 2 files
- haive-dataflow: 2 files
- haive-core: 1 file

## Split Strategy

### **Agent 1** (144 files - First half of haive-agents)
Take files 1-144 from haive-agents critical errors

### **Agent 2** (144 files - Second half of haive-agents + all other packages)
- Files 145-268 from haive-agents (124 files)
- All haive-mcp files (11 files)
- All haive-games files (4 files)
- All haive-prebuilt files (2 files)
- All haive-dataflow files (2 files)
- All haive-core files (1 file)
Total: 144 files

## How to Get Your File List

### Agent 1:
```bash
grep "### ModuleNotFoundError in" error_analysis/critical_errors.md | grep "haive-agents" | head -144 > agent1_files.txt
```

### Agent 2:
```bash
grep "### ModuleNotFoundError in" error_analysis/critical_errors.md | grep "haive-agents" | tail -124 > agent2_files_agents.txt
grep "### ModuleNotFoundError in" error_analysis/critical_errors.md | grep -v "haive-agents" > agent2_files_other.txt
cat agent2_files_agents.txt agent2_files_other.txt > agent2_files.txt
```

## Key Patterns to Fix

1. **haive.agents.simple.models** - This module doesn't exist, need to:
   - Either create it with proper exports
   - Or fix imports to use correct module

2. **plan_and_execute** - Wrong import paths:
   - Change: `from haive.agents.plan_and_execute`
   - To: `from haive.agents.planning.plan_and_execute`

3. **Relative imports** - Convert to absolute:
   - Change: `from models.join_step`
   - To: `from haive.agents.planning.rewoo.models.join_step`

4. **Missing exports** - Add to __init__.py files

## Coordination

- Both agents work independently on their file lists
- Share any discovered patterns or solutions
- If a fix in one file helps multiple files, share it