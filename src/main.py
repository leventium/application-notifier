import os
from multiprocessing import Process
from fastapi import FastAPI
import uvicorn
import preimports
from server.routers import router
from checker.main import main


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    Process(target=main).start()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
