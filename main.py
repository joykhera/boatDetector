from ultralytics import YOLO
import cv2
import pyautogui
from PIL import ImageGrab

# load yolov8 model
model = YOLO('yolov8x.pt')

cap = cv2.VideoCapture(0)

ret = True
# read frames
while ret:
    ret, frame = cap.read()

    if ret:

        # detect objects
        # track objects
        results = model.track(frame, persist=True)
        # print(results[0]._keys)
        # labels = results[0].boxes.labels if results.boxes is not None else []
        # print(labels)
        # print(type(results[0]))
        for box in results[0].boxes:
            detectedObject = results[0].names[box.cls[0].item()]
            print(detectedObject)

            if detectedObject == 'keyboard':
                print('keyboard detected')
                cv2.imwrite('./screenshot.png', frame)
                # myScreenshot = pyautogui.screenshot()
                # myScreenshot.save(r'./screenshot.png')

        # plot results
        # cv2.rectangle
        # cv2.putText
        frame_ = results[0].plot()

        # visualize
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
