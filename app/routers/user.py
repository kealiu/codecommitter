from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd, cloud, iam

router = APIRouter()

# the 'prefix' will be defined in main.py

@router.get("/", response_model=List[schema.User])
def user_list(db: Session = Depends(getsession)):
    return curd.User.get_all(db)

@router.post("/", response_model=schema.User)
def user_new(user: schema.UserNew, db: Session = Depends(getsession)):
    newuser = curd.User.new(db, user)
    yun = cloud.get()
    iamuser = yun.CloudIAM.create(newuser.name)
    ccuser = yun.CloudIAM.create_codecommit_passwd(newuser.name) # create one. and latest, just reset it
    newuser.arn = iamuser['arn']
    newuser.ccid = ccuser['ccid']
    newuser.ccname = ccuser['ccname']
    newuser.ccpasswd = ccuser['ccpasswd']
    newuser.ccpolicy = iam.update_user_policy(db, newuser, True)
    return curd.User.update(db, newuser)

@router.get("/name/{name}", response_model=schema.User)
def user_get_by_name(name: str, db: Session = Depends(getsession)):
    user = curd.User.get_by_name(db, name)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.put("/{userid}", response_model=schema.User)
def user_update(userid: int, user: schema.UserModify, db: Session = Depends(getsession)):
    theuser = curd.User.get(db, userid)
    theuser.__dict__.update(user)
    return curd.User.update(db, theuser)

@router.put("/{userid}/reset")
def user_update(userid: int, db: Session = Depends(getsession)):
    theuser = curd.User.get(db, userid)
    yun = cloud.get()
    return yun.CloudIAM.reset_codecommit_passwd(theuser.name)

@router.get("/{userid}", response_model=schema.User)
def user_detail(userid: int, db: Session = Depends(getsession)):
    user = curd.User.get(db, userid)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.delete("/{userid}", response_model=schema.User)
def user_detail(userid: int, db: Session = Depends(getsession)):
    theuser = curd.User.get(db, userid)
    if not theuser:
        raise HTTPException(status_code=404, detail="user not found")
    return curd.User.delete(db, theuser)