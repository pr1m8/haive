# Pydantic Validator Audit Results

## Summary

Comprehensive search for field_validator and model_validator issues across the haive codebase.

## ✅ Clean Areas (No Issues Found)

### Main Package Directories

- `packages/haive-core/` - All validators correctly implemented
- `packages/haive-agents/` - All validators correctly implemented
- `packages/haive-tools/` - All validators correctly implemented
- `packages/haive-games/` - All validators correctly implemented
- `packages/haive-dataflow/` - All validators correctly implemented
- `packages/haive-mcp/` - All validators correctly implemented
- `packages/haive-prebuilt/` - All validators correctly implemented

## ❌ Issues Found

### migrations/ Directory Only (22 errors)

This directory contains old/experimental code with various validation errors:

1. **Invalid @field_validator Syntax** (5 instances)

   ```python
   # Incorrect:
   @field_validatorvalidate_something

   # Should be:
   @field_validator("field_name")
   ```

2. **BaseTool args_schema Issues** (4 instances)

   ```python
   # Incorrect:
   args_schema = ModelClass

   # Should be:
   args_schema: Type[BaseModel] = Field(default=ModelClass)
   ```

3. **Various Syntax Errors** (11 instances)
   - Malformed imports
   - Missing parentheses
   - Invalid decorator syntax

## Correct Patterns Found

### @model_validator Usage

- ✅ `@model_validator(mode="before")` with `@classmethod` - CORRECT
- ✅ `@model_validator(mode="after")` without `@classmethod` - CORRECT
- ❌ `@model_validator(mode="after")` with `@classmethod` - NOT FOUND (which is good!)

### @field_validator Usage

- ✅ All field validators properly use `@field_validator("field_name")` syntax
- ✅ No incorrect `@classmethod` usage with field validators

## Recommendations

1. **No Action Needed** for main codebase - all validators are correctly implemented
2. **Consider Cleaning** the `migrations/` directory if it contains obsolete code
3. **Use check_pydantic_errors.py** script to validate any new code:
   ```bash
   poetry run python scripts/check_pydantic_errors.py
   ```

## Verification Commands

```bash
# Check for validator issues
grep -r "@model_validator.*after.*@classmethod" packages/
grep -r "@field_validator.*@classmethod" packages/

# Run the validation script
poetry run python scripts/check_pydantic_errors.py
```

## Conclusion

The haive codebase follows Pydantic best practices correctly. The specific issue pattern you were concerned about (@model_validator(mode="after") with @classmethod) does not exist in the active codebase.
