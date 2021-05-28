import enum

class ResponseErrorMessage(enum.Enum):
    DATA_NOT_FOUND = "No model data found"
    MISSING_INFO = "Please provide model details"
    ERORR_OCCUREED = "Some error occurred"
    START_TIME = "Start time not specified"
    END_TIME = "End time not specified"
    DATA_ALREADY_EXISTS = "Model already exists"
    DATA_DOES_NOT_ALREADY_EXISTS = "Model to be deleted is not available"
    NO_LOGS_FOUND = "NO report data found"
    Question_Not_Asked = "Please provide question details"
