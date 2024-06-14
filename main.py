from tkinter import *
from tkinter import ttk
from Connector import MySQLConnector
from Table import Table
from Tree import Tree

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
    db_type_combo = ttk.Combobox(frm, textvariable=db_type_var, values=["MySQL", "Postgres"])
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
        if user == "" or password == "":
            print("empty spaces")
            error_lbl.config(text="fill all blank spaces")
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
        view_db_window(schema)
    else:
        print("error")

def view_db_window(schema):
    db_window = Tk()
    db_window.title("Database Operations:")
    db_window.geometry('1500x800')

    frm_left = ttk.Frame(db_window, padding=20)
    frm_left.grid(row=0, column=0, sticky="nsew")

    ttk.Label(frm_left, text="Type query: ").grid(column=0, row=0, sticky=E, pady=5)
    query = ttk.Entry(frm_left, width=50)
    query.grid(column=1, row=0, sticky=(W, E), pady=5)

    execute_button = ttk.Button(frm_left, text="Execute", command=lambda: executeQuery(query.get(), db_window))
    execute_button.grid(column=2, row=0, sticky=(W), pady=5)

    result_frame = ttk.Frame(frm_left)
    result_frame.grid(column=0, row=1, columnspan=3, pady=10, sticky="nsew")

    frm_right = ttk.Frame(db_window, padding=20)
    frm_right.grid(row=0, column=1, sticky="nsew")

    tree_view = Tree(frm_right, db_connector)
    tree_view.populate_tree(schema)

    db_window.grid_columnconfigure(0, weight=1)
    db_window.grid_columnconfigure(1, weight=1)
    db_window.grid_rowconfigure(0, weight=1)

    db_window.mainloop()


def executeQuery(query, db_window):
    global db_connector
    result = db_connector.execute_query(query)
    if result:
        column_names = [desc[0] for desc in db_connector.cursor.description] 
        table = Table(db_window, result, column_names)
        table.create_table()
    else:
        print("error executing query")


if __name__ == "__main__":
    main()
