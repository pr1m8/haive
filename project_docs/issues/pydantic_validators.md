# Pydantic Validator Signature Issues

**Date**: August 1, 2025
**Priority**: MEDIUM - Multiple validation errors
**Status**: Partially Fixed

## Problem

Pydantic validation errors for incorrect validator signatures:

```
PydanticUserError: Unrecognized field_validator function signature for <bound method NumericGrade.validate_score_range of <class 'haive.agents.common.models.grade.numeric.NumericGrade'>> with `mode=after`:() -> 'NumericGrade'
```

## Affected Files

- `haive.agents.common.models.grade.numeric`
- `haive.agents.common.models.grade.qualitative`
- `haive.agents.common.models.grade.rubric`
- `haive.agents.common.models.grade.scale`

## Root Cause

Using `@classmethod` decorator with `@model_validator(mode="after")` which is incorrect in Pydantic v2.

## Solution

Remove `@classmethod` decorator from model validators:

```python
# WRONG
@classmethod
@model_validator(mode="after")
def validate_something(cls) -> "MyModel":
    pass

# CORRECT
@model_validator(mode="after")
def validate_something(self) -> "MyModel":
    pass
```

## Implementation

Need to fix all grade model validators to use correct signature.

## Files to Modify

- `/packages/haive-agents/src/haive/agents/common/models/grade/numeric.py`
- `/packages/haive-agents/src/haive/agents/common/models/grade/qualitative.py`
- `/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py`
- `/packages/haive-agents/src/haive/agents/common/models/grade/scale.py`

## Testing

```bash
# Test imports after fix
poetry run python -c "from haive.agents.common.models.grade import NumericGrade"
```

## Success Criteria

- No PydanticUserError during import
- All grade models validate correctly
- Documentation builds without validation errors
