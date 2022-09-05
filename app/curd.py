import hashlib
from sqlalchemy.orm import Session

import orm, schema

class User:
    @staticmethod
    def __hash_passwd(user: str, passwd: str):
        chksum = user+hashlib.sha256(user.encode()).hexdigest()+passwd+hashlib.sha256(passwd.encode()).hexdigest()
        return hashlib.sha256(chksum.encode()).hexdigest()

    @staticmethod
    def get(db: Session, userid: int):
        return db.query(orm.User).filter(orm.User.id == userid).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0):
        return db.query(orm.User).offset(skip).all()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(orm.User).filter(orm.User.email == email).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(orm.User).filter(orm.User.name == name).first()

    @staticmethod
    def get_by_auth(db: Session, auth: schema.Authorization):
        auth.passwd = User.__hash_passwd(auth.user, auth.passwd)
        return db.query(orm.User).filter(orm.User.name == auth.user).filter(orm.User.passwd == auth.passwd).first()

    @staticmethod
    def new(db: Session, user: schema.UserNew):
        user.passwd = User.__hash_passwd(user.name, user.passwd)
        newuser = orm.User(**user.dict())
        db.add(newuser)
        db.commit()
        db.refresh(newuser)
        return newuser

    @staticmethod
    def update(db: Session, user: orm.User):
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: orm.User):
        keepuser = user
        db.delete(user)
        db.commit()
        return keepuser

    @staticmethod
    def is_root(db: Session, userid: int):
        if userid == 1:
            return True
        return False

    @staticmethod
    def is_project_admin(db: Session, userid: int, projectid: int):
        admins = db.query(orm.ProjectAdmin).filter(orm.ProjectAdmin.projectid == projectid).all()
        for u in admins:
            if u.userid == userid:
                return True
        return False

    @staticmethod
    def is_team_admin(db: Session, userid: int, teamid: int):
        admins = db.query(orm.Perm).filter(orm.Perm.teamid == teamid).all()
        for u in admins:
            if u.userid == userid:
                return True
        return False
    
    @staticmethod
    def can_write(db: Session, userid: int, orgid: int):
        user = db.query(orm.User).filter(orm.User.id == userid).first()
        for perm in user.perms:
            if perm.perm == 'root' or (perm.orgid == orgid and (perm.perm == 'admin' or perm.perm == 'write')):
                return True
        return False

    @staticmethod
    def can_read(db: Session, userid: int, orgid: int):
        user = db.query(orm.User).filter(orm.User.id == userid).first()
        for perm in user.perms:
            if perm.perm == 'root' or perm.orgid == orgid:
                return True
        return False

class Project:
    @staticmethod
    def get(db: Session, projid: int):
        return db.query(orm.Project).filter(orm.Project.id == projid).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0):
        return db.query(orm.Project).offset(skip).all()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(orm.Project).filter(orm.Project.name == name).first()

    @staticmethod
    def new(db: Session, proj: schema.ProjectNew):
        newproj = orm.Project(**proj.dict())
        db.add(newproj)
        db.commit()
        db.refresh(newproj)
        return newproj

    @staticmethod
    def update(db: Session, proj: orm.Project):
        db.commit()
        db.refresh(proj)
        return proj

    @staticmethod
    def delete(db: Session, proj: orm.Project):
        keeporg = proj
        db.delete(proj)
        db.commit()
        return keeporg

class ProjectAdmin:
    @staticmethod
    def get(db: Session, paid: int):
        return db.query(orm.ProjectAdmin).filter(orm.ProjectAdmin.id == paid).first()

    @staticmethod
    def get_all(db: Session, projid: int, skip: int = 0):
        return db.query(orm.ProjectAdmin).filter(orm.ProjectAdmin.projectid == projid).offset(skip).all()

    staticmethod
    def get_all_by_user(db: Session, userid: int, skip: int = 0):
        return db.query(orm.ProjectAdmin).filter(orm.ProjectAdmin.userid == userid).offset(skip).all()

    @staticmethod
    def new(db: Session, pa: schema.ProjectAdminNew):
        newpa = orm.ProjectAdmin(**pa.dict())
        db.add(newpa)
        db.commit()
        db.refresh(newpa)
        return newpa

    @staticmethod
    def update(db: Session, pa: orm.ProjectAdmin):
        db.commit()
        db.refresh(pa)
        return pa

    @staticmethod
    def delete(db: Session, pa: orm.ProjectAdmin):
        keeppa = pa
        db.delete(pa)
        db.commit()
        return keeppa

class Team:
    @staticmethod
    def get(db: Session, teamid: int):
        return db.query(orm.Team).filter(orm.Team.id == teamid).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0):
        return db.query(orm.Team).offset(skip).all()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(orm.Team).filter(orm.Team.name == name).first()

    @staticmethod
    def new(db: Session, team: schema.TeamNew):
        newteam = orm.Team(**team.dict())
        newteam.id = None
        db.add(newteam)
        db.commit()
        db.refresh(newteam)
        return newteam

    @staticmethod
    def update(db: Session, team: orm.Team):
        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def delete(db: Session, team: orm.Team):
        keepteam = team
        db.delete(team)
        db.commit()
        return keepteam

class TeamAdmin:
    @staticmethod
    def get(db: Session, taid: int):
        return db.query(orm.TeamAdmin).filter(orm.TeamAdmin.id == taid).first()

    @staticmethod
    def get_all(db: Session, teamid: int, skip: int = 0):
        return db.query(orm.TeamAdmin).filter(orm.TeamAdmin.teamid == teamid).offset(skip).all()

    @staticmethod
    def get_all_by_user(db: Session, userid: int, skip: int = 0):
        return db.query(orm.TeamAdmin).filter(orm.TeamAdmin.userid == userid).offset(skip).all()

    @staticmethod
    def new(db: Session, ta: schema.TeamAdminNew):
        newta = orm.TeamAdmin(**ta.dict())
        db.add(newta)
        db.commit()
        db.refresh(newta)
        return newta

    @staticmethod
    def update(db: Session, ta: orm.TeamAdmin):
        db.commit()
        db.refresh(ta)
        return ta

    @staticmethod
    def delete(db: Session, ta: orm.TeamAdmin):
        keepta =ta
        db.delete(ta)
        db.commit()
        return keepta

class Repo:
    @staticmethod
    def get(db: Session, repoid: int):
        return db.query(orm.Repo).filter(orm.Repo.id == repoid).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0):
        return db.query(orm.Repo).offset(skip).all()

    @staticmethod
    def get_all_by_team(db: Session, teamid: int, skip: int = 0):
        return db.query(orm.Repo).filter(orm.Repo.teamid == teamid).offset(skip).all()
    
    @staticmethod
    def get_all_by_name(db: Session, name: str, skip: int = 0):
        return db.query(orm.Repo).filter(orm.Repo.name == name).offset(skip).all()

    @staticmethod
    def get_all_repo_writer(db: Session, repoid: int):
        return db.query(orm.Repo, orm.Perm, orm.User).filter(orm.Repo.id == repoid).filter(orm.Perm.id == orm.Repo.id).filter(orm.Perm.perm == 'write').all()

    @staticmethod
    def get_all_repo_reader(db: Session, repoid: int):
        return db.query(orm.Repo, orm.Perm, orm.User).filter(orm.Repo.id == repoid).filter(orm.Perm.id == orm.Repo.id).filter(orm.Perm.perm == 'read').all()

    @staticmethod
    def new(db: Session, repo: schema.RepoNew):
        newrepo = orm.Repo(**dict(repo))
        db.add(newrepo)
        db.commit()
        db.refresh(newrepo)
        return newrepo

    @staticmethod
    def update(db: Session, repo: orm.Repo):
        db.commit()
        db.refresh(repo)
        return repo

    @staticmethod
    def delete(db: Session, repo: orm.Repo):
        keeprepo =repo
        db.delete(repo)
        db.commit()
        return keeprepo

class Perm:
    # for PERM CURD
    @staticmethod
    def get(db: Session, permid: int):
        return db.query(orm.Perm).filter(orm.Perm.id == permid).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0):
        return db.query(orm.Perm).offset(skip).all()

    @staticmethod
    def get_by_org(db: Session, teamid: id):
        return db.query(orm.Perm).filter(orm.Perm.teamid == teamid).all()

    @staticmethod
    def get_by_user(db: Session, userid: id):
        return db.query(orm.Perm).filter(orm.Perm.userid == userid).all()

    @staticmethod
    def get_by_user_read(db: Session, userid: id):
        return db.query(orm.Perm).filter(orm.Perm.userid == userid).filter(orm.Perm.perm == 'read').all()
    
    @staticmethod
    def get_by_user_write(db: Session, userid: id):
        return db.query(orm.Perm).filter(orm.Perm.userid == userid).filter(orm.Perm.perm == 'write').all()

    @staticmethod
    def new(db: Session, perm: schema.PermNew):
        newperm = orm.Perm(**perm.dict())
        db.add(newperm)
        db.commit()
        db.refresh(newperm)
        return newperm

    @staticmethod
    def update(db: Session, perm: orm.Perm):
        db.commit()
        db.refresh(perm)
        return perm

    @staticmethod
    def delete(db: Session, perm: orm.Perm):
        keeperm = perm
        db.delete(perm)
        db.commit()
        return keeperm
    
    @staticmethod
    def delete_by_query(db: Session, perm: str, userid: str, repoid: str):
        p = db.query(orm.Perm).filter(orm.Perm.userid == userid).filter(orm.Perm.repoid == repoid).filter(orm.Perm.perm == perm).first()
        kp = p 
        db.delete(p)
        db.commit()
        return kp