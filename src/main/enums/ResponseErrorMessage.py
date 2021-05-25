import enum

class ResponseErrorMessage(enum.Enum):
    DATA_NOT_FOUND = "No model data found"
    MISSING_INFO = "Please provide model details"
    ERORR_OCCUREED = "Some error occurred"
    START_TIME = "Start Time not specified"
    END_TIME = "EndTime not specified"
    DATA_ALREDAY_EXISTS = "Model already exists"
    DATA_DOES_NOT_ALREDAY_EXISTS = "Model to be deleted is not available"