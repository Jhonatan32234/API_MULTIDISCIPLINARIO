from fastapi import APIRouter, HTTPException
from mongo.database import bloques_codigo_collection
from mongo.models import BloqueCodigo
from bson import ObjectId
from access.jwt_access import verify_role


router = APIRouter()

#obtener otods los bloqueCodigos
@router.get("/", response_model=dict)
def get_paredes(
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    bloquescodigo = list(bloques_codigo_collection.find().skip(skip).limit(limit))

    bloquescodigo_con_ids = [{**bloquecodigo, "_id": str(bloquecodigo["_id"])} for bloquecodigo in bloquescodigo]

    return {
        "data": bloquescodigo_con_ids
    }

#crear un bloqueCodigo
@router.post("/create", response_model=BloqueCodigo)
def create_bloquecodigo(
    bloquecodigo: BloqueCodigo,
    user: dict = verify_role(["admin"]) 
    ):
    bloquecodigo_dict = bloquecodigo.dict()
    result = bloques_codigo_collection.insert_one(bloquecodigo_dict)
    bloquecodigo_dict["_id"] = result.inserted_id
    return bloquecodigo_dict


#obtener un bloqueCodigo especifico
@router.get("/{id_bloquecodigo}", response_model=BloqueCodigo)
def get_bloquecodigo(
    id_bloquecodigo: str,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    bloquecodigo = bloques_codigo_collection.find_one({"_id": ObjectId(id_bloquecodigo)})
    if bloquecodigo is None:
        raise HTTPException(status_code=404, detail="BloqueCodigo no encontrado")
    return bloquecodigo

#actualizar un bloqueCodigo
@router.put("/{id_bloquecodigo}", response_model=BloqueCodigo)
def update_bloquecodigo(
    id_bloquecodigo: str, 
    bloquecodigo: BloqueCodigo,
    user: dict = verify_role(["admin"]) 
    ):
    bloquecodigo_dict = bloquecodigo.dict()
    result = bloques_codigo_collection.update_one(
        {"_id": ObjectId(id_bloquecodigo)},
        {"$set": bloquecodigo_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="BloqueCodigo no encontrado")
    return {**bloquecodigo_dict, "_id": id_bloquecodigo}

#eliminar un bloque
@router.delete("/{id_bloquecodigo}", response_model=BloqueCodigo)
def delete_bloquecodigo(
    id_bloquecodigo: str,
    user: dict = verify_role(["admin"]) 
    ):
    bloquecodigo = bloques_codigo_collection.find_one({"_id": ObjectId(id_bloquecodigo)})
    if bloquecodigo is None:
        raise HTTPException(status_code=404, detail="BloqueCodigo no encontrado")
    bloques_codigo_collection.delete_one({"_id": ObjectId(id_bloquecodigo)})
    return bloquecodigo
