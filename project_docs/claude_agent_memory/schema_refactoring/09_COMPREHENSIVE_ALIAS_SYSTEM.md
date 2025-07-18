# Comprehensive Alias Generation System Design

## Overview

The alias generation system needs to handle **WAY MORE** than just simple field renaming. It must support priorities, field syncing, root models, validation priorities, inheritance conflicts, and dynamic schema adaptation across multiple contexts.

## Current Pydantic Complexity Not Handled

### **1. Field Priorities and Conflicts**

```python
# Current Pydantic patterns we need to support:
class BaseConfig(BaseModel):
    name: str = Field(alias="config_name", priority=1)

class SpecificConfig(BaseConfig):
    name: str = Field(alias="specific_name", priority=2)  # Higher priority

# Which alias wins? How do priorities resolve?
```

### **2. Field Syncing Across Models**

```python
# Models that need synchronized fields
class InputModel(BaseModel):
    user_input: str = Field(alias="input")

class OutputModel(BaseModel):
    response: str = Field(alias="output")
    original_input: str = Field(alias="input")  # Same alias, different context!

# Field syncing between input/output models
```

### **3. Root Models and Validation**

```python
# Root models with alias generation
class DataList(RootModel[List[Dict[str, Any]]]):
    # How do we generate aliases for root model elements?
    pass

class DataDict(RootModel[Dict[str, str]]):
    # How do we handle dynamic keys with aliases?
    pass
```

### **4. Complex Field Types and Nesting**

```python
# Nested models with cascading aliases
class Address(BaseModel):
    street: str = Field(alias="street_address")
    city: str = Field(alias="city_name")

class Person(BaseModel):
    name: str = Field(alias="full_name")
    address: Address = Field(alias="location")  # Nested aliases
    addresses: List[Address] = Field(alias="all_locations")  # List of nested

# How do nested aliases compose? How do we generate them dynamically?
```

## Comprehensive Alias System Requirements

### **1. Priority-Based Alias Resolution**

```python
class AliasPriority(Enum):
    USER_OVERRIDE = 100     # User-specified aliases (highest)
    CONTEXT_SPECIFIC = 80   # Context-based generation
    SCHEMA_DEFAULT = 60     # Schema-level defaults
    FIELD_DEFAULT = 40      # Field-level defaults
    GENERATED = 20          # Auto-generated aliases
    FALLBACK = 0           # Last resort (lowest)

class AliasRule:
    field_name: str
    alias: str
    priority: AliasPriority
    context: Optional[str] = None  # Context-specific rules
    condition: Optional[Callable] = None  # Conditional application

class AliasPriorityResolver:
    def resolve_alias(self, field_name: str, context: str, rules: List[AliasRule]) -> str:
        """Resolve field alias based on priority and context."""
        applicable_rules = [
            rule for rule in rules
            if self._rule_applies(rule, field_name, context)
        ]

        if not applicable_rules:
            return field_name

        # Sort by priority and return highest
        highest_priority = max(applicable_rules, key=lambda r: r.priority.value)
        return highest_priority.alias
```

### **2. Field Syncing System**

```python
class FieldSyncRule:
    source_field: str
    target_field: str
    sync_type: SyncType  # BIDIRECTIONAL, SOURCE_TO_TARGET, TARGET_TO_SOURCE
    transform: Optional[Callable] = None  # Transform during sync

class SyncType(Enum):
    BIDIRECTIONAL = "bidirectional"
    SOURCE_TO_TARGET = "source_to_target"
    TARGET_TO_SOURCE = "target_to_source"

class FieldSyncManager:
    def __init__(self):
        self.sync_rules: Dict[str, List[FieldSyncRule]] = {}
        self.sync_graph = {}  # Track sync dependencies

    def register_sync_rule(self, rule: FieldSyncRule) -> None:
        """Register field synchronization rule."""
        if rule.source_field not in self.sync_rules:
            self.sync_rules[rule.source_field] = []
        self.sync_rules[rule.source_field].append(rule)

        # Update sync graph for dependency tracking
        self._update_sync_graph(rule)

    def sync_fields(self, source_model: BaseModel, target_model: BaseModel) -> BaseModel:
        """Synchronize fields between models based on rules."""
        updated_data = target_model.model_dump()

        for source_field, rules in self.sync_rules.items():
            if hasattr(source_model, source_field):
                source_value = getattr(source_model, source_field)

                for rule in rules:
                    if rule.sync_type in [SyncType.BIDIRECTIONAL, SyncType.SOURCE_TO_TARGET]:
                        transformed_value = rule.transform(source_value) if rule.transform else source_value
                        updated_data[rule.target_field] = transformed_value

        return target_model.__class__.model_validate(updated_data)
```

### **3. Root Model Alias Support**

```python
class RootModelAliasGenerator:
    def generate_root_aliases(self, root_model: Type[RootModel], context: str) -> Dict[str, Any]:
        """Generate aliases for root model elements."""
        root_type = root_model.__pydantic_generic_metadata__['args'][0]

        if get_origin(root_type) is list:
            # List root model
            return self._generate_list_aliases(root_type, context)
        elif get_origin(root_type) is dict:
            # Dict root model
            return self._generate_dict_aliases(root_type, context)
        else:
            # Single value root model
            return self._generate_value_aliases(root_type, context)

    def _generate_list_aliases(self, list_type: Type, context: str) -> Dict[str, Any]:
        """Generate aliases for list elements."""
        element_type = get_args(list_type)[0]

        if issubclass(element_type, BaseModel):
            # List of models - generate nested aliases
            element_aliases = self.generate_model_aliases(element_type, f"{context}_item")
            return {
                "list_wrapper": f"{context}_items",
                "element_aliases": element_aliases
            }
        else:
            # List of primitives
            return {"list_wrapper": f"{context}_values"}

    def _generate_dict_aliases(self, dict_type: Type, context: str) -> Dict[str, Any]:
        """Generate aliases for dict keys/values."""
        key_type, value_type = get_args(dict_type)

        aliases = {"dict_wrapper": f"{context}_data"}

        if issubclass(value_type, BaseModel):
            # Dict with model values
            aliases["value_aliases"] = self.generate_model_aliases(value_type, f"{context}_entry")

        return aliases
```

### **4. Dynamic Schema Adaptation**

```python
class SchemaAdapter:
    def __init__(self, alias_generator: AliasGenerator, priority_resolver: AliasPriorityResolver):
        self.alias_generator = alias_generator
        self.priority_resolver = priority_resolver
        self.adaptation_cache = {}

    def adapt_schema(
        self,
        model: Type[BaseModel],
        context: str,
        adaptations: Dict[str, Any]
    ) -> Type[BaseModel]:
        """Create adapted schema with context-specific aliases and modifications."""

        cache_key = (model.__name__, context, frozenset(adaptations.items()))
        if cache_key in self.adaptation_cache:
            return self.adaptation_cache[cache_key]

        # Generate context-specific aliases
        field_aliases = self.alias_generator.generate_aliases(model, context)

        # Apply priority resolution
        resolved_aliases = {}
        for field_name in model.model_fields:
            resolved_aliases[field_name] = self.priority_resolver.resolve_alias(
                field_name, context, field_aliases.get(field_name, [])
            )

        # Create new model class with adaptations
        adapted_model = self._create_adapted_model(
            model, context, resolved_aliases, adaptations
        )

        self.adaptation_cache[cache_key] = adapted_model
        return adapted_model

    def _create_adapted_model(
        self,
        base_model: Type[BaseModel],
        context: str,
        aliases: Dict[str, str],
        adaptations: Dict[str, Any]
    ) -> Type[BaseModel]:
        """Create new model class with aliases and adaptations."""

        # Build new field definitions with aliases
        new_fields = {}
        for field_name, field_info in base_model.model_fields.items():
            alias = aliases.get(field_name, field_name)

            # Apply adaptations
            field_kwargs = {
                "alias": alias,
                "default": field_info.default,
                "description": field_info.description,
            }

            # Apply context-specific adaptations
            if field_name in adaptations:
                field_kwargs.update(adaptations[field_name])

            new_fields[field_name] = Field(**field_kwargs)

        # Create new model class
        adapted_class_name = f"{base_model.__name__}_{context.title()}Adapted"
        adapted_model = create_model(
            adapted_class_name,
            **new_fields,
            __base__=base_model
        )

        return adapted_model
```

### **5. Context-Aware Alias Generation**

```python
class ContextAliasGenerator:
    def __init__(self):
        self.context_rules: Dict[str, AliasGenerationRule] = {}
        self.naming_conventions: Dict[str, NamingConvention] = {}

    def register_context(self, context: str, rule: AliasGenerationRule) -> None:
        """Register alias generation rule for specific context."""
        self.context_rules[context] = rule

    def generate_contextual_aliases(
        self,
        model: Type[BaseModel],
        context: str
    ) -> Dict[str, List[AliasRule]]:
        """Generate context-specific aliases for model fields."""

        if context not in self.context_rules:
            return self._generate_default_aliases(model)

        rule = self.context_rules[context]
        aliases = {}

        for field_name, field_info in model.model_fields.items():
            field_aliases = []

            # Apply context-specific transformations
            for transformation in rule.transformations:
                alias = transformation.apply(field_name, field_info)
                if alias != field_name:
                    field_aliases.append(AliasRule(
                        field_name=field_name,
                        alias=alias,
                        priority=transformation.priority,
                        context=context
                    ))

            aliases[field_name] = field_aliases

        return aliases

class AliasGenerationRule:
    context: str
    transformations: List[AliasTransformation]
    naming_convention: NamingConvention

class AliasTransformation:
    name: str
    apply: Callable[[str, FieldInfo], str]
    priority: AliasPriority
    condition: Optional[Callable[[str, FieldInfo], bool]] = None

class NamingConvention(Enum):
    SNAKE_CASE = "snake_case"
    CAMEL_CASE = "camelCase"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"
    SCREAMING_SNAKE = "SCREAMING_SNAKE"
```

### **6. Inheritance and Composition Handling**

```python
class InheritanceAliasResolver:
    def resolve_inherited_aliases(
        self,
        model: Type[BaseModel],
        context: str
    ) -> Dict[str, str]:
        """Resolve aliases across inheritance hierarchy."""

        # Collect aliases from all base classes
        alias_hierarchy = {}

        for base_class in reversed(model.__mro__):
            if issubclass(base_class, BaseModel) and base_class != BaseModel:
                base_aliases = self._extract_class_aliases(base_class, context)
                alias_hierarchy.update(base_aliases)

        # Apply override rules
        final_aliases = {}
        for field_name in model.model_fields:
            if field_name in alias_hierarchy:
                final_aliases[field_name] = alias_hierarchy[field_name]
            else:
                final_aliases[field_name] = field_name

        return final_aliases

    def _extract_class_aliases(self, model_class: Type[BaseModel], context: str) -> Dict[str, str]:
        """Extract aliases defined at specific class level."""
        aliases = {}

        for field_name, field_info in model_class.model_fields.items():
            if field_info.alias:
                aliases[field_name] = field_info.alias

        # Apply context-specific generation if no explicit alias
        for field_name in model_class.model_fields:
            if field_name not in aliases:
                generated_alias = self._generate_context_alias(field_name, context)
                if generated_alias != field_name:
                    aliases[field_name] = generated_alias

        return aliases
```

### **7. Validation and Error Handling**

```python
class AliasValidationError(Exception):
    """Specific error for alias validation issues."""
    pass

class AliasValidator:
    def validate_alias_rules(self, rules: List[AliasRule]) -> List[str]:
        """Validate alias rules for conflicts and issues."""
        errors = []

        # Check for alias conflicts
        alias_map = {}
        for rule in rules:
            if rule.alias in alias_map:
                existing_rule = alias_map[rule.alias]
                if existing_rule.priority == rule.priority:
                    errors.append(
                        f"Alias conflict: '{rule.alias}' used by both "
                        f"'{rule.field_name}' and '{existing_rule.field_name}' "
                        f"with same priority {rule.priority}"
                    )
            else:
                alias_map[rule.alias] = rule

        # Check for circular dependencies in syncing
        sync_graph = self._build_sync_graph(rules)
        cycles = self._detect_cycles(sync_graph)
        if cycles:
            errors.append(f"Circular sync dependencies detected: {cycles}")

        # Check for reserved names
        reserved_names = {"model_dump", "model_validate", "__dict__", "__class__"}
        for rule in rules:
            if rule.alias in reserved_names:
                errors.append(f"Alias '{rule.alias}' conflicts with reserved name")

        return errors

    def validate_schema_adaptation(
        self,
        original: Type[BaseModel],
        adapted: Type[BaseModel]
    ) -> List[str]:
        """Validate that schema adaptation preserves essential properties."""
        errors = []

        # Check that all original fields are represented
        original_fields = set(original.model_fields.keys())
        adapted_fields = set(adapted.model_fields.keys())

        missing_fields = original_fields - adapted_fields
        if missing_fields:
            errors.append(f"Adapted schema missing fields: {missing_fields}")

        # Check type compatibility
        for field_name in original_fields & adapted_fields:
            orig_type = original.model_fields[field_name].annotation
            adapted_type = adapted.model_fields[field_name].annotation

            if not self._types_compatible(orig_type, adapted_type):
                errors.append(
                    f"Incompatible types for field '{field_name}': "
                    f"{orig_type} -> {adapted_type}"
                )

        return errors
```

## Integration with Schema System

### **Usage in Schema Test Module**

```python
# schema_test/core/components/alias_manager.py
class UnifiedAliasManager:
    def __init__(self):
        self.priority_resolver = AliasPriorityResolver()
        self.sync_manager = FieldSyncManager()
        self.context_generator = ContextAliasGenerator()
        self.inheritance_resolver = InheritanceAliasResolver()
        self.schema_adapter = SchemaAdapter(self.context_generator, self.priority_resolver)
        self.validator = AliasValidator()

    def create_adapted_schema(
        self,
        model: Type[BaseModel],
        context: str,
        sync_rules: List[FieldSyncRule] = None,
        adaptations: Dict[str, Any] = None
    ) -> Type[BaseModel]:
        """Main entry point for creating adapted schemas."""

        # Register sync rules if provided
        if sync_rules:
            for rule in sync_rules:
                self.sync_manager.register_sync_rule(rule)

        # Generate and validate aliases
        aliases = self.context_generator.generate_contextual_aliases(model, context)
        flat_rules = [rule for rule_list in aliases.values() for rule in rule_list]

        validation_errors = self.validator.validate_alias_rules(flat_rules)
        if validation_errors:
            raise AliasValidationError(f"Alias validation failed: {validation_errors}")

        # Create adapted schema
        adapted_schema = self.schema_adapter.adapt_schema(
            model, context, adaptations or {}
        )

        # Final validation
        adaptation_errors = self.validator.validate_schema_adaptation(model, adapted_schema)
        if adaptation_errors:
            raise AliasValidationError(f"Schema adaptation failed: {adaptation_errors}")

        return adapted_schema
```

## Benefits of This Comprehensive System

### **1. Handles Complex Pydantic Patterns**

- ✅ Field priorities and inheritance conflicts
- ✅ Root models and nested aliases
- ✅ Field syncing across models
- ✅ Dynamic schema adaptation

### **2. Context-Aware Generation**

- ✅ Different aliases for different use contexts
- ✅ Naming convention enforcement
- ✅ Tool-specific adaptations
- ✅ LLM provider compatibility

### **3. Robust Validation**

- ✅ Conflict detection and resolution
- ✅ Circular dependency prevention
- ✅ Type compatibility checking
- ✅ Reserved name protection

### **4. Performance Optimized**

- ✅ Alias resolution caching
- ✅ Schema adaptation caching
- ✅ Lazy generation where possible
- ✅ Dependency graph optimization

This comprehensive alias system addresses the full complexity of real-world Pydantic usage patterns and provides the foundation for reliable, flexible schema adaptation across different contexts and use cases.
