from http import HTTPStatus
from typing import Optional, Dict, Any
from flask import jsonify
from utils.logger import project_logger
from configs.constants import DEFAULT_ERROR_REQUEST_MESSAGE, DEFAULT_MSG, STATUS_CODE, DATA, MSG, EMPTY_DATA, \
    DEFAULT_ERROR_RESPONSE_MESSAGE


class ApiResponse:
    def __init__(self, msg: Optional[str] = None, status_code: Optional[int] = None,
                 data: Optional[Dict[str, Any]] = None):
        """
        Initialize an API response object with a message, status code, and optional data.
        """
        self.msg = msg
        self.status_code = status_code or HTTPStatus.OK  # Default to HTTP 200
        self.data = data

    def set_response(self, msg: str, status_code: int, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Set the response message, status code, and data.
        """
        self.msg = msg
        self.status_code = status_code
        self.data = data

    def result(self) -> Dict[str, Any]:
        """
        Return the response as a dictionary.
        """
        return {
            MSG: self.msg if self.msg is not None else DEFAULT_MSG,
            STATUS_CODE: self.status_code.value,  # Get the numerical value of the status code
            DATA: self.data if self.data is not None else EMPTY_DATA
        }


def create_api_response(
        msg: str,
        status_code: int,
        data: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Utility function to create a consistent API response.
    """
    try:
        response = ApiResponse()
        response.set_response(msg=msg, status_code=status_code, data=data)
        return jsonify(response.result())
    except Exception as e:
        project_logger.error(f"{DEFAULT_ERROR_RESPONSE_MESSAGE}: {e}")
        return create_api_response(msg=DEFAULT_ERROR_REQUEST_MESSAGE, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


