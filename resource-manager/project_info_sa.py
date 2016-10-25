# Getting this working:
# 
# $ mkvirtualenv rsrc-mgr-projinfo
# $ pip install -r requirements.txt
# $ gcloud init
# <... choose your gcp account and project ...>
# $ python project_info_sa.py

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def resource_mgr_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

def resources_projects(service):
    projects = service.projects()
    return projects

def main():
    projects_api = resources_projects(resource_mgr_service())
    proj_request = projects_api.list()
    while proj_request is not None:
      response = proj_request.execute()
      for project in response['projects']:
        policy_req = projects_api.getIamPolicy(resource=project['projectId'], body={})
        policy_res = policy_req.execute()
        print '{0}: {1} bindings'.format(project['projectId'], len(policy_res['bindings']))

      proj_request = projects_api.list_next(previous_request=proj_request, previous_response=response)

if __name__ == '__main__':
    main()
