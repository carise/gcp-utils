# Getting this working:
# 
# $ mkvirtualenv rsrc-mgr-projinfo
# $ pip install -r requirements.txt
# $ gcloud beta auth application-default login
# <... your browser should open so you can login to gcp ...>
# $ python project_info_sa.py

import argparse

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from ratelimiter import RateLimiter

def resource_mgr_service(version='v1'):
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('cloudresourcemanager', version, credentials=credentials)

def resources_projects(service):
    projects = service.projects()
    return projects

def resources_folders(service):
    folders = service.folders()
    return folders

def main():
    """Find all the projects in an organization."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--organization_id', help='Organization id')
    parser.add_argument('--lifecycle_state', help='Lifecycle State')
    args = parser.parse_args()

    rate_limiter = RateLimiter(400, 100)

    filter_params = {}
    if args.organization_id:
        filter_params['parent.type'] = 'organization'
        filter_params['parent.id'] = args.organization_id
    if args.lifecycle_state:
        filter_params['lifecycleState'] = args.lifecycle_state

    projects_api = resources_projects(resource_mgr_service(version='v1'))
    folders_api = resources_folders(resource_mgr_service(version='v2alpha1'))

    with rate_limiter:
        for (project, num_bindings) in _find_resources(projects_api, folders_api, **filter_params):
            print '{} ({}) - {}; {} IAM bindings, parent={}'.format(
                project['projectId'],
                project['projectNumber'],
                project['lifecycleState'],
                num_bindings,
                project.get('parent'))

def _find_resources(projects_api, folders_api, **filter_params):
    """Find all the GCP resources given a filter.

    Args:
        **filter_params: dict of filter params.

    Returns:
        generator of projects.
    """

    print '===================', filter_params, _build_filter(filter_params)

    proj_request = projects_api.list(filter=_build_filter(filter_params))

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

                yield (project, num_bindings)
            except:
                print 'Error getting IAM policy for {}'.format(project)

        proj_request = projects_api.list_next(
            previous_request=proj_request, previous_response=response)

    if filter_params.get('parent.type'):
        folder_req = folders_api.list(parent=_build_parent_name(filter_params))
        folder_res = folder_req.execute()

        for f in folder_res.get('folders', []):
            folder_filter = {
                'parent.type': 'folder',
                'parent.id': f.get('name')[len('folders/'):]
            }
            for r in _find_resources(projects_api,
                                     folders_api,
                                     **folder_filter):
                yield r

def _build_filter(filter_params):
    filters = []
    for (key, val) in filter_params.iteritems():
        filters.append('{}:{}'.format(key, val))
    return ' '.join(filters)

def _build_parent_name(filter_params):
    parent_type = filter_params.get('parent.type')
    parent_id = filter_params.get('parent.id')
    return '{}s/{}'.format(parent_type, parent_id)

if __name__ == '__main__':
    main()
