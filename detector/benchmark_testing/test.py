import cv2
import os
import numpy as np
from main import detect as mp_detect
import sys
sys.path.append('../')
from main import detect


def process_detection_result(detection_result):
    # Check if any value in the array is non-zero (assuming non-zero indicates detection)
    return detection_result.any()


def find_differing_results(arr1, arr2):
    differing_indices = np.where(arr1 != arr2)[0]
    return differing_indices
    

def main():
    video_path = '../data/boat.mp4'
    cap = cv2.VideoCapture(video_path)
    detections = []
    differing_indices = []
    success = True

    while success:
        try:
            success, img = cap.read()
            yolo_detection = detect(img).any()
            mp_detection = mp_detect(img).any()
            detections.append([yolo_detection, mp_detection])
            index = len(detections) - 1
            # print(yolo_detection, mp_detection)
            print(index)
            if yolo_detection != mp_detection:
                print('Differing results found!', yolo_detection, mp_detection)
                index = len(detections) - 1
                differing_indices.append(index)
                cv2.imshow('Image', img)
                cv2.imwrite(f"images/{index}.jpg", img)
                cv2.waitKey(1)
                
        except Exception as e:
            print(e)
            # break
        
    print(differing_indices)


if __name__ == "__main__":
    main()
