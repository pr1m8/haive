# High Impact Function Documentation

**Status**: Ready for Implementation  
**Assigned**: Available for systematic work  
**Target**: Complete within 1 month

## Priority Focus

Target the **most-used public functions** across packages for maximum impact.

## Top Priority Packages

1. **haive-core**: Foundation APIs used by all other packages
2. **haive-agents**: Agent creation and management
3. **haive-tools**: Tool integration
4. **haive-engines**: LLM processing

## Implementation Strategy

### Week 1: haive-core Public APIs

```bash
# Find undocumented public functions in haive-core
cd packages/haive-core/src
find . -name "*.py" -exec grep -l "^def [^_]" {} \; | head -20
```

### Week 2: haive-agents Public APIs

Focus on agent creation, configuration, and execution functions.

### Week 3: Integration APIs

Tool and engine integration functions used by external code.

### Week 4: Review and Quality

Ensure all added documentation meets standards.

## Template for Documentation

```python
def function_name(param1: Type1, param2: Type2 = default) -> ReturnType:
    """One line summary.

    Longer description explaining the function's purpose,
    behavior, and any important implementation details.

    Args:
        param1: Clear description of the parameter.
        param2: Description including default behavior.

    Returns:
        ReturnType: Description of what is returned and when.

    Raises:
        ValueError: When invalid input is provided.
        RuntimeError: When system is in invalid state.

    Examples:
        Basic usage::

            result = function_name("value", 42)
            print(result.output)

        Advanced usage::

            with function_name("complex", validate=False) as ctx:
                ctx.process()
    """
```

## Success Metrics

- **Week 1**: 200+ functions documented
- **Week 2**: 400+ functions documented
- **Week 3**: 600+ functions documented
- **Week 4**: 800+ functions documented

Target: Document highest-impact 800 functions to achieve maximum developer experience improvement.
