from fastapi import Response, status


UNAUTHORIZED = Response(
    status_code=status.HTTP_401_UNAUTHORIZED,
    content={
        "error": {
            "comment": "Wrong token. Authorization header required."
        }
    },
    media_type="application/json"
)

PROJECT_NOT_FOUND = Response(
    status_code=status.HTTP_404_NOT_FOUND,
    content={
        "error": {
            "comment": "Wrong project slug. Project doesn't exist."
        }
    },
    media_type="application/json"
)

SUCCESS = Response(
    status_code=status.HTTP_201_CREATED,
    content={
        "comment": "Successful."
    },
    media_type="application/json"
)

SUCCESS_DEL = Response(
    status_code=status.HTTP_200_OK,
    content={
        "comment": "Successful."
    },
    media_type="application/json"
)

NOT_SUBSCRIBED = Response(
    status_code=status.HTTP_404_NOT_FOUND,
    content={
        "error": {
            "comment": "Project with this name is not subscribed."
        }
    }
)
