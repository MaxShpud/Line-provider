from fastapi import HTTPException, status

ACTIVE_EVENT_ALREADY_EXISTS_HTTP_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 1, "message": "Active event already exists."},
)

RETRIEVE_EVENT_HTTP_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 2, "message": "Event not found."},
)

UPDATE_EVENT_HTTP_ERROR = HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 3, "message": "Event update error."},
)