from database.base import Base
from database.connection import engine

from models.task_db import TaskDB
from models.user_db import UserDB


Base.metadata.create_all(engine)
print("Tables created successfully")

