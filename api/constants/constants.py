    
def custom_response(data: any, details: str, message: str, status_code: int):
    return {
            "data": data,
            "response": {
                "details": details,
                "message": message,
                "status": status_code
        }
    }


# ent -> entity
# ex -> exception
# ------------------------- Bad Request ----------------------------------

def bad_request_message():
    return f"The request is invalid. Please ensure the data in your request is correct and try again."

def route_request_mismatch_message(id: str, request_id: str) -> str:
    return f"The id in the route ({id}) does not match the id in the request body ({request_id}). Please ensure the ids match and try again."

def not_created_message(ent, ex: Exception) -> str:
    return f"The {ent} was not created. Please ensure the data in your request is correct and try again. Details: \n {ex}"

# ------------------------ Internal Server Error -----------------------------------

def internal_server_error_message(ex: Exception) -> str:
    return f"An unknown error occurred while processing the request. Details: \n {ex}"


# --------------------------- Not Found --------------------------------

def not_found_message(ent, ex: Exception) -> str:
    return f"No {ent} were found. Details: \n {ex}"


def not_found_by_id_message(ent, id, ex: Exception=None) -> str:
    if ex is not None:
        return f"The {ent} with `id` {id} could not be found. Please ensure the `id` in your request is correct and try again. Details: \n {ex}"
        
    return f"The {ent} with `id` {id} could not be found. Please ensure the `id` in your request is correct and try again"


# --------------------------- Success --------------------------------

def successful_message() -> str:
    return f"The request was successful"

# -----------------------------------------------------------