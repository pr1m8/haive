import pytest

from haive.core.types.advanced_registry import (
    ComponentSpec,
    Lowercaser,
    Registered,
    TextPipeline,
    Tokenizer,
)


def test_registry_has_keys():
    keys = Registered.list_available()
    assert "whitespace-tokenizer" in keys
    assert "lowercaser" in keys
    assert "basic-text-pipeline" in keys  # fixed from "basic-pipeline"


def test_registry_instantiates_by_name():
    comp = Registered.factory("whitespace-tokenizer", text="Hi there")
    assert isinstance(comp, Tokenizer)
    assert comp.build() == ["Hi", "there"]


def test_component_spec_inline():
    inline = Lowercaser(text="TEST")
    spec = ComponentSpec[str](inline=inline)
    assert spec.build() == "test"


def test_component_spec_type_and_params():
    spec = ComponentSpec[str](type="lowercaser", params={"text": "HeLLo"})
    assert spec.build() == "hello"


def test_component_spec_invalid_both_type_and_inline():
    inline = Lowercaser(text="Oops")
    with pytest.raises(
        ValueError, match="Must provide exactly one of 'type' or 'inline'"
    ):
        ComponentSpec[str](type="lowercaser", params={}, inline=inline)


def test_component_spec_invalid_neither_type_nor_inline():
    with pytest.raises(
        ValueError, match="Must provide exactly one of 'type' or 'inline'"
    ):
        ComponentSpec[str]()  # should raise error


def test_text_pipeline_build():
    config = {
        "tokenizer": {"type": "whitespace-tokenizer", "params": {"text": "Hi AI"}},
        "normaliser": {"type": "lowercaser", "params": {"text": "MoDeRn"}},
    }
    pipeline = TextPipeline(**config)
    result = pipeline.build()
    assert result == ["hi", "ai", "modern"]
    assert pipeline.summary.startswith("basic-text-pipeline")  # corrected name


def test_registry_summary_serialization():
    obj = Lowercaser(text="Caps")
    assert "lowercaser" in obj.summary
    dumped = obj.model_dump()
    assert dumped["text"] == "Caps"
    serialized = obj._serialize()
    assert serialized["type"] == "lowercaser"
    assert serialized["text"] == "Caps"
