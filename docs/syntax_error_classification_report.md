# Syntax Error Classification Report
Generated: 2025-07-28 14:28:39
## Summary
Total errors found: 65

### By Category:
- **incomplete_variable**: 1 errors
- **missing_block**: 3 errors
- **unknown**: 1 errors
- **unterminated_string**: 60 errors

## Examples by Category

### Unterminated String
**Pattern**: unterminated string literal
**Description**: String not properly closed
**Fix Strategy**: Close string or fix quotes
**Example**: `print("Hello!"!")`

**Found 60 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/tldr2/tools.py` (Line 198)
```python
195:             soup.find("article"),
196:             soup.find("div", class_="article-content"),
197:             soup.find("div", class_="entry-content"),
>>> 198:             soup.find("div", class ="post-content"),
```

📄 `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py` (Line 289)
```python
286:     print()
287:     return {"reference": [response]}
288:     def aggregator(state: AgentState):
>>> 289:     print("AGGREGATMake a title for this systematic review based on the abstract. Write it in markdow."),
```

📄 `packages/haive-prebuilt/src/haive/prebuilt/startup/prompts.py` (Line 938)
```python
935:     market_agent = market_research_aug_llm.create_runnable()
936:     market_research = market_agent.invoke(
937:         {
>>> 938:             "idea_nam": ideas.ideas[]["nam"],
```

... and 57 more

### Missing Block
**Pattern**: expected an indented block
**Description**: Missing code block after statement
**Fix Strategy**: Add pass statement or implement block
**Example**: `if condition:
# missing block`

**Found 3 instances:**

📄 `packages/haive-agents/tests/persistence/verify_message_quality.py` (Line 112)
```python
109:                 sslmode = match.group(1)
110: 
111:                 if sslmode == "require":
>>> 112:         else:
FIX:         else:
            pass  # TODO: Implement
```

📄 `packages/haive-agents/tests/utilities/view_metadata_details.py` (Line 130)
```python
127:                                 pass
128: 
129:                         except Exception as e:
>>> 130:                     else:
FIX:                     else:
                        pass  # TODO: Implement
```

📄 `packages/haive-agents/tests/integration/supabase/fix_prepared_statements.py` (Line 76)
```python
73:                 count = (await cur.fetchone())[0]
74: 
75:                 if count > 0:
>>> 76:                 else:
FIX:                 else:
                    pass  # TODO: Implement
```

### Incomplete Variable
**Pattern**: incomplete variable name
**Description**: Variable name cut off or typo
**Fix Strategy**: Complete variable name
**Example**: `state.revision_coun`

**Found 1 instances:**

📄 `packages/haive-prebuilt/src/haive/prebuilt/perplexity/base/state.py` (Line 240)
```python
237:         """Add a search result to the stat."""
238:         self.search_results.append(result)
239:         self.search_iteration += 1
>>> 240:         self.performance_metrics.total_searches += 1        self.performance_metrics.documents_processed += len(result.documents)
```
