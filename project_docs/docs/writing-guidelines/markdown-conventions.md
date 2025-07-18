# Markdown Conventions

Standardized Markdown formatting rules for the Haive project documentation.

## 📋 File Structure

### Required Elements

Every Markdown file should include:

```markdown
# Page Title

Brief description of the page content.

## Table of Contents (optional for long pages)

- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1

Content...

## Next Steps

What to do after reading this page.

---

Footer note if applicable.
```

### File Naming

- **Lowercase with hyphens**: `getting-started.md`
- **Descriptive names**: `agent-configuration-guide.md`
- **Not abbreviated**: `configuration-guide.md` not `config-guide.md`

## 🔤 Heading Standards

### Hierarchy Rules

```markdown
# Page Title (H1) - Only one per page

## Major Section (H2)

### Subsection (H3)

#### Detail Section (H4)

##### Minor Section (H5) - Use sparingly

###### Micro Section (H6) - Avoid if possible
```

### Capitalization

- **Sentence case**: `## Getting started with agents`
- **Not title case**: `## Getting Started With Agents` ❌

### Content Guidelines

- **Descriptive**: `## Installing the core package`
- **Not generic**: `## Setup` ❌
- **Action-oriented**: `## Creating your first agent`

## 🎨 Text Formatting

### Bold (`**text**`)

Use for:

- **UI elements**: Click the **Save** button
- **Important terms**: The **StateGraph** manages execution
- **Warnings**: **Warning**: This action cannot be undone
- **File names**: Edit the **config.py** file

### Italic (`*text*`)

Use for:

- **Emphasis**: This is _particularly_ important
- **Variables in text**: Replace _your_api_key_ with your key
- **Book titles**: See _Design Patterns_ for more details

### Code (`code`)

Use for:

- **Inline code**: Use the `configure()` method
- **Commands**: Run `poetry install`
- **Values**: Set to `true`
- **File paths**: Edit `src/config.py`

### Strikethrough (`~~text~~`)

Use sparingly for:

- **Deprecated features**: ~~This method is deprecated~~
- **Corrections**: ~~Incorrect~~ Correct information

## 📝 Code Blocks

### Language Specification

Always specify the language:

````markdown
```python
def create_agent():
    return SimpleAgent(name="my_agent")
```

```bash
poetry install
poetry run python script.py
```

```yaml
name: my_agent
type: simple
tools:
  - web_search
  - calculator
```

```json
{
  "name": "my_agent",
  "type": "simple",
  "tools": ["web_search"]
}
```
````

### Code Block Guidelines

- **Complete examples**: Include imports and setup
- **Working code**: Test before publishing
- **Comments**: Explain complex parts
- **Realistic**: Solve actual problems

## 📋 Lists and Tables

### Unordered Lists

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

### Ordered Lists

```markdown
1. First step
2. Second step
   1. Sub-step
   2. Another sub-step
3. Third step
```

### List Formatting Rules

- **Consistent punctuation**: All items with periods or none
- **Parallel structure**: All items same grammatical form
- **Proper nesting**: Use 2-space indentation

### Tables

```markdown
| Feature | Description       | Status         |
| ------- | ----------------- | -------------- |
| Agents  | Core agent system | ✅ Complete    |
| Tools   | Tool integration  | 🚧 In Progress |
| Docs    | Documentation     | 📋 Planned     |
```

### Table Guidelines

- **Headers**: Always include table headers
- **Alignment**: Use pipes to align columns
- **Content**: Keep cells concise
- **Formatting**: Use emojis sparingly for status

## 🔗 Links and References

### Internal Links

```markdown
[Link text](../path/to/file.md)
[Section reference](#section-header)
[Relative path](./subfolder/file.md)
```

### External Links

```markdown
[External resource](https://example.com)
[Documentation](https://docs.example.com/guide)
```

### Link Text Guidelines

- **Descriptive**: `[agent configuration guide](config-guide.md)`
- **Not generic**: `[click here](config-guide.md)` ❌
- **Not URLs**: `[https://example.com](https://example.com)` ❌

### Reference Links

For repeated links:

```markdown
This uses [Agent Framework][agent-framework] and [LangGraph][langgraph].

[agent-framework]: https://github.com/haive/framework
[langgraph]: https://langchain-ai.github.io/langgraph/
```

## 🖼️ Images and Media

### Image Syntax

```markdown
![Alt text](images/screenshot.png)
![Agent workflow](../images/workflow-diagram.svg)
```

### Image Guidelines

- **Alt text**: Always provide descriptive alt text
- **File naming**: Use descriptive, lowercase-with-hyphens
- **Location**: Store in `images/` or `../images/` folder
- **Format**: Prefer SVG for diagrams, PNG for screenshots

### Captions

```markdown
![Agent workflow diagram](images/workflow.svg)
_Figure 1: Agent execution workflow showing state transitions_
```

## 📐 Layout and Structure

### Line Length

- **Soft limit**: 80 characters per line
- **Hard limit**: 100 characters per line
- **Exception**: URLs and code can exceed limits

### Spacing

```markdown
# Title

Introduction paragraph.

## Section Header

Content paragraph with proper spacing.

- List item 1
- List item 2

Another paragraph after the list.
```

### Breaks and Separators

```markdown
---
```

Use horizontal rules sparingly to separate major sections.

## 🎯 Content Organization

### Section Length

- **Sections**: 3-7 paragraphs ideal
- **Paragraphs**: 2-4 sentences
- **Sentences**: 15-20 words average

### Information Hierarchy

```markdown
# Main Topic

## Key Concept

### Implementation Detail

#### Specific Configuration
```

### Cross-References

```markdown
For more information, see:

- [Agent Types](agent-types.md)
- [Configuration Guide](configuration.md)
- [API Reference](../api/agents.md)
```

## ✅ Quality Checklist

### Before Publishing

- [ ] All links work correctly
- [ ] Code examples are tested
- [ ] Images load properly
- [ ] Spelling and grammar checked
- [ ] Consistent formatting applied
- [ ] Proper heading hierarchy
- [ ] Alt text for all images

### Content Standards

- [ ] Clear and descriptive headings
- [ ] Complete code examples
- [ ] Proper link text
- [ ] Consistent terminology
- [ ] Appropriate use of formatting
- [ ] Logical content flow

---

**Remember**: Consistent Markdown formatting makes documentation easier to read, maintain, and automatically process.
