from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.entity_routes import entity

app = FastAPI()
app.mount('/static', StaticFiles(directory='static',html=True))
app.include_router(entity)