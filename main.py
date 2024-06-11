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
    ttk.Label(frm, text="User: ").grid(column=0, row=0, sticky=E, pady=5)
    user_input = ttk.Entry(frm)
    user_input.grid(column=1, row=0, sticky=(W, E), pady=5)

    ttk.Label(frm, text="Password: ").grid(column=0, row=1, sticky=E, pady=5)
    pass_input = ttk.Entry(frm, show="*")
    pass_input.grid(column=1, row=1, sticky=(W, E), pady=5)

    db_type_var = StringVar()
    ttk.Label(frm, text="Select database: ").grid(column=0, row=2, sticky=E, pady=5)
    db_type_combo = ttk.Combobox(frm, textvariable=db_type_var, values=["MySQL", "PostgreSQL"])
    db_type_combo.grid(column=1, row=2, sticky=(W, E), pady=5)
    db_type_combo.current(0) 

    login_button = ttk.Button(frm, text="Login", command=lambda: login(user_input, pass_input, error_lbl))
    login_button.grid(column=1, row=3, sticky=(W), pady=5)

    error_lbl = Label(frm, text="", fg="red")
    error_lbl.grid(column=1, row=4, columnspan=2, sticky=(W), pady=5)

    window.mainloop()

def login(user_input, pass_input, error_lbl):
    user = user_input.get()
    password = pass_input.get()
    success = connectToSQL(user, password)
    if(success):
        print("successful login")
        error_lbl.config(text="")
    else:
        print("error")
        error_lbl.config(text="user and/or password incorrect")


if __name__ == "__main__":
    main()
