from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd

router = APIRouter()

# the 'prefix' will be defined in main.py

@router.get("/", response_model=List[schema.Project])
def proj_list(db: Session = Depends(getsession)):
    return curd.Project.get_all(db)

@router.post("/", response_model=schema.Project)
def proj_new(proj: schema.ProjectNew, db: Session = Depends(getsession)):
    return curd.Project.new(db, proj)

@router.put("/{projid}", response_model=schema.Project)
def proj_update(projid: int, newproj: schema.ProjectNew, db: Session = Depends(getsession)):
    theproj = curd.Project.get(db, projid)
    theproj.__dict__.update(newproj)
    return curd.Project.update(db, theproj)

@router.get("/{projid}", response_model=schema.Project)
def proj_detail(projid: int, db: Session = Depends(getsession)):
    return curd.Project.get(db, projid)

@router.delete("/{projid}", response_model=schema.Project)
def proj_detail(projid: int, db: Session = Depends(getsession)):
    theproj = curd.Project.get(db, projid)
    return curd.Project.delete(db, theproj)


# for admin
@router.get("/{projid}/admin/", response_model=List[schema.ProjectAdmin])
def projad_list(projid: int, db: Session = Depends(getsession)):
    return curd.ProjectAdmin.get_all(projid, db)

@router.post("/{projid}/admin/", response_model=schema.ProjectAdmin)
def projad_new(projid: int, team: schema.ProjectAdminNew, db: Session = Depends(getsession)):
    return curd.ProjectAdmin.new(db, team)

@router.put("/{projid}/admin/{adminid}", response_model=schema.ProjectAdmin)
def projad_update(projid: int, adminid: int, newadmin: schema.ProjectAdminNew, db: Session = Depends(getsession)):
    theadmin = curd.ProjectAdmin.get(db, adminid)
    theadmin.__dict__.update(newadmin)
    return curd.ProjectAdmin.update(db, theadmin)

@router.get("/{projid}/admin/{adminid}", response_model=schema.ProjectAdmin)
def projad_detail(projid: int, adminid: int, db: Session = Depends(getsession)):
    return curd.ProjectAdmin.get(db, adminid)

@router.delete("/{projid}/admin/{adminid}", response_model=schema.ProjectAdmin)
def projad_detail(projid: int, adminid: int, db: Session = Depends(getsession)):
    theadmin = curd.ProjectAdmin.get(db, adminid)
    return curd.ProjectAdmin.delete(db, theadmin)