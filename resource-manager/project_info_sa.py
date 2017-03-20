# Getting this working:
# 
# $ mkvirtualenv rsrc-mgr-projinfo
# $ pip install -r requirements.txt
# $ gcloud beta auth application-default login
# <... your browser should open so you can login to gcp ...>
# $ python project_info_sa.py

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from ratelimiter import RateLimiter

def resource_mgr_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

def resources_projects(service):
    projects = service.projects()
    return projects

def main():
    rate_limiter = RateLimiter(400, 100)

    with rate_limiter:
        projects_api = resources_projects(resource_mgr_service())
        proj_request = projects_api.list()
        while proj_request is not None:
            response = proj_request.execute()
            for project in response['projects']:
                try:
                    policy_req = projects_api.getIamPolicy(
                        resource=project['projectId'], body={})
                    policy_res = policy_req.execute()
                    num_bindings = 0
                    if 'bindings' in policy_res:
                        num_bindings = len(policy_res['bindings'])

                    print '{} ({}) - {}; {} IAM bindings'.format(
                        project['projectId'],
                        project['projectNumber'],
                        project['lifecycleState'],
                        num_bindings)
                except:
                    print 'Error getting IAM policy for {}'.format(project)

            proj_request = projects_api.list_next(
                previous_request=proj_request, previous_response=response)

if __name__ == '__main__':
    main()
