import argparse

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from ratelimiter import RateLimiter

def main():
    pass

def get_discovery():
    credentials = GoogleCredentials.get_application_default()
    discovery_api = discovery.build('discovery', 'v1', credentials=credentials)
    return discovery_api

def get_doc():
    req = get_discovery().apis().list()
    doc = req.execute()
    print doc
    return doc

def get_api(api_version_name):
    api, version = api_version_name.split(':')
    req = get_discovery().apis().getRest(api=api, version=version)
    res = req.execute()
    return res

if __name__ == '__main__':
    main()
