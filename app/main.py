
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.conf.config import conf
import uvicorn

from app.conf.config import Config
from app.database.conn import close_db_connection, connect_to_db
from app.routes import subscription


templates = Jinja2Templates(directory="templates")

app = FastAPI()

# db
app.add_event_handler("startup", Config.app_setting_validate)
app.add_event_handler("startup", connect_to_db)
app.add_event_handler("shutdown", close_db_connection)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return JSONResponse(content=conf.app_settings)

app.include_router(
    subscription.router, 
    prefix="/api/subscriptions", 
    tags=['subscription']
)
