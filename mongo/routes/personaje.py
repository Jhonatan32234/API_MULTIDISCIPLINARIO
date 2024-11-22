from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from mongo.database import personajes_collection
from mongo.models import Personaje
from bson import ObjectId
from access.jwt_access import verify_role

router = APIRouter()


#obtener todos los personajes
@router.get("/", response_model=dict)
def get_personajes(
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    personajes = list(personajes_collection.find().skip(skip).limit(limit))

    personajes_con_ids = [{**personaje, "_id": str(personaje["_id"])} for personaje in personajes]

    return {
        "data": personajes_con_ids
    }


#crear un personaje
@router.post("/create", response_model=Personaje)
def create_personaje(
    personaje: Personaje,
    user: dict = verify_role(["admin"]) 
    ):
    personaje_dict = personaje.dict()
    result = personajes_collection.insert_one(personaje_dict)
    personaje_dict["_id"] = result.inserted_id
    return personaje_dict

#obtener un personaje especifico
@router.get("/{id_personaje}", response_model=Personaje)
def get_personaje(
    id_personaje: str,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    personaje = personajes_collection.find_one({"_id": ObjectId(id_personaje)})
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return personaje

#actualizar un personaje
@router.put("/{id_personaje}", response_model=Personaje)
def update_personaje(
    id_personaje: str, 
    personaje: Personaje,
    user: dict = verify_role(["admin"]) 
    ):
    personaje_dict = personaje.dict()
    result = personajes_collection.update_one(
        {"_id": ObjectId(id_personaje)},
        {"$set": personaje_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return {**personaje_dict, "_id": id_personaje}

#eliminar un personaje
@router.delete("/{id_personaje}", response_model=Personaje)
def delete_personaje(
    id_personaje: str,
    user: dict = verify_role(["admin"]) 
    ):
    personaje = personajes_collection.find_one({"_id": ObjectId(id_personaje)})
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    personajes_collection.delete_one({"_id": ObjectId(id_personaje)})
    return personaje
