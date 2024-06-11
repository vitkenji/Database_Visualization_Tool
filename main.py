from tkinter import *
from tkinter import ttk
import mysql.connector

def main():
    createWindow()


def connectToSQL(user, password):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user= user,
            password = password,
            database="university"
        )

        cursor = mydb.cursor()

        cursor.execute("show tables")

        respose = cursor.fetchall()
        
        print(respose)

        cursor.execute("select * from department")

        respose = cursor.fetchall()

        print(respose)
        
        print(mydb)
        return True

    except mysql.connector.Error as err:
        print("error")
        return False
        

def createWindow():
    window = Tk()
    window.title("Databases:")
    window.geometry('400x300')

    frm = ttk.Frame(window, padding=20)
    frm.grid()
    ttk.Label(frm, text="User: ").grid(column=0, row=0, sticky=E)
    user_input = ttk.Entry(frm)
    user_input.grid(column=1, row=0, sticky=(W, E))

    ttk.Label(frm, text="Password: ").grid(column=0, row=1, sticky=E)
    pass_input = ttk.Entry(frm, show="*")
    pass_input.grid(column=1, row=1, sticky=(W, E))

    login_button = ttk.Button(frm, text="Login", command=lambda: login(user_input, pass_input))
    login_button.grid(column=1, row=2, sticky=(W))

    window.mainloop()

def login(user_input, pass_input):
    user = user_input.get()
    password = pass_input.get()
    success = connectToSQL(user, password)
    if(success):
        print("successful login")
    else:
        print("error")



if __name__ == "__main__":
    main()
