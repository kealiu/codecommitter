import hashlib
from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session

from routers import perm, project, team, user, repo
import db, schema, curd

app = FastAPI()

app.include_router(user.router, prefix='/user')
app.include_router(perm.router, prefix='/perm')
app.include_router(project.router, prefix='/project')
app.include_router(team.router, prefix='/team')
app.include_router(repo.router, prefix='/repo')

# check if user is authorized, if not, redirect to login
@app.middleware("http")
def session_check(request: Request, call_next):
    if request.url.path == '/login' or request.url.path.startswith('/app'):
        return call_next(request)

    if 'user' not in request.session or not request.session['user']:
        #raise HTTPException(status_code=401, detail="username or password wrong, user not found")    
        return JSONResponse(status_code=403, content={"status_code": 403, "message": "not login"})

    return call_next(request)

# special url for login only 
@app.post('/login', response_model=schema.User, response_model_exclude_none=True)
def user_login(req: Request,  auth: schema.Authorization, db: Session = Depends(db.getsession)):
    me = curd.User.get_by_auth(db, auth)
    if me is None:
        raise HTTPException(status_code=403, detail="username or password wrong, user not found")    
    req.session['user'] = me.dict()
    return me

@app.get('/favicon.ico')
def get_favicon_ico():
    raise HTTPException(status_code=404)    

# for debug static web app
app.mount("/app/", StaticFiles(directory="../web", html = True), name="static")


app.add_middleware(SessionMiddleware, secret_key="SomeSecret1234%^&*")


# for test only
@app.on_event("startup")
def api_startup():
    dbsession = next(db.getsession())
    db.initdb()
    root = schema.UserNew(**{
        "desc": "builtin user",
        "email": "someone@testproject.com",
        "name":"root",
        "fullname": "Root User",
        "passwd": "keepitsecret"
    })
    checksum = root.name+hashlib.sha256(root.name.encode()).hexdigest()+root.passwd+hashlib.sha256(root.passwd.encode()).hexdigest()
    root.passwd = hashlib.sha256(checksum.encode()).hexdigest()
    try:
        rootuser = curd.User.new(dbsession, root)
        rootuser.arn = "n/a"
        rootuser.ccname = "n/a"
        rootuser.ccpasswd = "n/a"
        rootuser.ccpolicy = "n/a"
        rootuser.active = True
        u = curd.User.update(dbsession, rootuser)
    except Exception as e:
        print(e)