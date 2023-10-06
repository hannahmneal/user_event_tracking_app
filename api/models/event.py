from api.db.tables.event import Event
from piccolo.utils.pydantic import create_pydantic_model
from typing import Any


# 👇 A pydantic model in a 'delete event' request shape
EventDeleteModel: Any = create_pydantic_model(
    include_default_columns=True,
    model_name="EventDeleteModel",
    table=Event,
)

# 👇 A pydantic model in a 'create event' request shape 
EventPostModel: Any = create_pydantic_model(
    all_optional=True,
    include_default_columns=False,
    model_name="EventPostModel",
    table=Event,
)
