import pytest
import requests
import hashlib
import string
import random
import time

api="http://127.0.0.1:8000"
s = requests.Session()

random.seed(time.time_ns())

tmpvals = {
    "userid": 0,
    "projid": 0,
    "teamid": 0,
    "permid": 0
}

def randomstr(n=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))

def user_passwd(user, passwd):
    chksum = user+hashlib.sha256(user.encode()).hexdigest()+passwd+hashlib.sha256(passwd.encode()).hexdigest()
    return hashlib.sha256(chksum.encode()).hexdigest()

class TestClassUserApi:
    def test_login(self):
        r = s.post(api+"/login", json={"user":"root", "passwd": user_passwd("root", "keepitsecret")})
        assert r.status_code == 200

    def test_add(self):
        newuser = {
            "name": "pytest"+randomstr(),
            "email": "pytest"+randomstr()+"@pytest.com",
            "fullname": "pytest pytest",
            "desc": "test it",
            "passwd": "passwd"
        }
        newuser['passwd'] = user_passwd(newuser["name"], newuser["passwd"])
        r = s.post(api+"/user/", json=newuser)
        global tmpvals
        tmpvals["userid"] = r.json()['id']
        # self.tmpuser = r.json()['id']
        assert r.status_code == 200

    def test_list(self):
        r = s.get(api+'/user/')
        print(r.json())
        assert r.status_code == 200

    def test_update(self):
        newuser = {
            "active": False
        }
        print(str(tmpvals["userid"]))
        r = s.put(api+"/user/"+str(tmpvals["userid"]), json=newuser)
        print(r.json())
        assert r.status_code == 200

class TestClassProjectApi:
    def test_add_proj(self):
        newproj = {
            "name": "testproj"+randomstr(),
            "desc": "some desc here"
        }
        
        r = s.post(api+"/project/", json=newproj)
        global tmpvals
        tmpvals["projid"] = r.json()['id']
        print(r.json())
        assert r.status_code == 200

    def test_get(self):
        r = s.get(api+'/project/'+str(tmpvals["projid"]))
        print(r.json())
        assert r.status_code == 200

    def test_get_all(self):
        r = s.get(api+'/project/')
        print(r.json())
        assert r.status_code == 200

    def test_update(self):
        r = s.get(api+'/project/'+str(tmpvals["projid"]))
        team = r.json()
        team.pop('id')
        # team.pop('perms')
        team['desc'] = 'new desc'
        print(team)
        r = s.put(api+'/project/'+str(tmpvals["projid"]), json=team)
        print(r.json())
        assert r.status_code == 200

class TestClassTeamApi:
    def test_add_team(self):
        newproj = {
            "name": "testproj"+randomstr(),
            "desc": "some desc here",
            "projectid": tmpvals["projid"]
        }
        
        r = s.post(api+"/team/", json=newproj)
        #global tmpvals
        tmpvals["teamid"] = r.json()['id']
        print(r.json())
        assert r.status_code == 200

    def test_get(self):
        r = s.get(api+'/team/'+str(tmpvals["teamid"]))
        print(r.json())
        assert r.status_code == 200

    def test_get_all(self):
        r = s.get(api+'/team/?projid='+str(tmpvals["projid"]))
        print(r.json())
        assert r.status_code == 200

    def test_update(self):
        r = s.get(api+'/team/'+str(tmpvals["teamid"]))
        team = r.json()
        team['desc'] = 'new desc'
        print(team)
        r = s.put(api+'/team/'+str(tmpvals["teamid"]), json=team)
        print(r.json())
        assert r.status_code == 200

class TestClassRepoApi:
    def test_add_repo(self):
        newrepo = {
            "name": "testproj"+randomstr(),
            "desc": "some desc here",
            "teamid": tmpvals["teamid"]
        }
        
        r = s.post(api+"/repo/", json=newrepo)
        #global tmpvals
        tmpvals["repoid"] = r.json()['id']
        print(r.json())
        assert r.status_code == 200

    def test_get(self):
        r = s.get(api+'/repo/'+str(tmpvals["repoid"]))
        print(r.json())
        assert r.status_code == 200

    def test_get_all(self):
        r = s.get(api+'/repo/?teamid='+str(tmpvals["teamid"]))
        print(r.json())
        assert r.status_code == 200

    def test_update(self):
        r = s.get(api+'/repo/'+str(tmpvals["repoid"]))
        team = r.json()
        team['desc'] = 'new desc'
        print(team)
        r = s.put(api+'/repo/'+str(tmpvals["repoid"]), json=team)
        print(r.json())
        assert r.status_code == 200

class TestClassPermApi:
    def test_add(self):
        p = {
            "perm": "write",
            "desc": "some desc",
            "userid": tmpvals['userid'],
            "repoid": tmpvals['repoid']
        }
        print(p)
        r = s.post(api+"/perm/", json=p)
        tmpvals["permid"] = r.json()['id']
        print(r.json())
        assert r.status_code == 200

    def test_get(self):
        r = s.get(api+'/perm/'+str(tmpvals['permid']))
        print(r.json())
        assert r.status_code == 200

    def test_get_all(self):
        r = s.get(api+'/perm/')
        print(r.json())
        assert r.status_code == 200

    def test_update(self):
        r = s.get(api+'/perm/'+str(tmpvals['permid']))
        tmpperm = r.json()
        tmpperm.pop("id")
        tmpperm['desc'] = "new desc"
        r = s.put(api+'/perm/'+str(tmpvals['permid']), json=tmpperm)
        print(r.json())
        assert r.status_code == 200

# class TestClassTearDown:
    # def test_delete_perm(self):
    #     r = s.delete(api+'/perm/'+str(tmpvals["permid"]))
    #     print(r.json())
    #     assert r.status_code == 200 

    # def test_delete_project(self):
    #     r = s.delete(api+'/project/'+str(tmpvals["projid"]))
    #     print(r.json())
    #     assert r.status_code == 200
    
    # def test_delete_team(self):
    #     r = s.delete(api+'/team/'+str(tmpvals["teamid"]))
    #     print(r.json())
    #     assert r.status_code == 200
    
    # def test_delete_user(self):
    #     print(str(tmpvals["userid"]))
    #     r = s.delete(api+'/user/'+str(tmpvals["userid"]))
    #     print(r.json())
    #     assert r.status_code == 200
