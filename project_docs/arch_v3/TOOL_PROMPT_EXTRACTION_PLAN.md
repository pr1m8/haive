# Tool and Prompt System Extraction Plan

**Created**: 2025-09-09
**Purpose**: Extract and improve tool and prompt management from AugLLMConfig
**Status**: Design Document
**Impact**: -20🔥 complexity reduction

## 🎯 Current Problems

### Tool System Issues (in AugLLMConfig)

- **266 lines** of tool-related code mixed with everything else
- **23 tool-related fields** in a single config class
- **Multiple tool representations**: tools, pydantic_tools, schemas, tool_routes
- **Circular dependencies**: Tools can be engines, engines can be tools
- **No clear contracts** for tool capabilities and requirements
- **Mixed routing logic** scattered across methods

### Prompt System Issues

- **Prompt templates mixed** with LLM configuration
- **No prompt library** or reusable templates
- **Variables extraction** happens in multiple places
- **No prompt composition** patterns
- **Format instructions** tangled with tool logic
- **No prompt versioning** or management

## 🏗️ Proposed Architecture

### 1. ToolConfig - Focused Tool Management

````python
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, StructuredTool
from haive.core.contracts import EngineContract, FieldContract

class ToolCapabilities(BaseModel):
    """What a tool can do."""
    can_read_state: bool = False
    can_write_state: bool = False
    can_call_external: bool = False
    requires_confirmation: bool = False
    is_async: bool = False
    supports_streaming: bool = False
    max_retries: int = 3
    timeout: Optional[float] = None

class ToolContract(EngineContract):
    """Explicit contract for a tool."""
    name: str
    description: str
    capabilities: ToolCapabilities
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]
    examples: List[Dict[str, Any]] = Field(default_factory=list)

    def validate_call(self, args: Dict[str, Any]) -> bool:
        """Validate tool call arguments."""
        try:
            self.input_schema.model_validate(args)
            return True
        except:
            return False

class ToolConfig(BaseModel):
    """Focused configuration for tool management.

    This replaces the scattered tool configuration in AugLLMConfig
    with a focused, contract-based approach.
    """

    # Core tool management
    tools: List[Union[BaseTool, StructuredTool, type[BaseModel]]] = Field(
        default_factory=list,
        description="Registered tools"
    )

    # Tool contracts
    contracts: Dict[str, ToolContract] = Field(
        default_factory=dict,
        description="Tool contracts by name"
    )

    # Tool routing
    routing_strategy: Literal["auto", "capability", "priority", "manual"] = Field(
        default="auto",
        description="How to route to tools"
    )

    routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Explicit tool routes"
    )

    # Tool choice
    choice_mode: Literal["auto", "required", "none", "specific"] = Field(
        default="auto",
        description="Tool choice mode"
    )

    specific_tool: Optional[str] = Field(
        default=None,
        description="Specific tool to use if choice_mode is 'specific'"
    )

    # Capabilities filtering
    required_capabilities: Optional[ToolCapabilities] = Field(
        default=None,
        description="Filter tools by required capabilities"
    )

    def register_tool(
        self,
        tool: Any,
        contract: Optional[ToolContract] = None
    ) -> None:
        """Register a tool with its contract.

        Args:
            tool: The tool to register
            contract: Optional explicit contract
        """
        if contract is None:
            contract = self._derive_contract(tool)

        tool_name = self._get_tool_name(tool)
        self.tools.append(tool)
        self.contracts[tool_name] = contract

        # Auto-configure routing
        if self.routing_strategy == "auto":
            self._configure_auto_route(tool_name, contract)

    def get_tools_by_capability(
        self,
        capabilities: ToolCapabilities
    ) -> List[Any]:
        """Get tools matching required capabilities.

        Args:
            capabilities: Required capabilities

        Returns:
            List of matching tools
        """
        matching = []
        for tool in self.tools:
            name = self._get_tool_name(tool)
            contract = self.contracts.get(name)

            if contract and self._matches_capabilities(
                contract.capabilities,
                capabilities
            ):
                matching.append(tool)

        return matching

    def _derive_contract(self, tool: Any) -> ToolContract:
        """Derive contract from tool."""
        # Implementation to analyze tool and create contract
        pass

    def _get_tool_name(self, tool: Any) -> str:
        """Get standardized tool name."""
        if hasattr(tool, "name"):
            return tool.name
        elif hasattr(tool, "__name__"):
            return tool.__name__
        else:
            return str(tool)

    def _configure_auto_route(
        self,
        tool_name: str,
        contract: ToolContract
    ) -> None:
        """Configure automatic routing for tool."""
        if contract.capabilities.requires_confirmation:
            self.routes[tool_name] = "confirmation_required"
        elif contract.capabilities.can_write_state:
            self.routes[tool_name] = "state_writer"
        elif contract.capabilities.can_call_external:
            self.routes[tool_name] = "external_call"
        else:
            self.routes[tool_name] = "default"

    def _matches_capabilities(
        self,
        tool_caps: ToolCapabilities,
        required: ToolCapabilities
    ) -> bool:
        """Check if tool capabilities match requirements."""
        for field, value in required.model_dump().items():
            if value is not None:
                tool_value = getattr(tool_caps, field)
                if field.startswith("can_") or field.startswith("supports_"):
                    # Boolean capabilities must match if required
                    if value and not tool_value:
                        return False
                elif field == "max_retries":
                    # Numeric capabilities must meet minimum
                    if tool_value < value:
                        return False
        return True

    def to_langchain_tools(self) -> List[BaseTool]:
        """Convert all tools to LangChain format.

        Returns:
            List of LangChain-compatible tools
        """
        langchain_tools = []
        for tool in self.tools:
            if isinstance(tool, BaseTool):
                langchain_tools.append(tool)
            else:
                # Convert to StructuredTool
                converted = self._convert_to_structured_tool(tool)
                langchain_tools.append(converted)
        return langchain_tools

    def get_tool_choice_config(self) -> Dict[str, Any]:
        """Get tool choice configuration for LLM binding.

        Returns:
            Configuration dict for bind_tools
        """
        if self.choice_mode == "none":
            return {"tool_choice": "none"}
        elif self.choice_mode == "required":
            if self.specific_tool:
                return {
                    "tool_choice": {
                        "type": "function",
                        "function": {"name": self.specific_tool}
                    }
                }
            else:
                return {"tool_choice": "required"}
        else:
            return {"tool_choice": "auto"}


### 2. PromptConfig - Focused Prompt Management

```python
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from langchain_core.prompts import BasePromptTemplate, ChatPromptTemplate

class PromptVariable(BaseModel):
    """Definition of a prompt variable."""
    name: str
    type: type
    description: str
    required: bool = True
    default: Optional[Any] = None
    examples: List[Any] = Field(default_factory=list)

    def validate_value(self, value: Any) -> bool:
        """Validate a value for this variable."""
        if value is None and self.required:
            return False
        if value is not None and not isinstance(value, self.type):
            return False
        return True

class PromptMetadata(BaseModel):
    """Metadata about a prompt template."""
    version: str = "1.0.0"
    author: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    use_cases: List[str] = Field(default_factory=list)
    performance_notes: Optional[str] = None

class PromptContract(BaseModel):
    """Contract for a prompt template."""
    variables: List[PromptVariable]
    output_format: Optional[type[BaseModel]] = None
    max_tokens: Optional[int] = None
    temperature_range: tuple[float, float] = (0.0, 1.0)
    metadata: PromptMetadata = Field(default_factory=PromptMetadata)

    def get_required_variables(self) -> List[str]:
        """Get list of required variable names."""
        return [v.name for v in self.variables if v.required]

    def validate_inputs(self, inputs: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate inputs against contract.

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Check required variables
        required = self.get_required_variables()
        for var_name in required:
            if var_name not in inputs:
                issues.append(f"Missing required variable: {var_name}")

        # Validate types
        for var in self.variables:
            if var.name in inputs:
                if not var.validate_value(inputs[var.name]):
                    issues.append(
                        f"Variable '{var.name}' has invalid type or value"
                    )

        return len(issues) == 0, issues

class PromptConfig(BaseModel):
    """Focused configuration for prompt management.

    This extracts prompt management from AugLLMConfig and provides
    a clean, reusable prompt system.
    """

    # Core prompt template
    template: Optional[BasePromptTemplate] = Field(
        default=None,
        description="Active prompt template"
    )

    # Prompt library
    library: Dict[str, BasePromptTemplate] = Field(
        default_factory=dict,
        description="Reusable prompt templates"
    )

    # Contracts
    contracts: Dict[str, PromptContract] = Field(
        default_factory=dict,
        description="Prompt contracts"
    )

    # Template composition
    composition_mode: Literal["override", "extend", "merge"] = Field(
        default="override",
        description="How to compose templates"
    )

    # Variables management
    partial_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Partial variables for templates"
    )

    default_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Default values for variables"
    )

    # Format instructions
    include_format_instructions: bool = Field(
        default=False,
        description="Whether to include format instructions"
    )

    format_instruction_template: Optional[str] = Field(
        default=None,
        description="Template for format instructions"
    )

    def register_template(
        self,
        name: str,
        template: BasePromptTemplate,
        contract: Optional[PromptContract] = None
    ) -> None:
        """Register a template in the library.

        Args:
            name: Template identifier
            template: The prompt template
            contract: Optional contract
        """
        self.library[name] = template

        if contract is None:
            contract = self._derive_contract(template)
        self.contracts[name] = contract

    def load_template(self, name: str) -> BasePromptTemplate:
        """Load a template from library.

        Args:
            name: Template name

        Returns:
            The prompt template

        Raises:
            KeyError: If template not found
        """
        if name not in self.library:
            raise KeyError(f"Template '{name}' not found in library")

        return self.library[name]

    def compose_templates(
        self,
        base: Union[str, BasePromptTemplate],
        extension: Union[str, BasePromptTemplate]
    ) -> BasePromptTemplate:
        """Compose two templates.

        Args:
            base: Base template or name
            extension: Extension template or name

        Returns:
            Composed template
        """
        # Resolve templates
        if isinstance(base, str):
            base = self.load_template(base)
        if isinstance(extension, str):
            extension = self.load_template(extension)

        if self.composition_mode == "override":
            return extension
        elif self.composition_mode == "extend":
            # Combine templates
            return self._extend_templates(base, extension)
        elif self.composition_mode == "merge":
            # Merge variables and content
            return self._merge_templates(base, extension)
        else:
            return base

    def format_with_validation(
        self,
        template: Optional[BasePromptTemplate] = None,
        **kwargs
    ) -> str:
        """Format template with validation.

        Args:
            template: Template to use (or self.template)
            **kwargs: Variables for formatting

        Returns:
            Formatted prompt

        Raises:
            ValueError: If validation fails
        """
        if template is None:
            template = self.template

        if template is None:
            raise ValueError("No template available")

        # Get contract
        contract = self._get_contract_for_template(template)

        # Validate inputs
        if contract:
            valid, issues = contract.validate_inputs(kwargs)
            if not valid:
                raise ValueError(f"Validation failed: {issues}")

        # Apply defaults
        final_vars = self.default_variables.copy()
        final_vars.update(self.partial_variables)
        final_vars.update(kwargs)

        # Format
        return template.format(**final_vars)

    def get_format_instructions(
        self,
        output_model: Optional[type[BaseModel]] = None
    ) -> str:
        """Get format instructions for output.

        Args:
            output_model: Expected output model

        Returns:
            Format instruction string
        """
        if output_model:
            schema = output_model.model_json_schema()
            return self._generate_format_instructions(schema)
        elif self.format_instruction_template:
            return self.format_instruction_template
        else:
            return "Please format your response clearly."

    def _derive_contract(
        self,
        template: BasePromptTemplate
    ) -> PromptContract:
        """Derive contract from template."""
        variables = []

        # Extract variables from template
        if hasattr(template, "input_variables"):
            for var_name in template.input_variables:
                variables.append(PromptVariable(
                    name=var_name,
                    type=str,  # Default to string
                    description=f"Variable: {var_name}",
                    required=var_name not in self.partial_variables
                ))

        return PromptContract(variables=variables)

    def _extend_templates(
        self,
        base: BasePromptTemplate,
        extension: BasePromptTemplate
    ) -> BasePromptTemplate:
        """Extend base template with extension."""
        # Implementation for template extension
        pass

    def _merge_templates(
        self,
        base: BasePromptTemplate,
        extension: BasePromptTemplate
    ) -> BasePromptTemplate:
        """Merge two templates."""
        # Implementation for template merging
        pass


### 3. ToolRegistry - Central Tool Management

```python
class ToolRegistry:
    """Central registry for all tools in the system.

    This provides a single source of truth for tool management,
    replacing scattered tool definitions.
    """

    def __init__(self):
        self._tools: Dict[str, Any] = {}
        self._contracts: Dict[str, ToolContract] = {}
        self._categories: Dict[str, List[str]] = {}
        self._priorities: Dict[str, int] = {}

    def register(
        self,
        tool: Any,
        contract: ToolContract,
        category: Optional[str] = None,
        priority: int = 0
    ) -> None:
        """Register a tool globally.

        Args:
            tool: The tool to register
            contract: Tool's contract
            category: Optional category
            priority: Execution priority
        """
        name = contract.name

        self._tools[name] = tool
        self._contracts[name] = contract
        self._priorities[name] = priority

        if category:
            if category not in self._categories:
                self._categories[category] = []
            self._categories[category].append(name)

    def get_tool(self, name: str) -> Any:
        """Get tool by name."""
        return self._tools.get(name)

    def get_contract(self, name: str) -> Optional[ToolContract]:
        """Get tool contract."""
        return self._contracts.get(name)

    def get_by_category(self, category: str) -> List[Any]:
        """Get all tools in category."""
        names = self._categories.get(category, [])
        return [self._tools[name] for name in names if name in self._tools]

    def get_by_capability(
        self,
        capabilities: ToolCapabilities
    ) -> List[Any]:
        """Get tools matching capabilities."""
        matching = []
        for name, contract in self._contracts.items():
            if self._matches_capabilities(
                contract.capabilities,
                capabilities
            ):
                matching.append(self._tools[name])
        return matching

    def _matches_capabilities(
        self,
        tool_caps: ToolCapabilities,
        required: ToolCapabilities
    ) -> bool:
        """Check capability match."""
        # Same implementation as in ToolConfig
        pass


### 4. PromptLibrary - Reusable Prompts

```python
class PromptLibrary:
    """Library of reusable prompt templates.

    This provides a central repository for prompts,
    enabling reuse and versioning.
    """

    def __init__(self):
        self._templates: Dict[str, Dict[str, BasePromptTemplate]] = {}
        self._contracts: Dict[str, Dict[str, PromptContract]] = {}
        self._versions: Dict[str, str] = {}

    def register(
        self,
        name: str,
        template: BasePromptTemplate,
        contract: PromptContract,
        version: str = "1.0.0"
    ) -> None:
        """Register a prompt template.

        Args:
            name: Template name
            template: The template
            contract: Template contract
            version: Version string
        """
        if name not in self._templates:
            self._templates[name] = {}
            self._contracts[name] = {}

        self._templates[name][version] = template
        self._contracts[name][version] = contract
        self._versions[name] = version  # Latest version

    def get(
        self,
        name: str,
        version: Optional[str] = None
    ) -> BasePromptTemplate:
        """Get template by name and version.

        Args:
            name: Template name
            version: Optional version (latest if None)

        Returns:
            The prompt template
        """
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found")

        if version is None:
            version = self._versions[name]

        if version not in self._templates[name]:
            raise KeyError(f"Version '{version}' not found for '{name}'")

        return self._templates[name][version]

    def get_contract(
        self,
        name: str,
        version: Optional[str] = None
    ) -> PromptContract:
        """Get template contract."""
        if name not in self._contracts:
            raise KeyError(f"Contract for '{name}' not found")

        if version is None:
            version = self._versions[name]

        return self._contracts[name][version]

    def list_templates(self) -> List[str]:
        """List all template names."""
        return list(self._templates.keys())

    def list_versions(self, name: str) -> List[str]:
        """List versions for template."""
        if name not in self._templates:
            return []
        return list(self._templates[name].keys())


## 🔄 Integration Strategy

### Phase 1: Extract Tool System
1. Create `ToolConfig` class with contracts
2. Create `ToolRegistry` for central management
3. Extract tool logic from AugLLMConfig
4. Add capability-based routing

### Phase 2: Extract Prompt System
1. Create `PromptConfig` class
2. Create `PromptLibrary` for reuse
3. Extract prompt logic from AugLLMConfig
4. Add prompt composition patterns

### Phase 3: Simplify AugLLMConfig
1. Replace tool fields with `tool_config: ToolConfig`
2. Replace prompt fields with `prompt_config: PromptConfig`
3. Remove 400+ lines of tool/prompt code
4. Focus on pure LLM configuration

### Phase 4: Apply Contracts
1. Add contracts to all tools
2. Add contracts to all prompts
3. Use contracts for validation
4. Enable capability-based selection

## 📊 Impact Analysis

### Before (in AugLLMConfig)
- **2,647 total lines**
- **266 lines** of tool code
- **150+ lines** of prompt code
- **23 tool fields** mixed with LLM config
- **No contracts** or capabilities
- **No reuse** of prompts

### After
- **ToolConfig**: ~300 lines (focused)
- **PromptConfig**: ~250 lines (focused)
- **AugLLMConfig**: ~1,500 lines (reduced by 40%!)
- **Clear contracts** for everything
- **Capability-based** tool selection
- **Reusable** prompt library

### Complexity Reduction
- **Current**: 82🔥
- **After Tool/Prompt Extraction**: 62🔥 (-20🔥)
- **Clear separation** of concerns
- **Better testability**
- **Improved reusability**

## 🚀 Next Steps

1. **Implement ToolConfig** with contracts
2. **Build ToolRegistry** for central management
3. **Create PromptConfig** with composition
4. **Build PromptLibrary** for reuse
5. **Refactor AugLLMConfig** to use new configs
6. **Add capability-based routing**
7. **Create standard prompt templates**
8. **Write comprehensive tests**

---

**Key Benefit**: Tools and prompts become first-class citizens with clear contracts, capabilities, and reusability, while AugLLMConfig becomes focused on its core purpose - LLM configuration.
````
