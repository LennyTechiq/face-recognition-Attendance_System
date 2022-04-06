from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

def query():
    #global root2
    root2 = Tk()
    root2.title("Lenny Techiq")
    root2.geometry("450x550+400+100")
    #root2.config(bg="pink")


    Title2 = Label(root2, text="Attendance List", font="times 16 bold")
    Title2.grid(row=1, column=0, padx=150, pady=30)

    #update_btn = Button(root2, text="Click to Update Attendance", command=edit)
    #update_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=60)

    def employee_info():

        if select_box.get()=="":
            messagebox.showerror("Error", "Please insert the ID of the Employee!!!")
        else:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            value = select_box.get()

            c.execute("SELECT *,oid FROM employees WHERE oid= " + value)
            records = c.fetchall()

            conn.commit()
            conn.close()

            select_box.delete(0, END)

            root3 = Toplevel()
            root3.title("Lenny Techiq")
            root3.geometry("450x550+400+100")

            print_records = ''
            for record in records:
                print_records +=  str(record[0]) + "\n" + str(record[1]) + "\n" + str(record[3])+ "\n" + str(record[4]) + str(record[5])

            photoPath = str(record[5]) + '.jpg'

            global r_img

            my_pic = Image.open(photoPath)
            resized = my_pic.resize((100, 100), Image.ANTIALIAS)
            r_img = ImageTk.PhotoImage(resized)
    
            label1 = Label(root3, text="Full Details", font="times 16 bold")
            label1.grid(row=0, column=0, columnspan=2, pady=60, padx=(35, 0))

            f_name_1 = Label(root3, text="First name:  ")
            f_name_1.grid(row=1, column=0, padx=70)

            f_name_2 = Label(root3, text=str(record[0]))
            f_name_2.grid(row=1, column=1)

            l_name_1 = Label(root3, text="Last name:  ")
            l_name_1.grid(row=2, column=0)

            l_name_2 = Label(root3, text=str(record[1]))
            l_name_2.grid(row=2, column=1)

            address_1 = Label(root3, text="Address:  ")
            address_1.grid(row=3, column=0)

            address_2 = Label(root3, text=str(record[2]))
            address_2.grid(row=3, column=1)

            city_1 = Label(root3, text="City:  ")
            city_1.grid(row=4, column=0)

            city_2 = Label(root3, text=str(record[3]))
            city_2.grid(row=4, column=1)

            image_1 = Label(root3, text="Photo:  ")
            image_1.grid(row=5, column=0)

            image_2 = Label(root3, image = r_img, height=300, width=225)
            image_2.grid(row=5, column=1)
            
            root3.mainloop()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT *,oid FROM employees")
    records = c.fetchall()
    #print(records)
    conn.commit()
    conn.close()

    print_records = ''
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + "\t" + str(record[4])+ "\t" + str(record[5]) + "\n"
    
    title = Label(root2, text="Name\t    State\t  ID", font="times 14 bold")
    title.grid(row=2, column=0)

    query_label = Label(root2, text=print_records, font="Times 12")
    query_label.grid(row=3, column=0)

    label = Label(root2, text="Select ID", font="Times 12")
    label.grid(row=4, column=0, pady=5)
    
    select_box = Entry(root2, width=35)
    select_box.grid(row=5, column=0, pady=5)

    button1 = Button(root2, text="More about Employee", font="Times 12", command=employee_info)
    button1.grid(row=6, column=0, ipadx=35, pady=10)

    button2 = Button(root2, text="Exit", font="Times 12", command=root2.destroy)
    button2.grid(row=7, column=0, ipadx=95, pady=30)

    root2.mainloop()