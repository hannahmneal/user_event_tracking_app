from api.db.tables.person import Person
from piccolo.utils.pydantic import create_pydantic_model
from typing import Any


PersonModelDeleteRequest: Any = create_pydantic_model(
    exclude_columns=(Person.datetime_created, Person.datetime_modified, Person.email, Person.first_name, Person.last_name),
    include_default_columns=True,
    model_name="PersonModelDeleteRequest",
    table=Person,
)

# 👇 A pydantic model in a 'edit person' request shape
PersonModelPutRequest: Any = create_pydantic_model(
    exclude_columns=(Person.datetime_created, Person.datetime_modified),
    include_default_columns=True,
    model_name="PersonModelPutRequest",
    table=Person,
)

# 👇 A pydantic model in a 'create person' request shape 
PersonModelPostRequest: Any = create_pydantic_model(
    all_optional=True,
    # 👇 Fields like 'id' and 'datetime_create' will not be expected in the request
    include_default_columns=False,
    model_name="PersonModelPostRequest",
    table=Person,
)

