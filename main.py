from tkinter import *
from tkinter import ttk
from Connector import MySQLConnector

def main():
    create_login_window()

user_global = ""
password_global = ""
db_connector = None

def create_login_window():
    login_window = Tk()
    login_window.title("Databases:")
    login_window.geometry('400x300')

    frm = ttk.Frame(login_window, padding=20)
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

    error_lbl = Label(frm, text="", fg="red")
    error_lbl.grid(column=1, row=4, columnspan=2, sticky=(W), pady=5)

    login_button = ttk.Button(frm, text="Login", command=lambda: login(user_input, pass_input, error_lbl, login_window))
    login_button.grid(column=1, row=3, sticky=(W), pady=5)

    login_window.mainloop()

def login(user_input, pass_input, error_lbl, login_window):
    global user_global, password_global, db_connector
    user = user_input.get()
    password = pass_input.get()
    user_global = user
    password_global = password
    db_connector = MySQLConnector(user, password)
    success, schemas = db_connector.connect()
    if success:
        print("successful login")
        error_lbl.config(text="")
        login_window.destroy()
        select_schema_window(schemas)
    else:
        print("error")
        error_lbl.config(text="user and/or password incorrect")

def select_schema_window(schemas):
    schema_window = Tk()
    schema_window.title("Select Schema:")
    schema_window.geometry('400x300')

    frm = ttk.Frame(schema_window, padding=20)
    frm.grid()

    ttk.Label(frm, text="Select schema:").grid(column=0, row=0, columnspan=2, pady=5)
    db_var = StringVar()
    db_combo = ttk.Combobox(frm, textvariable=db_var, values=[db[0] for db in schemas])
    db_combo.grid(column=1, row=0, pady=5)
    db_combo.current(0)

    schema_button = ttk.Button(frm, text="Select", command=lambda: schema_selected(db_var.get(), schema_window))
    schema_button.grid(column=1, row=1, sticky=(W), pady=5)

    schema_window.mainloop()

def schema_selected(schema, db_window):
    success = db_connector.select_schema(schema)
    if success:
        print("schema selected")
        db_window.destroy()
        view_db_window()
    else:
        print("error")

def view_db_window():
    db_window = Tk()
    db_window.title("Database Operations:")
    db_window.geometry('400x300')

    frm = ttk.Frame(db_window, padding=20)
    frm.grid()

    ttk.Label(frm, text="Database operations").grid(column=0, row=0, columnspan=2, pady=5)
    create_table(db_window)
    db_window.mainloop()

def create_table(window):
    height = 3
    width = 5
    for i in range(height): # Rows
        for j in range(width): # Columns
            b = ttk.Entry(window, text="sample Text")
            b.grid(row=i+4, column=j+1)

if __name__ == "__main__":
    main()
