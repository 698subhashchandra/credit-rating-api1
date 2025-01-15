from typing import Optional, Any
from flask import jsonify
from http import HTTPStatus
from utils.logger import project_logger
from configs.constants import ERROR_MSG, TOO_MANY_REQUESTS_MSG, RETRY_AFTER_HEADER, MSG, STATUS_CODE, \
    ERROR_LOGGING_EXCEPTION, DESCRIPTION
from utils.response import create_api_response


def handle_error(
    exception: Exception,
    message: str,
    status_code: int,
    log_message: Optional[str] = None
) -> Any:
    """
    Helper function to handle error responses and log the exception.
    """
    try:
        if log_message:
            project_logger.error(f"{log_message}: {exception}")
        return create_api_response(msg=message, status_code=status_code, data={})
    except Exception as e:
        project_logger.error(f"{ERROR_LOGGING_EXCEPTION}: {e}")
        return create_api_response(msg=ERROR_MSG, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


def handle_too_many_requests(error) -> tuple:
    """
    Handle Too Many Requests (429) errors gracefully.
    """
    retry_after = error.description if hasattr(error, DESCRIPTION) else "60"  # Default retry time in seconds
    return (
        jsonify({
            MSG: TOO_MANY_REQUESTS_MSG,
            STATUS_CODE: HTTPStatus.TOO_MANY_REQUESTS,
            RETRY_AFTER_HEADER: retry_after,
        }),
        HTTPStatus.TOO_MANY_REQUESTS,
        {RETRY_AFTER_HEADER: retry_after},
    )
