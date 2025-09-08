# Engine Redesign - Breaking Down AugLLMConfig

**Created**: 2025-01-06
**Purpose**: Redesign AugLLMConfig to follow Single Responsibility Principle
**Status**: Brainstorming & Design Phase

## 🚨 Current Problems with AugLLMConfig

### The Mega-Bloat Issue

AugLLMConfig currently has **2600+ lines** and **80+ methods** trying to be:

1. An LLM configuration holder (temperature, max_tokens, model)
2. A prompt template manager (system messages, few-shot, templates)
3. A tool manager (add_tool, remove_tool, tool routes)
4. An output parser manager (structured output v1 and v2)
5. A message handler (add/remove/replace messages)
6. A validation system (comprehensive validation)
7. A debugging system (rich output, logging)
8. A factory system (15+ from\_\* methods)
9. A state manager (partial variables, optional variables)
10. A format instruction handler

**This is WAY too much for one class!**

## 🎯 Core Requirements

What does an Engine ACTUALLY need to do?

### 1. **Configure LLM Settings**

- Model selection
- Temperature, max_tokens, etc.
- Provider-specific settings

### 2. **Create Runnable Components**

- Build the actual LLM chain
- Bind tools if needed
- Apply output parsing

### 3. **Define I/O Schema**

- What inputs are expected
- What outputs are produced
- Type safety guarantees

### 4. **Integrate with Framework**

- Work with StateSchema
- Support graph execution
- Enable recompilation

## 💡 Proposed Architecture: Separation of Concerns

### Core Principle: Composition Over Configuration

Instead of one mega-config class, break into focused components:

```python
# 1. Pure LLM Configuration
class LLMSettings(BaseModel):
    """Just the LLM settings, nothing else"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    # Provider-specific
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    timeout: int = 30

# 2. Prompt Template System (separate)
class PromptTemplate:
    """Manages prompt construction"""
    def __init__(self):
        self.system_message: Optional[str] = None
        self.user_template: Optional[str] = None
        self.assistant_template: Optional[str] = None
        self.few_shot_examples: List[Example] = []
        self.variables: Set[str] = set()

    def format(self, **kwargs) -> List[Message]:
        """Format template with variables"""
        pass

    def add_few_shot(self, input: str, output: str):
        """Add example for few-shot learning"""
        pass

# 3. Tool Registry (separate)
class ToolRegistry:
    """Manages tools and their routes"""
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.routes: Dict[str, str] = {}
        self.metadata: Dict[str, Dict] = {}

    def register(self, tool: Tool, route: Optional[str] = None):
        """Register a tool with optional route"""
        pass

    def get_tools_for_binding(self) -> List[Tool]:
        """Get tools ready for LLM binding"""
        pass

    def validate_tool_call(self, call: ToolCall) -> bool:
        """Validate a tool call"""
        pass

# 4. Output Strategy (separate)
class OutputStrategy:
    """Handles output parsing and validation"""
    def __init__(self):
        self.strategy_type: Literal["raw", "json", "pydantic", "tool"]
        self.parser: Optional[BaseOutputParser] = None
        self.model: Optional[Type[BaseModel]] = None

    def parse(self, output: Any) -> Any:
        """Parse LLM output"""
        pass

    def get_format_instructions(self) -> str:
        """Get formatting instructions for prompt"""
        pass

# 5. Engine Builder (orchestrates)
class LLMEngineBuilder:
    """Builds configured LLM engines"""
    def __init__(self):
        self.settings = LLMSettings()
        self.prompt = PromptTemplate()
        self.tools = ToolRegistry()
        self.output = OutputStrategy()

    def with_settings(self, **kwargs) -> 'LLMEngineBuilder':
        """Configure LLM settings"""
        self.settings = LLMSettings(**kwargs)
        return self

    def with_prompt(self, template: str) -> 'LLMEngineBuilder':
        """Set prompt template"""
        self.prompt.user_template = template
        return self

    def with_tools(self, tools: List[Tool]) -> 'LLMEngineBuilder':
        """Add tools"""
        for tool in tools:
            self.tools.register(tool)
        return self

    def with_structured_output(self, model: Type[BaseModel]) -> 'LLMEngineBuilder':
        """Configure structured output"""
        self.output.strategy_type = "pydantic"
        self.output.model = model
        return self

    def build(self) -> LLMEngine:
        """Build the final engine"""
        return LLMEngine(
            settings=self.settings,
            prompt=self.prompt,
            tools=self.tools,
            output=self.output
        )

# 6. The Actual Engine (runtime)
class LLMEngine:
    """The runtime engine that executes"""
    def __init__(self, settings, prompt, tools, output):
        self.settings = settings
        self.prompt = prompt
        self.tools = tools
        self.output = output
        self._chain = None  # Built lazily

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define input schema"""
        return {
            var: (str, "")
            for var in self.prompt.variables
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define output schema"""
        if self.output.model:
            return {
                field: (info.annotation, info.default)
                for field, info in self.output.model.model_fields.items()
            }
        return {"output": (str, "")}

    def create_runnable(self) -> Runnable:
        """Create the LangChain runnable"""
        if not self._chain:
            self._chain = self._build_chain()
        return self._chain

    def _build_chain(self) -> Runnable:
        """Build the actual LangChain chain"""
        # Create LLM
        llm = self._create_llm()

        # Bind tools if any
        if self.tools.tools:
            llm = llm.bind_tools(self.tools.get_tools_for_binding())

        # Create prompt chain
        prompt_chain = self.prompt.format

        # Add output parsing
        if self.output.parser:
            return prompt_chain | llm | self.output.parser

        return prompt_chain | llm
```

## 🏗️ Detailed Design

### 1. Settings Management

```python
class LLMSettings(BaseModel):
    """Pure configuration for LLM"""
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True
    )

    # Core settings
    model: str = Field(description="Model identifier")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)

    # Advanced settings
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)

    # Provider settings
    provider: Literal["openai", "azure", "anthropic", "local"]
    api_key: Optional[SecretStr] = None
    endpoint: Optional[str] = None

    def to_langchain_kwargs(self) -> Dict[str, Any]:
        """Convert to LangChain LLM kwargs"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            # ... map other fields
        }
```

### 2. Prompt Management

```python
class PromptManager:
    """Manages prompt templates separately"""

    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self.active_template: Optional[str] = None

    def create_template(
        self,
        name: str,
        template: str,
        template_type: Literal["chat", "completion"] = "chat"
    ):
        """Create a new template"""
        self.templates[name] = PromptTemplate(
            template=template,
            type=template_type
        )

    def add_system_message(self, content: str):
        """Add system message to active template"""
        if self.active_template:
            template = self.templates[self.active_template]
            template.system_message = content

    def add_few_shot_example(self, input: str, output: str):
        """Add few-shot example"""
        if self.active_template:
            template = self.templates[self.active_template]
            template.examples.append({"input": input, "output": output})

    def get_prompt_chain(self) -> Callable:
        """Get the prompt formatting chain"""
        template = self.templates[self.active_template]
        return template.to_langchain_prompt()
```

### 3. Tool Management

```python
class ToolManager:
    """Dedicated tool management"""

    def __init__(self):
        self.tools: List[Tool] = []
        self.routes: Dict[str, str] = {}
        self.choice_mode: Literal["auto", "required", "none"] = "auto"

    def add_tool(self, tool: Tool, route: Optional[str] = None):
        """Add a tool with optional route"""
        self.tools.append(tool)
        if route:
            self.routes[tool.name] = route

    def remove_tool(self, tool_name: str):
        """Remove a tool"""
        self.tools = [t for t in self.tools if t.name != tool_name]
        self.routes.pop(tool_name, None)

    def get_binding_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for bind_tools"""
        return {
            "tools": self.tools,
            "tool_choice": self.choice_mode
        }
```

### 4. Output Handling

```python
class OutputHandler:
    """Manages output parsing strategies"""

    def __init__(self):
        self.strategy: Optional[OutputStrategy] = None

    def use_json_output(self, schema: Dict[str, Any]):
        """Configure JSON output"""
        self.strategy = JSONOutputStrategy(schema)

    def use_pydantic_output(self, model: Type[BaseModel]):
        """Configure Pydantic output"""
        self.strategy = PydanticOutputStrategy(model)

    def use_tool_output(self):
        """Configure tool-based output"""
        self.strategy = ToolOutputStrategy()

    def get_parser(self) -> Optional[BaseOutputParser]:
        """Get the output parser"""
        return self.strategy.get_parser() if self.strategy else None

    def get_format_instructions(self) -> str:
        """Get format instructions for prompt"""
        return self.strategy.get_instructions() if self.strategy else ""
```

## 🔄 Integration Pattern

### How Components Work Together

```python
# Usage example - clean and clear
builder = LLMEngineBuilder()

engine = (
    builder
    .with_settings(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000
    )
    .with_prompt("Analyze the following text: {text}")
    .with_tools([web_search_tool, calculator_tool])
    .with_structured_output(AnalysisResult)
    .build()
)

# Execute
result = engine.create_runnable().invoke({
    "text": "Climate change impacts on agriculture"
})
```

### Migration from Current AugLLMConfig

```python
# Old way (monolithic)
config = AugLLMConfig(
    llm_config=llm_config,
    prompt_template=template,
    tools=tools,
    structured_output_model=model,
    temperature=0.7,
    # ... 50 more parameters
)

# New way (composed)
engine = (
    LLMEngineBuilder()
    .with_settings(temperature=0.7)
    .with_prompt(template)
    .with_tools(tools)
    .with_structured_output(model)
    .build()
)
```

## 🎯 Benefits of This Design

### 1. **Single Responsibility**

- Each component has ONE clear job
- Easy to understand and test
- Clear boundaries

### 2. **Composable**

- Mix and match components
- Don't need all features for simple cases
- Can extend without modifying core

### 3. **Testable**

- Each component tested in isolation
- No 2600-line test files
- Clear mocking boundaries

### 4. **Maintainable**

- Changes localized to components
- No ripple effects
- Easy to debug

### 5. **Type Safe**

- Clear input/output contracts
- Proper generics usage
- Validation at boundaries

## 📋 Migration Strategy

### Phase 1: Create New Components

- Build new components alongside AugLLMConfig
- No breaking changes initially
- Thorough testing

### Phase 2: Adapter Layer

- Create adapter from old to new
- Gradual migration of features
- Maintain backwards compatibility

### Phase 3: Update Consumers

- Update agents to use new pattern
- Provide migration guide
- Support both patterns temporarily

### Phase 4: Deprecate Old System

- Mark AugLLMConfig as deprecated
- Set removal timeline
- Complete migration

## 🤔 Open Questions

1. **Factory Methods**: How to handle 15+ from\_\* methods?
   - Keep as convenience methods on builder?
   - Separate factory class?
   - Remove and use builder only?

2. **Backwards Compatibility**: How long to support old pattern?
   - 1 major version?
   - 6 months?
   - Based on usage?

3. **Feature Parity**: Must we support all current features?
   - Some rarely used?
   - Some better removed?
   - Simplification opportunity?

4. **Integration Points**: How to integrate with existing systems?
   - StateSchema integration
   - Node system usage
   - Graph compilation

## 🚀 Next Steps

1. **Prototype Core Components**
   - Build LLMSettings
   - Build PromptManager
   - Test integration

2. **Validate with Use Cases**
   - Simple chat agent
   - Tool-using agent
   - Structured output agent

3. **Performance Testing**
   - Compare with current AugLLMConfig
   - Memory usage
   - Execution speed

4. **Documentation**
   - Migration guide
   - API reference
   - Examples

## 📝 Design Principles

1. **Composition over Configuration**
2. **Explicit over Implicit**
3. **Simple over Clever**
4. **Testable from Day One**
5. **Clear Separation of Concerns**
6. **Type Safety Throughout**
7. **Progressive Enhancement**
8. **Backwards Compatible Migration**

## 🎯 Success Metrics

1. **Code Reduction**: From 2600 lines to <500 per component
2. **Method Count**: From 80+ to <10 per component
3. **Test Coverage**: 100% per component
4. **Migration Ease**: <1 hour to migrate existing code
5. **Performance**: No regression vs current
6. **Developer Experience**: Clear, intuitive API

---

**Key Insight**: AugLLMConfig became a "god object" by trying to handle every aspect of LLM interaction. By breaking it into focused, composable components, we can build a more maintainable, testable, and understandable system.
