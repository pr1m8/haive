# Backwards Compatibility Strategy

## Overview

The schema refactoring must maintain 100% backwards compatibility while introducing a new, modular architecture. This document outlines a comprehensive strategy using a `schema_test` module approach for safe, incremental migration.

## Core Strategy: Parallel Implementation with Adapter Pattern

### 1. Schema Test Module Structure

```
packages/haive-core/src/haive/core/schema_test/
├── __init__.py                    # New API exports
├── adapters/                      # Legacy compatibility adapters
│   ├── __init__.py
│   ├── state_schema_adapter.py    # Wraps new system for old API
│   ├── composer_adapter.py        # SchemaComposer compatibility
│   └── node_config_adapter.py     # Node config compatibility
├── core/                          # New modular core
│   ├── __init__.py
│   ├── interfaces/                # Abstract interfaces
│   │   ├── engine_provider.py     # Engine access contract
│   │   ├── tool_provider.py       # Tool access contract
│   │   ├── schema_metadata.py     # Unified metadata interface
│   │   └── field_registry.py      # Field management interface
│   ├── components/                # Single-responsibility components
│   │   ├── field_manager.py       # Field definition and validation
│   │   ├── engine_manager.py      # Engine access and coordination
│   │   ├── tool_manager.py        # Tool discovery and execution
│   │   ├── serialization.py       # JSON/dict conversion
│   │   └── visualization.py       # Pretty printing and UI
│   └── schemas/                   # Clean schema implementations
│       ├── base_schema.py         # Minimal base schema
│       ├── message_schema.py      # Message handling schema
│       ├── tool_schema.py         # Tool-enabled schema
│       └── agent_schema.py        # Agent state schema
├── compatibility/                 # Lightweight compatibility
│   ├── __init__.py
│   ├── converters.py             # Essential type conversions
│   └── validators.py             # Compatibility validation
├── migration/                     # Migration utilities
│   ├── __init__.py
│   ├── detector.py               # Detect legacy usage patterns
│   ├── migrator.py               # Automated migration tools
│   └── validator.py              # Validate migration correctness
└── tests/                        # Comprehensive test suite
    ├── test_adapters.py          # Adapter compatibility tests
    ├── test_migration.py         # Migration validation tests
    └── integration/              # End-to-end compatibility tests
```

### 2. Phased Migration Approach

#### Phase 1: Parallel Implementation (Weeks 1-2)

- Implement new modular system in `schema_test/`
- Create adapter layer that wraps new system with old API
- Ensure 100% API compatibility through adapters
- Run existing tests against adapter layer

#### Phase 2: Feature Flag Migration (Weeks 3-4)

- Add feature flag to switch between old and new implementations
- Migrate internal usage to new system gradually
- Maintain old API surface through adapters
- Comprehensive testing of both paths

#### Phase 3: Deprecation Period (Weeks 5-8)

- Mark old classes as deprecated with clear migration paths
- Provide migration utilities for external users
- Documentation and examples for new API
- Support both systems during transition

#### Phase 4: Legacy Removal (Weeks 9-12)

- Remove old implementation after deprecation period
- Keep minimal adapter layer for external compatibility
- Clean up and optimize new system
- Final documentation and release

## Technical Implementation Strategy

### 1. Adapter Pattern for API Compatibility

#### StateSchema Adapter

```python
# schema_test/adapters/state_schema_adapter.py
from typing import Any, Dict, List, Callable
from ..core.schemas.base_schema import BaseSchema
from ..core.components.field_manager import FieldManager
from ..core.components.engine_manager import EngineManager

class StateSchemaAdapter:
    """Adapter that provides old StateSchema API using new modular system."""

    def __init__(self, *args, **kwargs):
        # Create new system components
        self._field_manager = FieldManager()
        self._engine_manager = EngineManager()
        self._schema = BaseSchema()

        # Migrate old-style initialization
        self._migrate_init_args(*args, **kwargs)

    # OLD API: Maintain exact method signatures
    def share_field(self, field_name: str) -> None:
        """Legacy method - delegates to new field manager."""
        self._field_manager.share_field(field_name)

    def add_reducer(self, field: str, reducer: Callable) -> None:
        """Legacy method - delegates to new field manager."""
        self._field_manager.add_reducer(field, reducer)

    def pretty_print(self) -> str:
        """Legacy method - delegates to new visualization component."""
        from ..core.components.visualization import pretty_print_schema
        return pretty_print_schema(self._schema)

    def to_dict(self) -> Dict[str, Any]:
        """Legacy method - delegates to new serialization component."""
        from ..core.components.serialization import schema_to_dict
        return schema_to_dict(self._schema)

    # NEW INTERNAL: Use new system internally
    def _migrate_init_args(self, *args, **kwargs):
        """Convert old initialization pattern to new system."""
        # Handle legacy field definitions
        if 'fields' in kwargs:
            for field_def in kwargs['fields']:
                self._field_manager.register_field(field_def)

        # Handle legacy engine configuration
        if 'engine' in kwargs:
            self._engine_manager.set_primary_engine(kwargs['engine'])
```

#### Node Config Adapter

```python
# schema_test/adapters/node_config_adapter.py
from typing import Any, Optional
from ..core.interfaces.engine_provider import EngineProvider

class EngineNodeConfigAdapter:
    """Adapter for EngineNodeConfig that uses new engine provider interface."""

    def __init__(self, engine=None, engine_name=None, **kwargs):
        self.engine = engine
        self.engine_name = engine_name
        # Store other legacy attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_engine(self, state: Any) -> Any:
        """Legacy method with simplified, predictable logic."""
        # NEW APPROACH: Use standardized engine provider interface
        if isinstance(state, EngineProvider):
            return self._get_engine_from_provider(state)

        # FALLBACK: Handle legacy state objects
        return self._get_engine_legacy_fallback(state)

    def _get_engine_from_provider(self, provider: EngineProvider) -> Any:
        """Use new standardized engine access."""
        if self.engine:
            return self.engine

        if self.engine_name:
            return provider.get_engine(self.engine_name)

        return provider.get_primary_engine()

    def _get_engine_legacy_fallback(self, state: Any) -> Any:
        """Minimal fallback for legacy state objects."""
        if self.engine:
            return self.engine

        # Simplified legacy lookup - no complex fallback chains
        if hasattr(state, 'get_engine') and callable(state.get_engine):
            return state.get_engine(self.engine_name)

        if hasattr(state, 'engine'):
            return state.engine

        return None
```

### 2. Feature Flag System

#### Configuration-Based Switching

```python
# schema_test/__init__.py
import os
from typing import Type

# Feature flag for new system
USE_NEW_SCHEMA_SYSTEM = os.getenv('HAIVE_USE_NEW_SCHEMA', 'false').lower() == 'true'

def get_state_schema_class() -> Type:
    """Return appropriate StateSchema implementation based on feature flag."""
    if USE_NEW_SCHEMA_SYSTEM:
        from .core.schemas.base_schema import BaseSchema
        return BaseSchema
    else:
        from .adapters.state_schema_adapter import StateSchemaAdapter
        return StateSchemaAdapter

def get_schema_composer_class() -> Type:
    """Return appropriate SchemaComposer implementation."""
    if USE_NEW_SCHEMA_SYSTEM:
        from .core.components.schema_composer import ModularSchemaComposer
        return ModularSchemaComposer
    else:
        from .adapters.composer_adapter import SchemaComposerAdapter
        return SchemaComposerAdapter

# Export classes based on feature flag
StateSchema = get_state_schema_class()
SchemaComposer = get_schema_composer_class()
```

#### Gradual Migration Points

```python
# Example: Agent code can opt into new system
class MyAgent:
    def __init__(self, use_new_schema: bool = None):
        if use_new_schema or USE_NEW_SCHEMA_SYSTEM:
            from haive.core.schema_test import StateSchema
        else:
            from haive.core.schema import StateSchema

        self.schema_class = StateSchema
```

### 3. Migration Detection and Automation

#### Usage Pattern Detection

```python
# schema_test/migration/detector.py
import ast
import os
from typing import List, Dict, Any

class LegacyUsageDetector:
    """Detect legacy schema usage patterns in codebase."""

    def scan_codebase(self, root_path: str) -> Dict[str, List[str]]:
        """Scan for legacy usage patterns."""
        issues = {
            'direct_state_schema_imports': [],
            'legacy_field_access': [],
            'complex_engine_lookups': [],
            'deprecated_methods': []
        }

        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_issues = self._scan_file(file_path)
                    for category, file_issues_list in file_issues.items():
                        issues[category].extend(file_issues_list)

        return issues

    def _scan_file(self, file_path: str) -> Dict[str, List[str]]:
        """Scan single file for legacy patterns."""
        with open(file_path, 'r') as f:
            try:
                tree = ast.parse(f.read())
                return self._analyze_ast(tree, file_path)
            except SyntaxError:
                return {}

    def _analyze_ast(self, tree: ast.AST, file_path: str) -> Dict[str, List[str]]:
        """Analyze AST for legacy usage patterns."""
        issues = {
            'direct_state_schema_imports': [],
            'legacy_field_access': [],
            'complex_engine_lookups': [],
            'deprecated_methods': []
        }

        class LegacyPatternVisitor(ast.NodeVisitor):
            def visit_ImportFrom(self, node):
                if node.module == 'haive.core.schema':
                    for alias in node.names:
                        if alias.name == 'StateSchema':
                            issues['direct_state_schema_imports'].append(
                                f"{file_path}:{node.lineno}"
                            )

        visitor = LegacyPatternVisitor()
        visitor.visit(tree)
        return issues
```

#### Automated Migration Tools

```python
# schema_test/migration/migrator.py
import ast
import re
from typing import List, Tuple

class SchemaMigrator:
    """Automated migration tools for schema refactoring."""

    def migrate_file(self, file_path: str) -> List[str]:
        """Migrate a single file to new schema API."""
        with open(file_path, 'r') as f:
            content = f.read()

        changes = []

        # 1. Update imports
        new_content, import_changes = self._migrate_imports(content)
        changes.extend(import_changes)

        # 2. Update API calls
        new_content, api_changes = self._migrate_api_calls(new_content)
        changes.extend(api_changes)

        # 3. Update initialization patterns
        new_content, init_changes = self._migrate_initialization(new_content)
        changes.extend(init_changes)

        if changes:
            with open(file_path, 'w') as f:
                f.write(new_content)

        return changes

    def _migrate_imports(self, content: str) -> Tuple[str, List[str]]:
        """Update import statements."""
        changes = []

        # Replace direct schema imports
        old_import = r'from haive\.core\.schema import StateSchema'
        new_import = 'from haive.core.schema_test import StateSchema'

        if re.search(old_import, content):
            content = re.sub(old_import, new_import, content)
            changes.append("Updated StateSchema import to use new system")

        return content, changes

    def _migrate_api_calls(self, content: str) -> Tuple[str, List[str]]:
        """Update deprecated API calls."""
        changes = []

        # Example: Replace deprecated method calls
        migrations = [
            (r'\.share_field\(([^)]+)\)', r'.field_manager.share_field(\1)'),
            (r'\.add_reducer\(([^)]+)\)', r'.field_manager.add_reducer(\1)'),
        ]

        for old_pattern, new_pattern in migrations:
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                changes.append(f"Updated API call: {old_pattern} -> {new_pattern}")

        return content, changes
```

### 4. Comprehensive Testing Strategy

#### Compatibility Test Suite

```python
# schema_test/tests/test_adapters.py
import pytest
from haive.core.schema import StateSchema as OldStateSchema
from haive.core.schema_test import StateSchema as NewStateSchema

class TestBackwardsCompatibility:
    """Ensure new system maintains exact API compatibility."""

    def test_state_schema_api_parity(self):
        """Test that new StateSchema has same API as old one."""
        old_methods = set(dir(OldStateSchema))
        new_methods = set(dir(NewStateSchema))

        # All old public methods must exist in new implementation
        old_public = {m for m in old_methods if not m.startswith('_')}
        new_public = {m for m in new_methods if not m.startswith('_')}

        missing_methods = old_public - new_public
        assert not missing_methods, f"Missing methods in new implementation: {missing_methods}"

    def test_field_sharing_compatibility(self):
        """Test that field sharing works exactly like old system."""
        old_schema = OldStateSchema()
        new_schema = NewStateSchema()

        # Both should handle field sharing identically
        old_schema.share_field("test_field")
        new_schema.share_field("test_field")

        assert old_schema.is_field_shared("test_field") == new_schema.is_field_shared("test_field")

    def test_serialization_compatibility(self):
        """Test that serialization produces identical results."""
        # Create schemas with identical data
        old_schema = OldStateSchema(messages=["test"])
        new_schema = NewStateSchema(messages=["test"])

        old_dict = old_schema.to_dict()
        new_dict = new_schema.to_dict()

        assert old_dict == new_dict

    @pytest.mark.parametrize("test_case", [
        {"messages": ["hello", "world"]},
        {"tools": ["calculator", "search"]},
        {"engine_config": {"temperature": 0.7}},
    ])
    def test_initialization_compatibility(self, test_case):
        """Test that initialization works with various patterns."""
        old_schema = OldStateSchema(**test_case)
        new_schema = NewStateSchema(**test_case)

        # Should produce equivalent schemas
        assert old_schema.to_dict() == new_schema.to_dict()
```

#### Migration Validation Tests

```python
# schema_test/tests/test_migration.py
import tempfile
import os
from ..migration.migrator import SchemaMigrator
from ..migration.detector import LegacyUsageDetector

class TestMigrationTools:
    """Test migration detection and automation tools."""

    def test_legacy_pattern_detection(self):
        """Test that legacy usage patterns are correctly detected."""
        legacy_code = '''
from haive.core.schema import StateSchema

class MyAgent:
    def __init__(self):
        self.schema = StateSchema()
        self.schema.share_field("messages")
        '''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(legacy_code)
            f.flush()

            detector = LegacyUsageDetector()
            issues = detector._scan_file(f.name)

            assert len(issues['direct_state_schema_imports']) > 0

        os.unlink(f.name)

    def test_automated_migration(self):
        """Test that automated migration tools work correctly."""
        legacy_code = '''
from haive.core.schema import StateSchema

schema = StateSchema()
schema.share_field("test")
'''

        expected_migrated = '''
from haive.core.schema_test import StateSchema

schema = StateSchema()
schema.share_field("test")
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(legacy_code)
            f.flush()

            migrator = SchemaMigrator()
            changes = migrator.migrate_file(f.name)

            with open(f.name, 'r') as updated_f:
                migrated_content = updated_f.read()

            assert "schema_test" in migrated_content
            assert len(changes) > 0

        os.unlink(f.name)
```

## Migration Timeline and Process

### Week 1-2: Foundation

1. Create `schema_test/` module structure
2. Implement core interfaces and components
3. Create adapter layer for StateSchema
4. Basic compatibility tests

### Week 3-4: Expansion

1. Complete adapter layer for all major classes
2. Implement feature flag system
3. Create migration detection tools
4. Comprehensive compatibility test suite

### Week 5-6: Integration

1. Begin internal migration of haive packages
2. Update documentation with migration guides
3. Create automated migration tools
4. Performance testing and optimization

### Week 7-8: Validation

1. Test with real-world usage patterns
2. Fix compatibility issues discovered
3. Complete migration of internal usage
4. Prepare deprecation notices

### Week 9-12: Transition

1. Release with deprecation warnings
2. Support both systems during transition
3. Community feedback and issue resolution
4. Final cleanup and legacy removal

## Benefits of This Approach

1. **Zero Downtime**: Existing code continues working unchanged
2. **Gradual Migration**: Teams can migrate at their own pace
3. **Risk Mitigation**: Problems caught early through parallel testing
4. **Automated Support**: Tools help with detection and migration
5. **Clean Architecture**: New system designed properly from scratch
6. **Performance**: Opportunity to optimize without compatibility constraints

This strategy ensures we can completely redesign the schema system while maintaining perfect backwards compatibility throughout the transition period.
