from blacksheep import Request
import json
import uuid

# Use like this: json.dumps(cat.to_json(), cls=UUIDEncoder)
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            print(f"\nEncoding UUID...")
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
    

async def serialize_request(req: Request):
    """
    Encodes and serializes a request object so it can be entered into the database.
    """
    # TODO HN 10/7/23: I've experienced some issues with some requests that have 'complex' datatypes
    # (jsonb, datetime) when using `FromJSON[model_created_with_create_pydantic_model]`. Until I get
    # that sorted, this will remain here.

    # Due to the nature of asyncio + Python3 and coroutines, a Runtime error will occur if
    # this is not awaited. For more information, see the resource below:
    # https://xinhuang.github.io/posts/2017-07-31-common-mistakes-using-python3-asyncio.html
    # 👉 Note that if `req: FromJSON` were used (instead of req: Request), `req.value` would 
    # produce the same result as `req.json()` below.
    req_as_json: dict = await req.json()
    # Produces: "events": [{"id": "67186145-baac-4f76-aad4-1f0612a5c752", "datetime_created": "2023-10-07T17:13:59.567243", "event_type": "click", "person_id": "3ba243a5-25ba-4a87-bc4d-05103bd4acc8"}]

    # Encode the json'd request from above:
    req_json_encoded: str = json.JSONEncoder().encode(req_as_json)

    # Serialize request
    # (json.dumps 👉 Serialize obj to a JSON formatted str)
    req_serialized: str = json.dumps(req_json_encoded)
    # Produces: "{\"events\": [{\"id\": \"67186145-baac-4f76-aad4-1f0612a5c752\", \"datetime_created\": \"2023-10-07T17:13:59.567243\", \"event_type\": \"click\", \"person_id\": \"3ba243a5-25ba-4a87-bc4d-05103bd4acc8\"}]}"

    return req_serialized


def custom_print(varname, o):
    """
    Custom console `print` the way I like it (I'll find a better solution later)
    """
    return print(f"\n >>> {varname} >>> {o}")

