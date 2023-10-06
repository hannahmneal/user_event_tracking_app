from datetime import datetime
from enum import Enum
from piccolo.columns import Array, Column, Email, JSONB, Timestamp, UUID, Varchar
from piccolo.table import Table

# With the exception of the 'id' column, table columns are organized alphabetically

# Timestamps are prefaced with `datetime_` to visually and alphabetically 'chunk'
# them together for easier reference 

class Role(Enum):
    """
    Indicates what permissions level a Person has and how much access they have to the api.
    By default, a Person will have a 'user' role. A user will always have a signup event
    associated with them because, in its current version, this api does not support a 'guest'
    user (that is, an unknown Person with no personal identifying data associated with them
    who is accessing the api for the first time). 
    """
    USER = "user"
    ADMIN = "admin"

class Person(Table, help_text="Represents a person that accesses the api (i.e., a 'user')."):
    """
    Represents a Person that accesses the api (i.e., a 'user').
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    id: Column = UUID(
        helper_text="The id (primary key) of the Person.",
        primary_key=True,
        null=False,
        required=False,
        unique=True
    )

    datetime_created: Column = Timestamp(
        helper_text="The datetime the Person was created. Once set, this value will not change.",
        null=False,
        required=False
    )

    datetime_modified: Column = Timestamp(
        auto_update=datetime.now(),
        helper_text="The datetime the Person was modified. This automatically sets to 'datetime.now()' whenever a Person is updated (as in a PUT request).",
        null=False,
        required=False
    )

    email: Column = Email(
        helper_text="The email of the Person.",
        length=40,
        null=True,
        required=True
    )

    events: Column = Array(
        # TODO
        # base_column=JSONB(),
        base_column=Varchar(),
        helper_text="A list of event ids associated with the Person.",
    )

    first_name: Column = Varchar(
        default=None,
        helper_text="The first name of the Person.",
        length=40,
        null=True
    )

    last_name: Column = Varchar(
        default=None,
        helper_text="The last name of the Person.",
        length=40,
        null=True
    )

    role: Column = Varchar(
        choices=Role,
        default=Role.USER,
        helper_text="The role associated with the Person (used for permissions and api access). A 'signup' Event is assigned to a Person upon creation, mimicking a client-side signup event.",
        null=False,
    )
