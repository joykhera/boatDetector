import os
from ultralytics import YOLO
import cv2
from boat import Boat
from store_images import upload_image
import psycopg2
from dotenv import load_dotenv
from colorama import Fore, Style


# load yolov8 model
model = YOLO('yolov8x.pt')
cap = cv2.VideoCapture(0)
objectToDetect = 'boat'
boats = {}
load_dotenv(dotenv_path='../.env')

connection = psycopg2.connect(
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
connection.autocommit = True
cursor = connection.cursor()

success = True
# read frames
while success:
    success, frame = cap.read()
    frame_ = frame

    if success:
        height, width, _ = frame.shape
        center = (width // 2, height // 2)

        results = model.track(frame, persist=True)

        for box in results[0].boxes:
            detectedObject = results[0].names[box.cls[0].item()]
            confidence = box.conf.item()
            # print(detectedObject, confidence)

            if detectedObject == objectToDetect and confidence > 0.3:
                # print(box)
                print(f'{Fore.BLUE}{objectToDetect} detected{Style.RESET_ALL}')
                if box.id:
                    id = box.id.item()

                    if id not in boats:
                        boat = Boat(box, id)
                        boats[id] = boat
                        # ? Should we store screenshot path in the boat object
                        screenshot_path = f'./screenshots/{boat.id}.png'
                        cv2.imwrite(screenshot_path, frame)
                    else:
                        boat = boats[id]
                        screenshot_path = f'./screenshots/{boat.id}.png'

                    boat.update_coords(box)
                    boat.draw(frame, confidence)

                    # If boat is moving towards the center, update the local screenshot
                    if (boat.is_moving_towards_point(center)):
                        print('Updated local screenshot!')
                        cv2.imwrite(screenshot_path, frame)
                    
                    # Boat isn't moving towards center,
                    # if it hasn't already been captured,
                    # capture to cloud and update flag
                    else:
                        if (boat.captured == False):
                            response = upload_image(screenshot_path, description=f"Boat {boat.id}", filename=f'boat{boat.id}.png')
                            img_url = response['baseUrl']
                            query = f"INSERT INTO boats (link) VALUES ('{img_url}')"
                            cursor.execute(query)
                            boat.captured = True

        # visualize
        cv2.imshow('frame', frame_)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
