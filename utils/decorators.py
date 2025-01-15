import time
from functools import wraps

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.logger import project_logger


# Helper function to determine the class name or fallback to "Function"
def get_class_name(args):
    if args and hasattr(args[0], "__class__"):
        return args[0].__class__.__name__
    return "Function"


# Decorator for logging class methods or functions
def log_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        class_name = get_class_name(args)
        func_name = func.__name__
        project_logger.info(
            f"Starting: {class_name}.{func_name} with args: {args[1:] if class_name != 'Function' else args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            project_logger.info(f"Finished: {class_name}.{func_name} successfully.")
            return result
        except Exception as e:
            project_logger.error(f"Error in: {class_name}.{func_name}, Error: {str(e)}")
            raise

    return wrapper


# Decorator for measuring execution time of class methods
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Measure execution time for the method
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        class_name = args[0].__class__.__name__ if args else "Function"
        func_name = func.__name__
        project_logger.info(f"Execution time for {class_name}.{func_name}: {execution_time:.4f} seconds")
        return result

    return wrapper


# Initialize Limiter
limiter = Limiter(
    get_remote_address,  # Use client's IP address for rate limiting
    default_limits=["200 per day", "50 per hour"],  # Global limits
    storage_uri="memory://",  # In-memory storage for simplicity
)
