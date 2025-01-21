from typing import Any
from flask import Blueprint
from http import HTTPStatus
from json import JSONDecodeError
from utils.error_handlers import handle_too_many_requests, handle_error
from controllers.rating_controller import process_credit_rating_request
from utils.decorators import log_method, limiter
from configs.constants import (
    API_BLUEPRINT_NAME,
    CREDIT_RATING_ENDPOINT,
    ERROR_MSG,
    VALIDATION_ERROR_MSG,
    INPUT_ERROR_MSG,
    MISSING_KEY_IN_PAYLOAD_MSG,
    INCORRECT_TYPE_IN_PAYLOAD_MSG,
    INVALID_JSON_FORMAT_MSG,
    POST,
    PER_MINUTE_10,
)

# Initialize Blueprint
api = Blueprint(API_BLUEPRINT_NAME, __name__)


@api.route(CREDIT_RATING_ENDPOINT, methods=[POST] )
@log_method
@limiter.limit(PER_MINUTE_10)
def calculate_credit_rating() -> Any:
    """
    Endpoint to calculate credit rating with rate limiting.

    Returns:
        Any: JSON response object with the result or error details.
    """
    try:
        print("push latest version")
        return process_credit_rating_request()
    except JSONDecodeError as e:
        return handle_error(e, INPUT_ERROR_MSG, HTTPStatus.BAD_REQUEST, INVALID_JSON_FORMAT_MSG)
    except ValueError as e:
        return handle_error(e, VALIDATION_ERROR_MSG, HTTPStatus.UNPROCESSABLE_ENTITY)
    except KeyError as e:
        return handle_error(e, MISSING_KEY_IN_PAYLOAD_MSG, HTTPStatus.BAD_REQUEST)
    except TypeError as e:
        return handle_error(e, INCORRECT_TYPE_IN_PAYLOAD_MSG, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return handle_error(e, ERROR_MSG, HTTPStatus.INTERNAL_SERVER_ERROR)


# Register the error handler with the blueprint
@api.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
def too_many_requests_handler(error):
    return handle_too_many_requests(error)
