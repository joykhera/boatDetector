from ultralytics import YOLO
import cv2
from boat import Boat

# load yolov8 model
model = YOLO('yolov8x.pt')
cap = cv2.VideoCapture(0)
objectToDetect = 'boat'
boats = {}

ret = True
# read frames
while ret:
    ret, frame = cap.read()
    frame_ = frame

    if ret:
        results = model.track(frame, persist=True)

        for box in results[0].boxes:
            detectedObject = results[0].names[box.cls[0].item()]
            confidence = box.conf.item()
            print(detectedObject, confidence)
            
            if detectedObject == objectToDetect and confidence > 0.3:
                print(box)
                print(f'{objectToDetect} detected')
                if box.id:
                    id = box.id.item()
                    
                    if id not in boats:
                        boat = Boat(box, id)
                        boats[id] = boat
                    else:
                        boat = boats[id]
                
                    boat.update_coords(box)
                    boat.draw(frame, confidence)
                
                
                cv2.imwrite('./screenshot.png', frame)


        # visualize
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
