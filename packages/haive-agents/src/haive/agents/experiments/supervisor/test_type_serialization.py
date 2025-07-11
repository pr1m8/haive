"""Test why type objects aren't serializable."""

import ormsgpack
from pydantic import BaseModel


class MyModel(BaseModel):
    name: str = "test"


def test_type_serialization():
    """Test serializing different representations of types."""
    test_cases = [
        ("int type", int),
        ("str type", str),
        ("list type", list),
        ("dict type", dict),
    ]

    for name, obj in test_cases:
        try:
            ormsgpack.packb(obj)
        except Exception as e:
            pass")

    try:
        ormsgpack.packb(MyModel)
    except Exception as e:

    instance = MyModel(name="test")
    try:
        ormsgpack.packb(instance)
    except Exception as e:
        pass")

    try:
        serialized = ormsgpack.packb(instance, option=ormsgpack.OPT_SERIALIZE_PYDANTIC)
        # Try to deserialize
        deserialized = ormsgpack.unpackb(serialized)
    except Exception as e:
        pass

    # String representation
    try:
        ormsgpack.packb("MyModel")
    except Exception as e:
        pass")

    # Module + name
    try:
        class_ref = {"module": MyModel.__module__, "name": MyModel.__name__}
        ormsgpack.packb(class_ref)
    except Exception as e:
        pass")

    # Schema representation
    try:
        schema = MyModel.model_json_schema()
        ormsgpack.packb(schema)
    except Exception as e:
        pass")



if __name__ == "__main__":
    test_type_serialization()
