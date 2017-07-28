# orgs search

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

def resources_orgs(service):
    return service.organizations()

def main():
    """Find all the organizations."""
    rate_limiter = RateLimiter(400, 100)
    orgs_api = resources_orgs(resource_mgr_service())

    with rate_limiter:
        for response in _find_resources(orgs_api):
            print response

def _find_resources(orgs_api):
    """Find all the GCP resources.

    Args:
        orgs_api: The organizations API to use.

    Returns:
        Generator of the organizations API response.
    """
    next_page_token = None

    while True:
        req_body = {}
        if next_page_token:
            req_body['pageToken'] = next_page_token
        request = orgs_api.search(body=req_body)
        response = request.execute()
        yield response
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

if __name__ == '__main__':
    main()
