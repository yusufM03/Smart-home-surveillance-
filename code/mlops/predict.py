from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import json
import time
from datetime import datetime
from win32com.client import Dispatch
from collections import defaultdict

# Fonction pour la synthèse vocale
def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

# Fonction pour marquer l'attendance
def mark_attendance(name, timestamp, authorized=True):
    # Convertir le timestamp en date et heure
    try:
        # Si timestamp est une chaîne, le convertir en float
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
        
        date = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")
        time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
    except (ValueError, TypeError) as e:
        print(f"Error processing timestamp: {e}")
        return
    
    # Créer le dossier Attendance s'il n'existe pas
    attendance_dir = "Attendance"
    os.makedirs(attendance_dir, exist_ok=True)
    
    # Nom du fichier JSON
    attendance_file = os.path.join(attendance_dir, f"Attendance_{date}.json")
    
    # Données à enregistrer
    attendance_data = {
        "name": name,
        "time": time_str,
        "status": "Authorized" if authorized else "Unauthorized"
    }
    
    # Charger les données existantes ou initialiser une liste vide
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as file:
            data = json.load(file)
    else:
        data = []
    
    # Ajouter les nouvelles données
    data.append(attendance_data)
    
    # Enregistrer les données dans le fichier JSON
    with open(attendance_file, 'w') as file:
        json.dump(data, file, indent=4)

# Charger le modèle KNN pré-entraîné
try:
    with open('data/models/knn_model.pkl', 'rb') as f:
        knn = pickle.load(f)
    print("KNN model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file not found. Please run train.py first.")
    exit()

# Capturer la vidéo en direct
video = cv2.VideoCapture(0)

# Chemin vers le fichier XML inclus dans OpenCV
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
facedetect = cv2.CascadeClassifier(cascade_path)

# Seuil de confiance pour la reconnaissance
THRESHOLD = 3000  # Ajuste cette valeur en fonction de tes tests

# Nombre de frames à analyser
FRAME_COUNT = 50

# Dictionnaire pour compter les détections
detection_counts = defaultdict(int)

# Compteur de frames
frame_counter = 0

while frame_counter < FRAME_COUNT:
    ret, frame = video.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # Égalisation d'histogramme
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Conserver l'image en couleur (3 canaux RGB)
        crop_img = frame[y:y+h, x:x+w, :]
        
        # Redimensionner l'image à 50x50 pixels (comme pendant l'entraînement)
        resized_img = cv2.resize(crop_img, (50, 50))
        
        # Aplatir l'image en un vecteur de 7500 éléments (50x50x3)
        resized_img = resized_img.flatten().reshape(1, -1)
        
        # Prédire le nom et vérifier la confiance
        distances, indices = knn.kneighbors(resized_img)
        print(f"Distance to nearest neighbor: {distances[0][0]}")  # Log pour déboguer
        if distances[0][0] < THRESHOLD:
            output = knn.predict(resized_img)
            name = output[0]
            authorized = True
        else:
            name = "Unauthorized"
            authorized = False
        
        # Compter les détections
        detection_counts[name] += 1
        
        # Afficher le nom sur l'image
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, name, (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
    
    # Afficher l'image
    cv2.imshow("Frame", frame)
    
    # Incrémenter le compteur de frames
    frame_counter += 1
    
    # Attendre 1 ms entre les frames
    if cv2.waitKey(1) == ord('q'):
        break

# Fermer la caméra et les fenêtres
video.release()
cv2.destroyAllWindows()

# Si des détections ont été faites, enregistrer la personne la plus fréquente
if detection_counts:
    # Trouver la personne la plus fréquemment détectée
    most_common_person = max(detection_counts, key=detection_counts.get)
    
    # Obtenir le timestamp (en float)
    ts = time.time()
    
    # Marquer l'attendance pour la personne la plus fréquente
    mark_attendance(most_common_person, ts, authorized=(most_common_person != "Unauthorized"))
    print(f"Attendance marked for {most_common_person}.")
else:
    print("No faces detected in the 10 frames.")