import cv2
import mediapipe as mp
import time
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from utils import visualize
import numpy as np

mpDraw = mp.solutions.drawing_utils
base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.3)
detector = vision.ObjectDetector.create_from_options(options)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)


def detect(img, draw=True):
    if img is not None:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        detection_result = detector.detect(mp_image) 
        # print(detection_result)
        image_copy = np.copy(mp_image.numpy_view())
        annotated_image = visualize(image_copy, detection_result)
        rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        return rgb_annotated_image
    else:
        print('No image')
        return img


def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img = detect(img)

        if success:
            cv2.imshow('Image', img)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()
