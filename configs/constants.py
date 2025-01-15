import logging

SERVICE_NAME = "credit_rating_api"

# Default environment settings
LOCAL = "local"
DEFAULT_ENV = "dev"

# Configuration file name
CONFIG_FILE_NAME = "config.ini"

# General Configuration for environments

HOST = "host"  # Host address for the application
PORT = "port"  # Port for the application to run
RELOADED = True  # Whether to use Flask's reloader (True for development, False for production)

# Configuration keys
ENV_KEY = "ENV"
FLASK_ENV = "FLASK_ENV"
DEBUG_KEY = "DEBUG"
HOST_KEY = "HOST"
PORT_KEY = "PORT"
LOGGING_TYPE_KEY = "LOGGING_TYPE"
CACHE_TYPE_KEY = "CACHE_TYPE"
RELOADED_KEY = "RELOADED"

# request
POST = "POST"
PER_MINUTE_10 = "10 per minute"  # Allow up to 10 requests per minute per IP

# Default values for configuration keys
DEFAULT_CONFIG_VALUES = {

    FLASK_ENV: "dev",
    DEBUG_KEY: False,
    HOST_KEY: "127.0.0.1",
    PORT_KEY: 5000,
    LOGGING_TYPE_KEY: "ERROR",
    CACHE_TYPE_KEY: "simple",
    RELOADED_KEY: "false"
}
TRUE_VALUES = {'true', '1', 't', 'y', 'yes'}
USE_RELOADER = "use_reloader"
LOG_TYPE = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "ERROR": logging.ERROR,
    "FATAL": logging.FATAL,
}

# log_configs
MAX_LOG_SIZE = 25 * 1024 * 1024
BACKUP_COUNT = 5
ERROR_MSG_LOGGER_SETUP = "Error setting up logger"
ERROR_MSG_LOG_DIR_CREATION = "Error creating log directory"

# Valid Ranges for Credit Score
CREDIT_SCORE_MIN = 300
CREDIT_SCORE_MAX = 850

# Loan Type Options
LOAN_TYPE_FIXED = "fixed"
LOAN_TYPE_ADJUSTABLE = "adjustable"

# Property Type Options
PROPERTY_TYPE_SINGLE_FAMILY = "single_family"
PROPERTY_TYPE_CONDO = "condo"

# Constants for Loan-to-Value Risk
LTV_HIGH_THRESHOLD = 0.9
LTV_MEDIUM_THRESHOLD = 0.8
LTV_HIGH_SCORE = 2
LTV_MEDIUM_SCORE = 1
LTV_LOW_SCORE = 0

# Constants for Debt-to-Income Risk
DTI_HIGH_THRESHOLD = 50
DTI_MEDIUM_THRESHOLD = 40
DTI_HIGH_SCORE = 2
DTI_MEDIUM_SCORE = 1
DTI_LOW_SCORE = 0

# Constants for Credit Score Risk
CREDIT_SCORE_GOOD = 700
CREDIT_SCORE_POOR = 650
CREDIT_SCORE_GOOD_DEDUCTION = -1
CREDIT_SCORE_POOR_ADDITION = 1
CREDIT_SCORE_NEUTRAL = 0

# Constants for Loan Type Risk
LOAN_TYPE_FIXED_SCORE = -1
LOAN_TYPE_ADJUSTABLE_SCORE = 1

# Constants for Property Type Risk
PROPERTY_TYPE_SINGLE_FAMILY_SCORE = 0
PROPERTY_TYPE_CONDO_SCORE = 1

# Constants for Final Credit Rating
RATING_SCORE_AAA = 2
RATING_SCORE_BBB = 5
RATING_AAA = "AAA"
RATING_BBB = "BBB"
RATING_C = "C"

#  Credit API Blueprint Configuration

CREDIT_RATING = "credit_rating"
API_BLUEPRINT_NAME = "api"

# Endpoint Routes
CREDIT_RATING_ENDPOINT = "/calculate_credit_rating"

# Response Messages
SUCCESS_MSG = "Credit rating calculation successful"
ERROR_MSG = "An unexpected error occurred."

# HTTP Status Codes
HTTP_STATUS_OK = 200
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# Logger Messages
UNEXPECTED_ERROR = "An unexpected error occurred while processing the request."
CREDIT_RATING_NOT_FOUND_MSG = "Credit rating not found for the given input."
MISSING_KEY_IN_PAYLOAD_MSG = "Missing key in payload."
INCORRECT_TYPE_IN_PAYLOAD_MSG = "Incorrect type in payload."

# Error
ERROR_CALCULATING_RATING_MSG = "Error calculating credit rating."
ERROR_MSG_LTV = "Error calculating LoanToValueRisk"
ERROR_MSG_DTI = "Error calculating DebtToIncomeRisk"
ERROR_MSG_CREDIT_SCORE = "Error calculating CreditScoreRisk"
ERROR_MSG_LOAN_TYPE = "Error calculating LoanTypeRisk"
ERROR_MSG_PROPERTY_TYPE = "Error calculating PropertyTypeRisk"
ERROR_MSG_TOTAL_RISK = "Error calculating total risk score"
ERROR_MSG_CREDIT_RATING = "Error calculating credit rating"
INPUT_ERROR_MSG = "There was an error with the input data."
ERROR_LOGGING_EXCEPTION = "Error logging exception"

# Success Messages
SUCCESS_MSG_CREDIT_RATING = "Credit rating calculated successfully"

# Validation and Input Error Messages
MISSING_KEY_ERROR_MSG = "Missing key in payload"
INCORRECT_TYPE_ERROR_MSG = "Incorrect type in payload"
VALIDATION_ERROR_MSG = "The provided data is invalid."
VALIDATION_FAILED_MSG = "Validation failed."
INVALID_JSON_FORMAT_MSG = "Invalid JSON format."

# Constants related to API response messages
DEFAULT_SUCCESS_MESSAGE = "Request processed successfully."
DEFAULT_ERROR_REQUEST_MESSAGE = "An error occurred while processing the request."
DEFAULT_ERROR_RESPONSE_MESSAGE = "Error in creating API response"
ERROR_MSG_LOGGING_EXCEPTION = "Error occurred while logging exception"
DEFAULT_MSG = 'No message provided'

EMPTY_DATA = {}
STATUS_CODE = "status_code"
MSG = "msg"
DATA = "data"
DESCRIPTION = "description"
TOO_MANY_REQUESTS_MSG = "Too many requests. Please retry after the specified time."
RETRY_AFTER_HEADER = "Retry-After"

# Error Messages
ERROR_SERVER_START = "Error while starting the server"
ERROR_APP_CREATION = "Error during app creation"

# Log Messages
LOG_LISTENING_AT = "Listening at"

# unittest
LOW_RISK_PAYLOAD = {
    "mortgages": [
        {
            "credit_score": 750,
            "loan_amount": 200000,
            "property_value": 250000,
            "annual_income": 60000,
            "debt_amount": 20000,
            "loan_type": "fixed",
            "property_type": "single_family",
        }
    ]
}

MEDIUM_RISK_PAYLOAD = {
    "mortgages": [
        {
            "credit_score": 700,
            "loan_amount": 2000.0,
            "property_value": 250000.0,
            "annual_income": 6000.0,
            "debt_amount": 20000.0,
            "loan_type": "fixed",
            "property_type": "single_family"
        },
        {
            "credit_score": 680,
            "loan_amount": 150000.0,
            "property_value": 175000.0,
            "annual_income": 45000.0,
            "debt_amount": 10000.0,
            "loan_type": "adjustable",
            "property_type": "condo"
        }
    ]
}

HIGH_RISK_PAYLOAD = {
    "mortgages": [
        {
            "credit_score": 700,
            "loan_amount": 2000.0,
            "property_value": 250000.0,
            "annual_income": 6000.0,
            "debt_amount": 20000.0,
            "loan_type": "fixed",
            "property_type": "single_family"
        },
        {
            "credit_score": 680,
            "loan_amount": 150000.0,
            "property_value": 175000.0,
            "annual_income": 45000.0,
            "debt_amount": 10000.0,
            "loan_type": "adjustable",
            "property_type": "condo"
        },
        {
            "credit_score": 680,
            "loan_amount": 150000.0,
            "property_value": 175000.0,
            "annual_income": 45000.0,
            "debt_amount": 10000.0,
            "loan_type": "adjustable",
            "property_type": "condo"
        }
    ]
}
