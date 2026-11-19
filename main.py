from fastapi import FastAPI, Depends
from routers.tasks import router
from dependencies.common import (
    get_message,
    get_current_user,
    get_app_name,
    get_environment,
    get_user_role
)

app = FastAPI()

app.include_router(router)


# -------------------------
# Dependency Practice
# -------------------------

@app.get("/dependency")
def dep_demo(message=Depends(get_message)):
    return {
        "message": message
    }

@app.get("/info")
def get_info(
    app=Depends(get_app_name),
    env=Depends(get_environment)
):
    return {
        "app": app,
        "environment": env
    }

@app.get("/role")
def role(user_role=Depends(get_user_role)):
    return {
        "role": user_role
    }