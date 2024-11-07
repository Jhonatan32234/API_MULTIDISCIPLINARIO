# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Terminal
from schemas import terminalCreate, terminalResponse

router = APIRouter()


@router.get("/", response_model=List[terminalResponse])
def get_terminal(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminal = db.query(Terminal).offset(skip).limit(limit).all()
    return terminal

@router.post("/create", response_model=terminalResponse)
def create_terminal(terminal: terminalCreate, db: Session = Depends(get_db)):
    new_terminal = Terminal(**terminal.dict())
    db.add(new_terminal)
    db.commit()
    db.refresh(new_terminal)
    return new_terminal

@router.get("/{id_terminal}", response_model=terminalResponse)
def get_terminal(id_terminal: int, db: Session = Depends(get_db)):
    terminal = db.query(Terminal).filter(Terminal.idterminal == id_terminal).first()
    if terminal is None:
        raise HTTPException(status_code=404, detail="Terminal no encontrado")
    return terminal

@router.put("/{id_terminal}", response_model=terminalResponse)
def update_terminal(id_terminal: int, terminal: terminalCreate, db: Session = Depends(get_db)):
    db_terminal = db.query(Terminal).filter(Terminal.idterminal == id_terminal).first()
    if db_terminal is None:
        raise HTTPException(status_code=404, detail="Terminal no encontrado")
    
    for key, value in terminal.dict().items():
        setattr(db_terminal, key, value)
    
    db.commit()
    db.refresh(db_terminal)
    return db_terminal

@router.delete("/{id_terminal}", response_model=terminalResponse)
def delete_terminal(id_terminal: int, db: Session = Depends(get_db)):
    terminal = db.query(Terminal).filter(Terminal.idterminal == id_terminal).first()
    if terminal is None:
        raise HTTPException(status_code=404, detail="Terminal no encontrado")
    
    db.delete(terminal)
    db.commit()
    return terminal
