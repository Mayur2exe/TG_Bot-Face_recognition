import cv2
import numpy as np
import detector
import face_recognition
import math


def compare_faces(frame, encodings, names, models):
    boxes = detector.detect_face(frame, models)
    bo = face_recognition.face_locations(frame)
    try:
        boxes = [(box[1], box[2], box[3], box[0]) for box in boxes.astype("int")]
    except:
        boxes = []
    if len(boxes) < len(bo):
        boxes = bo
    m_names = []
    un_enc = face_recognition.face_encodings(frame, boxes, num_jitters=5)
    d = []
    n_d = []
    for un in un_enc:
        dist = face_recognition.face_distance(encodings, un)
        index = np.argmin(dist)
        if dist[index] <= 0.535:
            m_names = m_names + [names[index]]
            d.append(dist[index])
            n_d.append([names[index], dist[index]])
        else:
            m_names = m_names + ["Unknown"]
            l = dist[index]
            d.append(l)
            n_d.append(["Unknown", dist[index]])

    for k in m_names:
        res = []
        res_d = []
        for i in range(len(m_names)):
            if m_names[i] == k:
                res.append(i)
                res_d.append(d[i])
        act = n_d[res[res_d.index(min(res_d))]]
        for i in range(0, len(n_d)):
            if n_d[i][0] == k:
                if n_d[i] != act:
                    n_d[i][0] = "Unknown"
    acc = []
    for i in d:
        acc.append("{:.2f}".format(face_distance_to_conf(i) * 100))
    lis = []
    for i in n_d:
        lis.append(i[0])
    m_names = lis
    return m_names, boxes, acc


def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
