import pytest
from sqlmodel import SQLModel, create_engine, Session


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite://", echo=False)
    return engine


@pytest.fixture(scope="function")
def session(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def FooModel():
    from sqlmodel import Field

    class Foo(SQLModel):
        id: int | None = Field(default=None, primary_key=True)
        name: str = Field(max_length=20, description="Name")
        password: str = Field(max_length=20, description="Password")

        constraint_positive_int: int | None = Field(default=10, gt=0)

    return Foo
