import tkinter as tk

class TaskGridApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title('TaskGrid')
        self.geometry('700x700')
        self.grid_propagate(False)

if __name__ == '__main__':
    app = TaskGridApp()
    app.mainloop()
