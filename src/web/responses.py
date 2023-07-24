from configparser import ConfigParser
from fastapi import status
from fastapi.responses import JSONResponse


config = ConfigParser()
config.read("response_texts.conf")
response_texts = config["response.texts"]


CABINET_ERROR = JSONResponse(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    content={"error": {"comment": response_texts["CabinetError"]}},
    media_type="application/json"
)

PROJECT_NOT_FOUND = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"error": {"comment": response_texts["ProjectNotFound"]}},
    media_type="application/json"
)

SUCCESS = JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={"comment": response_texts["Success"]},
    media_type="application/json"
)

SUCCESS_UPDATE = JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={"comment": response_texts["SuccessUpdate"]},
    media_type="application/json"
)

SUCCESS_DEL = JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"comment": response_texts["SuccessDelete"]},
    media_type="application/json"
)

NOT_SUBSCRIBED = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"error": {"comment": response_texts["NotSubscribed"]}},
    media_type="application/json"
)
