import cloud

yun = cloud.get()

def _reponame(proj, team, name):
    return proj+"-"+team+"-"+name

def get(proj, team, name):
    return yun.CloudRepo.get(_reponame(proj, team, name))

def tag(proj, team, name, key, val):
    return yun.CloudRepo.tag(_reponame(proj, team, name), key, val)

def list(project, team):
    return yun.CloudRepo.list()

def create(proj, team, name, desc, tags):
    return yun.CloudRepo.create(_reponame(proj, team, name), desc, tags)

def delete(proj, team, name):
    return yun.CloudRepo.delete(_reponame(proj, team, name))
