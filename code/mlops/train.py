from sklearn.neighbors import KNeighborsClassifier
import pickle
import numpy as np
import os

print("Loading data...")
try:
    # Charger les labels
    with open('data/names.pkl', 'rb') as w:
        LABELS = pickle.load(w)
    
    # Charger les données des visages
    with open('data/faces_data.pkl', 'rb') as f:
        FACES = pickle.load(f)
    
    print("Data loaded successfully.")
except FileNotFoundError:
    print("Error: Data files not found. Please run add_faces.py first.")
    exit()
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Vérifier la cohérence des données
if len(FACES) != len(LABELS):
    print("Error: Inconsistent data. Faces and labels must have the same length.")
    exit()

# Afficher les dimensions des données
print('Shape of Faces matrix --> ', FACES.shape)
print('Number of Labels --> ', len(LABELS))

# Vérifier que toutes les images ont la même taille
if FACES.shape[1] != 7500:  # 50x50x3 = 7500 pour des images en couleur
    print(f"Error: Expected 7500 features, but got {FACES.shape[1]}. Please check the data.")
    exit()

print("Training KNN model...")
try:
    # Entraîner le modèle KNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)
    print("Model trained successfully.")
except Exception as e:
    print(f"Error during training: {e}")
    exit()

# Sauvegarder le modèle
if not os.path.exists('data/models/'):
    os.makedirs('data/models/')

try:
    with open('data/models/knn_model.pkl', 'wb') as f:
        pickle.dump(knn, f)
    print("Model saved to data/models/knn_model.pkl.")
except Exception as e:
    print(f"Error saving model: {e}")
    exit()