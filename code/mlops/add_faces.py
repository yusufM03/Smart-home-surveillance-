import cv2
import pickle
import numpy as np
import os

# Initialiser la capture vidéo
video = cv2.VideoCapture(0)

# Chemin vers le fichier XML inclus dans OpenCV
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
facedetect = cv2.CascadeClassifier(cascade_path)

# Liste pour stocker les visages et les étiquettes
faces_data = []
i = 0

# Demander le nom de l'utilisateur
name = input("Enter Your Name: ")

# Capturer des images et ajouter des visages
while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]  # Conserver l'image en couleur
        resized_img = cv2.resize(crop_img, (50, 50)).flatten()  # Redimensionner et aplatir l'image
        if len(faces_data) < 100 and i % 10 == 0:  # Collecter 100 échantillons
            faces_data.append(resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 100:  # Quitter après avoir collecté 100 échantillons
        break

video.release()
cv2.destroyAllWindows()

# Convertir en tableau numpy
faces_data = np.asarray(faces_data)

# Créer le dossier data/ s'il n'existe pas
if not os.path.exists('data/'):
    os.makedirs('data/')

# Charger ou créer les données existantes
if 'names.pkl' not in os.listdir('data/'):
    names = [name] * len(faces_data)  # Nombre d'étiquettes = nombre de visages
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    names.extend([name] * len(faces_data))  # Ajouter les nouvelles étiquettes

# Sauvegarder les étiquettes
with open('data/names.pkl', 'wb') as f:
    pickle.dump(names, f)

if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)  # Ajouter les nouveaux visages
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

print(f"Added {len(faces_data)} faces for {name}.")