from multiprocessing.heap import Arena
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base

def orm_repr(self):
    return str(self.__dict__)

def orm_dict(self):
    _dict = dict(self.__dict__)
    _dict.pop('_sa_instance_state')
    return _dict

# make some extension
Base.__repr__ = orm_repr
Base.dict = orm_dict

# this is abstract model
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)   # user sso account
    passwd = Column(String(64)) # sha256 sum, if sso, should be random generated
    fullname = Column(String, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    desc = Column(String, default="n/a")
    arn = Column(String, nullable=True)
    ccid = Column(String, nullable=True)
    ccpasswd = Column(String, nullable=True)
    ccname = Column(String, nullable=True)
    ccpolicy = Column(String, nullable=True)

    perms = relationship("Perm", back_populates="user")
    projects = relationship("ProjectAdmin", back_populates="user")
    teams = relationship("TeamAdmin", back_populates="user")

# for simplify, just define project/team as different table. also they have the same schema

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, default="n/a")

    teams = relationship("Team", back_populates="project")
    admins = relationship("ProjectAdmin", back_populates="project")

class ProjectAdmin(Base):
    __tablename__ = "projectadmin"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"), nullable=False)
    projectid = Column(Integer, ForeignKey("project.id"), nullable=False)
    
    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="admins")

# team will be the realy repo container. project is just for container of org

class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    projectid = Column(Integer, ForeignKey("project.id"))
    desc = Column(String, default="n/a")

    admins = relationship("TeamAdmin", back_populates="team")
    repos = relationship("Repo", back_populates="team")
    project = relationship("Project", back_populates="teams")

class TeamAdmin(Base):
    __tablename__ = "teamadmin"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"), nullable=False)
    teamid = Column(Integer, ForeignKey("team.id"), nullable=False)
    desc = Column(String, default="n/a")

    user = relationship("User", back_populates="teams")
    team = relationship("Team", back_populates="admins")

# for repo
class Repo(Base):
    __tablename__ = "repo"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, default="n/a")
    teamid = Column(Integer, ForeignKey("team.id"), nullable=False)
    arn = Column(String)
    url = Column(String)
    repoid = Column(String)

    team = relationship("Team", back_populates="repos")
    perms = relationship("Perm", back_populates="repo")

class Perm(Base):
    __tablename__ = "perm"
    id = Column(Integer, primary_key=True)#, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id"), nullable=False)
    repoid = Column(Integer, ForeignKey("repo.id"), nullable=False) # Resource Tag, such as 'project', 'team'
    perm = Column(String, nullable=False) # just 'read|write|admin' as read('GET*', 'LIST*'), write(*), admin(delete, change perm)
    desc = Column(String, default="n/a")

    user = relationship("User", back_populates="perms")
    repo = relationship("Repo", back_populates="perms")
