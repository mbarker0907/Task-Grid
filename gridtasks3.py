import tkinter as tk

class TaskGridApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title('TaskGrid')
        self.geometry('700x700')
        self.grid_propagate(False)

        # Instantiate the TaskGrid class and add it to the TaskGridApp window
        self.task_grid = TaskGrid(self)
        self.task_grid.pack(expand=True, fill=tk.BOTH)




'''#------------------------------------------------#'''



# Set up the grid
class TaskGrid(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_grid()

    def create_grid(self):
        # Loop through rows and columns to create the grid
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
            for j in range(3):
                self.create_text_widget(i, j)

    def create_text_widget(self, row, column):
        text_widget = tk.Text(self, bg='#B06D4D', font=("Arial Bold", 18), borderwidth=6, relief=tk.SUNKEN,
                              width=10, height=5, wrap=tk.WORD)
        text_widget.tag_configure("center", justify='center')

        # Add an empty space to make the tag cover the entire text area
        text_widget.insert(tk.END, " ", "center")

        text_widget.tag_bind("center", "<Button-1>",
                             lambda event, text_widget=text_widget: self.change_color(event, text_widget))
        text_widget.bind("<Button-3>",
                         lambda event, text_widget=text_widget: self.show_text_widget_context_menu(event, text_widget))

        text_widget.config(state=tk.DISABLED)

        text_widget.grid(row=row, column=column, sticky="nsew")


'''#------------------------------------------------#'''

class TaskPopupMenu(tk.Menu):
    def __init__(self, parent, text_widget):
        super().__init__(parent, tearoff=0)
        self.text_widget = text_widget
        self.create_menu()

    def create_menu(self):
        # Add the "Add Task" option to the context menu
        self.add_command(label="Add Task", command=self.show_add_task_popup)

        # Add the "Clear Task" option to the context menu
        self.add_command(label="Clear Task", command=self.clear_text_widget)

    def show_add_task_popup(self):
        add_task_popup = AddTaskPopup(self, self.text_widget)
        add_task_popup.show()

    def clear_text_widget(self):
        # Enable the widget to edit the content
        self.text_widget.config(state=tk.NORMAL)

        # Clear the text widget
        self.text_widget.delete(1.0, tk.END)

        # Add an empty space to make the tag cover the entire text area
        self.text_widget.insert(tk.END, " ", "center")

        # Disable the widget to make it uneditable
        self.text_widget.config(state=tk.DISABLED)


'''#------------------------------------------------#'''

class AddTaskPopup(tk.Toplevel):
    def __init__(self, master, apply_callback):
        """
        Initialize the AddTaskPopup class.

        :param master: The parent window (TaskApp instance)
        :param apply_callback: Function to call when the "Apply" button is clicked, takes the task text as a parameter
        """
        super().__init__(master)

        self.master = master
        self.apply_callback = apply_callback

        self.configure(bg='#8CD496')

        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the AddTaskPopup.
        """
        # Create a label widget with the text "Add a Task" in big bold black letters
        title_label = tk.Label(self, text="Add a Task", font=("Arial Bold", 36), fg='black', bg='#8CD496')
        title_label.pack(pady=20)

        # Create a user input box with a white background color
        self.input_box = tk.Entry(self, bg='white')
        self.input_box.pack(pady=10)

        # Create a button with a medium size, a yellow background color, and the text "Apply"
        apply_button = tk.Button(self, text="Apply", font=("Arial Bold", 20), fg='black', bg='#EBC994', command=self.apply_task)
        apply_button.pack(pady=10)

        # Set the focus to the input box to allow the user to start typing right away
        self.input_box.focus()

    def apply_task(self):
        """
        Apply the task and close the popup.
        """
        task_text = self.input_box.get()
        self.apply_callback(task_text)
        self.destroy()


'''#------------------------------------------------#'''


if __name__ == '__main__':
    app = TaskGridApp()
    app.mainloop()







