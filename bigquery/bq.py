import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--keyfile')
    args = parser.parse_args()
    list_datasets(args.project_id, args.keyfile)

def get_api(keyfile=None):
    scopes = ['https://www.googleapis.com/auth/bigquery.readonly']
    if keyfile:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            keyfile, scopes)
    else:
        credentials = GoogleCredentials.get_application_default()
    discovery_api = discovery.build('bigquery', 'v2', credentials=credentials)
    return discovery_api

def list_datasets(project_id, keyfile):
    req = get_api(keyfile).datasets().list(projectId=project_id)
    print req.uri
    doc = req.execute()
    print doc
    return doc

if __name__ == '__main__':
    main()
