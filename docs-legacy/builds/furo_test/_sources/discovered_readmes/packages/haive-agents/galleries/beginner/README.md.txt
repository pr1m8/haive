# Beginner Gallery - Your First Steps with Haive Agents

**Difficulty**: ⭐ Beginner  
**Estimated Time**: 15-30 minutes total  
**Prerequisites**: Python 3.12+, Haive installed

## 🎯 Learning Path

Follow these examples in order for the best learning experience:

### 1. **Simple Agent Tutorial** (`simple_agent_tutorial.py`)

- **What you'll learn**: Basic agent creation and conversation
- **Time**: 5 minutes
- **Key concepts**: Agent configuration, basic interactions
- **Next step**: ReactAgent with tools

### 2. **ReactAgent Tutorial** (`react_agent_tutorial.py`)

- **What you'll learn**: Tool-enabled agents and reasoning
- **Time**: 10 minutes
- **Key concepts**: Custom tools, reasoning loops, problem-solving
- **Next step**: Advanced patterns

### 3. **Basic Tools Tutorial** (`basic_tools_tutorial.py`)

- **What you'll learn**: Creating and using custom tools
- **Time**: 10 minutes
- **Key concepts**: Tool decorators, input validation, error handling
- **Next step**: Multi-agent coordination

## 🚀 Quick Start

```bash
# Navigate to the beginner gallery
cd packages/haive-agents/galleries/beginner

# Run your first agent
poetry run python simple_agent_tutorial.py

# Try the ReactAgent with tools
poetry run python react_agent_tutorial.py
```

## 📚 What You'll Learn

By the end of this gallery, you'll understand:

- **Agent Basics**: How to create and configure agents
- **Conversations**: How agents maintain context across interactions
- **Tools**: How to give agents capabilities beyond chat
- **Reasoning**: How ReactAgents think through problems
- **Error Handling**: How to build robust agent applications

## 🎯 Success Criteria

✅ **Completed when you can**:

- Create a SimpleAgent and have a conversation
- Build a ReactAgent with custom tools
- Understand when to use each agent type
- Explain the reasoning loop (Thought → Action → Observation)

## 🔗 Next Steps

Ready for more? Try these:

- **Intermediate Gallery**: Multi-agent coordination, structured outputs
- **Games Gallery**: AI agents playing games and competing
- **Advanced Gallery**: Complex workflows, custom patterns

## 🛠️ Troubleshooting

**Common issues**:

1. **Import errors**: Make sure you're in the correct directory and using `poetry run`
2. **API key issues**: Check your OpenAI/Anthropic API keys are configured
3. **Tool errors**: Verify your custom tools have proper type hints

**Get help**:

- Check the main README for setup instructions
- Look at the reference/ directory for implementation patterns
- Join our Discord for community support

## 📊 Gallery Stats

- **Examples**: 3 tutorials
- **Difficulty**: Beginner-friendly
- **Coverage**: Basic agent patterns, tool usage, conversations
- **Estimated completion**: 30 minutes

---

**Remember**: Take your time and experiment! The best way to learn is by modifying the examples and trying your own ideas.
