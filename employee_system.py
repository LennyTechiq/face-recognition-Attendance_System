from tkinter import *

from tkinter import messagebox
from csv import *
import sqlite3
from login import login

root1 = Tk()
root1.title("Lenny Techiq")
root1.geometry("450x550+400+100")
root1.config(bg="pink")

def sign_up():
    root1.destroy()
    root = Tk()
    root.title("Lenny Techiq")
    root.geometry("450x550+400+100")
    root.config(bg="pink")

    conn = sqlite3.connect('staff.db')

    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS staff (
            user_id integer,
            user_name text,
            gender text,
            phone integer,
            country text
            )""")

    main_list = []

    def sign_up_submit():
        with open('staff.csv', 'r+')as file:
            myDataList = file.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if user_id.get()=="" or user_name.get()=="" or gender.get()=="" or phone.get()=="" or country.get()=="":
                messagebox.showerror("Error", "Please fill all the blank spaces")
            elif user_id.get() not in nameList:
                lst = [user_id.get(), user_name.get(), gender.get(), phone.get(), country.get()]
                main_list.append(lst)


                Writer = writer(file)
                #Writer.writerow(["User_ID","Name", "Gender", "Phone", "Country"])
                Writer.writerows(main_list)
                messagebox.showinfo("Information", "Saved successfully!!")

                user_id.delete(0, END)
                user_name.delete(0, END)
                gender.delete(0, END)
                phone.delete(0, END)
                country.delete(0, END)
            else:
                messagebox.showerror("Error", "The user ID already exist!!!")

                user_id.delete(0, END)


    label1=Label(root, text="Techiq DigiCompany", font="times 18 bold", fg='red', bg="pink")
    label1.grid(row=3, column=0, columnspan=2, padx=100, pady=30)
    label2=Label(root, text="ADMIN", font="times 15 bold", bg="pink")
    label2.grid(row=4, column=0, columnspan=2, pady=20, padx=80)

    id_user = Label(root, text="User ID", font="Helvetica 12", bg="pink")
    id_user.grid(row=5, column=0, padx=1)
    name_user = Label(root, text="Name", font="Helvetica 12", bg="pink")
    name_user.grid(row=6, column=0, padx=1)
    gender_user = Label(root, text="Gender", font="Helvetica 12", bg="pink")
    gender_user.grid(row=7, column=0, padx=1)
    phone_user = Label(root, text="Phone", font="Helvetica 12", bg="pink")
    phone_user.grid(row=8, column=0, padx=1)
    country_user = Label(root, text="Country", font="Helvetica 12", bg="pink")
    country_user.grid(row=9, column=0, padx=1)

    user_id = Entry(root, width=30)
    user_id.grid(row=5, column=1)
    user_name = Entry(root, width=30)
    user_name.grid(row=6, column=1)
    gender = Entry(root, width=30)
    gender.grid(row=7, column=1)
    phone = Entry(root, width=30)
    phone.grid(row=8, column=1)
    country = Entry(root, width=30)
    country.grid(row=9, column=1)

    button1 = Button(root, text="Submit", font="times 12 bold", fg='white', bg='purple', command=sign_up_submit)
    button1.grid(row=10, column=0, ipadx=32, pady=(30,0), columnspan=2, padx=100)

    button2 = Button(root, text="Go to Login", font="times 12 bold", fg='white', bg='purple', command=login)
    button2.grid(row=11, column=0, ipadx=15, columnspan=2, pady=10, padx=170)

    root.mainloop()
            
login_label1=Label(root1, text="Techiq DigiCompany", font="times 18 bold", fg='red', bg="pink").grid(row=1, column=1, padx=120, pady=30)
login_label2=Label(root1, text="Note: Admin permission only!!!", font="times 15 italic", bg="pink").grid(row=2, column=1, pady=50)

login_button1 = Button(root1, text="Login", font="times 12 bold", fg='white', bg='purple', command=login)
login_button1.grid(row=3, column=1, ipadx=22, pady=10)

login_button2 = Button(root1, text="Sign Up", font="times 12 bold", fg='white', bg='purple', command=sign_up)
login_button2.grid(row=4, column=1, ipadx=15, pady=10)

login_button3 = Button(root1, text="Exit", font="times 12 bold", fg='white', bg='purple', command=root1.destroy)
login_button3.grid(row=5, column=1, ipadx=28, pady=100)

root1.mainloop()