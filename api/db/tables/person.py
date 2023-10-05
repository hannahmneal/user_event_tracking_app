from datetime import datetime
from piccolo.columns import Column, Email, Timestamp, UUID, Varchar
from piccolo.table import Table

# Timestamps are prefaced with `datetime_` to visually and alphabetically 'chunk'
# them together for easier reference 

class Person(Table, help_text="Represents a person that accesses the api (i.e., a 'user')."):
    """
    Represents a person that accesses the api (i.e., a 'user').
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def to_json(self):
        return {
            'datetime_created': self.datetime_created,
            'datetime_modified': self.datetime_modified,
            'email': self.email,
            'first_name': self.first_name,
            'id': self.id,
            'last_name': self.last_name,
        }


    datetime_created: Column = Timestamp(
        null=False,
        required=False
    )
    datetime_modified: Column = Timestamp(
        auto_update=datetime.now(),
        null=False,
        required=False
    )
    email: Column = Email(
        length=40,
        null=True,
        required=True
    )
    first_name: Column = Varchar(
        default=None,
        length=40,
        null=True
    )
    id: Column = UUID(
        primary_key=True,
        null=False,
        required=False,
        unique=True
    )
    last_name: Column = Varchar(
        default=None,
        length=40,
        null=True
    )

    # TODO: Add role
