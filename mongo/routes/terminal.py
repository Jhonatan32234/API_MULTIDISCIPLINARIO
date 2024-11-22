from fastapi import APIRouter, HTTPException
from mongo.database import terminales_collection
from mongo.models import Terminal
from bson import ObjectId
from access.jwt_access import verify_role

router = APIRouter()


#obtener todas las terminales
@router.get("/", response_model=dict)
def get_terminales(
    skip: int = 0, 
    limit: int = 100,
    user: dict = verify_role(["admin","usuario"]) 
    ):
    terminales = list(terminales_collection.find().skip(skip).limit(limit))

    terminales_con_ids = [{**terminal, "_id": str(terminal["_id"])} for terminal in terminales]

    return {
        "data": terminales_con_ids
    }

#crear una terminal
@router.post("/create", response_model=Terminal)
def create_terminal(
    terminal: Terminal,
    user: dict = verify_role(["admin"]) 
    ):
    terminal_dict = terminal.dict()
    result = terminales_collection.insert_one(terminal_dict)
    terminal_dict["_id"] = result.inserted_id
    return terminal_dict

#obtener una terminal en especifico
@router.get("/{id_terminal}", response_model=Terminal)
def get_terminal(
    id_terminal: str,
    user: dict = verify_role(["admin","usuario"]) 
    ):

    terminal = terminales_collection.find_one({"_id": ObjectId(id_terminal)})
    if terminal is None:
        raise HTTPException(status_code=404, detail="Terminal no encontrado")
    return terminal

#actualizar una terminal
@router.put("/{id_terminal}", response_model=Terminal)
def update_terminal(
    id_terminal: str, 
    terminal: Terminal,
    user: dict = verify_role(["admin"]) 
    ):
    terminal_dict = terminal.dict()
    result = terminales_collection.update_one(
        {"_id": ObjectId(id_terminal)},
        {"$set": terminal_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Terminal no encontrado")
    return {**terminal_dict, "_id": id_terminal}

#eliminar una terminal
@router.delete("/{id_terminal}", response_model=Terminal)
def delete_terminal(
    id_terminal: str,
    user: dict = verify_role(["admin"]) 
    ):
    terminal = terminales_collection.find_one({"_id": ObjectId(id_terminal)})
    if terminal is None:
        raise HTTPException(status_code=404, detail="Terminal no encontrado")
    terminales_collection.delete_one({"_id": ObjectId(id_terminal)})
    return terminal
