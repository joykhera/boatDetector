import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary
import traceback

load_dotenv(dotenv_path='../.env')

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

config = cloudinary.config(secure=True)

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


def upload_image(image_path, id):
    description = f"Boat {id}",
    public_id = f"boat{id}"
    filename = f"boat{id}.png"
    
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
                    # "description": description,
                    "simpleMediaItem": {
                        "uploadToken": upload_token,
                        "fileName": filename
                    }
                }]
            }
        )

        batch_create_response_json = batch_create_response.json()
        if 'error' in batch_create_response_json:
            raise Exception(batch_create_response_json['error'])

        media_item_id = batch_create_response_json['newMediaItemResults'][0]['mediaItem']['id']
        
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
        
        base_url = get_from_album_response.json()['baseUrl']
        cloudinary.uploader.upload(base_url, public_id=public_id, unique_filename=False, overwrite=True)
        srcURL = cloudinary.CloudinaryImage(public_id).build_url()
        
        return {'img_url': srcURL}
    
    except Exception as e:
        print(traceback.print_exc())
        print(e)
        return {'error': e}
