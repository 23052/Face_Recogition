from deepface import DeepFace
import mediapipe as mp
import cv2
import time

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Création d'une instance globale pour réutilisation
holistic_processor = mp_holistic.Holistic(min_detection_confidence=0.85, min_tracking_confidence=0.5)

def check_for_person(imPath):
    time.sleep(0.5)
    print("\n--- START ---\n")

    image = cv2.imread(imPath)
    if image is None:
        print("Error: Image not loaded.")
        return {"result": "Image not loaded"}

    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic_processor.process(image)

        print("---- RES -----\n")
        print(results)
        print("\n---------------")

        if results.face_landmarks:
            print("\n--- Detected ! ---\n")
            result = DeepFace.find(
                img_path=imPath,
                db_path="./img/db",
                model_name="GhostFaceNet",
                enforce_detection=False  # Permet de ne pas rejeter les images sans visage
            )

            final = []

            for df in result:
                img_paths = df["identity"].values.tolist()
                for img_path in img_paths:
                    print(img_path)
                    final.append(img_path[9:])
            print(final)
            return final
        else:
            return {"result": "No face detected !"}
    except Exception as e:
        print(f"Error processing the image: {e}")
        return {"result": f"Error: {str(e)}"}


# holistic_processor.close()  # à placer à la fin de l'app
