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
import logging

# Configurer les logs
logging.basicConfig(filename='predict.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Fonction pour la synthèse vocale
def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

# Fonction pour marquer l'attendance
def mark_attendance(name, timestamp, authorized=True):
    try:
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
        date = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")
        time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
    except (ValueError, TypeError) as e:
        print(f"Error processing timestamp: {e}")
        return
    
    attendance_dir = "Attendance"
    os.makedirs(attendance_dir, exist_ok=True)
    attendance_file = os.path.join(attendance_dir, f"Attendance_{date}.json")
    
    attendance_data = {
        "name": name,
        "time": time_str,
        "status": "Authorized" if authorized else "Unauthorized"
    }
    
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as file:
            data = json.load(file)
    else:
        data = []
    
    data.append(attendance_data)
    
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
except Exception as e:
    print(f"Error loading the model: {e}")
    exit()

# Capturer la vidéo en direct
video = cv2.VideoCapture(0)
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
facedetect = cv2.CascadeClassifier(cascade_path)

THRESHOLD = 3000
FRAME_COUNT = 50
detection_counts = defaultdict(int)
frame_counter = 0

while frame_counter < FRAME_COUNT:
    ret, frame = video.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        if w > 100 and h > 100:  # Ignorer les visages trop petits
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            
            start_time = time.time()
            distances, indices = knn.kneighbors(resized_img)
            prediction_time = time.time() - start_time
            print(f"Prediction time: {prediction_time:.2f} seconds")
            
            dynamic_threshold = np.mean(distances[0]) * 1.5
            if distances[0][0] < dynamic_threshold:
                output = knn.predict(resized_img)
                name = output[0]
                authorized = True
            else:
                name = "Unauthorized"
                authorized = False
            
            detection_counts[name] += 1
            logging.info(f"Detected face: {name}, Distance: {distances[0][0]}, Authorized: {authorized}")
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
            cv2.putText(frame, name, (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
    
    cv2.imshow("Frame", frame)
    frame_counter += 1
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("Exiting...")
        break
    elif key == ord('s'):
        print("Saving attendance data...")
        if detection_counts:
            most_common_person = max(detection_counts, key=detection_counts.get)
            ts = time.time()
            mark_attendance(most_common_person, ts, authorized=(most_common_person != "Unauthorized"))
            print(f"Attendance marked for {most_common_person}.")

video.release()
cv2.destroyAllWindows()

if detection_counts:
    most_common_person = max(detection_counts, key=detection_counts.get)
    ts = time.time()
    mark_attendance(most_common_person, ts, authorized=(most_common_person != "Unauthorized"))
    print(f"Attendance marked for {most_common_person}.")
else:
    print("No faces detected in the 10 frames.")