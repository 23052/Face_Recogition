from deepface import DeepFace
import mediapipe as mp
import cv2
from deepface import DeepFace
import time

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def recognize(path_to_img):
  dfs = DeepFace.find(img_path = path_to_img,
        db_path = "./img", 
        model_name = "GhostFaceNet"
  )
  return dfs

def check_for_person():
  cap = cv2.VideoCapture(0)

  try:
      with mp_holistic.Holistic(min_detection_confidence=0.85, min_tracking_confidence=0.5) as holistic:
      
          while cap.isOpened():
              
              ret, frame = cap.read()
              
              image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
              
              results = holistic.process(image)
              
              image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
              
              cv2.imshow('Face Detection', image)
              
              print(results.face_landmarks)
              
              if results.face_landmarks:
                  debut = time.time()
                  
                  while time.time()-debut <= 5 :
                      
                      if cv2.waitKey(1) & 0xFF == ord('q'):
                          break
                      
                      ret, frame = cap.read()
              
                      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                      results = holistic.process(image)

                      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                      
                      #draw rectangle on the detected face
                      if results.face_landmarks:
                          x1, y1 = (results.face_landmarks.landmark[234].x , results.face_landmarks.landmark[10].y)
                          x2, y2 = (results.face_landmarks.landmark[264].x , results.face_landmarks.landmark[152].y)
                          cv2.rectangle(image, (int(image.shape[1]*x1), int(image.shape[0]*y1)), (int(image.shape[1]*x2), int(image.shape[0]*y2)), (64, 245, 106), 2)
                      

                      
                      cv2.imshow('Face Detection', image)
                  
                  #-------------------------------------------------------- RECOGNIZE USER -----------------------------------------------------------------
                  img_path = "took.jpg"
                  cv2.imwrite(img_path, image)
                  result = recognize(img_path)
                  print(result)

                  #-----------------------------------------------------------------------------------------------------------------------------------------
              
              if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

      # Libérer la webcam et fermer toutes les fenêtres
      cap.release()
      cv2.destroyAllWindows()

  except :
      print(" ERREUR SURVENUE ")
      cap.release()
      cv2.destroyAllWindows()