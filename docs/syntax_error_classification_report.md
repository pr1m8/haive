# Syntax Error Classification Report
Generated: 2025-07-27 19:52:12
## Summary
Total errors found: 100

### By Category:
- **incomplete_assignment**: 1 errors
- **incomplete_comparison**: 1 errors
- **missing_block**: 30 errors
- **unclosed_parenthesis**: 1 errors
- **unknown**: 1 errors
- **unterminated_string**: 66 errors

## Examples by Category

### Incomplete Comparison
**Pattern**: missing value after comparison operator
**Description**: Comparison operator without right operand
**Fix Strategy**: Add placeholder value or remove incomplete comparison
**Example**: `if x >=:`

**Found 1 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py` (Line 87)
```python
84:     """Node to let the LLM judge the quality of its own final answe."""
85:     # End execution if the LLM failed to provide a good answer twice.
86:     num_feedback_requests = state.ge("num_feedback_requests", 0)
>>> 87:     if num_feedback_requests >=:
FIX:     if num_feedback_requests >= 0:
```

### Incomplete Assignment
**Pattern**: missing value after assignment
**Description**: Assignment operator without value
**Fix Strategy**: Add default value or remove line
**Example**: `max_retries =`

**Found 1 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py` (Line 78)
```python
75:         # Perform search with retry logic
76:         search_results = []
77:         retry_count = 0
>>> 78:         max_retries =
FIX:         max_retries = 0  # TODO: Add proper value
```

### Unterminated String
**Pattern**: unterminated string literal
**Description**: String not properly closed
**Fix Strategy**: Close string or fix quotes
**Example**: `print("Hello!"!")`

**Found 66 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py` (Line 111)
```python
108: 
109:     @validate_call
110:     def check_profanity(self, text: str) -> bool:
>>> 111:         for module i["profanity_check", "better_profanit"]:
```

📄 `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py` (Line 137)
```python
134:             focus_area=["methodology", "result", "implication"],
135:         ),
136:         report_config=ReportConfig(
>>> 137:             report_style="comprehensiv", max_categories=8, articles_per_category=),
```

📄 `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py` (Line 118)
```python
115:         if self.statements:
116:             self.total_claims = len(self.statements)
117:             self.confirmed_count = sum(
>>> 118:                 for s in self.statements if s.statu == "confirmed"
```

... and 63 more

### Missing Block
**Pattern**: expected an indented block
**Description**: Missing code block after statement
**Fix Strategy**: Add pass statement or implement block
**Example**: `if condition:
# missing block`

**Found 30 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py` (Line 615)
```python
612:         )
613: 
614:         # Update stage based on validation
>>> 615:         if len(self.validation_results) >= and self.stage == IdeaStage.RESEARCHED:
FIX:         if len(self.validation_results) >= and self.stage == IdeaStage.RESEARCHED:
            pass  # TODO: Implement
```

📄 `packages/haive-agents/tests/test_single_vs_multi.py` (Line 26)
```python
23:     if hasattr(main_engine, "add_tool"):
24:         main_engine.add_tool(add)
25:     else:
>>> 26: react_agent.compile()
FIX: react_agent.compile()
    pass  # TODO: Implement
```

📄 `packages/haive-agents/tests/test_self_discover_agent.py` (Line 99)
```python
96:     success = await test_self_discover_agent()
97: 
98:     if success:
>>> 99:     else:
FIX:     else:
        pass  # TODO: Implement
```

... and 27 more

### Unclosed Parenthesis
**Pattern**: parenthesis was never closed
**Description**: Missing closing parenthesis
**Fix Strategy**: Add closing parenthesis
**Example**: `func(arg1, arg2`

**Found 1 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/journalism_/engines.py` (Line 136)
```python
133: Create a comprehensive summary following the guideline.""")
134:     ])
135: 
>>> 136:     return AugLLMConfig(
```
