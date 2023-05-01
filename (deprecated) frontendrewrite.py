import tkinter as tk
import random
import os
import configparser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from weaponclassrewrite import Weapon


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
            self.matplotlibbg = "#1E1E1E"
        else:
            self.check_button_style = {}
            self.button_style = {}
            self.matplotlibbg = "#FFFFFF"

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
        self.ax.set_facecolor(self.matplotlibbg)
        self.fig.set_facecolor(self.matplotlibbg)

        # Create a Frame to hold input boxes, labels, and checkboxes
        self.inputs_frame = tk.Frame(self, bg=self.button_style.get('bg', ''))
        self.inputs_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        #name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, burst_weapon, burst_bullets, swap_group, swap_time

        # Create input boxes with labels
        self.name_label = tk.Label(self.inputs_frame, text="Name", **self.button_style)
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(self.inputs_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.fire_rate_label = tk.Label(self.inputs_frame, text="Fire Rate", **self.button_style)
        self.fire_rate_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)  # Change row number to 1
        self.fire_rate_entry = tk.Entry(self.inputs_frame)
        self.fire_rate_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)  # Change row number to 1

        self.reload_time_label = tk.Label(self.inputs_frame, text="Reload Time", **self.button_style)
        self.reload_time_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.reload_time_entry = tk.Entry(self.inputs_frame)
        self.reload_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.damage_per_shot_label = tk.Label(self.inputs_frame, text="Damage per Shot", **self.button_style)
        self.damage_per_shot_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.damage_per_shot_entry = tk.Entry(self.inputs_frame)
        self.damage_per_shot_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self.mag_cap_label = tk.Label(self.inputs_frame, text="Magazine Capacity", **self.button_style)
        self.mag_cap_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.mag_cap_entry = tk.Entry(self.inputs_frame)
        self.mag_cap_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self.ammo_total_label = tk.Label(self.inputs_frame, text="Ammo Total", **self.button_style)
        self.ammo_total_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.ammo_total_entry = tk.Entry(self.inputs_frame)
        self.ammo_total_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)


        # Create checkboxes
        self.delay_first_shot_var = tk.BooleanVar()
        self.delay_first_shot_button = tk.Checkbutton(self.inputs_frame, text="Delay First Shot", variable=self.delay_first_shot_var, command=self.update_graph, **self.check_button_style)
        self.delay_first_shot_button.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        self.burst_weapon_var = tk.BooleanVar()
        self.burst_weapon_check_button = tk.Checkbutton(self.inputs_frame, text="Burst Weapon", variable=self.burst_weapon_var, command=self.update_graph, **self.check_button_style)
        self.burst_weapon_check_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # Create additional input boxes
        self.burst_bullets_label = tk.Label(self.inputs_frame, text="Burst Bullets", **self.button_style)
        self.burst_bullets_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.burst_bullets_entry = tk.Entry(self.inputs_frame)
        self.burst_bullets_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

        self.swap_group_label = tk.Label(self.inputs_frame, text="Swap Group", **self.button_style)
        self.swap_group_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.swap_group_entry = tk.Entry(self.inputs_frame)
        self.swap_group_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

        self.swap_time_label = tk.Label(self.inputs_frame, text="Swap Time", **self.button_style)
        self.swap_time_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.swap_time_entry = tk.Entry(self.inputs_frame)
        self.swap_time_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

        # Create perk and buff checkboxes
        self.triple_tap_var = tk.BooleanVar()
        self.triple_tap_button = tk.Checkbutton(self.inputs_frame, text="Triple Tap", variable=self.triple_tap_var, command=self.update_graph, **self.check_button_style)
        self.triple_tap_button.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)

        self.FTTC_var = tk.BooleanVar()
        self.FTTC_button = tk.Checkbutton(self.inputs_frame, text="FTTC", variable=self.FTTC_var, command=self.update_graph, **self.check_button_style)
        self.FTTC_button.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)

        # Create a button to create a Weapon object
        self.create_weapon_button = tk.Button(self.inputs_frame, text="Create Weapon", command=self.create_weapon, **self.button_style)
        self.create_weapon_button.grid(row=15, column=0, padx=5, pady=5, sticky=tk.W)

        # Add the Matplotlib canvas to the GUI using the pack method
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    def create_weapon(self):
        # Retrieve values from input boxes and checkboxes
        name = self.name_entry.get()
        fire_rate = float(self.fire_rate_entry.get())
        reload_time = float(self.reload_time_entry.get())
        damage_per_shot = float(self.damage_per_shot_entry.get())
        mag_cap = int(self.mag_cap_entry.get())
        ammo_total = int(self.ammo_total_entry.get())
        delay_first_shot = self.delay_first_shot_var.get()
        burst_weapon = self.burst_weapon_var.get()
        burst_bullets = int(self.burst_bullets_entry.get()) if burst_weapon else 1
        swap_group = int(self.swap_group_entry.get())
        swap_time = float(self.swap_time_entry.get())

        # Create the Weapon object using the retrieved values
        weapon = Weapon(name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, burst_weapon, burst_bullets, swap_group, swap_time)

        # Print the weapon details for debugging purposes
        print("Created weapon: ", weapon.__dict__)



    #def plot_data(self):
        # Generate some random data and plot it
    #    x = [1, 2, 3, 4, 5]
    #    y = [random.randint(1, 10) for i in range(5)]
    #    self.ax.clear()
    #    self.ax.plot(x, y)
    #    self.canvas.draw()

    def update_graph(self):
        print("burst:", self.burst_weapon_var.get())
        print("delay:", self.delay_first_shot_var.get())
        print("perk1:", self.triple_tap_var.get())
        print("perk2:", self.FTTC_var.get())

    #def randomize_graph(self):
        # Randomize the graph data and redraw the canvas
    #    x = [1, 2, 3, 4, 5]
    #    y = [random.randint(1, 10) for i in range(5)]
    #    self.ax.clear()
    #    self.ax.plot(x, y)
    #    self.canvas.draw()

root = tk.Tk()
app = GUI(master=root)
app.mainloop()