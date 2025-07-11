import pytest

from haive.core.types.serializable_callable import SerializableCallable

# ---------- Sample Callables ----------


def sample_add(a: int, b: int) -> int:
    return a + b


class MathUtils:
    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b

    def instance_method(self):
        return "not supported"


# ---------- Tests ----------


def test_serialize_valid_function():
    path = SerializableCallable.serialize(sample_add)
    assert path.endswith("test_serializable_callable.sample_add")


def test_serialize_static_method():
    path = SerializableCallable.serialize(MathUtils.multiply)
    assert path.endswith("MathUtils.multiply")


def test_serialize_lambda_should_fail():
    with pytest.raises(ValueError, match="Cannot serialize"):
        SerializableCallable.serialize(lambda x: x + 1)


def test_serialize_closure_should_fail():
    def outer():
        def inner(x):
            return x * 2

        return inner

    closure = outer()
    with pytest.raises(ValueError, match="Cannot serialize"):
        SerializableCallable.serialize(closure)


def test_is_serializable_positive():
    assert SerializableCallable.is_serializable(sample_add)
    assert SerializableCallable.is_serializable(MathUtils.multiply)


def test_is_serializable_negative():
    assert not SerializableCallable.is_serializable(lambda x: x)
    assert not SerializableCallable.is_serializable(MathUtils().instance_method)


def test_serialize_valid_function():
    path = SerializableCallable.serialize(sample_add)
    assert path.endswith(".sample_add")


def test_deserialize_static_method():
    path = SerializableCallable.serialize(MathUtils.multiply)
    resolved = SerializableCallable.deserialize(path)
    assert resolved(3, 4) == 12


def test_deserialize_invalid_path_should_fail():
    with pytest.raises(ImportError):
        SerializableCallable.deserialize("nonexistent.module.function")


def test_deserialize_non_callable_should_fail(tmp_path):
    with pytest.raises(ImportError, match="is not callable"):
        SerializableCallable.deserialize(
            "os.path"
        )  # resolves to a module, not a function
