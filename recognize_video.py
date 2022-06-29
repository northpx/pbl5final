# import libraries
from calendar import weekday
import datetime
import os
import cv2
import imutils
import time
import pickle
import numpy as np
from imutils.video import FPS
from imutils.video import VideoStream
import pyrebase
from typing import Mapping
from tkinter import *

#Initialize Firebase
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

firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()


# load serialized face detector
print("Loading Face Detector...")
protoPath = "face_detection_model/deploy.prototxt"
modelPath = "face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load serialized face embedding model
print("Loading Face Recognizer...")
embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open("output/recognizer", "rb").read())
le = pickle.loads(open("output/le.pickle", "rb").read())

# initialize the video stream, then allow the camera sensor to warm up
print("Starting Video Stream...")
# vs = VideoStream(src=0).start()
vs = cv2.VideoCapture(0)
time.sleep(2.0)

# start the FPS throughput estimator
fps = FPS().start()
nametemp = []
name1 = ""
name2 = ""


#Create your own key + paths with child
# data={"name":nametemp, "age":20, "address":["new york", "los angeles"]}
# db.child("Branch").child("Employee").child("male employees").child("John's info").set(data)
# loop over frames from the video file stream
weekDays = ("Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","Chủ Nhật")##
thisXMas    = datetime.date(2017,12,25)#
thisXMasDay = thisXMas.weekday()#
thisXMasDayAsString = weekDays[thisXMasDay]#
while True:
	# grab the frame from the threaded video stream
	ret, frame = vs.read()

	# resize the frame to have a width of 600 pixels (while maintaining the aspect ratio), and then grab the image dimensions
	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]

	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)

	# apply OpenCV's deep learning-based face detector to localize faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI
			face = frame[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]

			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

			# construct a blob for the face ROI, then pass the blob through our face embedding model to obtain the 128-d quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()

			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]

			# draw the bounding box of the face along with the associated probability
			text = "{}: {:.2f}%".format(name, proba * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
			
			# window = Tk()
			# window.title("Thong tin sinh vien")
			# lb1 = Label(window, text=name, font=("arial bold", 50))
			# window.geometry("300x300")
			
			dt_string = datetime.datetime.now()
			db = firebase.database()

			clsSec = []
			clsSec = db.child("ClassSection").get().val()
			timeStart = 0
			timeEnd = 0
			for section in	clsSec:
				# if(db.child("/ClassSection/"+str(section)+"/room").get().val()== "P.202"):
				# 	timeStart = int(db.child("/ClassSection/"+str(section)+"/lessonstart").get().val())+6
				# 	timeEnd = int(db.child("/ClassSection/"+str(section)+"/lessonend").get().val())+6
				
				Weekday = db.child("ClassSection/"+str(section)+"/dayofweek").get().val()
				idRoom = db.child("ClassSection/"+str(section)+"/room").get().val()
				if(idRoom == "C205"):
					# dt_string = datetime.datetime.now()
					# dt3 = dt_string + datetime.timedelta(hours = 0)
					# print(dt3)
					# dt_now = dt_string.strftime("%Y/%m/%d, %H:%M:%S")
					week = 0
					dt_now = datetime.datetime(2022, 6, 28)
					
					dtOut = dt_now + datetime.timedelta(hours = 3)
					
					weekdaynow = weekDays[dt_now.date().weekday()]
					if(weekdaynow == Weekday):
						
						dt_start = dt_now +datetime.timedelta(days = 7 * week) + datetime.timedelta(hours = 7) + datetime.timedelta(minutes =00)
						dt_end = dt_now+datetime.timedelta(days = 7 * week) + datetime.timedelta(hours = 10) + datetime.timedelta(minutes =00)
						print(str(dt_end)+"ss")
						if(dt_now < dt_start+ datetime.timedelta(hours = 24)):
							if(dt_now > dt_start + datetime.timedelta(hours = -24)):
								if (name1 != name):
									name1 = name
									data = {"time": dt_string.strftime("%Y/%m/%d, %H:%M:%S")}
									db.child("DetailSection/C205/"+str(section)+"/TimeIn/" +str(name1)+"/").update(data)
									
						if(dtOut < dt_end + datetime.timedelta(hours = 24)):
							if(dtOut > dt_end + datetime.timedelta(hours=-24)):
								if (name2 != name):
									name2 = name
									timeOut = dt_string + datetime.timedelta(hours = 3)
									data = {"time": timeOut.strftime("%Y/%m/%d, %H:%M:%S")}
									db.child("DetailSection/C205/"+str(section)+"/TimeOut/" +str(name1)+"/").update(data)
					

	# update the FPS counter
	fps.update()

	# show the output frame
	cv2.imshow("Frame", frame)
	# window.mainloop()
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		# window.destroy()
		break
	#Create your own key + paths with child
	# data={"name":name, "age":20, "address":["new york", "los angeles"]}
	# db.child("Branch").child("Employee").child("male employees").child("John's info").set(data)
	#Create your own key
	# dt_str = datetime.now().strftime("%d/%m/%Y %H:%M")
	# data={"age":20, "time":dt_str}
	# db.child(name).set(data)
# stop the timer and display FPS information
fps.stop()
print("Elasped time: {:.2f}".format(fps.elapsed()))
print("Approx. FPS: {:.2f}".format(fps.fps()))

# cleanup
vs.release()
cv2.destroyAllWindows()
# vs.stop()
