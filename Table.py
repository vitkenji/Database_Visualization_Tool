from tkinter import ttk

class Table:
    def __init__(self, window, data, column_names):
        self.window = window
        self.data = data
        self.column_names = column_names

    def create_table(self):
        height = len(self.data)
        width = len(self.data[0])

        # Create a frame for the table
        frame = ttk.Frame(self.window)
        frame.grid(row=1, column=0, sticky='nsew')

        # Create the Treeview widget
        tree = ttk.Treeview(frame, columns=[f'#{i}' for i in range(1, width+1)], show='headings')
        tree.grid(row=0, column=0, sticky='nsew')

        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=vsb.set)

        # Add a horizontal scrollbar
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        tree.configure(xscrollcommand=hsb.set)

        # Configure the frame to expand with window resizing
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Define the column headings
        for i, col_name in enumerate(self.column_names):
            tree.heading(f'#{i+1}', text=col_name)
            tree.column(f'#{i+1}', width=100, anchor='center')  # You might want to adjust the width

        # Insert the data into the table
        for row in self.data:
            tree.insert('', 'end', values=row)
