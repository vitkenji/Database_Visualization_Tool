from tkinter import *
from tkinter import ttk
from MySQLConnector import MySQLConnector
from PostgresConnector import PostgresConnector
from Table import Table
from Tree import Tree
from jsonFunctions import saveData, readData, removeFile


def main():
    create_login_window()

user_global = ""
password_global = ""
remeber_user_var = None
db_connector = None
jsonQuery = None
db_type_var = None

def create_login_window():
    global db_type_var 

    login_window = Tk()
    login_window.title("Databases:")
    login_window.geometry('500x400')

    frm = ttk.Frame(login_window, padding=20)
    frm.grid()
    
    ttk.Label(frm, text="User: ").grid(column=0, row=0, sticky=E, pady=5)
    user_input = ttk.Entry(frm)

    login_saved_data = readData("loginData.json")

    if login_saved_data:
        user_input.insert(0, login_saved_data)

    user_input.grid(column=1, row=0, sticky=(W, E), pady=5)

    ttk.Label(frm, text="Password: ").grid(column=0, row=1, sticky=E, pady=5)
    pass_input = ttk.Entry(frm, show="*")
    pass_input.grid(column=1, row=1, sticky=(W, E), pady=5)

    db_type_var = StringVar()
    ttk.Label(frm, text="Select database: ").grid(column=0, row=2, sticky=E, pady=5)
    db_type_combo = ttk.Combobox(frm, textvariable=db_type_var, values=["MySQL", "Postgres"])
    db_type_combo.grid(column=1, row=2, sticky=(W, E), pady=5)
    db_type_combo.current(0)


    global remeber_user_var
    remeber_user_var = IntVar()
    remeber_user_checkbox = ttk.Checkbutton(frm, text="Remember login data", variable=remeber_user_var)
    remeber_user_checkbox.grid(column=1, row=3)


    error_lbl = Label(frm, text="", fg="red")
    error_lbl.grid(column=1, row=5, columnspan=2, sticky=(W), pady=5)

    login_button = ttk.Button(frm, text="Login", command=lambda: login(user_input, pass_input, error_lbl, login_window))
    login_button.grid(column=1, row=4, sticky=(W), pady=5)

    login_window.mainloop()

def login(user_input, pass_input, error_lbl, login_window):
    global user_global, password_global, db_connector, db_type_var, remeber_user_var
    user = user_input.get()
    password = pass_input.get()
    db_type = db_type_var.get()
    user_global = user
    password_global = password

    if db_type == "MySQL":
        db_connector = MySQLConnector(user, password)
    else:
        db_connector = PostgresConnector(user, password)

    success, schemas = db_connector.connect()
    if success:
        print("successful login")

        if remeber_user_var.get():
            saveData(user_input.get(), "loginData.json")
        else:
            removeFile("loginData.json")

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
    schema_window.geometry('500x400')

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

    execute_button = ttk.Button(frm_left, text="Execute", command=lambda: executeQuery(query.get(), limit_entry.get(), db_window))
    execute_button.grid(column=2, row=0, sticky=(W), pady=5)

    ttk.Label(frm_left, text="Limit: ").grid(column=0, row=1, sticky=E, pady=5)
    limit_entry = ttk.Entry(frm_left, width=50)
    limit_entry.grid(column=1, row=1, sticky=(W, E), pady=5)

    result_frame = ttk.Frame(frm_left)
    result_frame.grid(column=0, row=2, columnspan=3, pady=10, sticky=(N))

    global jsonQuery
    save_query_data_button = ttk.Button(frm_left, text="Save Query Data", command=lambda: saveData(jsonQuery, 'queryData.json'))
    save_query_data_button.grid(row=2, column=0)

    frm_right = ttk.Frame(db_window, padding=20)
    frm_right.grid(row=0, column=1, sticky="nsew")

    tree_view = Tree(frm_right, db_connector)
    tree_view.populate_tree(schema)

    save_table_data_button = ttk.Button(frm_right, text="Save Table Data", command=lambda: saveData(tree_view.json, 'treeData.json'))
    save_table_data_button.grid(row=1, column=0)

    frm_bottom = ttk.Frame(db_window, padding=20, padx=10)
    frm_bottom.grid(row=0, column=2, sticky="nsew")

    table = Table(frm_bottom, [], [])  
    table.create_table()

    db_window.grid_columnconfigure(0, weight=1)
    db_window.grid_columnconfigure(1, weight=1)
    db_window.grid_columnconfigure(2, weight=1)
    db_window.grid_rowconfigure(0, weight=1)

    db_window.mainloop()



def executeQuery(query, limit, db_window):
    global db_connector
    global jsonQuery

    if query.split()[0] == 'select':
        print(query)
        if query[-1] == ';':
            query = query[:-1] # Remove last character

        try: 
            limit = int(limit)
        except:
            limit = None

        if isinstance(limit, int) and limit > 0:
            query = query + ' limit ' + str(limit) + ';'
        else:
            query = query + ' limit 1000;'

    db_connector.execute_query(query)

    result = db_connector.execute_query(query)

    if result:
        column_names = [desc[0] for desc in db_connector.cursor.description] 
        
        jsonQuery = [dict(zip(column_names, row)) for row in result]

        table = Table(db_window, result, column_names)
        table.create_table()
    else:
        print("error executing query")


if __name__ == "__main__":
    main()
