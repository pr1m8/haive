# Quick Reference - Most Used Memories

## 🚨 Critical Rules

1. **Always use `poetry run`** → @memory_index/by_task/poetry_run_everything.md
2. **NO MOCKS EVER in tests** → @memory_index/by_pattern/no_mocks_testing.md
3. **Never override `__init__` in Pydantic** → @memory_index/by_error/pydantic_init_override.md
4. **Use explicit imports** → `from haive.core.engine import X`
5. **No unnecessary factories** → Just use the class directly!

## 🔧 Common Fixes

### Documentation Build Errors

```bash
# KeyError in AutoAPI
find . -name "*\ *" -o -name "*(*" -o -name "*)*"  # Find bad filenames
# See: @memory_index/by_error/containers_tilebag_keyerror.md

# Syntax errors in examples
find packages -name "*.py" -exec python -m py_compile {} \;
# See: @memory_index/by_task/documentation_97_percent_fix.md
```

### Import Errors

```bash
# Always test imports first
poetry run python -c "from haive.core import *; print('OK')"

# Fix with
poetry install --all-extras
```

### Test Failures

```python
# NO MOCKS pattern
config = AugLLMConfig()  # Real config
agent = SimpleAgent(engine=config)  # Real agent
result = agent.run("test")  # Real execution
```

## 📋 Common Patterns

### Agent Creation (No Factories!)

```python
# ✅ CORRECT - Direct instantiation
agent = SimpleAgent(
    name="my_agent",
    engine=AugLLMConfig(temperature=0.7)
)

# ❌ WRONG - Unnecessary factory function
def create_agent(): ...
```

### Prompt Templates (Direct Constants)

```python
# ✅ CORRECT - From task_analysis example
MY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert..."""),
    ("human", """Task: {task}

Details: {details}""")
])

# ❌ WRONG - Functions that return prompts
def create_prompt(): ...
```

### Structured Output Pattern

```python
# The universal pattern: Agent → StructuredOutputAgent
main_agent = ReactAgent(name="main", tools=[...])
structurer = StructuredOutputAgent(
    name="structurer",
    output_model=MyModel
)
# They work sequentially in workflow
```

### Message vs Structured Data Flow (NEW!)

```python
# Problem: Agents only accept messages, but we have structured data

# ✅ SOLUTION: Use prompt partials
prompt = REFLECTION_PROMPT.partial(
    grade_context=f"Grade: {result.letter_grade}"
)

# Not everything needs to be a message!
```

### Reflection Pattern with Message Transform (NEW!)

```python
# 1. Main agent responds
# 2. Grade (structured data)
# 3. Convert grade to prompt partial (not message!)
# 4. Message transform (AI → Human)
# 5. Reflection agent with grade in prompt context

grade_context = f"Grade: {result.letter_grade}"
prompt = REFLECTION_PROMPT.partial(grade_context=grade_context)
```

### Generic Pre/Post Hook Pattern (NEW!)

```python
class PrePostMultiAgent(MultiAgent, Generic[TPreAgent, TMainAgent, TPostAgent]):
    pre_agent: Optional[TPreAgent]
    main_agent: TMainAgent
    post_agent: Optional[TPostAgent]
    use_message_transform: bool = Field(default=False)
```

### Pydantic Models

```python
# NEVER override __init__
class MyConfig(BaseModel):
    name: str = Field(..., min_length=1)
    value: float = Field(default=0.0, ge=0.0)

    # Use validators instead
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return v
```

### Documentation Build

```bash
# Standard build
nox -s docs

# Quick test
poetry run sphinx-build -b html docs/source docs/build/html

# View locally
python -m http.server 8003 --directory docs/build/html/
```

## 🗺️ Navigation Shortcuts

- **By Error Type**: @memory_index/by_error/
- **By Date**: @memory_index/by_date/
- **By Agent**: @memory_index/by_agent/
- **By Package**: @memory_index/by_package/
- **By Task**: @memory_index/by_task/

## 🏷️ Most Referenced Tags

#no-mocks #poetry-run #documentation #import-errors #pydantic-patterns #no-factories #prompt-partials #reflection-pattern

## 🆕 Latest Discoveries (2025-01-28)

### Documentation Automation Discovery 🔥

- **44,450 documentation issues** analyzed across codebase
- **✅ UPDATE: 100% of Google-style tools already installed!** (not just 80%)
- **42,417 auto-fixable issues** (95.4% automation rate)
- **See**: @memory_index/by_date/2025-07-28/documentation_automation_discovery.md
- **Update**: @memory_index/by_date/2025-07-28/google_style_tools_status.md

### Google-Style Enforcement Ready - ALL TOOLS AVAILABLE! ✅

```bash
# These ALL work RIGHT NOW (100% tools ready):
poetry run interrogate packages/ --verbose  # Coverage measurement
poetry run pydocstyle packages/ --convention=google  # Style check
poetry run darglint packages/ --strictness=short  # Semantic validation
poetry run docformatter --in-place --recursive packages/  # Auto-fix
poetry run flake8 packages/ --docstring-convention=google --extend-select=D,DOC  # Full validation
poetry run pydoclint packages/  # Ultra-fast semantic check
poetry run ruff check packages/ --select=D  # Fast integrated check
```

### Critical Documentation Fixes

- **36 critical functions** missing all documentation
- **3,977 wrong style docstrings** - auto-fixable with docformatter
- **12,687 missing sections** (Args/Returns/Examples)
- **See**: @project_docs/documentation_fix/COMPREHENSIVE_GOOGLE_STYLE_SUMMARY.md

## 🆕 Previous Discoveries (2025-01-18)

- **Reflection Pattern**: @memory_index/by_date/2025-01-18/reflection_pattern_insights.md
- **Message-Only Challenge**: Agents only accept messages, use prompt partials for structured data
- **No model_post_init**: Usually unnecessary, just use field defaults
- **Direct Class Usage**: Stop making factory functions everywhere!
