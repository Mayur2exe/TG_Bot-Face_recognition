import os
import pickle
import cv2
import face_recognition
import numpy as np
import detector

from time import sleep



def load_images_to_db():
    path = "Path of known faces"
    list_images = os.listdir("Path of known faces")
    k = len(list_images)
    prototxt_path = r"Path of deploy.prototxt"
    caffemodel_path = r"Path of weights.caffemodel"
    models = [prototxt_path, caffemodel_path]
    list_images = [File for File in list_images if File.endswith(('.jpg', '.jpeg', 'JPEG', 'PNG', 'JPG', 'png'))]
    m = len(list_images)
    name = []
    Feats = []
    for file_name in list_images:
        im = cv2.imread(os.path.join(path, file_name))
        box = detector.detect_face(im, models)
        try:
            box_face = [(box[1], box[2], box[3], box[0]) for box in box.astype("int")]
        except:
            print(file_name)
            continue
        feat = face_recognition.face_encodings(im, box_face, num_jitters=100)
        if len(feat) != 1:
            continue
        else:
            ne_name = file_name.split("_")[0]
            new_name = ne_name.split(".")[0]
            if new_name == "":
                continue
            name.append(new_name)
            if len(Feats) == 0:
                Feats = np.frombuffer(feat[0], dtype=np.float64)
            else:
                Feats = np.vstack((Feats, np.frombuffer(feat[0], dtype=np.float64)))
    n = len(Feats)
    names = sorted(list(set(name)), key=str.lower)

    pick = [Feats, name, models]
    file_name = "sample.pkl"
    open_file = open(file_name, "wb")
    pickle.dump(pick, open_file)

    return Feats, name, models, k, m, n, names


def usepkl():
    open_file = open("sample.pkl", "rb")
    pick = pickle.load(open_file)
    open_file.close()
    return pick[0], pick[1], pick[2]
#encodings, names, models = load_images_to_db()