from fastapi import APIRouter, HTTPException
from mongo.database import paredes_collection
from mongo.models import Pared
from bson import ObjectId
from access.jwt_access import verify_role


router = APIRouter()

#obtener todas las paredes
@router.get("/", response_model=dict)
def get_paredes(
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    paredes = list(paredes_collection.find().skip(skip).limit(limit))

    paredes_con_ids = [{**pared, "_id": str(pared["_id"])} for pared in paredes]

    return {
        "data": paredes_con_ids
    }

#crear una pared
@router.post("/create", response_model=Pared)
def create_pared(
    pared: Pared,
    user: dict = verify_role(["admin"]) 
    ):
    pared_dict = pared.dict()
    result = paredes_collection.insert_one(pared_dict)
    pared_dict["_id"] = result.inserted_id
    return pared_dict

#obtener una pared especifica
@router.get("/{id_pared}", response_model=Pared)
def get_pared(
    id_pared: str,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    pared = paredes_collection.find_one({"_id": ObjectId(id_pared)})
    if pared is None:
        raise HTTPException(status_code=404, detail="Pared no encontrado")
    return pared

#actualizar una pared
@router.put("/{id_pared}", response_model=Pared)
def update_pared(
    id_pared: str, 
    pared: Pared,
    user: dict = verify_role(["admin"]) 
    ):
    pared_dict = pared.dict()
    result = paredes_collection.update_one(
        {"_id": ObjectId(id_pared)},
        {"$set": pared_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pared no encontrado")
    return {**pared_dict, "_id": id_pared}

#eliminar una pared
@router.delete("/{id_pared}", response_model=Pared)
def delete_pared(
    id_pared: str,
    user: dict = verify_role(["admin"]) 
    ):
    pared = paredes_collection.find_one({"_id": ObjectId(id_pared)})
    if pared is None:
        raise HTTPException(status_code=404, detail="Pared no encontrado")
    paredes_collection.delete_one({"_id": ObjectId(id_pared)})
    return pared
