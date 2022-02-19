import cv2
import numpy as np


def detect_face(image, models):
    detector = cv2.dnn.readNetFromCaffe(models[0], models[1])
    detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    detector.setInput(blob)  # setting new input value for our network "blob"
    detections = detector.forward()  # to compute output of the layer
    list_box = []
    for i in range(0, detections.shape[2]):
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        confidence = detections[0, 0, i, 2]
        if confidence >= 0.6:
            #cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 1)
            if list_box == []:
                list_box = np.expand_dims(box, axis=0)
            else:
                list_box = np.vstack((list_box, box))
    return list_box
