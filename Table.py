from tkinter import ttk

# TODO: texts that are to big get hidden

class Table:
    def __init__(self, window, data):
        self.window = window
        self.data = data

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
        for i in range(1, width+1):
            tree.heading(f'#{i}', text=f'Column {i}')
            tree.column(f'#{i}', width=width, anchor='center')

        # Insert the data into the table
        for row in self.data:
            tree.insert('', 'end', values=row)

        # for i in range(height): # Rows
        #     for j in range(width): # Columns
        #         b = ttk.Entry(self.window)
        #         b.insert(0, self.data[i][j])
        #         b.grid(row=i, column=j)
        #         b.place(x=20 + j*100, y=80 + i*21)
        #         b.config(state="readonly")
