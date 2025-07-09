import pytest

from haive.core.types.dynamic_literal import Colour, PaintJob


def test_valid_values():
    pj = PaintJob(base="red", accent="green")
    assert pj.base == "red"
    assert pj.accent == "green"


def test_register_and_use_new_value():
    Colour.register("violet")
    pj = PaintJob(base="violet", accent="blue")
    assert pj.base == "violet"
    assert pj.accent == "blue"


def test_unregister_value():
    Colour.register("tempcolor")
    pj = PaintJob(base="tempcolor", accent="red")
    assert pj.base == "tempcolor"
    Colour.unregister("tempcolor")
    with pytest.raises(ValueError):
        PaintJob(base="tempcolor", accent="red")


def test_invalid_type():
    with pytest.raises(TypeError):
        PaintJob(base=123, accent="green")  # type: ignore


def test_invalid_value():
    with pytest.raises(ValueError):
        PaintJob(base="chartreuse", accent="green")


def test_json_schema_contains_registered():
    Colour.register("ultraviolet")
    schema = PaintJob.model_json_schema()
    assert "ultraviolet" in schema["properties"]["base"]["enum"]
