import os
from routers import router
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(router)


uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))
