from pydantic import BaseModel, ValidationError

from haive.core.types.dynamic_enum import DynamicEnum, create_dynamic_enum


# ─── Example subclass ─── #
class AnimalType(DynamicEnum):
    START_VALUES = ("dog", "cat", "bird")


# ─── Example Pydantic usage ─── #
class Animal(BaseModel):
    kind: AnimalType
    name: str


def test_valid_enum():
    a = Animal(kind="dog", name="Fido")
    assert a.kind == "dog"


def test_dynamic_registration():
    AnimalType.register("lizard", "ferret")
    assert "lizard" in AnimalType.choices()
    a = Animal(kind="lizard", name="Slinky")
    assert a.kind == "lizard"


def test_dynamic_removal():
    AnimalType.unregister("cat")
    try:
        Animal(kind="cat", name="Whiskers")
    except ValidationError as e:
        passe)


def test_json_schema():
    schema = Animal.model_json_schema()


def test_dynamic_enum_factory():
    PlanetType = create_dynamic_enum("PlanetType", ["earth", "mars", "venus"])

    class Mission(BaseModel):
        destination: PlanetType

    m = Mission(destination="mars")
    assert m.destination == "mars"
    PlanetType.register("pluto")
    m2 = Mission(destination="pluto")
    assert m2.destination == "pluto"


if __name__ == "__main__":
    test_valid_enum()
    test_dynamic_registration()
    test_dynamic_removal()
    test_json_schema()
    test_dynamic_enum_factory()
