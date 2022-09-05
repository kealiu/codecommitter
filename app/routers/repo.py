from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd, repo, cloud

router = APIRouter()

# the 'prefix' will be defined in main.py


def _reponame(proj, team, name):
    return proj+"-"+team+"-"+name

@router.get("/", response_model=List[schema.Repo])
def repo_list(db: Session = Depends(getsession)):
    return curd.Repo.get_all(db)

@router.post("/", response_model=schema.Repo)
def repo_new(repo: schema.RepoNew, db: Session = Depends(getsession)):
    tmprepo = dict(repo)
    tmprepo.update({"arn": "n/a", "url": "n/a", "repoid": "n/a"})
    localrepo =  curd.Repo.new(db, tmprepo)
    yun = cloud.get()
    proj = curd.Project.get(db, localrepo.team.projectid)
    tags = {"Project": proj.name, "Team": localrepo.team.name}
    remoterepo = yun.CloudRepo.create(_reponame(proj.name, localrepo.team.name, localrepo.name), localrepo.desc, tags)
    localrepo.arn = remoterepo['arn']
    localrepo.url = remoterepo['url']
    localrepo.repoid = remoterepo['repoid']
    return curd.Repo.update(db, localrepo)

@router.put("/{repoid}", response_model=schema.Repo)
def repo_update(repoid: int, newrepo: schema.RepoNew, db: Session = Depends(getsession)):
    therepo = curd.Repo.get(db, repoid)
    therepo.__dict__.update(newrepo)
    return curd.Repo.update(db, therepo)

@router.get("/{repoid}", response_model=schema.Repo)
def repo_detail(repoid: int, db: Session = Depends(getsession)):
    return curd.Repo.get(db, repoid)

@router.get("/{repoid}/writer/", response_model=List[schema.User])
def repo_get_writer(repoid: int, db: Session = Depends(getsession)):
    records =  curd.Repo.get_all_repo_writer(db, repoid)
    if not records or len(records) == 0:
        # raise HTTPException(status_code=404, detail="project not found")
        return []
    return [r.User for r in records]

@router.get("/{repoid}/reader/", response_model=List[schema.User])
def repo_get_reader(repoid: int, db: Session = Depends(getsession)):
    records =  curd.Repo.get_all_repo_reader(db, repoid)
    if not records or len(records) == 0:
        # raise HTTPException(status_code=404, detail="project not found")
        return []
    return [r.User for r in records]

@router.post("/{repoid}/writer/", response_model=List[schema.User])
def repo_create_writer(repoid: int, user: schema.RepoUser, db: Session = Depends(getsession)):
    theuser = curd.User.get_by_name(user.user)
    curd.Perm.new(db, schema.PermNew({"perm":"write", "userid":theuser.id, "repoid": repoid}))
    return [r.user for r in curd.Repo.get_all_repo_writer(db, repoid)]

@router.post("/{repoid}/reader/", response_model=List[schema.User])
def repo_create_reader(repoid: int, user: schema.RepoUser, db: Session = Depends(getsession)):
    theuser = curd.User.get_by_name(user.user)
    curd.Perm.new(db, schema.PermNew({"perm":"read", "userid":theuser.id, "repoid": repoid}))
    return [r.user for r in curd.Repo.get_all_repo_writer(db, repoid)]

@router.delete("/{repoid}/writer/{writer}", response_model=List[schema.User])
def repo_delete_writer(repoid: int, writer: int, db: Session = Depends(getsession)):
    return curd.Perm.delete_by_query(db, "write", writer, repoid)

@router.delete("/{repoid}/reader/{reader}", response_model=List[schema.User])
def repo_delete_reader(repoid: int, reader: int, db: Session = Depends(getsession)):
    return curd.Perm.delete_by_query(db, "read", reader, repoid)

@router.delete("/{repoid}", response_model=schema.Repo)
def repo_detail(repoid: int, db: Session = Depends(getsession)):
    r = curd.Repo.get(db, repoid)
    yun = cloud.get()
    yun.CloudRepo.delete_repository(_reponame(r.team.project.name, r.team.name, r.name))
    return curd.Repo.delete(db, r)