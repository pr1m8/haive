# Collaborative Conversation

Structured multi-agent collaboration for building shared documents, plans, and creative content.

## Overview

The Collaborative Conversation agent orchestrates multiple participants working together to create shared content in a structured, section-based format. Unlike free-form conversations, this agent guides participants through defined sections, ensures balanced contributions, and compiles a cohesive final document. It's ideal for brainstorming sessions, code reviews, project planning, and any scenario requiring structured collaborative output.

## Architecture

```
CollaborativeConversation (extends BaseConversationAgent)
├── Document Structure Management
│   ├── Section Definition & Ordering
│   ├── Progress Tracking
│   └── Document Compilation
├── Contribution System
│   ├── Per-Section Tracking
│   ├── Balanced Participation
│   └── Attribution Management
├── Output Formatting
│   ├── Markdown
│   ├── Code
│   ├── Outline
│   └── Report
└── Review & Approval (Optional)
    ├── Section Completion
    ├── Revision Support
    └── Final Approval
```

## Key Features

- **Structured sections** - Organize collaboration into defined sections
- **Balanced contributions** - Ensure everyone participates in each section
- **Multiple output formats** - Markdown, code, outline, or report styles
- **Attribution tracking** - Know who contributed what
- **Progress monitoring** - Track completion of sections and contributions
- **Flexible workflows** - Support for revisions and approvals
- **Document compilation** - Automatic assembly of final output
- **Smart speaker selection** - Prioritize those who haven't contributed to current section

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Collaborative Document

```python
from haive.agents.conversation import CollaborativeConversation
from haive.agents.simple import SimpleAgent

# Create participants
writer1 = SimpleAgent(name="Alice", role="researcher")
writer2 = SimpleAgent(name="Bob", role="analyst")
writer3 = SimpleAgent(name="Charlie", role="editor")

# Create collaborative session
collaboration = CollaborativeConversation(
    participants=[writer1, writer2, writer3],
    topic="Climate Change Solutions",
    document_title="Comprehensive Climate Action Plan",
    sections=["Problem Analysis", "Proposed Solutions", "Implementation Plan"],
    output_format="markdown",
    min_contributions_per_section=1
)

# Run collaboration
result = await collaboration.arun()
document = result["shared_document"]
```

### Brainstorming Session

```python
# Use the brainstorming factory
session = CollaborativeConversation.create_brainstorming_session(
    topic="New mobile app features",
    participants=["ProductManager", "Designer", "Developer", "Marketer"],
    sections=["User Needs", "Feature Ideas", "Technical Feasibility", "Go-to-Market"]
)

result = await session.arun()
```

### Code Review

```python
# Use the code review factory
review = CollaborativeConversation.create_code_review(
    code_description="Authentication service with OAuth2 and JWT",
    reviewers={
        "SecurityExpert": "security specialist",
        "BackendLead": "architecture expert",
        "PerformanceEngineer": "optimization specialist"
    }
)

result = await review.arun()
```

## Document Sections

### Defining Sections

Sections provide structure to the collaborative process:

```python
# Linear sections (processed in order)
sections = ["Introduction", "Analysis", "Recommendations", "Conclusion"]

# Hierarchical sections (for complex documents)
sections = [
    "Executive Summary",
    "Background",
    "Technical Analysis",
    "Risk Assessment",
    "Implementation Plan",
    "Budget Considerations",
    "Timeline",
    "Success Metrics"
]
```

### Section Completion Rules

1. **Minimum Contributions**: Each participant must contribute at least `min_contributions_per_section` times
2. **Section Progress**: Sections are completed sequentially
3. **Automatic Advancement**: Moves to next section when minimums are met
4. **Revision Support**: Optional ability to revisit completed sections

## Configuration Options

### Core Parameters

```python
CollaborativeConversation(
    participants=agents,
    topic="Project Topic",
    document_title="Final Document Title",
    sections=["Section1", "Section2", "Section3"],

    # Contribution settings
    min_contributions_per_section=1,  # Min per participant per section
    require_approval=False,           # Require approval before section completion
    allow_revisions=True,            # Allow editing completed sections

    # Output settings
    output_format="markdown",        # markdown, code, outline, report
    include_attribution=True,        # Include contributor names

    # Conversation limits
    max_rounds=30                    # Enough for all contributions
)
```

### Output Formats

#### Markdown Format

```markdown
# Document Title

## Section 1

[Alice]: First contribution to section 1
[Bob]: Building on Alice's point...

## Section 2

[Charlie]: Starting section 2 with...
```

#### Code Format

```python
# Document Title
# Collaborative Code

# Section 1
[Alice]: def authenticate_user(token):
[Bob]:     # Validate token format first

# Section 2
[Charlie]: class TokenValidator:
```

#### Outline Format

```
Document Title
=============

Section 1:
[Alice]: Main point about...
[Bob]: Supporting detail...

Section 2:
[Charlie]: Next major topic...
```

#### Report Format

```
DOCUMENT TITLE

SECTION 1

[Alice]: Formal analysis of...
[Bob]: Additional findings indicate...

SECTION 2

[Charlie]: Recommendations based on...
```

## State Management

The CollaborativeState extends ConversationState with collaboration-specific fields:

```python
class CollaborativeState(ConversationState):
    # Document structure
    shared_document: str                    # Compiled document
    document_sections: Dict[str, str]       # Content per section
    sections_order: List[str]               # Section sequence

    # Progress tracking
    current_section: Optional[str]          # Active section
    completed_sections: List[str]           # Finished sections
    section_status: Dict[str, str]          # Status per section

    # Contribution tracking
    contributions: List[Tuple[str, str, str]]  # (speaker, section, content)
    contribution_count: Dict[str, int]         # Total per speaker
    section_contributors: Dict[str, List[str]] # Contributors per section

    # Configuration
    output_format: str                      # Output style
    approval_status: Dict[str, bool]        # Approval tracking
```

## Advanced Usage

### Custom Section Progression

```python
class CustomCollaborativeConversation(CollaborativeConversation):
    """Collaboration with custom section logic."""

    def _check_section_completion(self, state) -> Optional[Command]:
        """Custom completion criteria."""
        current = state.current_section

        # Special handling for conclusion section
        if current == "Conclusion":
            # Require all participants to contribute
            contributors = set()
            for speaker, section, _ in state.contributions:
                if section == current:
                    contributors.add(speaker)

            if len(contributors) < len(state.speakers):
                return None  # Keep section open

        return super()._check_section_completion(state)
```

### Dynamic Section Generation

```python
class AdaptiveCollaboration(CollaborativeConversation):
    """Generate sections based on initial discussion."""

    def __init__(self, *args, **kwargs):
        # Start with high-level sections
        kwargs["sections"] = ["Initial Discussion", "Topics Identified"]
        super().__init__(*args, **kwargs)
        self.topics_identified = []

    def process_response(self, state):
        """Extract topics and create new sections."""
        update = super().process_response(state)

        # In initial discussion, identify topics
        if state.current_section == "Initial Discussion":
            topics = self._extract_topics(state.messages[-1].content)
            if topics and not self.topics_identified:
                self.topics_identified = topics
                # Add new sections dynamically
                new_sections = state.sections_order + topics + ["Summary"]
                update["sections_order"] = new_sections

        return update
```

### Approval Workflow

```python
class ReviewedCollaboration(CollaborativeConversation):
    """Collaboration with approval requirements."""

    def __init__(self, *args, approvers=None, **kwargs):
        kwargs["require_approval"] = True
        super().__init__(*args, **kwargs)
        self.approvers = approvers or []

    def _check_section_completion(self, state):
        """Require approval before moving sections."""
        # Check if section has enough contributions
        base_check = super()._check_section_completion(state)
        if not base_check:
            return None

        # Check if approved
        current = state.current_section
        if not state.approval_status.get(current, False):
            # Request approval
            approval_msg = SystemMessage(
                content=f"Section '{current}' ready for approval. "
                f"Approvers: {', '.join(self.approvers)}"
            )
            return Command(update={"messages": [approval_msg]})

        return base_check
```

### Integration with External Tools

```python
from haive.tools import CodeAnalyzer, GrammarChecker

class ToolAssistedCollaboration(CollaborativeConversation):
    """Collaboration with tool support."""

    def __init__(self, *args, tools=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tools = tools or []

    async def process_contribution(self, content, contributor, section):
        """Enhance contributions with tools."""
        enhanced = content

        # Grammar check for report format
        if self.output_format == "report" and self.grammar_checker:
            enhanced = await self.grammar_checker.improve(content)

        # Code analysis for code format
        if self.output_format == "code" and self.code_analyzer:
            analysis = await self.code_analyzer.analyze(content)
            if analysis.issues:
                enhanced += f"\n# Analysis: {analysis.summary}"

        return enhanced
```

## Best Practices

### 1. Section Design

- Keep sections focused and achievable
- Order sections logically
- Balance section complexity
- Consider participant expertise

### 2. Contribution Balance

- Set appropriate minimums per section
- Monitor participation metrics
- Use speaker selection to balance input
- Allow flexibility for natural flow

### 3. Output Quality

- Choose appropriate output format
- Use attribution for accountability
- Enable revisions for polish
- Consider approval workflows

### 4. Collaboration Flow

- Start with clear objectives
- Provide section-specific guidance
- Allow for iterative refinement
- Summarize at transitions

### 5. Performance

- Set realistic max_rounds
- Monitor document size
- Consider section chunking
- Cache compiled documents

## Common Use Cases

1. **Product Development**
   - Feature brainstorming
   - Requirements gathering
   - Design documentation
   - Sprint planning

2. **Content Creation**
   - Blog post writing
   - Documentation updates
   - Marketing copy
   - Training materials

3. **Technical Reviews**
   - Code reviews
   - Architecture reviews
   - Security assessments
   - Performance audits

4. **Strategic Planning**
   - Business plans
   - Project proposals
   - Risk assessments
   - Roadmap creation

5. **Creative Projects**
   - Story writing
   - Script development
   - Game design
   - Content calendars

## Performance Considerations

- **Document Size**: Compiled documents grow with contributions
- **Section Count**: More sections = more state transitions
- **Attribution Overhead**: Tracking contributors adds memory usage
- **Revision History**: Storing revisions increases state size

## Example Outputs

The module includes example outputs in the `outputs/` directory:

- [Brainstorming Session](outputs/brainstorming.md) - Product ideation example
- [Code Review](outputs/code_review.md) - Technical review example

## Examples

See the [example.py](example.py) file for complete working examples including:

- Brainstorming sessions
- Code reviews
- Project planning
- Research papers
- Creative writing

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/haive/agents/conversation/collaborative/index.rst).

## See Also

- [Base Conversation Agent](../base/README.md) - Core conversation infrastructure
- [Round Robin Conversation](../round_robin/README.md) - Equal participation format
- [Directed Conversation](../directed/README.md) - Mention-based interaction
- [Debate Conversation](../debate/README.md) - Argumentative discussions
- [Social Media Conversation](../social_media/README.md) - Platform-style collaboration
