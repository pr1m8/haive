# Haive Documentation Style Guide

Comprehensive style guide for consistent, high-quality documentation across the Haive project.

## 🎯 Voice and Tone

### Overall Voice
- **Professional yet approachable** - Technical but not intimidating
- **Helpful and encouraging** - Guide users to success
- **Confident and authoritative** - Based on expertise and testing
- **Inclusive and accessible** - Welcome to all skill levels

### Tone by Content Type

#### **Tutorials and Getting Started**
- Encouraging and supportive
- Step-by-step and patient
- Anticipate and address concerns
- Celebrate small wins

*Example*: "Great! You've successfully created your first agent. Now let's add some tools to make it even more powerful."

#### **API References**
- Precise and factual
- Complete and comprehensive
- Neutral and objective
- Technically accurate

*Example*: "Returns a `StateGraph` instance configured with the specified state schema and execution nodes."

#### **Troubleshooting and Error Handling**
- Calm and solution-focused
- Acknowledge frustration
- Provide clear remedies
- Prevent future issues

*Example*: "This error typically occurs when the configuration is missing required fields. Here's how to fix it:"

## 📝 Language Conventions

### Grammar and Usage

#### **Voice**
- **Use active voice**: "Configure the agent" ✅
- **Avoid passive voice**: "The agent should be configured" ❌

#### **Tense**
- **Present tense for current capabilities**: "The system creates" ✅
- **Future tense only for roadmap items**: "The system will create" ❌

#### **Person**
- **Second person for instructions**: "You can configure" ✅
- **Third person for descriptions**: "The agent processes" ✅
- **Avoid first person plural**: "We recommend" ❌

#### **Contractions**
- **Avoid in formal documentation**: "cannot" not "can't" ✅
- **OK in conversational content**: "Let's get started" ✅

### Terminology Standards

#### **Haive-Specific Terms**
- **Agent** - Capitalize when referring to Haive agents
- **StateGraph** - One word, CamelCase
- **LangGraph** - Official spelling from LangChain
- **haive-core**, **haive-agents** - Lowercase with hyphens

#### **Technical Terms**
- **API** - All caps, no periods
- **JSON** - All caps
- **URL** - All caps
- **ID** - All caps (not "Id" or "id" in prose)

#### **Abbreviations**
- **Spell out on first use**: "Large Language Model (LLM)"
- **Use abbreviation after**: "The LLM processes the input"
- **Don't use periods**: "API" not "A.P.I."

### Spelling and Capitalization

#### **Spelling**
- **American English**: "color", "organize", "analyze"
- **Technical terms**: Follow industry standards
- **Proper nouns**: Follow official spelling

#### **Capitalization**
- **Sentence case for headers**: "Getting started with agents"
- **Title case for proper nouns**: "Haive Framework"
- **Lowercase for common terms**: "agent", "tool", "state"

## 🔤 Formatting Standards

### Headers and Titles

#### **Hierarchy**
```markdown
# Page Title (H1) - Only one per page
## Major Section (H2)
### Subsection (H3)
#### Detail Section (H4)
##### Minor Section (H5) - Rare
###### Micro Section (H6) - Very rare
```

#### **Capitalization**
- **Sentence case**: "Creating your first agent"
- **Not title case**: "Creating Your First Agent" ❌

#### **Content**
- **Descriptive and specific**: "Installing the core package"
- **Not generic**: "Setup" ❌

### Text Formatting

#### **Bold (`**text**`)**
- **UI elements**: Click the **Save** button
- **Important terms on first use**: The **StateGraph** manages execution
- **Warnings and cautions**: **Warning**: This action is irreversible

#### **Italic (`*text*`)**
- **Emphasis**: This is *particularly* important
- **Variable names in prose**: Replace *your_api_key* with your actual key
- **Book/publication titles**: See *Design Patterns* for more information

#### **Code (`code`)**
- **Inline code elements**: Use the `configure()` method
- **File names**: Edit the `config.py` file
- **Command names**: Run the `poetry install` command
- **Variable values**: Set the value to `true`

#### **Code Blocks**
````markdown
```python
# Use language-specific syntax highlighting
def create_agent():
    return SimpleAgent(name="my_agent")
```
````

### Lists and Bullets

#### **Unordered Lists**
```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

#### **Ordered Lists**
```markdown
1. First step
2. Second step
   1. Sub-step
   2. Another sub-step
3. Third step
```

#### **List Content**
- **Parallel structure**: All items same format
- **Complete sentences**: End with periods
- **Fragments**: No ending punctuation
- **Consistent tense**: All present or all imperative

### Links and References

#### **Internal Links**
```markdown
[Link text](../path/to/file.md)
[Section reference](#section-header)
```

#### **External Links**
```markdown
[External resource](https://example.com)
```

#### **Link Text**
- **Descriptive**: "See the configuration guide"
- **Not generic**: "Click here" ❌
- **Not URLs**: "https://..." ❌

## 📋 Content Structure

### Page Organization

#### **Required Elements**
1. **Title** - Clear and descriptive
2. **Introduction** - Purpose and scope
3. **Prerequisites** - What readers need first
4. **Main content** - Organized sections
5. **Examples** - Working code samples
6. **Next steps** - What to do after

#### **Introduction Pattern**
```markdown
# Page Title

Brief description of what this page covers and why it matters.

## What you'll learn
- First key concept
- Second key concept
- Third key concept

## Prerequisites
- Required knowledge
- Required setup
- Required tools
```

### Section Organization

#### **Logical Flow**
1. **Concept introduction**
2. **Basic examples**
3. **Advanced usage**
4. **Configuration options**
5. **Troubleshooting**

#### **Section Length**
- **Sections**: 3-7 paragraphs ideal
- **Paragraphs**: 2-4 sentences
- **Sentences**: 15-20 words average

## ✅ Quick Checklist

### Before Publishing
- [ ] Content is accurate and up-to-date
- [ ] Examples work as written
- [ ] Spelling and grammar checked
- [ ] Links verified and working
- [ ] Formatting consistent
- [ ] Tone appropriate for audience
- [ ] Technical terms defined
- [ ] Prerequisites clearly stated

### Content Quality
- [ ] Serves the intended audience
- [ ] Achieves stated objectives
- [ ] Flows logically from start to finish
- [ ] Includes relevant examples
- [ ] Addresses common questions
- [ ] Provides clear next steps

---

**Remember**: Consistency builds trust. When users can predict how information is presented, they can focus on learning rather than decoding your documentation format.