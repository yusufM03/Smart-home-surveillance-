import cv2
import numpy as np
import pickle
import os
from utils import detect_faces, preprocess_face

def add_face(name):
    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces_data = []
    i = 0

    while True:
        ret, frame = video.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        faces = detect_faces(frame, facedetect)

        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = preprocess_face(crop_img)
            if i % 10 == 0:
                faces_data.append(resized_img)
            i += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
            cv2.putText(frame, f"Capturing {name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 255), 1)

        cv2.imshow("Adding Face", frame)
        if cv2.waitKey(1) == ord('q') or i == 100:
            break

    video.release()
    cv2.destroyAllWindows()

    # Charger les données existantes
    if os.path.exists('data/faces_data.pkl'):
        with open('data/faces_data.pkl', 'rb') as f:
            existing_faces = pickle.load(f)
        with open('data/names.pkl', 'rb') as f:
            existing_names = pickle.load(f)
    else:
        existing_faces = []
        existing_names = []

    # Ajouter les nouvelles données
    existing_faces.extend(faces_data)
    existing_names.extend([name] * len(faces_data))

    # Sauvegarder les données mises à jour
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(np.array(existing_faces), f)
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(existing_names, f)

    print(f"Added {len(faces_data)} faces for {name}.")

    # Entraîner le modèle avec les nouvelles données
    os.system("python scripts/train.py")

if __name__ == "__main__":
    name = input("Enter the name of the person: ")
    add_face(name)