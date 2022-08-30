from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd

router = APIRouter()

# the 'prefix' will be defined in main.py

@router.get("/", response_model=List[schema.Perm])
def perm_list(db: Session = Depends(getsession)):
    return curd.Perm.get_all(db)

@router.post("/", response_model=schema.Perm)
def perm_new(perm: schema.PermNew, db: Session = Depends(getsession)):
    return curd.Perm.new(db, perm)

@router.put("/{permid}", response_model=schema.Perm)
def perm_update(permid: int, perm: schema.PermNew, db: Session = Depends(getsession)):
    theperm = curd.Perm.get(db, permid)
    theperm.__dict__.update(perm)
    return curd.Perm.update(db, theperm)

@router.get("/{permid}", response_model=schema.Perm)
def perm_detail(permid: int, db: Session = Depends(getsession)):
    return curd.Perm.get(db, permid)

@router.delete("/{permid}", response_model=schema.Perm)
def perm_detail(permid: int, db: Session = Depends(getsession)):
    theperm = curd.Perm.get(db, permid)
    return curd.Perm.delete(db, theperm)