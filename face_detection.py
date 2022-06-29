import cv2
from imutils.video import VideoStream
# from RPLCD import CharLCD
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = VideoStream(src=0).start()
# cap = cv2.VideoCapture(0)
# lcd = CharLCD(cols = 16, rows= 2, pin_rs=37, pin_e = 35, pin_data=[33,31,29,23])
# lcd.clear()
while True:
    count = 0
    frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        count += 1
    # print(len(faces))
    print(count)
    # lcd.write_string("Number of faces:")
    # lcd.cursor_pos = (1,0)
    # lcd.write_string(str(count))
    cv2.imshow("frame", frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# cap.release()
cap.stop()
cv2.destroyAllWindows()