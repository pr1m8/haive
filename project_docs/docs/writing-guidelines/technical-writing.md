# Technical Writing Best Practices

Advanced techniques for writing clear, effective technical documentation for the Haive project.

## 🎯 Principles of Technical Writing

### 1. **User-Centered Approach**

- **Know your audience** - Write for their skill level and context
- **Answer their questions** - What do they need to accomplish?
- **Provide context** - Why does this matter? When would they use it?
- **Show outcomes** - What will they achieve?

### 2. **Clarity Over Cleverness**

- **Use simple words** - "use" not "utilize", "help" not "facilitate"
- **Short sentences** - One idea per sentence
- **Active voice** - "Configure the agent" not "The agent should be configured"
- **Concrete examples** - Show, don't just tell

### 3. **Progressive Disclosure**

- **Start simple** - Basic concepts first
- **Build complexity** - Layer on advanced features
- **Chunk information** - Break into digestible pieces
- **Provide escapes** - Let users skip ahead or go deeper

## 📝 Writing Techniques

### Information Architecture

#### **Inverted Pyramid Structure**

```
Most Important Information
↓
Supporting Details
↓
Background Context
```

Example:

````markdown
# Creating Agents

Create a SimpleAgent to get started with Haive.

## Quick Start

```python
agent = SimpleAgent(name="helper")
result = agent.invoke({"input": "Hello"})
```
````

## Configuration Options

Advanced configuration allows you to customize...

## Implementation Details

The SimpleAgent class extends the base Agent...

````

#### **Layered Documentation**
1. **Overview** - High-level concept
2. **Quick Start** - Immediate success
3. **Common Patterns** - Typical usage
4. **Advanced Features** - Full capabilities
5. **Reference** - Complete details

### Explanatory Techniques

#### **Scaffolding**
Build understanding step by step:

```markdown
## Understanding Agent State

Agents maintain state throughout their execution. Think of state as the agent's "memory" of what has happened so far.

### Basic State
At minimum, state includes the conversation messages:
```python
state = {"messages": [HumanMessage(content="Hello")]}
````

### Extended State

You can add custom fields for your specific needs:

```python
state = {
    "messages": [...],
    "user_id": "user123",
    "preferences": {"language": "en"}
}
```

### State Schema

Define structure with Pydantic for validation:

```python
class MyAgentState(StateSchema):
    messages: List[BaseMessage]
    user_id: str
    preferences: dict = {}
```

````

#### **Analogies and Metaphors**
Make complex concepts accessible:

```markdown
## Agent Workflows as Recipes

Think of an agent workflow like a recipe:

- **Ingredients** (Input): The user's request and context
- **Steps** (Nodes): Each processing stage
- **Kitchen Tools** (Tools): External capabilities
- **Final Dish** (Output): The completed response

Just as a recipe can have variations (add spices, substitute ingredients), agent workflows can be customized for different use cases.
````

### Clarity Techniques

#### **Signposting**

Help readers navigate:

```markdown
This guide covers three approaches to agent configuration:

1. **Code-based configuration** - Direct instantiation (recommended for simple cases)
2. **File-based configuration** - YAML/JSON files (best for complex setups)
3. **Environment-based configuration** - Environment variables (ideal for deployment)

We'll start with code-based configuration, then show how to migrate to file-based approaches for more complex scenarios.
```

#### **Transitions**

Connect ideas smoothly:

- **Sequential**: "Next, we'll configure the tools..."
- **Causal**: "Because of this behavior, you should..."
- **Comparative**: "Unlike the previous approach, this method..."
- **Amplifying**: "More importantly, this enables..."

## 🎨 Language and Style

### Sentence Construction

#### **Sentence Length**

- **Ideal**: 15-20 words
- **Maximum**: 25 words
- **Complex ideas**: Break into multiple sentences

```markdown
Good:
Configure the agent with tools. This enables external data access.

Poor:
Configure the agent with tools to enable external data access which allows the agent to retrieve information from web services and databases.
```

#### **Parallel Structure**

Keep similar elements consistent:

```markdown
Good:

- Create the agent
- Configure the tools
- Test the setup

Poor:

- Create the agent
- Tool configuration
- Testing should be performed
```

### Word Choice

#### **Precision**

Choose exact words:

```markdown
Precise: "The agent processes the input"
Vague: "The agent handles the input"

Precise: "Returns a StateGraph instance"
Vague: "Returns the result"
```

#### **Concision**

Eliminate unnecessary words:

```markdown
Concise: "Configure the timeout"
Wordy: "In order to configure the timeout setting"

Concise: "This enables caching"
Wordy: "This feature provides the capability to enable caching"
```

### Technical Accuracy

#### **Consistency**

Use the same terms throughout:

```markdown
Consistent:

- "agent" (always lowercase)
- "StateGraph" (always CamelCase)
- "configuration" (not "config" in prose)

Inconsistent:

- "agent" vs "Agent" vs "AGENT"
- "StateGraph" vs "stategraph" vs "state graph"
```

#### **Precision in Instructions**

Be exact about what to do:

```markdown
Precise:

1. Install the package: `poetry add haive-core`
2. Import the SimpleAgent class: `from haive.agents.simple import SimpleAgent`
3. Create an instance: `agent = SimpleAgent(name="helper")`

Imprecise:

1. Get the package
2. Import what you need
3. Set up an agent
```

## 📋 Content Organization

### Information Hierarchy

#### **Logical Grouping**

Group related information:

```markdown
## Agent Configuration

### Basic Configuration

Core settings every agent needs...

### Tool Configuration

Adding external capabilities...

### Advanced Configuration

Fine-tuning for specific use cases...
```

#### **Dependency Order**

Present information in dependency order:

```markdown
## Getting Started

### Prerequisites

Before creating agents, ensure you have...

### Installation

Install the required packages...

### Basic Setup

Create your first agent...

### Adding Tools

Extend your agent with tools...
```

### Cross-References

#### **Internal Linking**

Connect related concepts:

```markdown
Agents use [tools](../tools/overview.md) to access external capabilities. For more details on tool configuration, see the [Tool Configuration Guide](./tool-configuration.md).
```

#### **Contextual References**

Provide context for links:

```markdown
If you're new to agent concepts, start with the [Agent Overview](overview.md) before diving into configuration details.

For production deployments, also review the [Security Guidelines](../security/overview.md) to ensure proper authentication handling.
```

## 🧪 Testing Your Writing

### Readability Tests

#### **The Skim Test**

Can readers understand the main points by skimming?

- Clear headings
- Bullet points for key information
- Important terms emphasized
- Code examples visible

#### **The Fresh Eyes Test**

Have someone unfamiliar with the topic read your draft:

- Do they understand the purpose?
- Can they follow the instructions?
- What questions do they have?
- Where do they get confused?

#### **The Context Switch Test**

Can someone interrupted mid-reading pick up where they left off?

- Clear section boundaries
- Recap important context
- Self-contained sections
- Progress indicators

### Accuracy Validation

#### **Technical Review**

- Code examples work as written
- API calls are current
- Dependencies are correct
- Configuration is valid

#### **User Testing**

- New users can follow instructions
- Examples solve real problems
- Troubleshooting covers common issues
- Next steps are clear

## 🎯 Special Considerations

### API Documentation

#### **Parameter Descriptions**

Be specific about requirements:

```markdown
Args:
name: Agent identifier. Must be alphanumeric characters only,
1-50 characters in length. Used for logging and debugging.
config: Optional configuration object. If None, uses default
settings with temperature=0.7 and max_tokens=1000.
tools: List of tool instances. Each tool must implement the
Tool protocol. Maximum 10 tools per agent.
```

#### **Return Value Documentation**

Explain the structure:

```markdown
Returns:
AgentResult containing: - messages: List of processed messages including the final response - metadata: Execution metadata with timing and tool usage information - state: Final agent state after processing, including any updates
```

### Error Documentation

#### **Error Context**

Explain when errors occur:

```markdown
Raises:
ValidationError: When input_data doesn't match the agent's state schema.
Common causes: missing required fields, incorrect data types.

    ExecutionError: When the agent encounters an unrecoverable error during
                   processing. This may indicate LLM service issues or tool failures.

    TimeoutError: When execution exceeds the configured timeout (default 30s).
                 Consider increasing timeout for complex workflows.
```

### Tutorial Writing

#### **Learning Objectives**

Start with clear outcomes:

```markdown
# Building Your First Agent

By the end of this tutorial, you'll have:

- Created a working SimpleAgent
- Added web search capabilities
- Tested the agent with realistic queries
- Understood the basic agent workflow
```

#### **Success Criteria**

Define what success looks like:

```markdown
## Verification

If everything worked correctly, you should see:

1. The agent responds to your query
2. Tool usage appears in the logs
3. The response includes search results
4. No error messages in the output
```

## ✅ Quality Checklist

### Content Quality

- [ ] Serves a clear purpose
- [ ] Appropriate for the target audience
- [ ] Logically organized
- [ ] Technically accurate
- [ ] Examples work as written
- [ ] Covers common edge cases

### Writing Quality

- [ ] Clear and concise language
- [ ] Active voice used
- [ ] Consistent terminology
- [ ] Proper grammar and spelling
- [ ] Appropriate tone
- [ ] Good flow between sections

### Usability

- [ ] Easy to scan and navigate
- [ ] Clear headings and structure
- [ ] Working links
- [ ] Helpful cross-references
- [ ] Clear next steps
- [ ] Search-friendly formatting

---

**Remember**: Great technical writing serves the reader's goals, not the writer's ego. Every word should help users accomplish their objectives more effectively.
