from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from typing import List
from db import getsession
import schema, curd

router = APIRouter()

# the 'prefix' will be defined in main.py

@router.get("/", response_model=List[schema.Repo])
def repo_list(db: Session = Depends(getsession)):
    return curd.Repo.get_all(db)

@router.post("/", response_model=schema.Repo)
def repo_new(repo: schema.RepoNew, db: Session = Depends(getsession)):
    localrepo =  curd.Repo.new(db, repo)
    # remoterepo = yun.Repo.create()
    # localrepo.arn = remoterepo['arn']
    # localrepo.url = remoterepo['url']
    # localrepo.repoid = remoterepo['repoid']
    # curd.Repo.update(db, localrepo)
    localrepo.arn = "someARN"
    localrepo.url = "someURL"
    localrepo.repoid = "someUUID"
    return curd.Repo.update(db, localrepo)

@router.put("/{repoid}", response_model=schema.Repo)
def repo_update(repoid: int, newrepo: schema.RepoNew, db: Session = Depends(getsession)):
    therepo = curd.Repo.get(db, repoid)
    therepo.__dict__.update(newrepo)
    return curd.Repo.update(db, therepo)

@router.get("/{repoid}", response_model=schema.Repo)
def repo_detail(repoid: int, db: Session = Depends(getsession)):
    return curd.Repo.get(db, repoid)

@router.delete("/{repoid}", response_model=schema.Repo)
def repo_detail(repoid: int, db: Session = Depends(getsession)):
    theteam = curd.Repo.get(db, repoid)
    return curd.Repo.delete(db, theteam)