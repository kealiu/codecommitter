from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd, cloud

router = APIRouter()

# the 'prefix' will be defined in main.py

@router.get("/", response_model=List[schema.User])
async def user_list(db: Session = Depends(getsession)):
    return curd.User.get_all(db)

@router.post("/", response_model=schema.User)
async def user_new(user: schema.UserNew, db: Session = Depends(getsession)):
    newuser = curd.User.new(db, user)
    # yun = cloud.get()
    # yun.CloudIAM.create(newuser.name)
    # yun.CloudIAM.create_codecommit_passwd(newuser.name) # create one. and latest, just reset it
    return newuser

@router.put("/{userid}", response_model=schema.User)
async def user_update(userid: int, user: schema.UserModify, db: Session = Depends(getsession)):
    theuser = curd.User.get(db, userid)
    theuser.__dict__.update(user)
    return curd.User.update(db, theuser)

@router.get("/{userid}", response_model=schema.User)
async def user_detail(userid: int, db: Session = Depends(getsession)):
    return curd.User.get(db, userid)

@router.delete("/{userid}", response_model=schema.User)
async def user_detail(userid: int, db: Session = Depends(getsession)):
    theuser = curd.User.get(db, userid)
    return curd.User.delete(db, theuser)
