from api.db.tables.person import Person
from piccolo.utils.pydantic import create_pydantic_model
from typing import Any


PersonDeleteModel: Any = create_pydantic_model(
    exclude_columns=(Person.datetime_created, Person.datetime_modified, Person.email, Person.first_name, Person.last_name, Person.role),
    include_default_columns=True,
    model_name="PersonDeleteModel",
    table=Person,
)

# 👇 A pydantic model in a 'edit person' request shape
PersonPutModel: Any = create_pydantic_model(
    deserialize_json=True,
    include_default_columns=True,
    model_name="PersonPutModel",
    table=Person,
)

# 👇 A pydantic model in a 'create person' request shape 
PersonPostModel: Any = create_pydantic_model(
    exclude_columns=(Person.id, Person.datetime_created, Person.datetime_modified),
    deserialize_json=True,
    include_default_columns=False,
    model_name="PersonPostModel",
    table=Person,
)
