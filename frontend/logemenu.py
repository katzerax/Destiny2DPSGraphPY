import tkinter as tk

class LogMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.config(**self.master.frame_style)
        self.pack()
        self.navname = 'Log'

        self.init_menu()

    def init_menu(self):
        self.log_ui()
        self.pack_forget()

    def log_ui(self):
        # Define color variables
        background_color = self.master.matplotlib_bg
        text_color = self.master.white_text

        # Create a Text widget for displaying the console output
        self.log_text = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, bg=background_color, fg=text_color)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the Text widget
        self.scrollbar = tk.Scrollbar(self, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.log_text.config(yscrollcommand=self.scrollbar.set)