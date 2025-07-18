# Design Decisions

## Module Purpose Identified

**Decision**: The document_modifiers module is for transforming and extracting structured information from documents

**Rationale**: Based on code analysis, the module contains:

- TNT: Taxonomy generation from conversation histories
- Complex Extraction: Structured data extraction with validation
- Summarizer: Map-reduce document summarization
- KG: Knowledge graph construction from documents

**Trade-offs**: Keeping all document transformation agents in one module vs splitting

- Pro: Logical grouping of document-focused agents
- Con: Module is getting large with many submodules

## Documentation Approach

**Decision**: Document actual functionality found in code, not placeholder text

**Rationale**: The existing READMEs are all TODOs, but the code shows clear purpose

- Each agent has specific use cases and examples
- Code quality is good but documentation is missing

**Alternative**: Wait for original developers to document

- Rejected: Code is mature enough to document now

## Module Organization

**Decision**: Keep current structure but add clear hierarchy documentation

**Rationale**:

- Base module provides shared state (DocumentModifierState)
- Each submodule is independent but shares common document processing theme
- Structure makes sense once documented properly
