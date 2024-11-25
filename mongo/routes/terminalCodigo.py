from fastapi import APIRouter, HTTPException
from mongo.database import terminales_codigo_collection
from mongo.models import TerminalCodigo
from bson import ObjectId
from access.jwt_access import verify_role

router = APIRouter()

#obtener todas las terminalescodigo
@router.get("/", response_model=dict)
def get_terminalescodigo(
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    terminalescodigo = list(terminales_codigo_collection.find().skip(skip).limit(limit))

    terminalescodigo_con_ids = [{**terminalcodigo, "_id": str(terminalcodigo["_id"])} for terminalcodigo in terminalescodigo]

    return {
        "data": terminalescodigo_con_ids
    }

#crear una terminalcodigo
@router.post("/create", response_model=TerminalCodigo)
def create_terminalcodigo(
    terminalcodigo: TerminalCodigo,
    user: dict = verify_role(["admin"]) 
    ):
    terminalcodigo_dict = terminalcodigo.dict()
    result = terminales_codigo_collection.insert_one(terminalcodigo_dict)
    terminalcodigo_dict["_id"] = result.inserted_id
    return terminalcodigo_dict

#obtener una terminalcodigo especifica
@router.get("/{id_terminalcodigo}", response_model=TerminalCodigo)
def get_terminalcodigo(
    id_terminalcodigo: str,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    terminalcodigo = terminales_codigo_collection.find_one({"_id": ObjectId(id_terminalcodigo)})
    if terminalcodigo is None:
        raise HTTPException(status_code=404, detail="TerminalCodigo no encontrado")
    return terminalcodigo

#actualizar una terminalcodigo
@router.put("/{id_terminalcodigo}", response_model=TerminalCodigo)
def update_terminalcodigo(
    id_terminalcodigo: str, 
    terminalcodigo: TerminalCodigo,
    user: dict = verify_role(["admin"]) 
    ):
    terminalcodigo_dict = terminalcodigo.dict()
    result = terminales_codigo_collection.update_one(
        {"_id": ObjectId(id_terminalcodigo)},
        {"$set": terminalcodigo_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="TerminalCodigo no encontrado")
    return {**terminalcodigo_dict, "_id": id_terminalcodigo}

#elimnar una terminalcodigo
@router.delete("/{id_terminalcodigo}", response_model=TerminalCodigo)
def delete_terminalcodigo(
    id_terminalcodigo: str,
    user: dict = verify_role(["admin"]) 
    ):
    terminalcodigo = terminales_codigo_collection.find_one({"_id": ObjectId(id_terminalcodigo)})
    if terminalcodigo is None:
        raise HTTPException(status_code=404, detail="TerminalCodigo no encontrado")
    terminales_codigo_collection.delete_one({"_id": ObjectId(id_terminalcodigo)})
    return terminalcodigo




#obtener un terminalcodigo especifico a base del idterminal
@router.get("/terminal/{idterminal}", response_model=dict)
def get_terminal(
    idterminal: int,
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin", "usuario"])
):
    terminalescodigo = list(terminales_codigo_collection.find({"idterminal": idterminal}).skip(skip).limit(limit))

    terminalescodigo_con_ids = [{**terminalcodigo, "_id": str(terminalcodigo["_id"])} for terminalcodigo in terminalescodigo]

    return {"data": terminalescodigo_con_ids}


#obtener un terminalcodigo especifico a base del idcodigo
@router.get("/codigo/{idcodigo}", response_model=dict)
def get_terminal(
    idcodigo: int,
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin", "usuario"])
):
    terminalescodigo = list(terminales_codigo_collection.find({"idbloquecodigo": idcodigo}).skip(skip).limit(limit))

    terminalescodigo_con_ids = [{**terminalcodigo, "_id": str(terminalcodigo["_id"])} for terminalcodigo in terminalescodigo]

    return {"data": terminalescodigo_con_ids}