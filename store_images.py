import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession

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


def upload_image(image_path, description="Test photo", filename="test.jpg"):
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
                "description": description,
                "simpleMediaItem": {
                    "uploadToken": upload_token,
                    "fileName": filename
                }
            }]
        }
    )
    return response.json()