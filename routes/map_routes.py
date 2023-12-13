from fastapi import APIRouter, Request, Depends
from config.database import entity_collection
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from config.template import templates
from services.dependencies import get_user_token

map = APIRouter()

@map.get("/mapa/direccion/{id}", response_class=Jinja2Templates)
async def map_direccion(request: Request, id: str, user = Depends(get_user_token)):  
    result = entity_collection.find_one({"_id": ObjectId(id)})
    return templates.TemplateResponse("verMapaDireccion.jinja", {"request": request, "entity": result, "user": user})

@map.get("/mapa/{id}", response_class=Jinja2Templates)
async def show_map(request: Request, id: str, user = Depends(get_user_token)):
    result = entity_collection.find_one({"_id": ObjectId(id)})

    return templates.TemplateResponse("verMapa.jinja", {"request": request, "entity": result, "user": user})