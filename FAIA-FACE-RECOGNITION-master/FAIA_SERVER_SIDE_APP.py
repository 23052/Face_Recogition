from modules import recognizer
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import json
import pandas as pd
from store import strore
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#CORS(app, resources={r"/api/*": {"origins": "http://exemple.com"}})

@app.route('/')
def home():
    return render_template('stream-index.html')

@app.route('/test')
def test():
    return render_template('test-detect.html')

@app.route('/stream', methods=['POST'])
def stream():
    frame = request.files['frame'].read()
    nparr = np.frombuffer(frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imwrite('./img/from_web/saved_from_web.png', img)

    print("\n---------- RECOGNIZER ----------")

    rep = recognizer.check_for_person('./img/from_web/saved_from_web.png')
    timing = {}
    if len(rep) == 1:
        try :
            

            rep = strore.db[str(rep[0])]

            timing["heure"] = str(datetime.datetime.now().time().hour)
            timing["minute"] = str(datetime.datetime.now().time().minute)
            timing["seconde"] = str(datetime.datetime.now().time().second)
            print(" --------------- ")
            print(rep)
            
            rep = [rep[0]]
            rep.append(timing) 

        except Exception as e:
            print(e)
            rep = "ERREUR"

    else:
        rep = "ERREUR DE RECONNAISSANCE VEUILLEZ VOUS POSITIONNER CORRECTEMENT"

    print(rep)
    rep_json = ""
    rep_json = json.dumps(rep)  # Convertir directement si ce n'est pas un DataFrame
    rep_json = jsonify(json.loads(rep_json))

    return rep_json, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
