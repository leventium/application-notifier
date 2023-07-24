import os
from multiprocessing import Process
from fastapi import FastAPI
import uvicorn
import preimports
from container import Container
from server.routers import router
from checker.checker import Checker
from checker.main import main


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    Process(target=main, args=(Container.get(Checker),)).start()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
