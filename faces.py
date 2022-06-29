import datetime
import numpy as np
import cv2
import pickle
import pyrebase
from typing import Mapping
import time
# Initialize Firebase

firebaseConfig = {
    'apiKey': "AIzaSyD5JNwgNouvihlohxiGa8Bpg67pkmvkFK8",
    'authDomain': "mydbpbl5.firebaseapp.com",
    'databaseURL': "https://mydbpbl5-default-rtdb.firebaseio.com",
    'projectId': "mydbpbl5",
    'storageBucket': "mydbpbl5.appspot.com",
    'messagingSenderId': "779874823764",
    'appId': "1:779874823764:web:73a3033d24ed17902ac7c1",
    'measurementId': "G-E7XC29K07T"
}
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


face_cascade = cv2.CascadeClassifier(
    'src\cascades\data\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('src\cascades\data\haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(
    'src\cascades\data\haarcascade_smile.xml')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(r"src\recognizers\face-trainner.yml")


labels = {"person_name": 1}
with open(r"src\pickles\face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}
    # print(labels)
    cap = cv2.VideoCapture(0)
    name1 = ""
    name2 = ""
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in faces:
        	#print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w]  # (ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]
            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            print(id_)
            print(conf)
            if conf < 85:
                # print(5: #id_)
                # print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_] + " Hello"
                color = (255, 255, 255)
                stroke = 1
                cv2.putText(frame, name, (x, y), font, 1,color, stroke, cv2.LINE_AA)
                dt_string = datetime.datetime.now()
                db = firebase.database()

                timeIn = []
                timeIn = db.child("ClassSection").get().val()
                timeStart = 0
                timeEnd = 0
                for section in timeIn:
                    if(db.child("/ClassSection/"+str(section)+"/room").get().val()== "P.202"):
                        timeStart = int(db.child("/ClassSection/"+str(section)+"/lessonstart").get().val())+6
                        timeEnd = int(db.child("/ClassSection/"+str(section)+"/lessonend").get().val())+6
                    dt_string = datetime.datetime.now()
                    dt3 = dt_string + datetime.timedelta(hours = 3)
                    print(dt3)
                    dt_now = dt_string.strftime("%Y-%m-%d %H:%M")
                    week = 0
                    dt = datetime.datetime(2022, 6, 24)
                    dt1 = dt+datetime.timedelta(days = 7 * week) + datetime.timedelta(hours = 13) + datetime.timedelta(minutes =40)
                    dt2 = dt+datetime.timedelta(days = 7 * week) + datetime.timedelta(hours = 16) + datetime.timedelta(minutes =40)
                    print(str(dt2)+"ss")
                    if(dt_string < dt1+ datetime.timedelta(minutes = 15)):
                        if(dt_string > dt1 + datetime.timedelta(minutes = - 15)):
                            if (name1 != name):
                                name1 = name
                                data = {"time": dt_string.strftime("%Y-%m-%d %H:%M")}
                                db.child("DetailSection/C205/1/TimeIn/" +str(name1)+"/").update(data)
                                
                    if(dt3 < dt2 + datetime.timedelta(minutes = 15)):
                        if(dt3 > dt2 + datetime.timedelta(minutes = - 15)):
                            if (name2 != name):
                                name2 = name
                                data = {"time": dt_string.strftime("%Y-%m-%d %H:%M")}
                                db.child("DetailSection/C205/1/TimeOut/" +str(name1)+"/").update(data)
            time.sleep(0.1)
            color = (255, 0, 0)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x,
                        end_cord_y), color, stroke)
            #subitems = smile_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in subitems:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            # Display the resulting frame
        cv2.imshow('Window', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def check_time(time1, time2):
    if((time2-time1).seconds) > 10:
        return True
