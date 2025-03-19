from pydantic import BaseModel, create_model, Field, field_validator, model_validator
from langchain.tools import StructuredTool
from typing import Dict, Type, Optional, Any, Callable, Union, ClassVar

def create_pydantic_model(
    model_name: str, 
    fields: Dict[str, Dict[str, Any]], 
    base_model: Optional[Type[BaseModel]] = None,
    description: Optional[str] = None
) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model with field descriptions, titles, validators, nested fields,
    and support for field and model validators.

    :param model_name: Name of the model.
    :param fields: Dictionary mapping field names to metadata.
    :param base_model: Optional base Pydantic model to inherit from.
    :param description: Optional overall model description.
    :return: A Pydantic model class.
    """
    field_definitions = {}
    validators_dict = {}
    class_attributes = {}
    
    for field_name, meta in fields.items():
        field_type = meta.get("type", str)
        field_title = meta.get("title", None)
        field_description = meta.get("description", "")
        default_value = meta.get("default", ...)
        is_nested = isinstance(field_type, dict)

        if is_nested:
            nested_model_name = f"{model_name}_{field_name}_Nested"
            field_type = create_pydantic_model(nested_model_name, field_type)
        
        field_definitions[field_name] = (
            field_type, 
            Field(
                default_value, 
                title=field_title, 
                description=field_description
            )
        )
        
        # Add field validators if specified
        if "field_validator" in meta and isinstance(meta["field_validator"], Callable):
            @field_validator(field_name, mode='before')
            def validate_field(cls, value):
                return meta["field_validator"](value)
            validators_dict[f"validate_{field_name}"] = validate_field
    
    # Add model validator if specified
    if "model_validator" in fields:
        model_validator_func = fields["model_validator"].get("function")
        if isinstance(model_validator_func, Callable):
            @model_validator(mode='before')
            def validate_model(cls, values):
                return model_validator_func(values)
            validators_dict["validate_model"] = validate_model
    
    # Add class properties or methods if specified
    for key, meta in fields.items():
        if meta.get("class_var", False):
            class_attributes[key] = ClassVar[meta["type"]]
        if "property" in meta and isinstance(meta["property"], Callable):
            class_attributes[key] = property(meta["property"])
        if "staticmethod" in meta and isinstance(meta["staticmethod"], Callable):
            class_attributes[key] = staticmethod(meta["staticmethod"])
        if "classmethod" in meta and isinstance(meta["classmethod"], Callable):
            class_attributes[key] = classmethod(meta["classmethod"])
    
    model = create_model(
        model_name, 
        __base__=base_model if base_model else BaseModel,
        __doc__=description,
        **field_definitions,
        **validators_dict,
        **class_attributes
    )
    model.model_rebuild()
    return model

def create_pydantic_model_tool(model_name: str, fields: Dict[str, Dict[str, Any]]) -> Dict:
    """
    Wrapper function to generate a Pydantic model with specified fields.
    
    :param model_name: Name of the model.
    :param fields: Dictionary mapping field names to metadata.
    :return: JSON schema of the generated model.
    """
    model = create_pydantic_model(model_name, fields)
    return model.model_json_schema()

pydantic_tool = StructuredTool.from_function(
    name="pydantic_model_creator",
    description="A tool to generate a Pydantic model dynamically with metadata, validation, and nested structures.",
    func=create_pydantic_model_tool,
)

# Example usage:
# schema = create_pydantic_model_tool("UserModel", {
#     "name": {"type": "str", "title": "Full Name", "description": "The user's full name."},
#     "age": {"type": "int", "title": "Age", "description": "The user's age.", "default": 18},
#     "address": {
#         "type": {
#             "street": {"type": "str", "title": "Street Address"},
#             "city": {"type": "str", "title": "City"},
#             "zip": {"type": "int", "title": "ZIP Code"}
#         },
#         "title": "Address",
#         "description": "The user's address."
#     },
#     "model_validator": {
#         "function": lambda values: values if values.get("age", 0) >= 18 else {**values, "age": 18}
#     },
#     "is_adult": {
#         "property": lambda self: self.age >= 18
#     }
# })
# print(schema)