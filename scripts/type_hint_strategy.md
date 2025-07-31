# Type Hint Improvement Strategy

## 🎯 **3-Phase Approach to 3,568 Missing Type Hints**

### **Phase 1: Analysis & Quick Wins (Now)**

**Tools Available:**

- ✅ **mypy** - Static type checker (installed)
- ✅ **pyright** - Microsoft's type checker (installed)
- ✅ **ruff** - Fast linter with type checking (installed)

**Automated Analysis:**

```bash
# Analyze specific package
poetry run python scripts/type_hint_analyzer.py --package haive-core

# Analyze all packages
poetry run python scripts/type_hint_analyzer.py --all

# Quick analysis of priority packages
poetry run python scripts/type_hint_analyzer.py
```

**Expected Output:**

- Files with most missing type hints
- Common patterns and suggested fixes
- Mypy errors categorized by type

### **Phase 2: Automated Fixes (After Parse Errors)**

**Smart Pattern Recognition:**

- Parameter types based on naming (`config` → `Dict[str, Any]`)
- Return types based on function names (`is_*` → `bool`)
- Import management (auto-add `from typing import`)

**Dry Run Testing:**

```bash
# See what would be fixed
poetry run python scripts/type_hint_fixer.py --package haive-core --dry-run

# Apply fixes to specific package
poetry run python scripts/type_hint_fixer.py --package haive-core

# Fix single file
poetry run python scripts/type_hint_fixer.py path/to/file.py
```

### **Phase 3: Validation & Quality (Ongoing)**

**Integration with existing tools:**

```bash
# Type checking in CI/CD
poetry run mypy packages/ --ignore-missing-imports
poetry run pyright packages/
poetry run ruff check --select F401,F811,F821  # Type-related rules
```

## 📊 **Type Hint Priority Matrix**

### **High Impact - Low Effort (Do First)**

1. **Public API functions** - Most visible to users
2. **`__init__` methods** - Constructor parameters
3. **Return type hints** - Easier to add than parameters
4. **Boolean functions** - `is_*`, `has_*`, `can_*` → `bool`

### **High Impact - Medium Effort**

1. **Core utility functions** - Used across packages
2. **Configuration classes** - Config objects and params
3. **Data processing functions** - Transform, validate, parse

### **Medium Impact - Low Effort**

1. **Helper functions** - Internal utilities
2. **String/number parameters** - Clear type patterns
3. **List/dict parameters** - Collection types

## 🔧 **Automated Pattern Recognition**

### **Parameter Type Patterns**

```python
# Configuration patterns
config: Dict[str, Any]
params: Dict[str, Any]
options: Dict[str, Any]
settings: Dict[str, Any]

# String patterns
name: str
text: str
content: str
message: str
query: str
prompt: str
path: str
url: str

# Numeric patterns
count: int
size: int
limit: int
temperature: float
threshold: float
timeout: float

# Boolean patterns
enabled: bool
active: bool
debug: bool
strict: bool

# Collection patterns
items: List[Any]
results: List[Any]
tools: List[str]
messages: List[Dict[str, Any]]
headers: Dict[str, str]
```

### **Return Type Patterns**

```python
# Function name → Return type
def is_*() -> bool
def has_*() -> bool
def can_*() -> bool
def get_*() -> Optional[Any]
def find_*() -> Optional[Any]
def create_*() -> Any
def build_*() -> Any
def list_*() -> List[Any]
def __init__() -> None
```

## 🚀 **Implementation Workflow**

### **Step 1: Quick Analysis**

```bash
# Get overview of all packages
poetry run python scripts/type_hint_analyzer.py --all > type_hint_analysis.txt

# Focus on high-priority packages first
poetry run python scripts/type_hint_analyzer.py --package haive-core
poetry run python scripts/type_hint_analyzer.py --package haive-agents
```

### **Step 2: Targeted Fixes**

```bash
# Start with core package (foundation)
poetry run python scripts/type_hint_fixer.py --package haive-core --dry-run
# Review output, then apply:
poetry run python scripts/type_hint_fixer.py --package haive-core

# Move to agents package
poetry run python scripts/type_hint_fixer.py --package haive-agents --dry-run
poetry run python scripts/type_hint_fixer.py --package haive-agents
```

### **Step 3: Validation**

```bash
# Check mypy improvement
poetry run mypy packages/haive-core/src/ --ignore-missing-imports

# Check with pyright for additional insights
poetry run pyright packages/haive-core/src/

# Run ruff type checking
poetry run ruff check packages/haive-core/src/ --select F
```

### **Step 4: Iterate**

```bash
# Re-analyze to see progress
poetry run python scripts/type_hint_analyzer.py --package haive-core

# Apply manual fixes for complex cases
# Commit progress: git add . && git commit -m "feat: add type hints to haive-core"
```

## 📈 **Success Metrics**

### **Quantitative Goals**

- **Week 1**: 50% reduction in missing parameter hints (1,063 → 500)
- **Week 2**: 80% reduction in missing return hints (721 → 144)
- **Month 1**: 90%+ type hint coverage across all packages

### **Quality Metrics**

- **Mypy score**: < 100 type-related errors
- **IDE experience**: IntelliSense/autocompletion works
- **Developer productivity**: Fewer runtime type errors

### **Tracking Progress**

```bash
# Before fixes
poetry run python scripts/type_hint_analyzer.py --all | grep "Total Issues"

# After each package
poetry run python scripts/type_hint_analyzer.py --package haive-core | grep "Total Issues"

# Final validation
poetry run mypy packages/ --ignore-missing-imports | wc -l
```

## 🛠️ **Tool Integration Strategy**

### **Pre-commit Hooks (Future)**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: mypy
        name: mypy type checking
        entry: poetry run mypy
        language: system
        types: [python]
        args: [--ignore-missing-imports]
```

### **CI/CD Integration**

```yaml
# .github/workflows/type-check.yml
- name: Type checking
  run: |
    poetry run mypy packages/ --ignore-missing-imports
    poetry run pyright packages/
```

### **VS Code Integration**

```json
// .vscode/settings.json
{
  "python.linting.mypyEnabled": true,
  "python.linting.pyrightEnabled": true,
  "python.analysis.typeCheckingMode": "basic"
}
```

## 🎯 **Ready to Start!**

**No blockers for type hints** - Unlike docstrings, type hints don't depend on parse errors being fixed.

**Immediate next step:**

```bash
# Test our tools
poetry run python scripts/type_hint_analyzer.py --package haive-core
```

This will give us concrete data on exactly what needs fixing and prioritization!
