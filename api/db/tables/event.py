from api.db.tables.person import Person
from enum import Enum
from piccolo.columns import Column, ForeignKey, Timestamp, UUID, Varchar
from piccolo.table import Table
import json

# With the exception of the 'id' column, table columns are organized alphabetically

# Timestamps are prefaced with `datetime_` to visually and alphabetically 'chunk'
# them together for easier reference 

class EventType(Enum):
    """
    The types that may be associated with an Event. 
    """
    CLICK = "click"
    SIGNUP = "signup"
    # 👇 Use this for manually adding/associating an event with a user for demo purposes
    SUBMITTED_FEEDBACK = "submitted_feedback" 

class Event(Table, help_text="Represents an Event associated with a Person"):
    """
    Represents a (client-side) Event associated with a Person.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # 💡 https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


    id: Column = UUID(
        helper_text="The id (primary key) of the Event.",
        null=False,
        primary_key=True,
        required=False,
        unique=True
    )

    datetime_created: Column = Timestamp(
        helper_text="The datetime the Event was created (or, when the event occurred).",
        null=False,
        required=False
    )

    event_type: Column = Varchar(
        choices=EventType,
        helper_text="The type of Event. Valid options are: 'click', 'signup', and 'submitted_feedback'.",
        null=False,
        required=True
    )

    person_id: Column = ForeignKey(
        helper_text="The id of the Person for whom this Event occurred (i.e., the id of the Person this Event is associated with).",
        null=False,
        required=True,
        references=Person
    )

