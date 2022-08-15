import face_recognition
import numpy as np


def extracting_faces(img_path):
    faces = face_recognition.load_image_file(img_path)
    face_location = face_recognition.face_locations(faces)
    top, right, bottom, left = face_location[0]
    face_img = faces[top:bottom, left:right]
    return face_img


def get_encodings(img_path):
    face_list = extracting_faces(img_path)
    img_encodings = face_recognition.face_encodings(face_list)[0]
    return img_encodings


def compare_faces(img_path, compare_face_encodings, tolerance=0.6):
    compare_face_encodings = np.array(compare_face_encodings)
    new_encodings = get_encodings(img_path)
    result = face_recognition.compare_faces([new_encodings], compare_face_encodings, tolerance=tolerance)
    return result
