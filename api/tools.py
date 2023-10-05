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