import enum

class ResponseErrorMessage(enum.Enum):
    DATA_NOT_FOUND = "No model data found"
    MISSING_INFO = "Please provide model details"
    ERORR_OCCUREED = "Some error occurred"
    START_TIME = "Start Time not specified"
    END_TIME = "EndTime not specified"