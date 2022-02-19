import cv2
import numpy as np
import recognizer
import loader

# encodings, names, models, _, _, _ = loader.load_images_to_db()
encodings, names, models = loader.usepkl()


def name_box(img, box, match_name):
    for i in np.arange(len(box)):
        y0, x1, y1, x0 = box[i]
        if not match_name:
            continue
        else:
            cv2.putText(img, match_name[i], (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    for b in box:
        cv2.rectangle(img, (b[3], b[0]), (b[1], b[2]), (0, 0, 255), 1)
    return img


def main1():
    frame = cv2.imread("Path and image where image is stored")
    h, w, _ = frame.shape
    f = 1
    fr = cv2.resize(frame, (int(w / f), int(h / f)))
    n_name, box_faces, acc= recognizer.compare_faces(fr, encodings, names, models)
    n = n_name
    fr = name_box(fr, box_faces, n_name)
    cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
    cv2.imshow("Face Recognition", fr)
    img_name = "Image.png"
    cv2.imwrite(img_name, fr)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    return n, acc
