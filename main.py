#!/usr/bin/env python3

from pprint import pprint

# pip install -r requirements.txt
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

# OAuth stuff
# This file must be created or downloaded, see https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/photoslibrary.readonly'
]
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


def auth_google():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

    credentials = flow.run_local_server(
        host='localhost',
        port=8080, 
        authorization_prompt_message='Please visit this URL: {url}', 
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True
    )

    return credentials


def list_files():
    credentials = auth_google()
    # Only works for Google services listed at https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
    drive_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    files = drive_service.files().list().execute()
    pprint(files)

def list_albums():
    # List photo albums
    # REQUIRES https://www.googleapis.com/auth/photoslibrary or https://www.googleapis.com/auth/photoslibrary.readonly OAuth scope
    list_albums_url = 'https://photoslibrary.googleapis.com/v1/albums'
    more_albums = True
    while more_albums:
        response = requests.get(list_albums_url)
        if response.ok:
            for album in response['albums']:
                print('{} | {} items'.format(album['title'], album['mediaItemsCount']))
            if 'nextPageToken' not in response:
                more_albums = False
        else:
            error_response = response.json()
            error_code = error_response['error']['code']
            error_message = error_response['error']['message']
            error_status = error_response['error']['status']
            print('Error {} / {} - {}'.format(error_code, error_status, error_message))
            more_albums = False


def main():
    list_files()
    list_albums()


if __name__ == '__main__':
    main()
