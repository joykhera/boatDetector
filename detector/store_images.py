import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

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
    try:
        # read image from file
        with open(image_path, "rb") as f:
            image_contents = f.read()

        # upload photo and get upload token
        upload_response = authed_session.post(
            "https://photoslibrary.googleapis.com/v1/uploads",
            headers={},
            data=image_contents
        )
        upload_token = upload_response.text

        # use batch create to add photo and description
        batch_create_response = authed_session.post(
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

        media_item_id = batch_create_response.json()['newMediaItemResults'][0]['mediaItem']['id']
        
        authed_session.post(
            f"https://photoslibrary.googleapis.com/v1/albums/{os.getenv('ALBUM_ID')}:batchAddMediaItems",
            headers={
                'content-type': 'application/json',
            },
            json={
                "mediaItemIds": [
                    media_item_id,
                ]
            }
        )
        
        get_from_album_response = authed_session.get(
            f"https://photoslibrary.googleapis.com/v1/mediaItems/{media_item_id}"
        )
        
        return get_from_album_response.json()
    
    except Exception as e:
        print(e)
        return {'error': e}