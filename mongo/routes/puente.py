from fastapi import APIRouter, HTTPException
from mongo.database import puentes_collection
from mongo.models import Puente
from bson import ObjectId
from access.jwt_access import verify_role

router = APIRouter()

#obtener todos los puentes
@router.get("/", response_model=dict)
def get_puentes(
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    puentes = list(puentes_collection.find().skip(skip).limit(limit))

    puentes_con_ids = [{**puente, "_id": str(puente["_id"])} for puente in puentes]

    return {
        "data": puentes_con_ids
    }

#crear un puente
@router.post("/create", response_model=Puente)
def create_puente(
    puente: Puente,
    user: dict = verify_role(["admin"]) 
    ):
    puente_dict = puente.dict()
    result = puentes_collection.insert_one(puente_dict)
    puente_dict["_id"] = result.inserted_id
    return puente_dict

#obtener un puente en especifico
@router.get("/{id_puente}", response_model=Puente)
def get_puente(
    id_puente: str,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    puente = puentes_collection.find_one({"_id": ObjectId(id_puente)})
    if puente is None:
        raise HTTPException(status_code=404, detail="Puente no encontrado")
    return puente

#actualizar un puente
@router.put("/{id_puente}", response_model=Puente)
def update_puente(
    id_puente: str, 
    puente: Puente,
    user: dict = verify_role(["admin"]) 
    ):
    puente_dict = puente.dict()
    result = puentes_collection.update_one(
        {"_id": ObjectId(id_puente)},
        {"$set": puente_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Puente no encontrado")
    return {**puente_dict, "_id": id_puente}

#eliminar un puente
@router.delete("/{id_puente}", response_model=Puente)
def delete_puente(
    id_puente: str,
    user: dict = verify_role(["admin"]) 
    ):
    puente = puentes_collection.find_one({"_id": ObjectId(id_puente)})
    if puente is None:
        raise HTTPException(status_code=404, detail="Puente no encontrado")
    puentes_collection.delete_one({"_id": ObjectId(id_puente)})
    return puente

#obtener un puente especifico a base del idnivel
@router.get("/nivel/{idnivel}", response_model=dict)
def get_puentenivel(
    idnivel: int,
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin", "usuario"])
):
    puentes = list(puentes_collection.find({"idnivel": idnivel}).skip(skip).limit(limit))

    puentes_con_ids = [{**puente, "_id": str(puente["_id"])} for puente in puentes]

    return {"data": puentes_con_ids}