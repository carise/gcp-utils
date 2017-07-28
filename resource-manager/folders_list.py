# folders list

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from ratelimiter import RateLimiter

def resource_mgr_service(version='v1'):
    credentials = GoogleCredentials.get_application_default()
    return discovery.build(
        'cloudresourcemanager',
        version,
        credentials=credentials,
        cache_discovery=False)

def resources_folders(service):
    folders = service.folders()
    return folders

def main():
    """Find all the folders."""
    rate_limiter = RateLimiter(400, 100)
    folders_api = resources_folders(resource_mgr_service(version='v2beta1'))

    with rate_limiter:
        for folder_response in _find_resources(folders_api):
            for folder in folder_response.get('folders', []):
                folder_id = folder.get('name')[len('folders/'):]
                print folder
                response = folders_api.getIamPolicy(resource='folders/%s' % folder_id, body={}).execute()
                print response

def _find_resources(folders_api):
    """Find all the GCP resources.

    Args:
        folders_api: The folders API to use.

    Returns:
        Generator of the folders API response.
    """
    next_page_token = None

    while True:
        req_body = {}
        if next_page_token:
            req_body['pageToken'] = next_page_token
        request = folders_api.search(body=req_body)
        response = request.execute()
        yield response
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

if __name__ == '__main__':
    main()
