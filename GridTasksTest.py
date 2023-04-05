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

# Set up the grid
class TaskGrid(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#297ac1')

        self.create_grid()

    def create_grid(self):
        # Loop through rows and columns to create the grid
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
            for j in range(3):
                self.create_text_widget(i, j)

    def create_text_widget(self, row, column):
        text_widget = tk.Text(self, bg='#ac3a11', fg='white', font=("Arial Bold", 26), borderwidth=6, relief=tk.SUNKEN,
                              width=10, height=5, wrap=tk.WORD)
        text_widget.tag_configure("center", justify='center', wrap='word', spacing1=50, spacing2=0, spacing3=50)

        # Add an empty space to make the tag cover the entire text area
        text_widget.insert(tk.END, " ", "center")

        text_widget.tag_bind("center", "<Button-1>",
                             lambda event, text_widget=text_widget: self.change_color(event, text_widget))
        text_widget.bind("<Button-3>",
                         lambda event, text_widget=text_widget: self.show_text_widget_context_menu(event, text_widget))

        # Bind the hover enter and leave events
        text_widget.bind("<Enter>", lambda event, text_widget=text_widget: self.hover_enter(event, text_widget))
        text_widget.bind("<Leave>", lambda event, text_widget=text_widget: self.hover_leave(event, text_widget))

        text_widget.config(state=tk.DISABLED)

        text_widget.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)

    def show_text_widget_context_menu(self, event, text_widget):
        """
        Show the context menu for the text widget.

        :param event: The event object containing information about the event that triggered the method
        :param text_widget: The text widget for which the context menu is being displayed
        """
        # Instantiate the TaskPopupMenu class
        task_popup_menu = TaskPopupMenu(self, text_widget)

        # Display the context menu at the cursor's position
        task_popup_menu.post(event.x_root, event.y_root)

    def hover_enter(self, event, text_widget):
        if not self.is_task_added(text_widget):
            text_widget.config(bg="#d45242")

    def hover_leave(self, event, text_widget):
        if not self.is_task_added(text_widget):
            text_widget.config(bg="#ac3a11")

    def is_task_added(self, text_widget):
        return text_widget.get(1.0, tk.END).strip() != ""


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
        add_task_popup = AddTaskPopup(self.master, self.text_widget)
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

class AddTaskPopup(tk.Toplevel):
    def __init__(self, master, text_widget):
        super().__init__(master)

        self.master = master
        self.text_widget = text_widget

        self.configure(bg='#8CD496')

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Add a Task", font=("Arial Bold", 36), fg='black', bg='#8CD496')
        title_label.pack(pady=20)

        self.input_box = tk.Entry(self, bg='white')
        self.input_box.pack(pady=10)

        apply_button = tk.Button(self, text="Apply", font=("Arial Bold", 20), fg='black', bg='#EBC994', command=self.apply_task)
        apply_button.pack(pady=10)

        self.input_box.focus()

        self.input_box.bind('<Return>', lambda event: self.apply_task())

        def apply_task(self):
            task_text = self.input_box.get()

            self.text_widget.config(state=tk.NORMAL)

            self.text_widget.delete(1.0, tk.END)

            self.text_widget.insert(tk.END, task_text, "center")

            self.text_widget.config(bg='#8CD496')

            self.destroy()

    if __name__ == '__main__':
        app = TaskGridApp()
        app.mainloop()

    def apply_task(self):
        pass





