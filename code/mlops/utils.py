import cv2
import numpy as np

def detect_faces(frame, facedetect):
    """
    Détecte les visages dans une image.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    return faces

def preprocess_face(crop_img):
    """
    Redimensionne et aplati une image de visage.
    """
    resized_img = cv2.resize(crop_img, (50, 50)).flatten()
    return resized_img