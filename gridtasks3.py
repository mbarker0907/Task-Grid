import tkinter as tk
from tkinter import ttk

class DarkModeStyling:
    def __init__(self):
        self.bg_color = '#2e2e2e'
        self.fg_color = '#ffffff'
        self.btn_color = '#3c3c3c'

class TaskGrid(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="TaskGrid")
        self.label.pack()

    def toggle_dark_mode(self):
        self.master.dark_mode = not self.master.dark_mode
        self.style_widgets()

    def style_widgets(self):
        if self.master.dark_mode:
            styling = self.master.dark_mode_styling
            self.config(bg=styling.bg_color)
            self.label.config(bg=styling.bg_color, fg=styling.fg_color)
        else:
            self.config(bg=None)
            self.label.config(bg=None, fg=None)


class TaskGridApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title('TaskGrid')
        self.geometry('700x700')
        self.grid_propagate(False)

        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width / 2) - (700 / 2)
        y = (screen_height / 2) - (700 / 2)

        # Set the window's starting position
        self.geometry(f'+{int(x)}+{int(y)}')

        # Set up dark mode styling and state
        self.dark_mode_styling = DarkModeStyling()
        self.dark_mode = False


        # Configure ttk styles for dark mode
        self.style = ttk.Style()
        self.style.configure('DarkMode.TButton', background=self.dark_mode_styling.btn_color,
                             foreground=self.dark_mode_styling.fg_color)

        # Instantiate the TaskGrid class and add it to the TaskGridApp window
        self.task_grid = TaskGrid(self)
        self.task_grid.pack(expand=True, fill=tk.BOTH)

        # Set up the menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Create the "View" menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Add "Toggle Dark Mode" menu item to the "View" menu
        self.view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)


    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.task_grid.style_widgets()


'''#------------------------------------------------#'''



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

    def style_widgets(self):
        if self.master.dark_mode:
            styling = self.master.dark_mode_styling
            self.config(bg=styling.bg_color)
            self.label.config(bg=styling.bg_color, fg=styling.fg_color)
        else:
            self.config(bg='#297ac1')  # Set the original background color
            self.label.config(bg='#297ac1', fg='black')  # Set the original background and text colors

    def create_widgets(self):
        self.label = tk.Label(self, text="TaskGrid")
        self.label.pack()
        self.style_widgets()




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




'''#------------------------------------------------#'''

class AddTaskPopup(tk.Toplevel):
    def __init__(self, master, text_widget):
        """
        Initialize the AddTaskPopup class.

        :param master: The parent window (TaskApp instance)
        :param apply_callback: Function to call when the "Apply" button is clicked, takes the task text as a parameter
        """
        super().__init__(master)

        self.master = master
        self.text_widget = text_widget

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

        # Bind the "Enter" key to the apply_task method
        self.input_box.bind('<Return>', lambda event: self.apply_task())

    def apply_task(self):
        """
        Apply the task and close the popup.
        """
        # Get the task text from the input box
        task_text = self.input_box.get()

        # Enable the widget to edit the content
        self.text_widget.config(state=tk.NORMAL)

        # Clear the text widget
        self.text_widget.delete(1.0, tk.END)

        # Insert the task text into the text widget
        self.text_widget.insert(tk.END, task_text, "center")

        # Change the background color of the text widget to yellow
        self.text_widget.config(bg='#43E069')



        # Close the popup
        self.destroy()


'''#------------------------------------------------#'''


if __name__ == '__main__':
    app = TaskGridApp()
    app.mainloop()







