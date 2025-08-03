# HAIVE-PREBUILT - Pyright Issues Checklist

**Total Errors**: 489
**Total Warnings**: 0
**Priority**: 📋 Standard

## Summary by Issue Type

### Error Categories

- **reportAttributeAccessIssue**: 111 issues
- **reportOptionalMemberAccess**: 93 issues
- **reportCallIssue**: 70 issues
- **reportMissingImports**: 67 issues
- **reportIndexIssue**: 51 issues
- **reportArgumentType**: 43 issues
- **reportReturnType**: 15 issues
- **reportInvalidTypeForm**: 15 issues
- **reportOperatorIssue**: 11 issues
- **reportGeneralTypeIssues**: 6 issues
- **reportAssignmentType**: 5 issues
- **reportOptionalCall**: 1 issues
- **reportOptionalSubscript**: 1 issues

## 🚨 ERRORS (Must Fix)

### 📄 haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py

- [ ] **Line 185** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "dict[str, Any]\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:185:21`

- [ ] **Line 185** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "type[BaseModel]\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:185:21`

- [ ] **Line 185** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "BaseModel\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:185:21`

- [ ] **Line 185** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "StateSchema[Unknown, Unknown]\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:185:21`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "dict[str, Any]\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:210:37`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "type[BaseModel]\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:210:37`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "BaseModel\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:210:37`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "report_config" for class "StateSchema[Unknown, Unknown]\*"
      Attribute "report_config" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:210:37`

### 📄 haive-prebuilt/src/haive/prebuilt/ai_insight/tools.py

- [ ] **Line 40** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['news', 'general', 'academic', 'business']" cannot be assigned to parameter "topic" of type "Literal['general', 'news', 'finance']" in function "search"
      Type "Literal['news', 'general', 'academic', 'business']" is not assignable to type "Literal['general', 'news', 'finance']"
        Type "Literal['academic']" is not assignable to type "Literal['general', 'news', 'finance']"
          "Literal['academic']" is not assignable to type "Literal['general']"
          "Literal['academic']" is not assignable to type "Literal['news']"
          "Literal['academic']" is not assignable to type "Literal['finance']"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/ai_insight/tools.py:40:18`

### 📄 haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.company_researcher.config" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:4:5`

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.company_researcher.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:5:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.company_researcher.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:9:5`

- [ ] **Line 43** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:43:19`

- [ ] **Line 44** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:44:19`

- [ ] **Line 45** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:45:19`

- [ ] **Line 46** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:46:19`

- [ ] **Line 50** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:50:19`

- [ ] **Line 53** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:53:19`

- [ ] **Line 56** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:56:19`

- [ ] **Line 66** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:66:19`

- [ ] **Line 69** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:69:19`

### 📄 haive-prebuilt/src/haive/prebuilt/company_researcher/config.py

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.company_researcher.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/config.py:5:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.company_researcher.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/config.py:8:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.priv.prompts" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/config.py:11:5`

### 📄 haive-prebuilt/src/haive/prebuilt/company_researcher/engines.py

- [ ] **Line 113** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "additional_notes"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/engines.py:113:15`

### 📄 haive-prebuilt/src/haive/prebuilt/company_researcher/state.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.company_researcher.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/company_researcher/state.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py

- [ ] **Line 159** (`reportArgumentType`)
  - **Issue**: Argument of type "Set[str] | None" cannot be assigned to parameter "iterable" of type "Iterable[_T@list]" in function "**init**"
      Type "Set[str] | None" is not assignable to type "Iterable[str]"
        "None" is incompatible with protocol "Iterable[str]"
          "**iter**" is not present
  - **Location**: `haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py:159:21`

### 📄 haive-prebuilt/src/haive/prebuilt/content/document_extractor.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/document_extractor.py:7:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/document_extractor.py:9:5`

### 📄 haive-prebuilt/src/haive/prebuilt/content/qa_for_rag.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/qa_for_rag.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/content/summarizer.py

- [ ] **Line 1** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/summarizer.py:1:5`

- [ ] **Line 2** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/summarizer.py:2:5`

### 📄 haive-prebuilt/src/haive/prebuilt/content/tagger.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/tagger.py:8:5`

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/content/tagger.py:10:5`

### 📄 haive-prebuilt/src/haive/prebuilt/contract_analysis/agent.py

- [ ] **Line 1** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.base" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/contract_analysis/agent.py:1:5`

- [ ] **Line 2** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.contract_analysis.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/contract_analysis/agent.py:2:5`

### 📄 haive-prebuilt/src/haive/prebuilt/contract_analysis/aug_llms.py

- [ ] **Line 1** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/contract_analysis/aug_llms.py:1:5`

- [ ] **Line 2** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.contract_analysis.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/contract_analysis/aug_llms.py:2:5`

### 📄 haive-prebuilt/src/haive/prebuilt/contract_analysis/state.py

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.contract_analysis.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/contract_analysis/state.py:4:5`

### 📄 haive-prebuilt/src/haive/prebuilt/essay_grading/**init**.py

- [ ] **Line 21** (`reportAttributeAccessIssue`)
  - **Issue**: "Agent" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:21:34`

- [ ] **Line 102** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "with_structured_output" for class "None"
      Attribute "with_structured_output" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:102:28`

- [ ] **Line 142** (`reportOperatorIssue`)
  - **Issue**: Operator "|" not supported for types "PromptTemplate" and "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:142:16`

- [ ] **Line 173** (`reportOperatorIssue`)
  - **Issue**: Operator "|" not supported for types "PromptTemplate" and "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:173:28`

- [ ] **Line 204** (`reportOperatorIssue`)
  - **Issue**: Operator "|" not supported for types "PromptTemplate" and "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:204:26`

- [ ] **Line 244** (`reportReturnType`)
  - **Issue**: Type "dict[str, List[str]]" is not assignable to return type "State"
      "article_text" is required in "State"
      "current_query" is required in "State"
      "chunks" is required in "State"
      "summary_result" is required in "State"
      "fact_check_result" is required in "State"
      "tone_analysis_result" is required in "State"
      "quote_extraction_result" is required in "State"
      "grammar_and_bias_review_result" is required in "State"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:244:11`

- [ ] **Line 261** (`reportReturnType`)
  - **Issue**: Type "dict[str, list[Unknown]]" is not assignable to return type "State"
      "article_text" is required in "State"
      "current_query" is required in "State"
      "chunks" is required in "State"
      "actions" is required in "State"
      "summary_result" is required in "State"
      "tone_analysis_result" is required in "State"
      "quote_extraction_result" is required in "State"
      "grammar_and_bias_review_result" is required in "State"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:261:11`

- [ ] **Line 268** (`reportReturnType`)
  - **Issue**: Type "dict[str, list[Unknown]]" is not assignable to return type "State"
      "article_text" is required in "State"
      "current_query" is required in "State"
      "chunks" is required in "State"
      "actions" is required in "State"
      "summary_result" is required in "State"
      "fact_check_result" is required in "State"
      "quote_extraction_result" is required in "State"
      "grammar_and_bias_review_result" is required in "State"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:268:11`

- [ ] **Line 275** (`reportReturnType`)
  - **Issue**: Type "dict[str, list[Unknown]]" is not assignable to return type "State"
      "article_text" is required in "State"
      "current_query" is required in "State"
      "chunks" is required in "State"
      "actions" is required in "State"
      "summary_result" is required in "State"
      "fact_check_result" is required in "State"
      "tone_analysis_result" is required in "State"
      "grammar_and_bias_review_result" is required in "State"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:275:11`

- [ ] **Line 329** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "with_structured_output" for class "None"
      Attribute "with_structured_output" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:329:38`

- [ ] **Line 367** (`reportReturnType`)
  - **Issue**: Type "dict[str, list[Unknown]]" is not assignable to return type "State"
      "article_text" is required in "State"
      "current_query" is required in "State"
      "chunks" is required in "State"
      "actions" is required in "State"
      "summary_result" is required in "State"
      "fact_check_result" is required in "State"
      "tone_analysis_result" is required in "State"
      "quote_extraction_result" is required in "State"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:367:11`

- [ ] **Line 374** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "values" for class "list[Unknown]"
      Attribute "values" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:374:24`

- [ ] **Line 380** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:380:30`

- [ ] **Line 380** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      "str" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:380:30`

- [ ] **Line 385** (`reportReturnType`)
  - **Issue**: Type "Unknown | list[Unknown]" is not assignable to return type "str"
      Type "Unknown | list[Unknown]" is not assignable to type "str"
        "list[Unknown]" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:385:11`

- [ ] **Line 415** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_node" for class "None"
      Attribute "add_node" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:415:19`

- [ ] **Line 416** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_node" for class "None"
      Attribute "add_node" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:416:19`

- [ ] **Line 417** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_node" for class "None"
      Attribute "add_node" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:417:19`

- [ ] **Line 418** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_node" for class "None"
      Attribute "add_node" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:418:19`

- [ ] **Line 419** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_node" for class "None"
      Attribute "add_node" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:419:19`

- [ ] **Line 420** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_node" for class "None"
      Attribute "add_node" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:420:19`

- [ ] **Line 422** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "set_entry_point" for class "None"
      Attribute "set_entry_point" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:422:19`

- [ ] **Line 424** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edges" for class "None"
      Attribute "add_conditional_edges" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:424:19`

- [ ] **Line 438** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_edge" for class "None"
      Attribute "add_edge" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:438:19`

- [ ] **Line 439** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_edge" for class "None"
      Attribute "add_edge" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:439:19`

- [ ] **Line 440** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_edge" for class "None"
      Attribute "add_edge" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:440:19`

- [ ] **Line 441** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_edge" for class "None"
      Attribute "add_edge" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:441:19`

- [ ] **Line 442** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_edge" for class "None"
      Attribute "add_edge" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:442:19`

### 📄 haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py

- [ ] **Line 19** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:19:19`

- [ ] **Line 20** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:20:19`

- [ ] **Line 21** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:21:19`

- [ ] **Line 22** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:22:19`

- [ ] **Line 23** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:23:19`

- [ ] **Line 26** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:26:19`

- [ ] **Line 30** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "BaseModel\*"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:30:19`

- [ ] **Line 30** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "StateSchema[Unknown, Unknown]\*"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:30:19`

- [ ] **Line 30** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "Any | type[BaseModel]_ | Unknown" and "float"
      Operator ">" not supported for types "type[BaseModel]_" and "float"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:30:19`

- [ ] **Line 34** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:34:19`

- [ ] **Line 38** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "BaseModel\*"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:38:19`

- [ ] **Line 38** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "StateSchema[Unknown, Unknown]\*"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:38:19`

- [ ] **Line 38** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "Any | type[BaseModel]_ | Unknown" and "float"
      Operator ">" not supported for types "type[BaseModel]_" and "float"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:38:19`

- [ ] **Line 42** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:42:19`

- [ ] **Line 46** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "BaseModel\*"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:46:19`

- [ ] **Line 46** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "StateSchema[Unknown, Unknown]\*"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:46:19`

- [ ] **Line 46** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "Any | type[BaseModel]_ | Unknown" and "float"
      Operator ">" not supported for types "type[BaseModel]_" and "float"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:46:19`

- [ ] **Line 50** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:50:19`

- [ ] **Line 55** (`reportOptionalMemberAccess`)
  - **Issue**: "set_entry_point" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:55:19`

- [ ] **Line 58** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:58:19`

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "compile" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:61:30`

### 📄 haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py

- [ ] **Line 6** (`reportAttributeAccessIssue`)
  - **Issue**: "State" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:6:47`

- [ ] **Line 30** (`reportArgumentType`)
  - **Issue**: Argument of type "str | list[str | dict[Unknown, Unknown]]" cannot be assigned to parameter "content" of type "str" in function "extract_score"
      Type "str | list[str | dict[Unknown, Unknown]]" is not assignable to type "str"
        "list[str | dict[Unknown, Unknown]]" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:30:49`

- [ ] **Line 47** (`reportArgumentType`)
  - **Issue**: Argument of type "str | list[str | dict[Unknown, Unknown]]" cannot be assigned to parameter "content" of type "str" in function "extract_score"
      Type "str | list[str | dict[Unknown, Unknown]]" is not assignable to type "str"
        "list[str | dict[Unknown, Unknown]]" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:47:47`

- [ ] **Line 64** (`reportArgumentType`)
  - **Issue**: Argument of type "str | list[str | dict[Unknown, Unknown]]" cannot be assigned to parameter "content" of type "str" in function "extract_score"
      Type "str | list[str | dict[Unknown, Unknown]]" is not assignable to type "str"
        "list[str | dict[Unknown, Unknown]]" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:64:49`

- [ ] **Line 81** (`reportArgumentType`)
  - **Issue**: Argument of type "str | list[str | dict[Unknown, Unknown]]" cannot be assigned to parameter "content" of type "str" in function "extract_score"
      Type "str | list[str | dict[Unknown, Unknown]]" is not assignable to type "str"
        "list[str | dict[Unknown, Unknown]]" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:81:45`

### 📄 haive-prebuilt/src/haive/prebuilt/essay_grading/state.py

- [ ] **Line 18** (`reportGeneralTypeIssues`)
  - **Issue**: Cannot create consistent method ordering
  - **Location**: `haive-prebuilt/src/haive/prebuilt/essay_grading/state.py:18:6`

### 📄 haive-prebuilt/src/haive/prebuilt/journalism\_/engines.py

- [ ] **Line 30** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/engines.py:30:4`

- [ ] **Line 31** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/engines.py:31:4`

### 📄 haive-prebuilt/src/haive/prebuilt/journalism\_/models.py

- [ ] **Line 55** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Keywords for further research if verification is i…'], type[list[Unknown]], Literal[5])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:55:36`

- [ ] **Line 61** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:61:16`

- [ ] **Line 110** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:110:25`

- [ ] **Line 154** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Main points and events from the article'], Literal[3], Literal[7])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:154:29`

- [ ] **Line 194** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:194:21`

- [ ] **Line 198** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Specific examples from text supporting the tone an…'], Literal[1], Literal[5])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:198:42`

- [ ] **Line 208** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:208:23`

- [ ] **Line 374** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:374:27`

- [ ] **Line 378** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:378:23`

- [ ] **Line 382** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:382:16`

- [ ] **Line 386** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['General recommendations for improvement'], type[list[Unknown]], Literal[5])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:386:33`

- [ ] **Line 438** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:438:21`

- [ ] **Line 441** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/models.py:441:32`

### 📄 haive-prebuilt/src/haive/prebuilt/journalism\_/prompts.py

- [ ] **Line 506** (`reportArgumentType`)
  - **Issue**: Argument of type "MessagesPlaceholder" cannot be assigned to parameter "object" of type "tuple[str, str]" in function "append"
      "MessagesPlaceholder" is not assignable to "tuple[str, str]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/prompts.py:506:24`

### 📄 haive-prebuilt/src/haive/prebuilt/journalism\_/tools.py

- [ ] **Line 489** (`reportArgumentType`)
  - **Issue**: Argument of type "int" cannot be assigned to parameter "callbacks" of type "Callbacks" in function "**call**"
      Type "int" is not assignable to type "Callbacks"
        "int" is not assignable to "list[BaseCallbackHandler]"
        "int" is not assignable to "BaseCallbackManager"
        "int" is not assignable to "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:489:42`

- [ ] **Line 495** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['url']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['url']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['url']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['url']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:495:47`

- [ ] **Line 497** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['success']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['success']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['success']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['success']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:497:15`

- [ ] **Line 499** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['content']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['content']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['content']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['content']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:499:24`

- [ ] **Line 504** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['title']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['title']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['title']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['title']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:504:33`

- [ ] **Line 505** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['url']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['url']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['url']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['url']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:505:31`

- [ ] **Line 507** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['word_count']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['word_count']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['word_count']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['word_count']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:507:38`

- [ ] **Line 508** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "str"
      Attribute "get" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:508:41`

- [ ] **Line 515** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['title']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['title']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['title']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['title']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:515:33`

- [ ] **Line 516** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['url']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['url']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['url']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['url']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:516:31`

- [ ] **Line 517** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['snippet']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['snippet']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['snippet']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['snippet']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:517:35`

- [ ] **Line 518** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['snippet']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['snippet']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['snippet']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['snippet']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:518:42`

- [ ] **Line 519** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "str"
      Attribute "get" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:519:41`

- [ ] **Line 524** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['url']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['url']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['url']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['url']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:524:45`

### 📄 haive-prebuilt/src/haive/prebuilt/misc/**init**.py

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.misc.agent_utilities_models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/misc/__init__.py:19:5`

- [ ] **Line 50** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.misc.agent_utilities_prompts" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/misc/__init__.py:50:5`

### 📄 haive-prebuilt/src/haive/prebuilt/misc/agent_management/goal_decompisition/**init**.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.misc.agent_management.goal_decompisition.agent_utilities_models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/misc/agent_management/goal_decompisition/__init__.py:10:5`

### 📄 haive-prebuilt/src/haive/prebuilt/open_researcher/models.py

- [ ] **Line 26** (`reportAssignmentType`)
  - **Issue**: Type "None" is not assignable to declared type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/open_researcher/models.py:26:24`

### 📄 haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.agents.perplexity.base.prompts" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:15:5`

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.agents.perplexity.base.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:16:5`

- [ ] **Line 21** (`reportMissingImports`)
  - **Issue**: Import "haive.agents.perplexity.labs.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:21:5`

- [ ] **Line 25** (`reportMissingImports`)
  - **Issue**: Import "haive.agents.perplexity.pro.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:25:5`

- [ ] **Line 26** (`reportMissingImports`)
  - **Issue**: Import "haive.agents.perplexity.research.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:26:5`

- [ ] **Line 103** (`reportReturnType`)
  - **Issue**: Type "TavilySearchResults" is not assignable to return type "StructuredTool"
      "TavilySearchResults" is not assignable to "StructuredTool"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:103:11`

- [ ] **Line 234** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:234:12`

- [ ] **Line 235** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:235:12`

- [ ] **Line 330** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:330:12`

- [ ] **Line 331** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:331:12`

- [ ] **Line 343** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:343:50`

- [ ] **Line 343** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:343:67`

- [ ] **Line 365** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:365:54`

- [ ] **Line 365** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:365:71`

- [ ] **Line 378** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:378:50`

- [ ] **Line 378** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:378:67`

- [ ] **Line 428** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:428:50`

- [ ] **Line 428** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:428:67`

- [ ] **Line 440** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:440:50`

- [ ] **Line 440** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:440:67`

- [ ] **Line 457** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:457:50`

- [ ] **Line 457** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:457:67`

- [ ] **Line 469** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:469:50`

- [ ] **Line 469** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:469:67`

- [ ] **Line 481** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:481:50`

- [ ] **Line 481** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:481:67`

- [ ] **Line 498** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:498:50`

- [ ] **Line 498** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:498:67`

- [ ] **Line 510** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:510:50`

- [ ] **Line 510** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:510:67`

### 📄 haive-prebuilt/src/haive/prebuilt/podcast_generator/agent.py

- [ ] **Line 20** (`reportGeneralTypeIssues`)
  - **Issue**: Argument to class must be a base class
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/agent.py:20:28`

- [ ] **Line 25** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "graph" for class "None"
      Attribute "graph" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/agent.py:25:49`

- [ ] **Line 27** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "graph" for class "None"
      Attribute "graph" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/agent.py:27:61`

### 📄 haive-prebuilt/src/haive/prebuilt/podcast_generator/interview/agent.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "prebuilt.podcast_generator.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/interview/agent.py:3:5`

- [ ] **Line 16** (`reportGeneralTypeIssues`)
  - **Issue**: Argument to class must be a base class
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/interview/agent.py:16:21`

### 📄 haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py

- [ ] **Line 3** (`reportAttributeAccessIssue`)
  - **Issue**: "Send" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:3:28`

- [ ] **Line 20** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:20:12`

- [ ] **Line 33** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:33:24`

- [ ] **Line 39** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:39:15`

- [ ] **Line 40** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:40:12`

- [ ] **Line 49** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "send_message" for class "None"
      Attribute "send_message" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:49:27`

- [ ] **Line 55** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:55:15`

- [ ] **Line 56** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:56:12`

- [ ] **Line 66** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "send_message" for class "None"
      Attribute "send_message" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:66:26`

- [ ] **Line 72** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:72:15`

- [ ] **Line 73** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:73:12`

- [ ] **Line 83** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "send_message" for class "None"
      Attribute "send_message" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:83:31`

- [ ] **Line 90** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:90:14`

- [ ] **Line 92** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:92:8`

- [ ] **Line 96** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PodcastGeneratorState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:96:10`

### 📄 haive-prebuilt/src/haive/prebuilt/project_manager/agent.py

- [ ] **Line 1** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.project_manager.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/project_manager/agent.py:1:5`

- [ ] **Line 4** (`reportAttributeAccessIssue`)
  - **Issue**: "llm" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/project_manager/agent.py:4:52`

- [ ] **Line 4** (`reportAttributeAccessIssue`)
  - **Issue**: "schedule_llm" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/project_manager/agent.py:4:57`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_batch.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_batch.py:8:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.simple.query.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_batch.py:9:5`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_decomposer.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_decomposer.py:6:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_decomposer.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_enhance.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_enhance.py:7:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_enhance.py:9:5`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_intent.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_intent.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_rewriter.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_rewriter.py:6:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_rewriter.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_to_sql.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_to_sql.py:6:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_to_sql.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/query/query_type_detector.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_type_detector.py:6:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.simple.factory" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/query/query_type_detector.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/agent.py

- [ ] **Line 18** (`reportGeneralTypeIssues`)
  - **Issue**: Argument to class must be a base class
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/agent.py:18:27`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/example.py

- [ ] **Line 29** (`reportOptionalMemberAccess`)
  - **Issue**: "content" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/example.py:29:36`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/models.py

- [ ] **Line 19** (`reportReturnType`)
  - **Issue**: Function with declared return type "dict[Unknown, Unknown]" must return value on all code paths
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/models.py:19:50`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py

- [ ] **Line 18** (`reportAttributeAccessIssue`)
  - **Issue**: "AgentState" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:18:56`

- [ ] **Line 20** (`reportAttributeAccessIssue`)
  - **Issue**: "format_tools_description" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:20:4`

- [ ] **Line 35** (`reportAssignmentType`)
  - **Issue**: Type "\_DictOrPydantic[Unknown]" is not assignable to declared type "DecisionMakingOutput"
      Type "\_DictOrPydantic[Unknown]" is not assignable to type "DecisionMakingOutput"
        "Dict[Unknown, Unknown]" is not assignable to "DecisionMakingOutput"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:35:37`

- [ ] **Line 40** (`reportArgumentType`)
  - **Issue**: Argument of type "list[AIMessage]" cannot be assigned to parameter "value" of type "bool" in function "**setitem**"
      "list[AIMessage]" is not assignable to "bool"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:40:8`

- [ ] **Line 109** (`reportAssignmentType`)
  - **Issue**: Type "\_DictOrPydantic[Unknown]" is not assignable to declared type "JudgeOutput"
      Type "\_DictOrPydantic[Unknown]" is not assignable to type "JudgeOutput"
        "Dict[Unknown, Unknown]" is not assignable to "JudgeOutput"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:109:28`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/state.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.haive.utils.message_utils" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/state.py:7:5`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py

- [ ] **Line 30** (`reportOptionalCall`)
  - **Issue**: Object of type "None" cannot be called
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py:30:15`

- [ ] **Line 36** (`reportReturnType`)
  - **Issue**: Function with declared return type "str" must return value on all code paths
      "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py:36:32`

### 📄 haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py

- [ ] **Line 5** (`reportAttributeAccessIssue`)
  - **Issue**: "CompiledStateGraph" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:5:28`

- [ ] **Line 8** (`reportAssignmentType`)
  - **Issue**: Type "type[IPython.core.display.Markdown]" is not assignable to declared type "type[haive.prebuilt.scientific_paper_agent.utils.Markdown]"
      "IPython.core.display.Markdown" is not assignable to "haive.prebuilt.scientific_paper_agent.utils.Markdown"
      Type "type[IPython.core.display.Markdown]" is not assignable to type "type[haive.prebuilt.scientific_paper_agent.utils.Markdown]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:8:32`

- [ ] **Line 8** (`reportAssignmentType`)
  - **Issue**: Type "(..., include: Unknown | None = None, exclude: Unknown | None = None, metadata: Unknown | None = None, transient: Unknown | None = None, display_id: Unknown | None = None, raw: bool = False, clear: bool = False) -> (DisplayHandle | None)" is not assignable to declared type "(content: Unknown) -> None"
      Type "(..., include: Unknown | None = None, exclude: Unknown | None = None, metadata: Unknown | None = None, transient: Unknown | None = None, display_id: Unknown | None = None, raw: bool = False, clear: bool = False) -> (DisplayHandle | None)" is not assignable to type "(content: Unknown) -> None"
        Function return type "DisplayHandle | None" is incompatible with type "None"
          Type "DisplayHandle | None" is not assignable to type "None"
            "DisplayHandle" is not assignable to "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:8:42`

### 📄 haive-prebuilt/src/haive/prebuilt/search_and_summarize/example.py

- [ ] **Line 23** (`reportArgumentType`)
  - **Issue**: Argument of type "list[HumanMessage]" cannot be assigned to parameter "messages" of type "MessageList" in function "**init**"
      "list[HumanMessage]" is not assignable to "MessageList"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/example.py:23:17`

- [ ] **Line 106** (`reportArgumentType`)
  - **Issue**: Argument of type "list[HumanMessage]" cannot be assigned to parameter "messages" of type "MessageList" in function "**init**"
      "list[HumanMessage]" is not assignable to "MessageList"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/example.py:106:46`

- [ ] **Line 122** (`reportArgumentType`)
  - **Issue**: Argument of type "list[HumanMessage]" cannot be assigned to parameter "messages" of type "MessageList" in function "**init**"
      "list[HumanMessage]" is not assignable to "MessageList"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/example.py:122:17`

### 📄 haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py

- [ ] **Line 75** (`reportReturnType`)
  - **Issue**: Type "str | list[str | dict[Unknown, Unknown]]" is not assignable to return type "str"
      Type "str | list[str | dict[Unknown, Unknown]]" is not assignable to type "str"
        "list[str | dict[Unknown, Unknown]]" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py:75:27`

### 📄 haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py

- [ ] **Line 19** (`reportCallIssue`)
  - **Issue**: No parameter named "max_results"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:19:37`

- [ ] **Line 67** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "url" of type "HttpUrl" in function "**init**"
      "str" is not assignable to "HttpUrl"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:67:36`

- [ ] **Line 108** (`reportReturnType`)
  - **Issue**: Type "str" is not assignable to return type "SearchResults"
      "str" is not assignable to "SearchResults"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:108:11`

- [ ] **Line 108** (`reportArgumentType`)
  - **Issue**: Argument of type "int" cannot be assigned to parameter "callbacks" of type "Callbacks" in function "**call**"
      Type "int" is not assignable to type "Callbacks"
        "int" is not assignable to "list[BaseCallbackHandler]"
        "int" is not assignable to "BaseCallbackManager"
        "int" is not assignable to "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:108:38`

- [ ] **Line 125** (`reportReturnType`)
  - **Issue**: Type "str" is not assignable to return type "SearchResults"
      "str" is not assignable to "SearchResults"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:125:11`

- [ ] **Line 125** (`reportArgumentType`)
  - **Issue**: Argument of type "int" cannot be assigned to parameter "callbacks" of type "Callbacks" in function "**call**"
      Type "int" is not assignable to type "Callbacks"
        "int" is not assignable to "list[BaseCallbackHandler]"
        "int" is not assignable to "BaseCallbackManager"
        "int" is not assignable to "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:125:34`

- [ ] **Line 142** (`reportArgumentType`)
  - **Issue**: Argument of type "int" cannot be assigned to parameter "callbacks" of type "Callbacks" in function "**call**"
      Type "int" is not assignable to type "Callbacks"
        "int" is not assignable to "list[BaseCallbackHandler]"
        "int" is not assignable to "BaseCallbackManager"
        "int" is not assignable to "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:142:37`

- [ ] **Line 145** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "query" for class "str"
      Attribute "query" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:145:12`

- [ ] **Line 146** (`reportReturnType`)
  - **Issue**: Type "str" is not assignable to return type "SearchResults"
      "str" is not assignable to "SearchResults"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:146:11`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/agent.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.business_model_subgraph" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:16:5`

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.ideation_subgraph" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:19:5`

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.market_research_subgraph" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:22:5`

- [ ] **Line 26** (`reportAttributeAccessIssue`)
  - **Issue**: "IdeaCategory" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:26:4`

- [ ] **Line 27** (`reportAttributeAccessIssue`)
  - **Issue**: "IdeaPortfolio" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:27:4`

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "StartupIdea" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:28:4`

- [ ] **Line 29** (`reportAttributeAccessIssue`)
  - **Issue**: "create_basic_idea" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:29:4`

- [ ] **Line 31** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.pitch_deck_models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:31:5`

- [ ] **Line 32** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.pitch_deck_subgraph" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:32:5`

- [ ] **Line 232** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "raw_ideas" for class "MasterStartupState"
      Attribute "raw_ideas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:232:53`

- [ ] **Line 236** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "raw_ideas" for class "MasterStartupState"
      Attribute "raw_ideas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:236:38`

- [ ] **Line 258** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "raw_ideas" for class "MasterStartupState"
      Attribute "raw_ideas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:258:49`

- [ ] **Line 265** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "market_research" for class "MasterStartupState"
      Attribute "market_research" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:265:59`

- [ ] **Line 267** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "market_research" for class "MasterStartupState"
      Attribute "market_research" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:267:33`

- [ ] **Line 268** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "market_research" for class "MasterStartupState"
      Attribute "market_research" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:268:41`

- [ ] **Line 269** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "market_research" for class "MasterStartupState"
      Attribute "market_research" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:269:51`

- [ ] **Line 270** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "go_no_go_recommendation" for class "MasterStartupState"
      Attribute "go_no_go_recommendation" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:270:38`

- [ ] **Line 272** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "market_size_validated" for class "MasterStartupState"
      Attribute "market_size_validated" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:272:52`

- [ ] **Line 276** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "market_research" for class "MasterStartupState"
      Attribute "market_research" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:276:64`

- [ ] **Line 280** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "business_model_canvas" for class "MasterStartupState"
      Attribute "business_model_canvas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:280:65`

- [ ] **Line 282** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "business_model_canvas" for class "MasterStartupState"
      Attribute "business_model_canvas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:282:45`

- [ ] **Line 283** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "business_model_canvas" for class "MasterStartupState"
      Attribute "business_model_canvas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:283:41`

- [ ] **Line 285** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "idea_metrics" for class "MasterStartupState"
      Attribute "idea_metrics" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:285:30`

- [ ] **Line 285** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "idea_metrics" for class "MasterStartupState"
      Attribute "idea_metrics" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:285:66`

- [ ] **Line 292** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "business_model_canvas" for class "MasterStartupState"
      Attribute "business_model_canvas" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:292:63`

- [ ] **Line 293** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "idea_metrics" for class "MasterStartupState"
      Attribute "idea_metrics" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:293:56`

- [ ] **Line 297** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "pitch_deck" for class "MasterStartupState"
      Attribute "pitch_deck" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:297:54`

- [ ] **Line 298** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "pitch_deck" for class "MasterStartupState"
      Attribute "pitch_deck" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/agent.py:298:54`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/business_model/prompts.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.core.models.llm.azure" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/business_model/prompts.py:8:5`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py

- [ ] **Line 260** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "float | None" and "float | None"
      Operator ">" not supported for types "float" and "None"
      Operator ">" not supported for types "None" and "float"
      Operator ">" not supported for types "None" and "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:260:15`

- [ ] **Line 265** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "float | None" and "float | None"
      Operator ">" not supported for types "float" and "None"
      Operator ">" not supported for types "None" and "float"
      Operator ">" not supported for types "None" and "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:265:15`

- [ ] **Line 751** (`reportCallIssue`)
  - **Issue**: No overloads for "sorted" match the provided arguments
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:751:15`

- [ ] **Line 752** (`reportArgumentType`)
  - **Issue**: Argument of type "(x: StartupIdea) -> (float | None)" cannot be assigned to parameter "key" of type "(\_T@sorted) -> SupportsRichComparison" in function "sorted"
      Type "(x: StartupIdea) -> (float | None)" is not assignable to type "(StartupIdea) -> SupportsRichComparison"
        Function return type "float | None" is incompatible with type "SupportsRichComparison"
          Type "float | None" is not assignable to type "SupportsRichComparison"
            Type "None" is not assignable to type "SupportsRichComparison"
              "None" is incompatible with protocol "SupportsDunderLT[Any]"
              "None" is incompatible with protocol "SupportsDunderGT[Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:752:30`

- [ ] **Line 752** (`reportOptionalMemberAccess`)
  - **Issue**: "overall_score" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:752:50`

- [ ] **Line 793** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "emotional_impact", "financial_impact", "validation_score"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:793:11`

- [ ] **Line 810** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "technical_feasibility", "implementation_complexity", "wow_factor"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:810:23`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/market_research/agent.py

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.market_research.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/market_research/agent.py:13:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.market_research.prompts" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/market_research/agent.py:18:5`

- [ ] **Line 266** (`reportReturnType`)
  - **Issue**: Type "CompiledStateGraph" is not assignable to return type "StateGraph"
      "CompiledStateGraph" is not assignable to "StateGraph"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/market_research/agent.py:266:11`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py

- [ ] **Line 27** (`reportAttributeAccessIssue`)
  - **Issue**: "slide_content_aug_llm" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:27:4`

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "storytelling_aug_llm" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:28:4`

- [ ] **Line 76** (`reportOptionalMemberAccess`)
  - **Issue**: "to_pitch_deck_brief" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:76:35`

- [ ] **Line 79** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "brand_colors", "font_preferences"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:79:38`

- [ ] **Line 108** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "quality_score", "color_scheme", "animation_style"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:108:16`

- [ ] **Line 113** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "subheadline", "call_to_action"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:113:20`

- [ ] **Line 275** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "status" for class "PitchDeck"
      "Literal['REVISION_NEEDED']" is not assignable to "ContentStatus"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:275:30`

- [ ] **Line 289** (`reportOptionalMemberAccess`)
  - **Issue**: "slides" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:289:56`

- [ ] **Line 349** (`reportReturnType`)
  - **Issue**: Type "CompiledStateGraph" is not assignable to return type "StateGraph"
      "CompiledStateGraph" is not assignable to "StateGraph"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:349:11`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py

- [ ] **Line 335** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "headline" for class "BaseModel\*"
      Attribute "headline" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:335:28`

- [ ] **Line 610** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "quality_score", "color_scheme", "animation_style"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:610:20`

- [ ] **Line 615** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "subheadline", "call_to_action", "speaker_notes"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:615:24`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/prompts.py

- [ ] **Line 69** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/prompts.py:69:46`

- [ ] **Line 146** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/prompts.py:146:46`

### 📄 haive-prebuilt/src/haive/prebuilt/startup/prompts.py

- [ ] **Line 23** (`reportAttributeAccessIssue`)
  - **Issue**: "BusinessModelCanvas" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:23:4`

- [ ] **Line 24** (`reportAttributeAccessIssue`)
  - **Issue**: "CompetitorAnalysis" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:24:4`

- [ ] **Line 25** (`reportAttributeAccessIssue`)
  - **Issue**: "IdeaCategory" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:25:4`

- [ ] **Line 26** (`reportAttributeAccessIssue`)
  - **Issue**: "IdeaMetrics" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:26:4`

- [ ] **Line 27** (`reportAttributeAccessIssue`)
  - **Issue**: "MarketResearch" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:27:4`

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "ProblemStatement" is unknown import symbol
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:28:4`

- [ ] **Line 30** (`reportMissingImports`)
  - **Issue**: Import "haive.prebuilt.startup.pitch_deck_models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:30:5`

- [ ] **Line 59** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:59:46`

- [ ] **Line 132** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:132:46`

- [ ] **Line 194** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:194:46`

- [ ] **Line 265** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:265:46`

- [ ] **Line 326** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:326:46`

- [ ] **Line 385** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:385:46`

- [ ] **Line 468** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:468:46`

- [ ] **Line 530** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:530:46`

- [ ] **Line 601** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:601:46`

- [ ] **Line 669** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:669:46`

- [ ] **Line 742** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:742:46`

- [ ] **Line 813** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:813:46`

- [ ] **Line 888** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/startup/prompts.py:888:46`

### 📄 haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py

- [ ] **Line 34** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:34:19`

- [ ] **Line 35** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:35:19`

- [ ] **Line 36** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:36:19`

- [ ] **Line 37** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:37:19`

- [ ] **Line 38** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:38:19`

- [ ] **Line 39** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:39:19`

- [ ] **Line 40** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:40:19`

- [ ] **Line 42** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:42:19`

- [ ] **Line 43** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:43:19`

- [ ] **Line 44** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:44:19`

- [ ] **Line 45** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:45:19`

- [ ] **Line 46** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:46:19`

- [ ] **Line 47** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:47:19`

- [ ] **Line 49** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:49:19`

- [ ] **Line 50** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:50:19`

- [ ] **Line 51** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:51:19`

- [ ] **Line 52** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:52:19`

- [ ] **Line 54** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:54:19`

- [ ] **Line 55** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:55:19`

- [ ] **Line 56** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:56:19`

- [ ] **Line 57** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:57:19`

- [ ] **Line 58** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:58:19`

- [ ] **Line 59** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:59:19`

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:61:19`

- [ ] **Line 62** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:62:19`

- [ ] **Line 63** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:63:19`

- [ ] **Line 64** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:64:19`

- [ ] **Line 65** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:65:19`

- [ ] **Line 66** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:66:19`

- [ ] **Line 68** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:68:19`

- [ ] **Line 69** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:69:19`

- [ ] **Line 70** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:70:19`

- [ ] **Line 71** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:71:19`

- [ ] **Line 72** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:72:19`

- [ ] **Line 73** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:73:19`

- [ ] **Line 74** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:74:19`

- [ ] **Line 76** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:76:19`

- [ ] **Line 86** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:86:19`

- [ ] **Line 87** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:87:19`

- [ ] **Line 89** (`reportOptionalMemberAccess`)
  - **Issue**: "set_entry_point" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:89:19`

### 📄 haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "pymupdf4llm" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:6:7`

- [ ] **Line 49** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "AgentState"
      Attribute "get" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:49:21`

- [ ] **Line 69** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:69:15`

- [ ] **Line 80** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:80:23`

- [ ] **Line 99** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:99:18`

- [ ] **Line 114** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:114:19`

- [ ] **Line 117** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:117:28`

- [ ] **Line 140** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:140:18`

- [ ] **Line 153** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:153:19`

- [ ] **Line 212** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:212:17`

- [ ] **Line 222** (`reportOperatorIssue`)
  - **Issue**: Operator "+=" not supported for types "str" and "str | list[str | dict[Unknown, Unknown]]"
      Operator "+" not supported for types "str" and "list[str | dict[Unknown, Unknown]]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:222:8`

- [ ] **Line 244** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:244:18`

- [ ] **Line 245** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:245:15`

- [ ] **Line 256** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:256:18`

- [ ] **Line 257** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:257:15`

- [ ] **Line 268** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:268:18`

- [ ] **Line 269** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:269:15`

- [ ] **Line 280** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:280:18`

- [ ] **Line 281** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:281:15`

- [ ] **Line 292** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:292:18`

- [ ] **Line 293** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:293:15`

- [ ] **Line 304** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:304:18`

- [ ] **Line 305** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:305:15`

- [ ] **Line 316** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:316:15`

- [ ] **Line 317** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:317:19`

- [ ] **Line 318** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:318:14`

- [ ] **Line 319** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:319:14`

- [ ] **Line 320** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:320:17`

- [ ] **Line 321** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:321:17`

- [ ] **Line 332** (`reportOperatorIssue`)
  - **Issue**: Operator "+" not supported for types "str | list[str | dict[Unknown, Unknown]]" and "Literal['\n\n']"
      Operator "+" not supported for types "list[str | dict[Unknown, Unknown]]" and "Literal['\n\n']"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:332:8`

- [ ] **Line 352** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:352:12`

- [ ] **Line 353** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:353:18`

- [ ] **Line 360** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "AgentState"
      Attribute "get" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:360:58`

- [ ] **Line 365** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:365:15`

- [ ] **Line 366** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:366:12`

- [ ] **Line 382** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:382:7`

- [ ] **Line 382** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:382:31`

- [ ] **Line 386** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:386:15`

- [ ] **Line 400** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "AgentState"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:400:21`

### 📄 haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/state.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.haive.utils.message_utils" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/state.py:7:5`

### 📄 haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/tools.py

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.systemic_review_of_scientific_articles.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/tools.py:5:5`

- [ ] **Line 14** (`reportGeneralTypeIssues`)
  - **Issue**: "name" overrides a field of the same name but is missing a default value
  - **Location**: `haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/tools.py:14:4`

### 📄 haive-prebuilt/src/haive/prebuilt/taskifier/agent.py

- [ ] **Line 12** (`reportGeneralTypeIssues`)
  - **Issue**: Argument to class must be a base class
  - **Location**: `haive-prebuilt/src/haive/prebuilt/taskifier/agent.py:12:21`

### 📄 haive-prebuilt/src/haive/prebuilt/tldr2/agent.py

- [ ] **Line 128** (`reportCallIssue`)
  - **Issue**: No parameter named "state_transformer"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:128:16`

- [ ] **Line 141** (`reportCallIssue`)
  - **Issue**: No parameter named "state_transformer"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:141:16`

- [ ] **Line 154** (`reportCallIssue`)
  - **Issue**: No parameter named "state_transformer"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:154:16`

- [ ] **Line 164** (`reportCallIssue`)
  - **Issue**: No parameter named "state_transformer"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:164:16`

- [ ] **Line 174** (`reportCallIssue`)
  - **Issue**: No parameter named "state_transformer"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:174:16`

- [ ] **Line 235** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "source" for class "ArticleContent"
      Attribute "source" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:235:61`

- [ ] **Line 236** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:236:32`

- [ ] **Line 330** (`reportOptionalMemberAccess`)
  - **Issue**: "main_themes" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:330:39`

- [ ] **Line 331** (`reportOptionalMemberAccess`)
  - **Issue**: "key_findings" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:331:34`

- [ ] **Line 332** (`reportOptionalMemberAccess`)
  - **Issue**: "confidence_level" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:332:34`

- [ ] **Line 333** (`reportOptionalMemberAccess`)
  - **Issue**: "data_gaps" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:333:31`

- [ ] **Line 384** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['success']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['success']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['success']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['success']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:384:19`

- [ ] **Line 384** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['word_count']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['word_count']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['word_count']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['word_count']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:384:41`

- [ ] **Line 384** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "str" and "Literal[100]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:384:41`

- [ ] **Line 389** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['content']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['content']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['content']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['content']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:389:29`

- [ ] **Line 390** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['word_count']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['word_count']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['word_count']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['word_count']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:390:35`

- [ ] **Line 390** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "word_count" of type "int | None" in function "**init**"
      Type "str" is not assignable to type "int | None"
        "str" is not assignable to "int"
        "str" is not assignable to "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:390:35`

- [ ] **Line 394** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['word_count']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['word_count']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['word_count']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['word_count']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:394:37`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "AIMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "HumanMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ChatMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "SystemMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "FunctionMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ToolMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "AIMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "HumanMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ChatMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "SystemMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "FunctionMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ToolMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 423** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "list[AnyMessage]"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:423:46`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "AIMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "HumanMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ChatMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "SystemMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "FunctionMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ToolMessage"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "AIMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "HumanMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ChatMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "SystemMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "FunctionMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "ToolMessageChunk"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "parsed" for class "list[AnyMessage]"
      Attribute "parsed" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:483:38`

### 📄 haive-prebuilt/src/haive/prebuilt/tldr2/engines.py

- [ ] **Line 43** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/engines.py:43:25`

- [ ] **Line 43** (`reportCallIssue`)
  - **Issue**: No parameter named "max_tokens"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/engines.py:43:42`

### 📄 haive-prebuilt/src/haive/prebuilt/tldr2/models.py

- [ ] **Line 93** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:93:15`

- [ ] **Line 174** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:174:27`

- [ ] **Line 202** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Bullet-point summary of key points'], Literal[3], Literal[10])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:202:25`

- [ ] **Line 205** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:205:21`

- [ ] **Line 229** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:229:16`

- [ ] **Line 249** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Primary themes identified across articles'], Literal[1])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:249:29`

- [ ] **Line 252** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Most important discoveries from the research'], Literal[1])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:252:30`

- [ ] **Line 259** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:259:22`

- [ ] **Line 293** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Report sections with heading and content'], Literal[2])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:293:37`

- [ ] **Line 297** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (Literal['Actionable recommendations based on research'], Literal[1])
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:297:33`

- [ ] **Line 303** (`reportInvalidTypeForm`)
  - **Issue**: Call expression not allowed in type expression
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/models.py:303:22`

### 📄 haive-prebuilt/src/haive/prebuilt/tldr2/prompts.py

- [ ] **Line 486** (`reportArgumentType`)
  - **Issue**: Argument of type "MessagesPlaceholder" cannot be assigned to parameter "object" of type "tuple[str, str]" in function "append"
      "MessagesPlaceholder" is not assignable to "tuple[str, str]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/prompts.py:486:24`

### 📄 haive-prebuilt/src/haive/prebuilt/tldr2/tools.py

- [ ] **Line 28** (`reportMissingImports`)
  - **Issue**: Import "newsapi" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:28:5`

- [ ] **Line 188** (`reportOptionalMemberAccess`)
  - **Issue**: "get_text" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:188:36`

- [ ] **Line 361** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['success']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['success']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['success']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['success']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:361:65`

### 📄 haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.config" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:10:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:13:5`

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "haive.haive.toolkits.weather" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:22:5`

- [ ] **Line 118** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "val" of type "str" in function "**setitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:118:8`

- [ ] **Line 119** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "val" of type "str" in function "**setitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:119:8`

- [ ] **Line 124** (`reportCallIssue`)
  - **Issue**: Expected 0 positional arguments
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:124:41`

- [ ] **Line 130** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "user" of type "str" in function "login"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:130:25`

- [ ] **Line 130** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "password" of type "str" in function "login"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:130:39`

- [ ] **Line 132** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "from_addr" of type "str" in function "sendmail"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:132:28`

- [ ] **Line 132** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "to_addrs" of type "str | Sequence[str]" in function "sendmail"
      Type "str | None" is not assignable to type "str | Sequence[str]"
        Type "None" is not assignable to type "str | Sequence[str]"
          "None" is not assignable to "str"
          "None" is not assignable to "Sequence[str]"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:132:42`

- [ ] **Line 245** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "city" for class "BaseModel"
      Attribute "city" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:245:21`

- [ ] **Line 245** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "city" for class "dict[Unknown, Unknown]"
      Attribute "city" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:245:21`

- [ ] **Line 246** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "messages" for class "BaseModel"
      Attribute "messages" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:246:14`

- [ ] **Line 246** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "messages" for class "dict[Unknown, Unknown]"
      Attribute "messages" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:246:14`

- [ ] **Line 251** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "city" for class "BaseModel"
      Attribute "city" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:251:34`

- [ ] **Line 251** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "city" for class "dict[Unknown, Unknown]"
      Attribute "city" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:251:34`

- [ ] **Line 252** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "country" for class "BaseModel"
      Attribute "country" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:252:37`

- [ ] **Line 252** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "country" for class "dict[Unknown, Unknown]"
      Attribute "country" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:252:37`

- [ ] **Line 448** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:448:19`

- [ ] **Line 449** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:449:19`

- [ ] **Line 450** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:450:19`

- [ ] **Line 451** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:451:19`

- [ ] **Line 452** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:452:19`

- [ ] **Line 453** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:453:19`

- [ ] **Line 454** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:454:19`

- [ ] **Line 455** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:455:19`

- [ ] **Line 456** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:456:19`

- [ ] **Line 457** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:457:19`

- [ ] **Line 458** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:458:19`

- [ ] **Line 461** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:461:19`

- [ ] **Line 462** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:462:19`

- [ ] **Line 463** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:463:19`

- [ ] **Line 464** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:464:19`

- [ ] **Line 466** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:466:19`

- [ ] **Line 468** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:468:19`

- [ ] **Line 469** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:469:19`

- [ ] **Line 470** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:470:19`

- [ ] **Line 473** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:473:19`

- [ ] **Line 474** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:474:19`

- [ ] **Line 475** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:475:19`

- [ ] **Line 477** (`reportOptionalMemberAccess`)
  - **Issue**: "set_entry_point" is not a known attribute of "None"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:477:19`

- [ ] **Line 525** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "config"
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:525:4`

- [ ] **Line 526** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_weather_emergency_system" for class "Agent[Unknown]"
      Attribute "run_weather_emergency_system" is unknown
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:526:2`

### 📄 haive-prebuilt/src/haive/prebuilt/weather_disaster_management/config.py

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.branches" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/config.py:4:5`

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.engines" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/config.py:5:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.state" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/config.py:13:5`

- [ ] **Line 20** (`reportMissingImports`)
  - **Issue**: Import "haive.haive.toolkits.weather" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/config.py:20:5`

### 📄 haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py

- [ ] **Line 2** (`reportMissingImports`)
  - **Issue**: Import "haive_agents.react_agent2.config2" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:2:5`

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.models" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:3:5`

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive_prebuilt.misc.weather_disaster_management.prompts" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:7:5`

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.haive.tools.search_tools" could not be resolved
  - **Location**: `haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:16:5`

## Fix Priority Guidelines

### High Priority (Fix First)

1. `reportAttributeAccessIssue` - Missing/unknown attributes
2. `reportArgumentType` - Type mismatches in function calls
3. `reportOptionalMemberAccess` - Accessing potentially None objects

### Medium Priority

4. `reportTypedDictNotRequiredAccess` - Unsafe TypedDict access
5. `reportCallIssue` - Function call problems
6. `reportOptionalSubscript` - Subscripting None objects

### Low Priority (Polish)

7. `reportUnusedImport` - Cleanup unused imports
8. `reportUnnecessaryTypeIgnore` - Remove unnecessary ignores

## Testing After Fixes

```bash
# Test imports still work
poetry run python -c "from haive.prebuilt import *; print('✅ Imports OK')"

# Re-run pyright to verify fixes
poetry run pyright packages/haive-prebuilt/src/ --level error

# Run any existing tests
poetry run pytest packages/haive-prebuilt/tests/ -v
```

---

**Generated**: 2025-08-02  
**Source**: `project_docs/build-reports/pyright-issues/haive-prebuilt-*.json`
