from .constants import *
from .models import (
    EventDeleteModel,
    EventPostModel,
    PersonDeleteModel,
    PersonPostModel,
    PersonPutModel,
)
from api.db.tables.event import Event
from api.db.tables.person import Person
from blacksheep import Application, FromJSON, FromQuery, Response, bad_request, not_found, ok
from blacksheep.exceptions import InternalServerError
from blacksheep.server.openapi.v3 import OpenAPIHandler
from datetime import datetime
from dotenv import load_dotenv
from openapidocs.v3 import Info
from piccolo.engine import engine_finder
from typing import Optional
import os
import uuid

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
# 👇 For security reasons, we only want this variable to be true in a local environment
SHOW_ERROR_DETAILS = os.environ.get("SHOW_ERROR_DETAILS", None)

if ENVIRONMENT in ["local"]:
    os.environ[SHOW_ERROR_DETAILS] = "true"
    app = Application(show_error_details=SHOW_ERROR_DETAILS)
else:
    os.environ[SHOW_ERROR_DETAILS] = "false"
    app = Application(show_error_details=SHOW_ERROR_DETAILS)

delete = app.router.delete
get = app.router.get
post = app.router.post
put = app.router.put

docs = OpenAPIHandler(info=Info(title="User Event Tracking Api Application", version="0.0.1"))
docs.bind_app(app)

# -------------------------------------------------------------------------------------------

@get("/")
def home():
    return f"\nHello, World! {datetime.utcnow().isoformat()}"

@get("/crash_test")
def crash_test():
    raise Exception("Crash test")

# -------------------------------------------------------------------------------------------

@get("/persons")
async def persons() -> Response:
    """
    Gets a list of all Persons. Note that if _no_ Person items are present in the database, an empty array is returned *successfully*.
    """
    try:
        print(f"\nGetting a list of all Persons...")
        persons = await Person.select()
        if not persons:
            # 💡 This 'successfully returned no data in array' situation might be really annoying for UI development,
            # especially if array operations are involved. It might be easier to throw an error instead.
            return ok(message=custom_response(data=persons, details="The request was successful, however, there are no items in the database to retrieve.", message="Ok", status_code=200))
        return ok(message=custom_response(data=persons, details=successful_message(), message="Ok", status_code=200))
    except Exception as e:
        return not_found(message=custom_response(data=persons, details=not_found_message(ex=e), message="Not Found", status_code=404))


@get("/persons/{id}")
async def persons(id: str) -> Response:
    """
    Gets a Person by its id.
    """
    try:
        print(f"\nGetting Person by id {id}...")
        person = await Person.select().where(id==Person.id).first()

        if not person:
            return not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=id), message="Not Found", status_code=404))
        
        return ok(message=custom_response(data=person, details=successful_message(), message="Ok", status_code=200))
    except Exception as e:
        return bad_request(message=custom_response(data=person, details=bad_request_message(ex=e), message="Bad Request", status_code=400))


@post("/persons")
async def persons(req: FromJSON[PersonPostModel]) -> Response:
    """
    Creates a new Person.
    """
    try:
        print("\nCreating new Person...")
        person = Person(**req.value.dict())

        if person.id is None:
            person.id = uuid.uuid4()

        if person.datetime_created is None:
            person.datetime_created = datetime.utcnow()
            # Set modified to the same value as created
            person.datetime_modified = person.datetime_created

        person.events = []

        await person.save().run()
        created_person = await Person.select().where(person.id==Person.id).first()
        
        if not created_person:
            return not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=person.id), message="Not Found", status_code=404))

        # # TODO: Move to a service layer
        # # 👇 Logic to add 'signup' event to newly-created Person
        # print(f"\nCreating signup Event for Person with id {created_person.id} and role {created_person.role}...")
        # events = []
        # signup_event = Event(
        #     id = uuid.uuid4(),
        #     datetime_created = datetime.utcnow(),
        #     event_type = EventType.SIGNUP,
        #     person_id = person.id
        # )

        # print(f"\n >>> signup_event >>> {signup_event}")
        # events.append(signup_event)
        # await signup_event.save().run()
        # created_person.events = events
        # print(f"\n >>> created_person >>> {created_person}")

        return ok(message=custom_response(data=created_person, details=successful_message(), message="Ok", status_code=201))
    except Exception as e:
        return bad_request(message=custom_response(data=None, details=not_created_message(ent='Person', ex=e), message="Bad Request", status_code=400))
    
@put("/persons/{id}")
async def persons(id: str, req: FromJSON[PersonPutModel]) -> Response:
    """
    Updates an existing Person with the data from the request
    """
    try:
        print(f"\nEditing Person with id {id}...")

        request_id = req.value.dict()['id']
        # 👇 Ensure the ids in the route and request body match
        if id != str(request_id):
            return bad_request(message=custom_response(data=None, details=route_request_mismatch_message(id=id, request_id=request_id), message="Bad Request", status_code=400))

        await Person.update(**req.value.dict()).where(id==Person.id).run()

        print(f"\nGetting Person by id {id}...")
        edited_person = await Person.select().where(id==Person.id).first()

        if not edited_person:
            return not_found(message=custom_response(data=edited_person, details=not_found_by_id_message(ent='Person', id=id), message="Not Found", status_code=404))

        return ok(message=custom_response(data=edited_person, details=successful_message(), message="Ok", status_code=200))

    except Exception as e:
        raise InternalServerError(message=custom_response(data=None, details=internal_server_error_message(ex=e), message="Internal Server Error", status_code=500))


@delete("/persons/{id}")
async def persons(id: str, req: FromJSON[PersonDeleteModel]) -> Response:
    """
    Deletes a Person from the database
    """

    try:
        request_id = req.value.dict()['id']
        # 👇 Ensure the ids in the route and request body match
        if id != str(request_id):
            return bad_request(message=custom_response(data=None, details=route_request_mismatch_message(id=id, request_id=request_id), message="Bad Request", status_code=400))
        
        print(f"\nGetting Person by id {id}...")
        person = await Person.select().where(id==Person.id).first()

        if not person:
            return not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=id), message="Not Found", status_code=404))

        print(f"\nDeleting Person with id {id}...")
        await Person.delete().where(id==Person.id).run()
        return ok(message=custom_response(data=None, details=successful_message(), message="Ok", status_code=200))

    except Exception as e:
        return bad_request(message=custom_response(data=person, details=f"{route_request_mismatch_message(id=id, request_id=request_id)} Details: {e}", message="Bad Request", status_code=400))

# -------------------------------------------------------------------------------------------

# TODO: Add search params for event id and person_id
@get("/events")
async def events(keyword: Optional[FromQuery[str]]) -> Response:
    """
    Gets a list of all Events
    """

    try:
        print(f"\nGetting a list of all Events...")
        if not keyword:
            events = await Event.select()
            if not events:
                # 💡 This 'successfully returned no data in array' situation might be really annoying for UI development,
                # especially if array operations are involved. It might be easier to throw an error instead.
                return ok(message=custom_response(data=events, details="The request was successful, however, there are no items in the database to retrieve.", message="Ok", status_code=200))
            return ok(message=custom_response(data=events, details=successful_message(), message="Ok", status_code=200))

        events_search = await Event.select().where(keyword.value == Event.event_type).run()
        if not events_search:
            # 💡 This 'successfully returned no data in array' situation might be really annoying for UI development,
            # especially if array operations are involved. It might be easier to throw an error instead.
            return ok(message=custom_response(data=events_search, details="The request was successful, however, there are no items in the database to retrieve.", message="Ok", status_code=200))
        return ok(message=custom_response(data=events_search, details=successful_message(), message="Ok", status_code=200))
    except Exception as e:
        return not_found(message=custom_response(data=None, details=not_found_message(ent='Event', ex=e), message="Not Found", status_code=404))    


@get("/events/{id}")
async def events(id: str) -> Response:
    """
    Gets an Event by its id.
    """
    try:
        print(f"\nGetting Event by id {id}...")
        event = await Event.select().where(id==Event.id).first()

        if not event:
            return not_found(message=custom_response(data=event, details=not_found_by_id_message(ent='Event', id=id), message="Not Found", status_code=404))
        
        return ok(message=custom_response(data=event, details=successful_message(), message="Ok", status_code=200))
    except Exception as e:
        return bad_request(message=custom_response(data=event, details=bad_request_message(ex=e), message="Bad Request", status_code=400))


@post("/events")
async def events(req: FromJSON[EventPostModel]) -> Response:
    """
    Creates a new Event.
    """

    try:
        print("\nCreating new Event...")
        event = Event(**req.value.dict())

        if event.id is None:
            event.id = uuid.uuid4()

        if event.datetime_created is None:
            event.datetime_created = datetime.utcnow()

    #     # 👇 Check that the person_id in the request actually exists on a person before trying to attach an event to it
        print(f"\Confirming that a Person with id {event.person_id} exists...")
        person = await Person.select().where(event.person_id==Person.id).first().output(load_json=True)
        if not person:
            return not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=event.id), message="Not Found", status_code=404))
        
        # TODO
        # # 👇 Check event_type and confirm that if the requested event_type is 'signup', this type doesn't already exist for the person ('signup' should only be stored once for a Person)
        # person_with_signup_event = await Person.select(Event.event_type.arrow("signup")).where(event.person_id==Person.id).first().output(load_json=True)
        # print(f"\n e in person_with_signup_event >>> {person_with_signup_event}")
        # if person_with_signup_event is EventType.SIGNUP and event.event_type is EventType.SIGNUP:
        #     # Should this be 409 Conflict?
        #     return bad_request(message="An event type of 'signup' cannot be added to a Person with an existing 'signup' event type.")

        serializable_event = Event(
            id=event.id,
            datetime_created = event.datetime_created,
            event_type=req.value.dict()['event_type'],
            person_id=req.value.dict()['person_id']
        )

        await serializable_event.save().run()

        # TODO: This still needs to be joined to the Person
        created_event = await Event.select().where(event.id==Event.id).first()
        if not created_event:
            return not_found(message=custom_response(data=serializable_event, details=not_found_by_id_message(ent='Event', id=event.id), message="Not Found", status_code=404))

        return ok(message=custom_response(data=created_event, details=successful_message(), message="Ok", status_code=201))
    except Exception as e:
        return bad_request(message=custom_response(data=event, details=not_created_message(ent='Event', ex=e), message="Bad Request", status_code=400))


@delete("/events/{id}")
async def events(id: str, req: FromJSON[EventDeleteModel]) -> Response:
    """
    Deletes a Event from the database
    """

    try:
        request_id = req.value.dict()['id']
        # 👇 Ensure the ids in the route and request body match
        if id != str(request_id):
            return bad_request(message=custom_response(data=None, details=route_request_mismatch_message(id=id, request_id=request_id), message="Bad Request", status_code=400))
        
        print(f"\nGetting Event by id {id}...")
        event = await Event.select().where(id==Event.id).first()

        if not event:
            return not_found(message=custom_response(data=event, details=not_found_by_id_message(ent='Event', id=id), message="Not Found", status_code=404))

        print(f"\nDeleting Event with id {id}...")
        await Event.delete().where(id==Event.id).run()
        return ok(message=custom_response(data=None, details=successful_message(), message="Ok", status_code=200))

    except Exception as e:
        return bad_request(message=custom_response(data=event, details=f"{route_request_mismatch_message(id=id, request_id=request_id)} Details: {e}", message="Bad Request", status_code=400))

# -------------------------------------------------------------------------------------------

# TODO: Either move db session code to another file or move routes (above) to a separate file
async def open_database_connection_pool(application):
    print("Opening database connection pool...")
    try:
        # TODO: Tables need to be created (if they don't exist) prior to executing transactions; handle this here?
        engine = engine_finder()
        await engine.start_connection_pool()
        await Person.create_table(if_not_exists=True)
        await Event.create_table(if_not_exists=True)
    except Exception as e:
        print(f"Unable to connect to the database. Details: \n{e}")


async def close_database_connection_pool(application):
    print("\nClosing database connection pool...")
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception as e:
        print(f"Unable to close connection to the database. Details: \n{e}")


app.on_start += open_database_connection_pool
app.on_stop += close_database_connection_pool
