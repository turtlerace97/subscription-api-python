
from fastapi import FastAPI
import uvicorn

from app.conf.config import Config
from app.database.conn import close_db_connection, connect_to_db
from app.routes import subscription


app = FastAPI()

# db
app.add_event_handler("startup", Config.app_setting_validate)
app.add_event_handler("startup", connect_to_db)
app.add_event_handler("shutdown", close_db_connection)

app.include_router(
    subscription.router, 
    prefix="/api/subscriptions", 
    tags=['subscription']
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)