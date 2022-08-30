import boto3

# !!! ATTENTION :  AK/SK in ENV only
#   export AWS_DEFAULT_REGION=cn-northwest-1
#   export AWS_ACCESS_KEY_ID=AK
#   export AWS_SECRET_ACCESS_KEY=SK
#   export AWS_SESSION_TOKEN=SESSIONTOKEN

class CloudIAM:
    client = boto3.client('iam')
    @staticmethod
    def create(name):
        resp = CloudIAM.client.create_user(UserName=name)
        if (not resp) or ('User' not in resp):
            return None
        return {
            "name": resp['User']['UserName'],
            "arn": resp['User']['Arn']
        }
    
    def create_codecommit_passwd(name):
        resp = CloudIAM.client.create_service_specific_credential(UserName=name, ServiceName='codecommit.amazonaws.com')
        if (not resp) or ('ServiceSpecificCredential' not in resp):
            return None
        cred = resp['ServiceSpecificCredential']
        return {
            "user": cred['UserName'],
            "ccid": cred['ServiceSpecificCredentialId'],
            "ccname": cred['ServiceUserName'],
            "ccpasswd": cred['ServicePassword']
        }
    
    def list_codecommit_passwd(name):
        resp = CloudIAM.client.list_service_specific_credentials(UserName=name, ServiceName='codecommit.amazonaws.com')
        if (not resp) or ('ServiceSpecificCredentials' not in resp):
            return None
        cred = resp['ServiceSpecificCredentials'][0]
        return {
            "user": cred['UserName'],
            "ccid": cred['ServiceSpecificCredentialId'],
            "ccname": cred['ServiceUserName'],
            "ccpasswd": cred['ServicePassword']
        }

    def reset_codecommit_passwd(name):
        cc = CloudIAM.list_codecommit_passwd(name)
        resp = CloudIAM.client.reset_service_specific_credential(UserName=name, ServiceSpecificCredentialId=cc['ccid'])
        if (not resp) or ('ServiceSpecificCredential' not in resp):
            return None
        cred = resp['ServiceSpecificCredential']
        return {
            "user": cred['UserName'],
            "ccid": cred['ServiceSpecificCredentialId'],
            "ccname": cred['ServiceUserName'],
            "ccpasswd": cred['ServicePassword']
        }

    @staticmethod
    def delete(name):
        cc = CloudIAM.list_codecommit_passwd(name)
        CloudIAM.client.delete_service_specific_credential(UserName=name, ServiceSpecificCredentialId=cc['ccid'])
        resp = CloudIAM.client.delete_user(UserName=name)
        return None

    @staticmethod
    def policy_update():
        pass

    @staticmethod
    def group_update():
        pass

# for repo
class CloudRepo:
    client = boto3.client('codecommit')
    @staticmethod
    def create(name, desc, tags=None):
        repo = CloudRepo.client.create_repository(repositoryName=name, repositoryDescription=desc, tags=tags)
        if (not repo) or ('repositoryMetadata' not in repo):
            return None
        meta = repo['repositoryMetadata']
        return {
            'name': meta['repositoryName'],
            'desc': meta['repositoryDescription'],
            'url': meta['cloneUrlHttp'],
            'arn': meta['arn'],
            'id': meta['repositoryId']
        }

    @staticmethod
    def list():
        repos = []
        resp = CloudRepo.client.list_repositories()
        if (not resp) or ('repositories' not in resp):
            return None
        repos.append([CloudRepo.get(r['repositoryName']) for r in resp['repositories']])
        while 'nextToken' in resp:
            resp = CloudRepo.client.list_repositories(nextToken=resp.nextToken)
            if (not resp) or ('repositories' not in resp):
                break
            repos.append([CloudRepo.get(r['repositoryName']) for r in resp['repositories']])
        return repos

    @staticmethod
    def get(name):
        resp = CloudRepo.client.get_repository(repositoryName = name)
        if (not resp) or ('repositoryMetadata' not in resp):
            return None
        meta = resp['repositoryMetadata']
        return {
            'name': meta['repositoryName'],
            'desc': meta['repositoryDescription'],
            'url': meta['cloneUrlHttp'],
            'arn': meta['arn'],
            'id': meta['repositoryId']
        }

    @staticmethod
    def delete(name):
        keeprepo = CloudRepo.get(name)
        resp = CloudRepo.client.delete_repository(repositoryName = name)
        return keeprepo

    @staticmethod
    def tag(name, key, val):
        tags = {}
        tags[key] = val
        resp = CloudRepo.client.tag_resource(repositoryName = name, tags = tags)
        return tags