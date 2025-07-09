"""Test why type objects aren't serializable."""

import ormsgpack
from pydantic import BaseModel


class MyModel(BaseModel):
    name: str = "test"


def test_type_serialization():
    """Test serializing different representations of types."""

    print("1. Testing basic Python types:")
    test_cases = [
        ("int type", int),
        ("str type", str),
        ("list type", list),
        ("dict type", dict),
    ]

    for name, obj in test_cases:
        try:
            ormsgpack.packb(obj)
            print(f"✅ {name}: SERIALIZABLE")
        except Exception as e:
            print(f"❌ {name}: NOT SERIALIZABLE - {e}")

    print("\n2. Testing Pydantic model class:")
    try:
        ormsgpack.packb(MyModel)
        print(f"✅ MyModel class: SERIALIZABLE")
    except Exception as e:
        print(f"❌ MyModel class: NOT SERIALIZABLE - {e}")
        print(f"   Type: {type(MyModel)}")
        print(f"   __class__: {MyModel.__class__}")

    print("\n3. Testing model instance:")
    instance = MyModel(name="test")
    try:
        ormsgpack.packb(instance)
        print(f"✅ MyModel instance: SERIALIZABLE")
    except Exception as e:
        print(f"❌ MyModel instance: NOT SERIALIZABLE - {e}")

    print("\n3b. Testing with OPT_SERIALIZE_PYDANTIC:")
    try:
        serialized = ormsgpack.packb(instance, option=ormsgpack.OPT_SERIALIZE_PYDANTIC)
        print(f"✅ MyModel instance with OPT_SERIALIZE_PYDANTIC: SERIALIZABLE")
        print(f"   Serialized length: {len(serialized)} bytes")
        # Try to deserialize
        deserialized = ormsgpack.unpackb(serialized)
        print(f"   Deserialized: {deserialized}")
    except Exception as e:
        print(
            f"❌ MyModel instance with OPT_SERIALIZE_PYDANTIC: NOT SERIALIZABLE - {e}"
        )

    print("\n4. Testing different representations:")
    # String representation
    try:
        ormsgpack.packb("MyModel")
        print(f"✅ Class name as string: SERIALIZABLE")
    except Exception as e:
        print(f"❌ Class name as string: NOT SERIALIZABLE - {e}")

    # Module + name
    try:
        class_ref = {"module": MyModel.__module__, "name": MyModel.__name__}
        ormsgpack.packb(class_ref)
        print(f"✅ Class reference dict: SERIALIZABLE")
    except Exception as e:
        print(f"❌ Class reference dict: NOT SERIALIZABLE - {e}")

    # Schema representation
    try:
        schema = MyModel.model_json_schema()
        ormsgpack.packb(schema)
        print(f"✅ Model JSON schema: SERIALIZABLE")
    except Exception as e:
        print(f"❌ Model JSON schema: NOT SERIALIZABLE - {e}")

    print("\n5. Why types aren't serializable:")
    print(f"   - Types are Python objects in memory")
    print(f"   - They contain methods, attributes, metaclasses")
    print(f"   - msgpack only handles data, not executable code")
    print(f"   - Example: {type(int)} = {type(int)}")
    print(f"   - Example: {type(MyModel)} = {type(MyModel)}")


if __name__ == "__main__":
    test_type_serialization()
