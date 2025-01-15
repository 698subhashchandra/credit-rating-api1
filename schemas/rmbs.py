from pydantic import BaseModel, Field, PositiveFloat, ValidationError
from typing import List, Literal
from configs.constants import CREDIT_SCORE_MIN, CREDIT_SCORE_MAX, LOAN_TYPE_FIXED, LOAN_TYPE_ADJUSTABLE, \
    PROPERTY_TYPE_SINGLE_FAMILY, PROPERTY_TYPE_CONDO
from utils.logger import project_logger


class Mortgage(BaseModel):
    """
    Represents a mortgage record for a borrower.

    Attributes:
        credit_score (int): Borrower's credit score between 300 and 850.
        loan_amount (PositiveFloat): The loan amount for the mortgage.
        property_value (PositiveFloat): The value of the property for the mortgage.
        annual_income (PositiveFloat): Borrower's annual income.
        debt_amount (PositiveFloat): Borrower's total debt.
        loan_type (Literal["fixed", "adjustable"]): The type of loan, either "fixed" or "adjustable".
        property_type (Literal["single_family", "condo"]): The type of property, either "single_family" or "condo".
    """
    credit_score: int = Field(..., ge=CREDIT_SCORE_MIN, le=CREDIT_SCORE_MAX, description="Borrower's credit score")
    loan_amount: PositiveFloat
    property_value: PositiveFloat
    annual_income: PositiveFloat
    debt_amount: PositiveFloat
    loan_type: Literal[LOAN_TYPE_FIXED, LOAN_TYPE_ADJUSTABLE]
    property_type: Literal[PROPERTY_TYPE_SINGLE_FAMILY, PROPERTY_TYPE_CONDO]

    def __init__(self, **kwargs):
        """
        Initialize the Mortgage instance.

        Args:
            **kwargs: Keyword arguments for the mortgage attributes.
        """
        try:
            super().__init__(**kwargs)
        except ValidationError as e:
            project_logger.error(f"Error initializing Mortgage: {e.json()}")
            raise ValueError("Invalid data provided for Mortgage") from e


class RMBSPayload(BaseModel):
    """
    Represents the payload for the RMBS (Residential Mortgage-Backed Securities) data.

    Attributes:
        mortgages (List[Mortgage]): A list of Mortgage objects.
    """
    mortgages: List[Mortgage]

    def __init__(self, **kwargs):
        """
        Initialize the RMBSPayload instance.

        Args:
            **kwargs: Keyword arguments for the payload attributes.
        """
        try:
            super().__init__(**kwargs)
        except ValidationError as e:
            project_logger.error(f"Error initializing RMBSPayload: {e.json()}")
            raise ValueError("Invalid data provided for RMBSPayload") from e
