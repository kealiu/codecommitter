from sqlalchemy.orm import Session
import curd, cloud, orm

def policy_with_projects(yun, projects):
    if not projects or len(projects) == 0:
        return None
    tagvals = ','.join(['"'+p.project.name+'"' for p in projects])
    return yun.CloudIAM.policy_gen_write_with_tag("Project", tagvals)

def policy_with_teams(yun, teams):
    if not teams or len(teams) == 0:
        return None
    tagvals = ','.join(['"'+p.team.name+'"' for p in teams])
    return yun.CloudIAM.policy_gen_write_with_tag("Team", tagvals)

def policy_with_repos_read(yun, repos):
    if not repos or len(repos) == 0:
        return None
    arns = ','.join(['"'+p.repo.arn+'"' for p in repos])
    return yun.CloudIAM.get_by_user_read(arns)

def policy_with_repos_write(yun, repos):
    if not repos or len(repos) == 0:
        return None
    arns = ','.join(['"'+p.repo.arn+'"' for p in repos])
    return yun.CloudIAM.get_by_user_write(arns)

def update_user_policy(db: Session, user: orm.User, newly=False):
    actions = []
    name = user.name
    projects = curd.ProjectAdmin.get_all_by_user(db, user.id)
    teams = curd.TeamAdmin.get_all_by_user(db, user.id)
    repos_read = curd.Perm.get_by_user_read(db, user.id)
    repos_write = curd.Perm.get_by_user_write(db, user.id)

    yun = cloud.get()

    projectpolicy = policy_with_projects(yun, projects)
    if projectpolicy:
        actions.append(projectpolicy)

    teampolicy = policy_with_teams(yun, teams)
    if teampolicy:
        actions.append(teampolicy)

    readpolicy = policy_with_repos_read(yun, repos_read)
    if readpolicy:
        actions.append(readpolicy)
    
    writepolicy = policy_with_repos_write(yun, repos_write)
    if writepolicy:
        actions.append(writepolicy)

    rules = ','.join(actions)
    policy = '{"Version": "2012-10-17","Statement": {['+rules+']}}'

    if newly:
        return yun.CloudIAM.policy_create(name, policy)
    else:
        return yun.CloudIAM.policy_update(user.ccpolicy, policy)

def refresh_policy_with_uid(db: Session, userid: int):
    user = curd.User.get(db, userid)
    return update_user_policy(db, user)

def refresh_policy_with_uname(db: Session, username: str):
    user = curd.User.get_by_name(db, username)
    return update_user_policy(db, user)
