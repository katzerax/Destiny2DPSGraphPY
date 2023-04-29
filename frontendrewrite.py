import tkinter as tk
import random
import os
import configparser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')
        with open(ini_path, 'r', encoding='utf-8') as f:
            self.config.read_file(f)
        self.interface_mode = self.config.get('Interface', 'Mode')
        self.cmd_prints = self.config.getboolean('Interface', 'CMDPrints')
        self.multi_weapon = self.config.getboolean('Interface', 'Multiweapon')
        self.calc_when_damage_dealt = self.config.get('Calculations', 'WhenDamageDealt')

    def set_interface_mode(self, mode):
        self.interface_mode = mode

    def set_cmd_prints(self, value):
        self.cmd_prints = value

    def set_multi_weapon(self, value):
        self.multi_weapon = value

    def set_calc_when_damage_dealt(self, value):
        self.calc_when_damage_dealt = value

    def save_settings(self):
        self.config.set('Interface', 'Mode', self.interface_mode)
        self.config.set('Interface', 'CMDPrints', str(self.cmd_prints))
        self.config.set('Interface', 'Multiweapon', str(self.multi_weapon))
        self.config.set('Calculations', 'WhenDamageDealt', self.calc_when_damage_dealt)

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

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

        if self.settings.cmd_prints == 'True':
            pass
        else:
            pass

        if self.settings.multi_weapon == 'True':
            pass
        else:
            pass

        if self.settings.calc_when_damage_dealt.lower() == 'whenattacking':
            pass
        else:
            pass

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
        # Print the state of the check box (True or False)
        print(self.var.get())

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