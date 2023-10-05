from blacksheep import Application, FromQuery, FromJSON, Response, bad_request, not_found, ok
from blacksheep.exceptions import InternalServerError
from blacksheep.server.openapi.v3 import OpenAPIHandler
from .constants import *
from datetime import datetime
from api.db.tables.person import Person
from dotenv import load_dotenv
import json
from .models import (
    PersonModelDeleteRequest,
    PersonModelPostRequest,
    PersonModelPutRequest,
)
from openapidocs.v3 import Info
import os
from piccolo.engine import engine_finder
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
    Gets a list of all Persons
    """
    try:
        print(f"\nGetting a list of all Persons...")
        persons = await Person.select()
        if not persons:
            return ok(message=custom_response(data=persons, details="The request was successful, however, there are no items in the database to retrieve.", message="Ok", status_code=200))
        return ok(message=custom_response(data=persons, details=successful_message(), message="Ok", status_code=200))
    except Exception as e:
        raise InternalServerError(message=custom_response(data=None, details=internal_server_error_message(ex=e), message="Internal Server Error", status_code=500))


@get("/persons/{id}")
async def persons(id: str) -> Response:
    """
    Gets a Person by its id
    """
    try:
        print(f"\nGetting Person by id {id}...")
        person = await Person.select().where(id==Person.id).first()

        if not person:
            return not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=id), message="Not Found", status_code=404))
        
        return ok(message=custom_response(data=person, details=successful_message(), message="Ok", status_code=200))
    except Exception as e:
        raise InternalServerError(message=custom_response(data=None, details=internal_server_error_message(ex=e), message="Internal Server Error", status_code=500))


@post("/persons")
async def persons(req: FromJSON[PersonModelPostRequest]) -> Response:
    """
    Creates a new Person
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

        await person.save().run()
        created_person = await Person.select().where(person.id==Person.id).first()
        
        if not created_person:
            raise not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=person.id), message="Not Found", status_code=404))

        return ok(message=custom_response(data=created_person, details=successful_message(), message="Ok", status_code=201))
    except Exception as e:
        raise bad_request(message=custom_response(data=None, details=not_created_message(ent='Person', ex=e), message="Bad Request", status_code=400))
    
@put("/persons/{id}")
async def persons(id: str, req: FromJSON[PersonModelPutRequest]) -> Response:
    """
    Updates an existing Person with the data from the request
    """
    try:
        print(f"\nEditing Person with id {id}...")

        request_id = req.value.dict()['id']
        if id is not request_id:
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
async def persons(id: str, req: FromJSON[PersonModelDeleteRequest]) -> Response:
    """
    Deletes a Person from the database
    """

    try:
        request_id = req.value.dict()['id']
        # TODO: The route and request body should be checked the same way here as in the PUT but that isn't the case. Currently the item is deleted based solely on the existence of the id in the route.
        # This is necessary because the types are different for the id and request_id even when their string counterpart is the same:
        # print(f"\n type id >>> {id} \n type request_id >>> {request_id}")
        # if id is not request_id:
        #     return bad_request(message=custom_response(data=None, details=route_request_mismatch_message(id=id, request_id=request_id), message="Bad Request", status_code=400))
        
        print(f"\nGetting Person by id {id}...")
        person = await Person.select().where(id==Person.id).first()

        if not person:
            return not_found(message=custom_response(data=person, details=not_found_by_id_message(ent='Person', id=id), message="Not Found", status_code=404))

        print(f"\nDeleting Person with id {id}...")
        await Person.delete().where(id==Person.id).run()
        return ok(message=custom_response(data=None, details=successful_message(), message="Ok", status_code=200))

    except Exception as e:
        return bad_request(message=custom_response(data=None, details=route_request_mismatch_message(id=id, request_id=request_id), message="Bad Request", status_code=400))

# -------------------------------------------------------------------------------------------

# TODO: Either move db session code to another file or move routes (above) to a separate file
async def open_database_connection_pool(application):
    print("Opening database connection pool...")
    try:
        # TODO: Tables need to be created (if they don't exist) prior to executing transactions; handle this here?
        engine = engine_finder()
        await engine.start_connection_pool()
        await Person.create_table(if_not_exists=True)
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
