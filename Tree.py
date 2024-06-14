from tkinter import ttk
from Connector import MySQLConnector

class Tree:
    def __init__(self, window, db_connector):
        self.window = window
        self.db_connector = db_connector
        self.tree = None

    def populate_tree(self):
        self.tree = ttk.Treeview(self.window)
        self.tree.grid(column=0, row=0, sticky='nsew')

        vsb = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        vsb.grid(column=1, row=0, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree["columns"] = ("type", "null", "key", "default")
        self.tree.column("#0", width=150)
        self.tree.column("type", width=100)
        self.tree.column("key", width=100)
        self.tree.column("null", width=100)
        self.tree.column("default", width=100)

        self.tree.heading("#0", text="Table")
        self.tree.heading("type", text="Type")
        self.tree.heading("key", text="Key")
        self.tree.heading("null", text="Nullable")
        self.tree.heading("default", text="Default")

        databases = self.db_connector.get_databases()
        for database in databases:
            tables = self.db_connector.get_tables(database)
            db_node = self.tree.insert("", "end", text=database)
            for table in tables:
                table_node = self.tree.insert(db_node, "end", text=table)
                columns = self.db_connector.get_columns(database, table)
                for column in columns:
                    self.tree.insert(table_node, "end", text=column['Field'], values=(column['Type'], column['Null'], column['Key'], column['Default']))

        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        children = self.tree.get_children(item)
        if children:
            self.tree.delete(children)

            database = self.tree.item(item, "text")
            table = self.tree.item(item, "text")
            columns = self.db_connector.get_columns(database, table)
            for column in columns:
                self.tree.insert(item, "end", text=column['Field'], values=(column['Type'], column['Null'], column['Key'], column['Default']))

