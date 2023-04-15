from fastapi import status
from fastapi.responses import JSONResponse


CABINET_ERROR = JSONResponse(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    content={
        "error": {
            "comment": "МИЭМ кабинет не отвечает, повторите попытку позже."
        }
    },
    media_type="application/json"
)

PROJECT_NOT_FOUND = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={
        "error": {
            "comment": "Проекта с таким номером не существует."
        }
    },
    media_type="application/json"
)

SUCCESS = JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={
        "comment": "Проект успешно подписан на рассылку."
    },
    media_type="application/json"
)

SUCCESS_UPDATE = JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={
        "comment": "Канал для уведомлений успешно обновлён."
    },
    media_type="application/json"
)

SUCCESS_DEL = JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
        "comment": "Проект успешно отписан от рассылки."
    },
    media_type="application/json"
)

NOT_SUBSCRIBED = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={
        "error": {
            "comment": "Проект с таким именем не подписан на рассылку."
        }
    },
    media_type="application/json"
)
