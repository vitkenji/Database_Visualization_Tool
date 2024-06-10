from tkinter import *
from tkinter import ttk
import mysql.connector

def connectToSQL():
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="honeyhub"
    )

    print('teste')

    cursor = mydb.cursor()

    cursor.execute("show tables")

    respose = cursor.fetchall()
    
    print(respose)

    cursor.execute("select * from community")

    respose = cursor.fetchall()

    print(respose)
    
    print(mydb)

connectToSQL()

root = Tk()
frm = ttk.Frame(root, padding=10)

frm.grid()

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

root.mainloop()
