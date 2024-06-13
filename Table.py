from tkinter import ttk

class Table:
    def __init__(self, window, data):
        self.window = window
        self.data = data

    def create_table(self):
        height = len(self.data)
        width = len(self.data[0])

        for i in range(height): # Rows
            for j in range(width): # Columns
                b = ttk.Entry(self.window)
                b.insert(0, self.data[i][j])
                b.grid(row=i, column=j)
                b.place(x=20 + j*100, y=80 + i*21)
