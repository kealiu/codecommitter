from typing import List, Union, Any
from orm import Project

from pydantic import BaseModel, constr

# login
class Authorization(BaseModel):
    user: str
    passwd: str

# define Perm
class PermBase(BaseModel):
    perm: str
    desc: Union[str, None] = None

class PermNew(PermBase):
    userid: int
    repoid: int

class Perm(PermNew): # base on new
    id: int
    class Config:
        orm_mode = True

#define Repo
class RepoBase(BaseModel):
    name: constr(min_length=5, max_length=24)
    desc: Union[str, None] = None

class RepoNew(RepoBase):
    teamid: int

class Repo(RepoNew):
    id: int
    arn: str
    url: str
    repoid: str
    perms: List[Perm] = []
    class Config:
        orm_mode = True

# TeamAdmin
class TeamAdminBase(BaseModel):
    userid: int
    teamid: int
    desc: Union[str, None] = None

class TeamAdminNew(TeamAdminBase):
    pass

class TeamAdmin(TeamAdminBase):
    id: int
    class Config:
        orm_mode = True

# define Team
class TeamBase(BaseModel):
    name: constr(min_length=3, max_length=24)
    projectid: int
    desc: Union[str, None] = None

class TeamNew(TeamBase):
    pass

class Team(TeamBase):
    id: int
    perms: List[Perm] = []
    admins: List[TeamAdmin] = []
    repos: List[Repo] = []

    class Config:
        orm_mode = True

# define Project
class ProjectBase(BaseModel):
    name: constr(min_length=3, max_length=24)
    desc: Union[str, None] = None

class ProjectNew(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    teams: List[Team] = []
    admins: List
    class Config:
        orm_mode = True

# define ProjectAdmin
class ProjectAdminBase(BaseModel):
    userid: int
    projectid: int

class ProjectAdminNew(ProjectAdminBase):
    pass

class ProjectAdmin(ProjectAdminBase):
    id: int
    class Config:
        orm_mode = True

# define User
class UserBase(BaseModel):
    name: constr(min_length=4, max_length=24)
    email: str
    fullname: str
    desc: Union[str, None] = None

class UserModify(BaseModel):
    desc: Union[str, None] = None
    passwd: Union[str, None] = None
    active: Union[bool, None] = None

class UserNew(UserBase):
    passwd: str

class User(UserBase):
    id: int
    arn: str
    ccname: str
    ccpasswd: str
    ccpolicy: str
    active: bool

    class Config:
        orm_mode = True

# Tag
class ResourceTag(BaseModel):
    key: str
    val: str

# RepoUser
class RepoUser(BaseModel):
    user: str