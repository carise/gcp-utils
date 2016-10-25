import argparse

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def resource_mgr_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

def list_buckets(service, project_id):
    buckets = service.buckets().list(project=project_id).execute()
    return buckets

def resources_projects(service):
    projects = service.projects()
    return projects

def main(project_id):
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
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')

    args = parser.parse_args()

    main(args.project_id)
