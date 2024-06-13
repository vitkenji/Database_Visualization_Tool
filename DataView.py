from tkinter import ttk

class DataView:
    def tableDataView(self, window, table):
        tree = ttk.Treeview(window)

        tree["columns"] = ("type", "null", "key", "default")

        tree.column("#0", width=150, minwidth=150)
        tree.column("type", width=100, minwidth=100)
        tree.column("key", width=100, minwidth=100)
        tree.column("nullable", width=100, minwidth=100)

        tree.heading("#0", text="name")
        tree.heading("type", text="type")
        tree.heading("key", text="key")
        tree.heading("nullable", text="null")

        for col in table.cols:
            tree.insert("", "end", text=col.name, values=(col.type, col.null, col.key, col.default))

        tree.grid(column=1, row=4, pady=20, padx=20)