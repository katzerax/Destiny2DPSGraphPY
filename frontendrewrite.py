import tkinter as tk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from settingstest import *

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.load_settings()  # Call the load_settings method
        self.create_widgets()

    def load_settings(self):
        self.settings = Settings()  # Create an instance of the Settings class

        # Access and apply settings to the program
        if self.settings.interface_mode.lower() == 'dark':
            self.configure(bg='#1E1E1E')
            self.master.configure(bg='#1E1E1E')
            self.check_button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC', 'selectcolor': '#1E1E1E'}
            self.button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC'}
        else:
            self.check_button_style = {}
            self.button_style = {}


    def create_widgets(self):
        # Create a Matplotlib figure and canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_data()

        # Create a tkinter check button
        self.var = tk.BooleanVar()
        self.check_button = tk.Checkbutton(self, text="Check Box", variable=self.var, command=self.update_graph, **self.check_button_style)

        # Create a tkinter button to randomize the graph
        self.randomize_button = tk.Button(self, text="Randomize Graph", command=self.randomize_graph, **self.button_style)


        # Configure row and column weights for expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Add the Matplotlib canvas, check button, and randomize button to the GUI using the grid method
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)  # Use rowspan and sticky options
        self.check_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.randomize_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    def plot_data(self):
        # Generate some random data and plot it
        x = [1, 2, 3, 4, 5]
        y = [random.randint(1, 10) for i in range(5)]
        self.ax.clear()
        self.ax.plot(x, y)
        self.canvas.draw()

    def update_graph(self):
        # Update the graph based on the state of the check box
        if self.var.get():
            self.ax.set_xlabel("X Label")
            self.ax.set_ylabel("Y Label")
        else:
            self.ax.set_xlabel("")
            self.ax.set_ylabel("")
        self.canvas.draw()

    def randomize_graph(self):
        # Randomize the graph data and redraw the canvas
        x = [1, 2, 3, 4, 5]
        y = [random.randint(1, 10) for i in range(5)]
        self.ax.clear()
        self.ax.plot(x, y)
        self.canvas.draw()

root = tk.Tk()
app = GUI(master=root)
app.mainloop()