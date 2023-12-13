from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.entity_routes import entity
from routes.map_routes import map
from routes.sso_routes import sso
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount('/static', StaticFiles(directory='static',html=True))

app.include_router(entity)
app.include_router(sso)
app.include_router(map)


allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)
 