from http import HTTPStatus
from typing import Any, Dict, List

from flask import request
from pydantic import ValidationError
from configs.constants import (
    VALIDATION_ERROR_MSG,
    ERROR_CALCULATING_RATING_MSG,
    VALIDATION_FAILED_MSG, CREDIT_RATING_NOT_FOUND_MSG, SUCCESS_MSG, CREDIT_RATING
)
from domain.credit_rating import CreditRatingService
from schemas.rmbs import RMBSPayload
from utils.logger import project_logger
from utils.response import create_api_response


def validate_payload(data: Dict[List, Any]) -> RMBSPayload:
    """
    Validate and parse the incoming payload.

    Args:
        data (Dict[str, Any]): The incoming data, expected to match the structure of RMBSPayload.

    Returns:
        RMBSPayload: Parsed payload if valid.

    Raises:
        ValidationError: If the payload is not valid according to the RMBSPayload schema.
    """
    try:
        return RMBSPayload.model_validate(data)
    except ValidationError as e:
        project_logger.error(f"{VALIDATION_ERROR_MSG}: {e.json()}")
        raise ValidationError(f"{VALIDATION_FAILED_MSG}: {e}") from e


def calculate_credit_rating_service(mortgages: Dict[str, Any]) -> str:
    """
    Service to calculate credit rating based on mortgage data.

    Args:
        mortgages (Dict[str, Any]): The mortgage data, expected to be a dictionary containing mortgage details.

    Returns:
        float: The calculated credit rating based on the mortgage data.

    Raises:
        Exception: If there is any error during the credit rating calculation process.
    """
    try:
        return CreditRatingService().calculate_credit_rating(mortgages)
    except Exception as e:
        project_logger.error(f"{ERROR_CALCULATING_RATING_MSG}: {e}")
        raise Exception(ERROR_CALCULATING_RATING_MSG) from e


def process_credit_rating_request() -> Any:
    """
    Process the credit rating calculation request.

    Returns:
        Any: JSON response object with the result or error details.
    """
    # Parse and validate payload
    payload = validate_payload(request.json)

    # Compute credit rating
    rating = calculate_credit_rating_service(payload.mortgages)

    if not rating:
        project_logger.warning(CREDIT_RATING_NOT_FOUND_MSG)
        return create_api_response(
            msg=CREDIT_RATING_NOT_FOUND_MSG,
            status_code=HTTPStatus.NOT_FOUND,
            data={},
        )

    return create_api_response(
        msg=SUCCESS_MSG,
        status_code=HTTPStatus.OK,
        data={CREDIT_RATING: rating},
    )

