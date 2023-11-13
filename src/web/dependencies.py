import os
from configparser import ConfigParser
from fastapi import Header, HTTPException, status
from loguru import logger


config = ConfigParser()
config.read("response_texts.conf")
response_texts = config["response.texts"]


async def verify_token(authorization: str = Header(default=None)):
    if authorization is None:
        logger.debug("No token given.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response_texts["NoToken"]
        )
    logger.debug(f"Received token -- {authorization}")
    if authorization != f"Bearer {os.environ['SECRET']}":
        logger.debug("Token is wrong.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response_texts["WrongToken"]
        )
