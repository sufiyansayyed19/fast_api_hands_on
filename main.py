from fastapi import FastAPI, Depends
from routers.tasks import router

app = FastAPI()

app.include_router(router)