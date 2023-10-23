import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials


scopes = ['https://www.googleapis.com/auth/photoslibrary.appendonly']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/photoslibrary'])
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
authed_session = AuthorizedSession(creds)


def upload_image(image_path):
    # read image from file
    with open(image_path, "rb") as f:
        image_contents = f.read()

    # upload photo and get upload token
    response = authed_session.post(
        "https://photoslibrary.googleapis.com/v1/uploads",
        headers={},
        data=image_contents
    )
    upload_token = response.text

    # use batch create to add photo and description
    response = authed_session.post(
        'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate',
        headers={'content-type': 'application/json'},
        json={
            "newMediaItems": [{
                "description": "Test photo",
                "simpleMediaItem": {
                    "uploadToken": upload_token,
                    "fileName": "test.jpg"
                }
            }]
        }
    )
    return response.json()