from tkinter import *
import cv2
import os
import face_recognition
from tkinter import messagebox
import sqlite3
import numpy as np
from attend import attend
from query import query

def login():
    path = "Admins"
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

    with open('staff.csv', 'r+')as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if user_id not in nameList:
            messagebox.showerror("Error", "Sorry, Permission Denied!!!")
        else:
            messagebox.showinfo("Information", "Permission Granted")

            login = Tk()
            login.title('Lenny Techiq')
            login.geometry("450x550+400+100")

            conn = sqlite3.connect('database.db')

            #c = conn.cursor()

            #c.execute("ALTER TABLE employees ADD state text")

            conn.commit()
            conn.close()


            def delete():
                if delete_box.get()=="":
                    messagebox.showerror("Error", "Please insert the ID of employee to delete!!!")
                else:
                    conn = sqlite3.connect('database.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM employees WHERE oid= " + delete_box.get())
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Information", "Employee deleted. Load the List")
                    delete_box.delete(0, END)

            def submit():
                if f_name.get()=="" or l_name.get()=="" or address.get()=="" or city.get()=="" or state.get()=="":
                    messagebox.showerror("Error","Please fill all the blank spaces!!!")
                else:
                    conn = sqlite3.connect('database.db')
                    c = conn.cursor()

                    #c.execute("ALTER TABLE employees ADD CONSTRAINT v_default DEFAULT N'Absent' FOR state")

                    c.execute("INSERT INTO employees VALUES (:f_name, :l_name, :address, :city, :state)",
                            {
                                'f_name': f_name.get(),
                                'l_name': l_name.get(),
                                'address': address.get(),
                                'city': city.get(),
                                'state': state.get(),
                                #'photo': photo.get()
                            })

                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Info", f_name.get() + " successfully added")

                    f_name.delete(0, END)
                    l_name.delete(0, END)
                    address.delete(0, END)
                    city.delete(0, END)
                    state.delete(0, END)

            def reset():
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute("UPDATE employees SET state = 'Absent'")
                messagebox.showinfo("Info","Attendance updated successfully")
                #print(records)
                conn.commit()
                conn.close()


            f_name = Entry(login, width=35)
            f_name.grid(row=1, column=1, padx=20, pady=(10, 0))
            l_name = Entry(login, width=35)
            l_name.grid(row=2, column=1)
            address = Entry(login, width=35)
            address.grid(row=3, column=1)
            city = Entry(login, width=35)
            city.grid(row=4, column=1)
            state = Entry(login, width=35)
            state.grid(row=5, column=1)
            delete_box = Entry(login, width=35)
            delete_box.grid(row=9, column=1, pady=35)
            #image = Button(login, text="Select Image", command=filedialogs)
            #image.grid(row=6, column=1, pady=30, ipadx=50)


            Title1 = Label(login, text="Employee Management", font="times 16 bold")
            Title1.grid(row=0,columnspan=2, column=0, pady=20, padx=(30, 0))
            f_name_label = Label(login, text="First Name")
            f_name_label.grid(row=1, column=0,columnspan=1, padx=30, pady=(10, 0))
            l_name_label = Label(login, text="Last Name")
            l_name_label.grid(row=2, column=0, columnspan=1)
            address_label = Label(login, text="Address")
            address_label.grid(row=3, column=0, columnspan=1)
            city_label = Label(login, text="City")
            city_label.grid(row=4, column=0)
            state_label = Label(login, text="State")
            state_label.grid(row=5, column=0)
            #photo_label = Label(login, text="Photo")
            #photo_label.grid(row=6, column=0)
            delete_box_label = Label(login, text="Select ID")
            delete_box_label.grid(row=9, column=0, pady=5)



            submit_btn = Button(login, text="Register", command=submit)
            submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=35, ipadx=160)

            query_btn = Button(login, text="Load List", command=query)
            query_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=35, ipadx=160)

            delete_btn = Button(login, text="Delete Record", command=delete)
            delete_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=35, ipadx=145)

            salary_btn = Button(login, text="Salary")
            salary_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=166)

            update_btn = Button(login, text="Update Attendance", command=attend)
            update_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=35, ipadx=130)

            reset_btn = Button(login, text="Reset Attendance", command=reset)
            reset_btn.grid(row=14, column=0, columnspan=2, pady=10, padx=35, ipadx=135)


            login.mainloop()