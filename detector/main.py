import os
import cv2
import psycopg2
import threading
from ultralytics import YOLO
from boat import Boat
from store_images import upload_image
from dotenv import load_dotenv
from colorama import Fore, Style
import uuid


# Initialize
load_dotenv(dotenv_path='../.env')
model = YOLO('yolov8x.pt')
cap = cv2.VideoCapture(0)
objectToDetect = 'boat'
boats = {}
connection = psycopg2.connect(
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
connection.autocommit = True
cursor = connection.cursor()
error = False


def save_image(screenshot_path, id):
    print(f'{Fore.RED}Saving image to cloud...{Style.RESET_ALL}')
    upload_image_response = upload_image(screenshot_path, id=id)
    if 'error' in upload_image_response:
        print(f'{Fore.RED}Error uploading image to cloud!{Style.RESET_ALL}')
        global error
        error = True
        return
    img_url = upload_image_response['img_url']
    print(img_url)
    query = f"INSERT INTO boats (link) VALUES ('{img_url}')"
    cursor.execute(query)


def detect(frame):
    height, width, _ = frame.shape
    center = (width // 2, height // 2)
    results = model.track(frame, persist=True, verbose=False)

    for box in results[0].boxes:
        detectedObject = results[0].names[box.cls[0].item()]
        confidence = box.conf.item()

        if detectedObject == objectToDetect and confidence > 0.3:
            print(f'{Fore.BLUE}{objectToDetect} detected{Style.RESET_ALL}')
            id = uuid.uuid4()

            if id not in boats:
                boat = Boat(box, id)
                boats[id] = boat
                screenshot_path = f'./screenshots/{boat.id}.png'
                cv2.imwrite(screenshot_path, frame)
            else:
                boat = boats[id]
                screenshot_path = f'./screenshots/{boat.id}.png'

            boat.update_coords(box)
            boat.draw(frame, confidence)

            if boat.is_moving_towards_point(center):
                print('Updated local screenshot!')
                cv2.imwrite(screenshot_path, frame)
            elif not boat.captured:
                boat.captured = True
                thr = threading.Thread(target=save_image, args=(screenshot_path, boat.id))
                thr.start()

    return frame


# Main loop
success = True
while success:
    success, frame = cap.read()
    print('errorr', error)
    if error:
        break
    
    if success:
        frame = detect(frame)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
