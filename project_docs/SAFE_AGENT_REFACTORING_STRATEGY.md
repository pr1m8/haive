# Safe Agent Refactoring Strategy - Complete Implementation Plan

**Date**: 2025-08-07  
**Risk Level**: 🔴 EXTREME (1200+ files, 862 SimpleAgentV3 usages)  
**Strategy**: Multi-layered safety with rope + dry run + comprehensive testing

## 🛡️ Multi-Layered Safety Strategy

### Layer 1: Pre-Flight Safety Checks

### Layer 2: Rope-Based Safe Refactoring

### Layer 3: Dry Run Validation

### Layer 4: Progressive Testing

### Layer 5: Rollback Mechanisms

---

## 🔍 Layer 1: Pre-Flight Safety Analysis

### 1.1 Comprehensive Dependency Mapping

```bash
# Map all dependencies before touching anything
poetry run task analyze-agent-dependencies-dry
```

**Script**: `scripts/maintenance/analyze_agent_dependencies.py`

```python
#!/usr/bin/env python3
"""
Pre-flight dependency analysis for agent consolidation.
Maps every import, inheritance, and usage pattern.
"""

class AgentDependencyAnalyzer:
    def analyze_all_dependencies(self):
        """Complete dependency mapping before refactoring."""
        return {
            "enhanced_agent_imports": self.find_enhanced_imports(),
            "simpleagentv3_usages": self.find_v3_usages(),
            "inheritance_chains": self.find_inheritance_patterns(),
            "export_conflicts": self.find_export_conflicts(),
            "circular_imports": self.find_circular_imports(),
            "test_dependencies": self.find_test_patterns(),
            "example_dependencies": self.find_example_patterns(),
            "lazy_loading_mappings": self.find_lazy_mappings()
        }

    def generate_refactor_plan(self, dependencies):
        """Generate detailed refactoring plan with risk assessment."""
        return {
            "phase_1_critical": ["base/__init__.py", "simple/__init__.py"],
            "phase_2_core": ["enhanced_agent.py", "agent_v3.py"],
            "phase_3_imports": dependencies["enhanced_agent_imports"],
            "phase_4_usages": dependencies["simpleagentv3_usages"],
            "phase_5_tests": dependencies["test_dependencies"],
            "rollback_checkpoints": self.create_checkpoint_plan()
        }

# Usage:
# DRY_RUN=1 python scripts/maintenance/analyze_agent_dependencies.py
```

### 1.2 Safety Pre-Checks

```bash
# Ensure clean state
git status --porcelain | wc -l  # Should be 0
git diff --quiet  # Should exit 0

# Verify no broken imports currently exist
poetry run python -c "
import haive.agents.base
import haive.agents.simple
import haive.agents.multi
print('✅ Current imports work')
"

# Check test suite baseline
poetry run pytest packages/haive-agents/tests/ --collect-only -q | grep "error\|FAILED" && echo "❌ Tests broken before refactor" || echo "✅ Tests clean"
```

---

## 🔧 Layer 2: Rope-Based Safe Refactoring

### 2.1 Rope Project Setup with Safety

```python
class SafeRopeRefactorer:
    def __init__(self, project_root: Path, dry_run: bool = True):
        self.dry_run = dry_run
        self.project = Project(str(project_root))
        self.changes_log = []
        self.validation_errors = []

    def safe_restructure(self, pattern: str, goal: str, scope: str = None):
        """Rope restructuring with comprehensive safety checks."""
        if self.dry_run:
            print(f"[DRY RUN] Would restructure: {pattern} → {goal}")
            return self.preview_changes(pattern, goal, scope)

        # Create checkpoint before each operation
        checkpoint = self.create_operation_checkpoint(f"restructure_{pattern}")

        try:
            # Apply rope changes
            changes = self.apply_rope_restructure(pattern, goal, scope)

            # Validate changes immediately
            if not self.validate_changes_safe(changes):
                self.rollback_to_checkpoint(checkpoint)
                raise RefactoringError(f"Validation failed for {pattern}")

            self.changes_log.append(f"✅ Restructured: {pattern} → {goal}")
            return changes

        except Exception as e:
            self.rollback_to_checkpoint(checkpoint)
            raise RefactoringError(f"Rope operation failed: {e}")

    def validate_changes_safe(self, changes):
        """Validate that rope changes don't break imports."""
        # Compile all affected files
        for change in changes.changes:
            try:
                py_compile.compile(change.resource.path, doraise=True)
            except py_compile.PyCompileError:
                return False

        # Test imports still work
        try:
            subprocess.run([
                "poetry", "run", "python", "-c",
                "import haive.agents; print('Import test passed')"
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            return False

        return True
```

### 2.2 Progressive Rope Operations

```python
# Phase-by-phase rope refactoring with validation

ROPE_REFACTOR_PHASES = [
    # Phase 1: Fix export conflicts (CRITICAL)
    {
        "name": "fix_export_conflicts",
        "operations": [
            {
                "type": "file_edit",
                "file": "packages/haive-agents/src/haive/agents/base/__init__.py",
                "changes": "Remove Agent import conflicts"
            }
        ]
    },

    # Phase 2: Import restructuring (HIGH RISK)
    {
        "name": "restructure_enhanced_imports",
        "operations": [
            {
                "pattern": "from haive.agents.base.enhanced_agent import ${name}",
                "goal": "from haive.agents.base.agent import ${name}",
                "scope": "packages/haive-agents/src/"
            }
        ]
    },

    # Phase 3: SimpleAgentV3 → SimpleAgent (MASSIVE)
    {
        "name": "rename_simpleagentv3",
        "operations": [
            {
                "pattern": "SimpleAgentV3",
                "goal": "SimpleAgent",
                "scope": "packages/haive-agents/"
            }
        ]
    },

    # Phase 4: Class instantiation updates
    {
        "name": "update_instantiations",
        "operations": [
            {
                "pattern": "SimpleAgentV3(${args})",
                "goal": "SimpleAgent(${args})",
                "scope": "packages/haive-agents/"
            }
        ]
    }
]

def execute_phased_refactoring():
    for phase in ROPE_REFACTOR_PHASES:
        print(f"\n🔄 Phase: {phase['name']}")

        # Create phase checkpoint
        checkpoint = create_git_checkpoint(phase['name'])

        try:
            # Execute all operations in phase
            for operation in phase['operations']:
                rope_refactorer.safe_restructure(**operation)

            # Validate entire phase
            if not validate_phase_success(phase):
                rollback_to_checkpoint(checkpoint)
                raise PhaseFailureError(f"Phase {phase['name']} validation failed")

            print(f"✅ Phase {phase['name']} completed successfully")

        except Exception as e:
            print(f"❌ Phase {phase['name']} failed: {e}")
            rollback_to_checkpoint(checkpoint)
            raise
```

---

## 🧪 Layer 3: Comprehensive Dry Run Validation

### 3.1 Enhanced Dry Run Wrapper

```bash
# Enhanced dry run for each phase
DRY_RUN=1 VALIDATE_DEEP=1 python scripts/maintenance/agent_consolidation_refactorer.py --phase=1

# Deep validation dry run
DRY_RUN=1 COMPREHENSIVE_CHECK=1 python scripts/maintenance/comprehensive_agent_validator.py
```

**Enhanced Dry Run Features**:

```python
class ComprehensiveAgentValidator:
    def deep_dry_run_validation(self):
        """Comprehensive validation without making changes."""
        validations = {
            "syntax_check": self.validate_all_python_syntax(),
            "import_resolution": self.validate_all_imports(),
            "inheritance_chains": self.validate_inheritance_patterns(),
            "test_compatibility": self.validate_test_patterns(),
            "example_compatibility": self.validate_example_patterns(),
            "circular_imports": self.detect_circular_imports(),
            "performance_impact": self.estimate_performance_impact()
        }

        return self.generate_validation_report(validations)

    def validate_all_python_syntax(self):
        """Compile every Python file in haive-agents."""
        errors = []
        python_files = list(Path("packages/haive-agents").rglob("*.py"))

        for py_file in python_files:
            try:
                py_compile.compile(py_file, doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(f"{py_file}: {e}")

        return {"passed": len(errors) == 0, "errors": errors}

    def validate_all_imports(self):
        """Test that all imports resolve correctly."""
        import_tests = [
            "import haive.agents",
            "from haive.agents import SimpleAgent, ReactAgent, MultiAgent",
            "from haive.agents.base import Agent",
            "from haive.agents.multi import EnhancedMultiAgentV4",
        ]

        results = {}
        for test in import_tests:
            try:
                subprocess.run([
                    "poetry", "run", "python", "-c", test
                ], check=True, capture_output=True)
                results[test] = "✅ PASS"
            except subprocess.CalledProcessError as e:
                results[test] = f"❌ FAIL: {e.stderr.decode()}"

        return results
```

### 3.2 Preview Mode for Every Change

```python
def preview_all_changes():
    """Show exactly what would change before applying anything."""

    print("📋 COMPREHENSIVE CHANGE PREVIEW")
    print("=" * 60)

    # Show file moves/renames
    file_changes = {
        "enhanced_agent.py": "RENAME → agent.py (with backup)",
        "agent.py": "ARCHIVE → archive/agent_original.py",
        "agent_v3.py": "ARCHIVE → archive/agent_v3.py",
        "agent_v2.py": "ARCHIVE → archive/agent_v2.py"
    }

    print("\n🔄 FILE OPERATIONS:")
    for old, new in file_changes.items():
        print(f"  {old} {new}")

    # Show import changes
    print(f"\n📦 IMPORT CHANGES: {len(enhanced_imports)} files")
    for imp in enhanced_imports[:5]:  # Show first 5
        print(f"  {imp}")
    if len(enhanced_imports) > 5:
        print(f"  ... and {len(enhanced_imports) - 5} more")

    # Show usage changes
    print(f"\n🏷️  USAGE CHANGES: {len(v3_usages)} SimpleAgentV3 → SimpleAgent")

    # Show risk assessment
    risk_level = calculate_risk_level()
    print(f"\n⚠️  RISK LEVEL: {risk_level}")
    print(f"   Affected files: {total_files}")
    print(f"   Total changes: {total_changes}")
```

---

## 🧪 Layer 4: Progressive Testing Strategy

### 4.1 Test-Driven Refactoring Phases

```bash
# Test each phase incrementally

# Phase 1: Core exports test
poetry run pytest packages/haive-agents/tests/test_core_exports.py -v

# Phase 2: Import resolution test
poetry run pytest packages/haive-agents/tests/test_import_resolution.py -v

# Phase 3: SimpleAgent functionality test
poetry run pytest packages/haive-agents/tests/simple/ -v -k "not v3"

# Phase 4: Multi-agent integration test
poetry run pytest packages/haive-agents/tests/multi/ -v --tb=short

# Phase 5: Full integration test
poetry run pytest packages/haive-agents/tests/ -v --durations=10
```

### 4.2 Critical Test Categories

```python
CRITICAL_TEST_SUITES = {
    "core_functionality": [
        "packages/haive-agents/tests/simple/test_simple_agent_v3.py",
        "packages/haive-agents/tests/react/test_react_agent_v3.py",
        "packages/haive-agents/tests/multi/test_enhanced_multi_agent_v4.py"
    ],
    "import_resolution": [
        "packages/haive-agents/tests/test_imports.py",
        "packages/haive-agents/tests/simple/test_lazy_loading.py"
    ],
    "integration": [
        "packages/haive-agents/tests/multi/test_v3_v4_real_execution.py",
        "packages/haive-agents/tests/multi/test_react_simple_structured_output.py"
    ]
}

def run_critical_tests_after_phase(phase_name: str):
    """Run critical tests after each refactoring phase."""
    print(f"\n🧪 Running critical tests for phase: {phase_name}")

    for category, test_files in CRITICAL_TEST_SUITES.items():
        print(f"\n📋 Category: {category}")

        for test_file in test_files:
            if Path(test_file).exists():
                result = subprocess.run([
                    "poetry", "run", "pytest", test_file, "-v", "--tb=short"
                ], capture_output=True)

                if result.returncode == 0:
                    print(f"  ✅ {Path(test_file).name}")
                else:
                    print(f"  ❌ {Path(test_file).name}")
                    print(f"     Error: {result.stderr.decode()[:200]}...")
                    return False

    return True
```

### 4.3 Example Validation

```python
CRITICAL_EXAMPLES = [
    "examples/simple_agent_v3_example.py",
    "examples/multi_agent_v4/working_sequential_example.py",
    "examples/multi_agent_v4/clean_branching_example.py",
    "examples_new/03_multi_agents/sequential_workflow.py",
    "examples_new/02_single_agents/agent_with_memory.py"
]

def validate_examples_after_refactor():
    """Ensure key examples still work after refactoring."""
    for example in CRITICAL_EXAMPLES:
        if Path(example).exists():
            print(f"\n🔍 Testing example: {Path(example).name}")

            # Try to run the example in dry run mode if possible
            result = subprocess.run([
                "poetry", "run", "python", example, "--dry-run"
            ], capture_output=True, timeout=30)

            if result.returncode == 0:
                print(f"  ✅ Example works")
            else:
                print(f"  ❌ Example broken: {result.stderr.decode()[:100]}...")
```

---

## 🔙 Layer 5: Bulletproof Rollback Mechanisms

### 5.1 Multi-Level Checkpoint System

```python
class CheckpointManager:
    def __init__(self):
        self.checkpoints = []
        self.backup_files = {}

    def create_comprehensive_checkpoint(self, phase_name: str):
        """Create git + file + state checkpoint."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_id = f"agent-consolidation-{phase_name}-{timestamp}"

        # Git checkpoint
        git_tag = self.create_git_checkpoint(checkpoint_id)

        # File backups
        file_backups = self.create_file_backups(phase_name)

        # Environment snapshot
        env_snapshot = self.capture_environment_state()

        checkpoint = {
            "id": checkpoint_id,
            "phase": phase_name,
            "git_tag": git_tag,
            "file_backups": file_backups,
            "env_snapshot": env_snapshot,
            "timestamp": timestamp
        }

        self.checkpoints.append(checkpoint)
        return checkpoint

    def emergency_rollback(self, checkpoint_id: str = None):
        """Emergency rollback to specific checkpoint."""
        if not checkpoint_id:
            # Use latest checkpoint
            checkpoint = self.checkpoints[-1]
        else:
            checkpoint = self.find_checkpoint(checkpoint_id)

        print(f"🚨 EMERGENCY ROLLBACK to {checkpoint['id']}")

        # Git rollback
        subprocess.run(["git", "reset", "--hard", checkpoint["git_tag"]])

        # Restore file backups
        for backup_file, original_file in checkpoint["file_backups"].items():
            if Path(backup_file).exists():
                shutil.copy(backup_file, original_file)
                print(f"✅ Restored {original_file}")

        # Validate rollback worked
        if self.validate_rollback_success():
            print("✅ Emergency rollback successful!")
            return True
        else:
            print("❌ Emergency rollback failed!")
            return False
```

### 5.2 Automated Recovery Tests

```python
def test_rollback_mechanisms():
    """Test that rollback mechanisms work before starting refactoring."""

    # Create test checkpoint
    test_checkpoint = checkpoint_manager.create_comprehensive_checkpoint("rollback_test")

    # Make a small test change
    test_file = Path("packages/haive-agents/ROLLBACK_TEST.txt")
    test_file.write_text("This is a rollback test")

    # Test rollback
    success = checkpoint_manager.emergency_rollback(test_checkpoint["id"])

    # Verify test file is gone
    rollback_worked = not test_file.exists()

    return success and rollback_worked
```

---

## 🚀 Complete Execution Workflow

### Master Control Script

```bash
#!/bin/bash
# scripts/maintenance/safe_agent_consolidation_master.sh

set -e

echo "🛡️ SAFE AGENT CONSOLIDATION - MASTER CONTROLLER"
echo "=================================================="

# Phase 0: Pre-flight safety checks
echo "🔍 Phase 0: Pre-flight safety checks..."
./scripts/maintenance/pre_flight_safety_check.sh || exit 1

# Phase 1: Comprehensive dependency analysis
echo "📊 Phase 1: Dependency analysis..."
DRY_RUN=1 python scripts/maintenance/analyze_agent_dependencies.py || exit 1

# Phase 2: Test rollback mechanisms
echo "🔙 Phase 2: Testing rollback mechanisms..."
python scripts/maintenance/test_rollback_mechanisms.py || exit 1

# Phase 3: Deep dry run of entire refactoring
echo "🧪 Phase 3: Comprehensive dry run..."
DRY_RUN=1 COMPREHENSIVE_CHECK=1 python scripts/maintenance/agent_consolidation_refactorer.py || exit 1

# Phase 4: User confirmation
echo "⚠️  Ready to proceed with LIVE refactoring?"
echo "   This will modify 1200+ files with 862 SimpleAgentV3 usages"
echo "   Are you sure? Type 'CONSOLIDATE' to proceed:"
read confirmation

if [ "$confirmation" != "CONSOLIDATE" ]; then
    echo "❌ Aborted by user"
    exit 1
fi

# Phase 5: Execute live refactoring with full safety
echo "🚀 Phase 5: Executing live refactoring..."
python scripts/maintenance/agent_consolidation_refactorer.py --live --safe || {
    echo "❌ Refactoring failed, attempting emergency rollback..."
    python scripts/maintenance/emergency_rollback.py
    exit 1
}

# Phase 6: Comprehensive validation
echo "✅ Phase 6: Final validation..."
python scripts/maintenance/post_refactor_validation.py || {
    echo "❌ Validation failed, rolling back..."
    python scripts/maintenance/emergency_rollback.py
    exit 1
}

echo "🎉 AGENT CONSOLIDATION COMPLETED SUCCESSFULLY!"
echo "✅ All 1200+ files updated"
echo "✅ All tests passing"
echo "✅ All examples working"
echo "✅ Imports resolved correctly"
```

### Usage Commands

```bash
# Full safe execution
./scripts/maintenance/safe_agent_consolidation_master.sh

# Individual phases for testing
./scripts/maintenance/pre_flight_safety_check.sh
DRY_RUN=1 python scripts/maintenance/analyze_agent_dependencies.py
DRY_RUN=1 python scripts/maintenance/agent_consolidation_refactorer.py
python scripts/maintenance/test_rollback_mechanisms.py

# Emergency procedures
python scripts/maintenance/emergency_rollback.py
python scripts/maintenance/validate_system_health.py
```

---

## 🎯 Success Criteria & Validation

### Must Pass (Blocking):

- ✅ **Zero import errors** across entire haive-agents package
- ✅ **All Python files compile** without syntax errors
- ✅ **Critical test suites pass** (core functionality)
- ✅ **Key examples execute** without errors
- ✅ **Lazy loading works** correctly
- ✅ **No circular imports** detected

### Should Pass (Warning):

- ✅ **All test suites pass** (100% compatibility)
- ✅ **All examples work** (100% compatibility)
- ✅ **Documentation builds** without errors
- ✅ **Import performance** maintained or improved

### Recovery Readiness:

- ✅ **Emergency rollback tested** and working
- ✅ **Multiple checkpoint levels** available
- ✅ **File backups verified** and accessible
- ✅ **Git history preserved** with detailed commits

---

This strategy provides **comprehensive safety** for the massive agent consolidation refactoring, with multiple layers of protection and validation at every step. The risk is high, but the safety measures are bulletproof.

Ready to implement this safe refactoring strategy?
