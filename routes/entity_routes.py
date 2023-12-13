from fastapi import APIRouter, Request, Form, File, UploadFile, Cookie, Depends
from typing import Annotated
from schemas.entity import entityList
from datetime import datetime
from config.database import entity_collection
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from cachetools import TTLCache

import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

cloudinary.config(
    cloud_name="da0ektd8h",
    api_key="894373368299374",
    api_secret="p2sa9oi9KyG9CX9nTDFMqforpz0",
    secure=True,
)

token_cache = TTLCache(ttl=None)

entity = APIRouter()

templates = Jinja2Templates(directory="templates")

def get_cookie(request: Request):
    cookies = request.cookies

    token = cookies.get("token")
    expire = cookies.get("expires")

    return token, expire

def formdata_to_json(formdata):
    json_data = {}
    for key, value in formdata.items():
        if key == "file":
            continue
        json_data[key] = value  # Assuming values are bytes and need to be decoded
    return json_data

@entity.get("/", response_class=Jinja2Templates)
async def main(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request})

@entity.get("/mostrar", response_class=Jinja2Templates)
async def show_entity(request: Request):
    result_list = entityList(entity_collection.find())
    return templates.TemplateResponse("mostrarEntidad.jinja", {"request": request, "entities_list": result_list})

@entity.get("/crear", response_class=Jinja2Templates)
async def create_entity(request: Request):  
    return templates.TemplateResponse("crearEntidad.jinja", {"request": request})

@entity.post("/crear", response_class=Jinja2Templates)
async def create_entity(request: Request, file: UploadFile = ""): # list[UploadFile] = []):
    
    # cloudinary_response = []
    # for file in file:
    #     cloudinary_response.append(cloudinary.uploader.upload(file.file, folder="parcial-3")["url"])
    formdata = await request.form()
    json_data = formdata_to_json(formdata)

    if file.size != 0:
        cloudinary_response = cloudinary.uploader.upload(file.file, folder="parcial-3")["url"]
        json_data["images"] = cloudinary_response
    else:
        json_data["images"] = ""

    json_data["created_at"] = datetime.now()
    json_data["updated_at"] = datetime.now()

    entity_collection.insert_one(json_data)

    return templates.TemplateResponse("index.jinja", {"request": request})

@entity.get("/editar/{id}", response_class=Jinja2Templates)
async def update_entity(request: Request, id: str):
    result = entity_collection.find_one({"_id": ObjectId(id)})

    return templates.TemplateResponse("editarEntidad.jinja", {"request": request, "entity": result})

@entity.post("/editar/{id}", response_class=Jinja2Templates)
async def update_entity(request: Request, id: str, file: UploadFile = ""): # list[UploadFile] = []):
    
    # cloudinary_response = []
    # for file in file:
    #     cloudinary_response.append(cloudinary.uploader.upload(file.file, folder="parcial-3")["url"])

    formdata = await request.form()
    json_data = formdata_to_json(formdata)

    if file.size != 0:
        cloudinary_response = cloudinary.uploader.upload(file.file, folder="parcial-3")["url"]
        json_data["images"] = cloudinary_response

    json_data["updated_at"] = datetime.now()

    entity_collection.update_one({"_id": ObjectId(id)}, {"$set": {**json_data}})

    return templates.TemplateResponse("index.jinja", {"request": request})

@entity.get("/mapa/{id}", response_class=Jinja2Templates)
async def show_map(request: Request, id: str):
    result = entity_collection.find_one({"_id": ObjectId(id)})

    return templates.TemplateResponse("verMapa.jinja", {"request": request, "entity": result})

@entity.get("/borrar/{id}", response_class=Jinja2Templates)
async def delete_entity(request: Request, id: str):  
    entity_collection.delete_one({"_id": ObjectId(id)})
    return templates.TemplateResponse("index.jinja", {"request": request})

@entity.get("/mapa/direccion/{id}", response_class=Jinja2Templates)
async def delete_entity(request: Request, id: str):  
    result = entity_collection.find_one({"_id": ObjectId(id)})
    return templates.TemplateResponse("verMapaDireccion.jinja", {"request": request, "entity": result})

@entity.get("/signin", response_class=Jinja2Templates)
async def signin(request: Request, token_data: dict = Depends(lambda req: token_cache.get(get_cookie(req)[0]))):
    
    return templates.TemplateResponse("index.jinja", {"request": request})

@entity.get("/signout", response_class=Jinja2Templates)
async def signout(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request})
