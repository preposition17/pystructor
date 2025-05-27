import pytest

from pydantic import BaseModel, Field
from pydantic.fields import PydanticUndefined
from sqlmodel import SQLModel

from pystructor import partial
from pystructor import omit
from pystructor import pick


def test_partial(FooModel):

    @partial(FooModel)
    class PartialFooModel(SQLModel):
        required_field: str = Field(...)

    assert PartialFooModel.model_fields["name"].default is None
    assert PartialFooModel.model_fields["name"].is_required() is False
    assert PartialFooModel.model_fields["required_field"].is_required()
    assert issubclass(PartialFooModel, BaseModel)


def test_partial_no_pydantic(FooModel):

    with pytest.raises(TypeError):
        @partial(FooModel)
        class PartialFooModel:
            required_field: str = Field(...)

    with pytest.raises(TypeError):

        class BarModel:
            a: str

        @partial(BarModel)
        class PartialFooModel(BaseModel):
            required_field: str


def test_omit(FooModel):

    @omit(FooModel, "id")
    class OmitFooModel(BaseModel):
        test_field: str

    assert "id" not in OmitFooModel.model_fields
    assert "test_field" in OmitFooModel.model_fields


def test_pick(FooModel):

    @pick(FooModel, "name")
    class PickFooModel(BaseModel):
        test_field: str

    assert "id" not in PickFooModel.model_fields
    assert "password" not in PickFooModel.model_fields
    assert "name" in PickFooModel.model_fields
    assert "test_field" in PickFooModel.model_fields


def test_omit_fields_override(FooModel):

    @omit(FooModel, "id")
    class OmitFooModel(BaseModel):
        name: str = Field(..., max_length=10)

    omit_foo_schema = OmitFooModel.schema()

    assert "id" not in OmitFooModel.model_fields
    assert omit_foo_schema["properties"]["name"]["maxLength"] == 10


def test_partial_fields_override(FooModel):

    @partial(FooModel)
    class PartialFooModel(SQLModel):
        name: str = Field(..., max_length=10)

    partial_foo_schema = PartialFooModel.schema()

    assert PartialFooModel.model_fields["name"].default is PydanticUndefined
    assert partial_foo_schema["properties"]["name"]["maxLength"] == 10
