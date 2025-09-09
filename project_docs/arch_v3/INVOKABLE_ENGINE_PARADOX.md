# The InvokableEngine Paradox - Critical Analysis

**Created**: 2025-01-30  
**Purpose**: Understanding the core confusion in Engine architecture  
**Finding**: InvokableEngine creates and invokes in one step

## 🔴 The Paradox

### What the Documentation Says

Line 7-9 of base.py:

> "The Engine class is a configuration/factory class that produces runnable objects, **not an invokable itself**."

Line 563-564:

> "While the engine itself is not directly invokable (it's a factory/configuration), these methods create the runnable and invoke it in a single operation."

### What the Code Does

```python
class InvokableEngine(Engine[TIn, TOut]):
    def invoke(self, input_data: TIn, config=None) -> TOut:
        """Creates AND invokes in one step"""
        runnable = self.create_runnable(config)
        return runnable.invoke(input_data)
```

**The engine claims it's not invokable, but InvokableEngine has an invoke() method!**

## 🎯 Understanding the Semantic Trick

The code is playing a semantic game:

1. **Engine itself doesn't execute** - it creates something that executes
2. **InvokableEngine.invoke()** - creates a runnable THEN invokes it
3. **It's a convenience wrapper** - not "true" invocation

This is like saying:

- "A car factory doesn't drive"
- "But InvokableCarFactory has a test_drive() method"
- "It creates a car then drives it for you"

## 🔄 How This Affects Everything

### Agent Inheritance Chain

```
Agent extends InvokableEngine extends Engine
```

So Agent:

- IS a factory (from Engine)
- CAN invoke (from InvokableEngine)
- But invoke() creates something then runs it

This explains why Agent both IS and HAS engines!

### The Tool Confusion

When Tool can be Engine:

- Tool might be InvokableEngine
- So Tool creates a runnable and executes it
- But Tool itself isn't the executor

### The Document System

DocumentEngine extends InvokableEngine:

- It's a factory for document processors
- invoke() creates a processor and runs it
- The engine isn't doing the processing

## 📊 Mapping to Our Contracts

### What InvokableEngine Really Is

```python
class InvokableEngine:
    # It's a Factory
    def create_runnable(self) -> Runnable  # Factory contract

    # With a convenience method
    def invoke(self, input):
        runnable = self.create_runnable()  # Factory behavior
        return runnable.invoke(input)       # Delegation
```

**InvokableEngine is Factory + Convenience, not Factory + Executable**

### How Our Contracts Should Handle This

#### Option 1: Strict Separation

```python
class EngineAdapter:
    """Engine as pure Factory"""

    def create(self, **config) -> Executable:
        return ExecutableAdapter(self.engine.create_runnable(config))

class InvokableEngineAdapter:
    """InvokableEngine as Factory with convenience"""

    def create(self, **config) -> Executable:
        return ExecutableAdapter(self.engine.create_runnable(config))

    def create_and_execute(self, input, **config):
        """Convenience method - explicit about what it does"""
        executable = self.create(**config)
        return executable.execute(input)
```

#### Option 2: Accept the Duality

```python
class DualRoleComponent:
    """Component that's both Factory and Executable"""

    # Factory role
    def create(self, **config) -> Executable:
        return self._create_runnable(config)

    # Executable role (delegates internally)
    def execute(self, input):
        runnable = self.create()
        return runnable.execute(input)
```

## 🚨 The Real Problem

The confusion comes from **implicit behavior**:

```python
# What it looks like
result = engine.invoke(input)  # Seems like engine is executing

# What actually happens
runnable = engine.create_runnable()  # Step 1: Factory
result = runnable.invoke(input)      # Step 2: Execution
```

**The two-step process is hidden!**

## 💡 Solution: Make It Explicit

### Clear Naming

```python
class Engine:
    def create_runnable(self) -> Runnable  # Clear: creates something

class InvokableEngine(Engine):
    def create_and_invoke(self, input):    # Clear: two steps
        runnable = self.create_runnable()
        return runnable.invoke(input)
```

### Clear Contracts

```python
# Factory creates
class Factory(Protocol):
    def create(self) -> Executable

# Executable executes
class Executable(Protocol):
    def execute(self, input) -> output

# Convenience combines both
class FactoryWithConvenience(Factory):
    def create_and_execute(self, input):
        return self.create().execute(input)
```

## 🎯 Implications for Our Architecture

### 1. Agent Should NOT Extend InvokableEngine

**Current**: Agent IS InvokableEngine  
**Problem**: Agent appears to be a factory  
**Solution**: Agent HAS engines, doesn't extend them

### 2. Rename invoke() Methods

**Current**: `engine.invoke()` hides two-step process  
**Better**: `engine.create_and_invoke()` or `engine.run()`

### 3. Separate Factory from Execution

**Current**: Mixed in InvokableEngine  
**Better**: Clear separation with explicit convenience methods

## 📋 Action Items

1. **Document the two-step process** everywhere
2. **Create adapters** that make it explicit
3. **New components** should separate concerns
4. **Migration path** for existing code

## 🔑 Key Insight

**InvokableEngine is a CONVENIENCE PATTERN, not a violation of the factory pattern.**

But it's a confusing convenience that makes it seem like engines execute when they don't. Our contracts should make this explicit rather than hiding it.
