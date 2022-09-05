from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd

router = APIRouter()

# the 'prefix' will be defined in main.py

@router.get("/", response_model=List[schema.Team]) # get /?projid=1
def team_list(db: Session = Depends(getsession)):
    return curd.Team.get_all(db)

@router.post("/", response_model=schema.Team)
def team_new(team: schema.TeamNew, db: Session = Depends(getsession)):
    return curd.Team.new(db, team)

@router.get("/name/{team}", response_model=schema.Team)
def team_detail_by_name(team: str, db: Session = Depends(getsession)):
    tm = curd.Team.get_by_name(db, team)
    if not tm:
        raise HTTPException(status_code=404, detail="team not found")
    return tm

@router.put("/{teamid}", response_model=schema.Team)
def team_update(teamid: int, newteam: schema.TeamNew, db: Session = Depends(getsession)):
    theteam = curd.Team.get(db, teamid)
    theteam.__dict__.update(newteam)
    return curd.Team.update(db, theteam)

@router.get("/{teamid}", response_model=schema.Team)
def team_detail(teamid: int, db: Session = Depends(getsession)):
    team = curd.Team.get(db, teamid)
    if not team:
        raise HTTPException(status_code=404, detail="team not found")
    return team

@router.delete("/{teamid}", response_model=schema.Team)
def team_detail(teamid: int, db: Session = Depends(getsession)):
    repos = curd.Repo.get_all_by_team(db, teamid)
    if repos:
        raise HTTPException(status_code=412, detail="Should remove all repo in this team firstly")    
    theteam = curd.Team.get(db, teamid)
    return curd.Team.delete(db, theteam)

# for admin
@router.get("/{teamid}/admin/", response_model=List[schema.TeamAdmin])
def teamad_list(teamid: int, db: Session = Depends(getsession)):
    return curd.TeamAdmin.get_all(teamid, db)

@router.post("/{teamid}/admin/", response_model=schema.TeamAdmin)
def teamad_new(teamid: int, team: schema.TeamAdminNew, db: Session = Depends(getsession)):
    return curd.TeamAdmin.new(db, team)

@router.put("/{teamid}/admin/{adminid}", response_model=schema.TeamAdmin)
def teamad_update(teamid: int, adminid: int, newadmin: schema.TeamAdminNew, db: Session = Depends(getsession)):
    theadmin = curd.TeamAdmin.get(db, adminid)
    theadmin.__dict__.update(newadmin)
    return curd.TeamAdmin.update(db, theadmin)

@router.get("/{teamid}/admin/{adminid}", response_model=schema.TeamAdmin)
def teamad_detail(teamid: int, adminid: int, db: Session = Depends(getsession)):
    return curd.TeamAdmin.get(db, adminid)

@router.delete("/{teamid}/admin/{adminid}", response_model=schema.TeamAdmin)
def teamad_detail(teamid: int, adminid: int, db: Session = Depends(getsession)):
    theadmin = curd.TeamAdmin.get(db, adminid)
    return curd.TeamAdmin.delete(db, theadmin)