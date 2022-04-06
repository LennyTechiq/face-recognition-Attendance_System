import sqlite3
import os
import cv2
import face_recognition
import numpy as np
import time

def attend():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
                
    conn.commit()
    conn.close()

    path = "ImagesAttendance"
    images = []
    classNames = []
    myList = os.listdir(path)

    for cl in myList:
        curImage = cv2.imread(f'{path}/{cl}')
        images.append(curImage)
        classNames.append(os.path.splitext(cl)[0])


    def findEncodingImg(images):
        encodeList=[]
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    known_face_encodings = findEncodingImg(images)
    #print("Images encoding complete..!")

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(known_face_encodings, encodeFace)
            faceDis = face_recognition.face_distance(known_face_encodings, encodeFace)
            matcheIndexes = np.argmin(faceDis)
            if(matches[matcheIndexes]):
                user_id = classNames[matcheIndexes]
                #print(user_id)

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, user_id, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(img, 'Press q to Exit', (10, 18), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("Lenny  Attendance", img)
        if(cv2.waitKey(1) & 0xFF== ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE employees SET state = 'Present' WHERE oid= " + user_id)
    conn.commit()
    conn.close()
