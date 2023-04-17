import tkinter as tk
from tkinter import ttk, filedialog
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calculations import *

class weapon:
    def __init__(self,name,fire_rate,reload_time,damage_per_shot,magazine_capacity,ammo_reserve,delay_first_shot):
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.magazine_capacity = magazine_capacity
        self.ammo_reserve = ammo_reserve
        self.delay_first_shot = delay_first_shot
    # Maybe we could do a def dps over time in the weapon class or sumn idk self.dps

# Graph Definitions
#def graphing_definitions():
    #ax.clear()
data_points = 45000
x_scale = 45
y_scale = 300000

fig, ax = plt.subplots()
ax.set_xlim(0, x_scale)
ax.set_ylim(0, y_scale)
ax.set_xlabel("Time (Seconds)")
ax.set_ylabel("Damage Per Second")

x_increments = x_scale / data_points
x = []
for i in range(data_points):
    x.append(round(i * x_increments, 5))
    #return x, x_increments, data_points, ax

# Plotting
def plot_dps(ax, x, dps, x_scale, y_scale):
    ax.clear()
    ax.set_xlim(0, x_scale)
    ax.set_ylim(0, y_scale)
    ax.set_xlabel("Time (Seconds)")
    ax.set_ylabel("Damage Per Second")
    ax.plot(x, dps)
    #ax.set_xlabel("Time (Seconds)")
    #ax.set_ylabel("Damage Per Second")
    canvas.draw()


# Callback functions for buttons
def add_weapon():
    weapon_name = weapon_name_entry.get()
    fire_rate = float(fire_rate_entry.get())
    reload_time = float(reload_time_entry.get())
    damage_per_shot = float(damage_per_shot_entry.get())
    magazine_capacity = int(magazine_capacity_entry.get())
    ammo_reserve = int(ammo_reserve_entry.get())
    delay_first_shot = int(delay_first_shot_var.get())
    perk1 = perk1_var.get()
    perk2 = perk2_var.get()
    buff1 = buff1_var.get()
    buff2 = buff2_var.get()
    buff3 = buff3_var.get()
    
    textweapon = weapon(weapon_name, fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, delay_first_shot)

    #since the class is called weapon, i didnt want to name it weapon and it was being weird about setting the object to weapon name? idk
    #lol = weapon(fire_rate,reload_time,damage_per_shot,magazine_capacity,ammo_reserve,delay_first_shot)

    #x, x_increments, data_points, ax = graphing_definitions()
    dps = calculate_dps(textweapon.fire_rate, textweapon.reload_time, textweapon.damage_per_shot, textweapon.magazine_capacity, textweapon.ammo_reserve, textweapon.delay_first_shot, x, x_increments, data_points)
    plot_dps(ax, x, dps, x_scale, y_scale)

def debug_print():
    print("lol")

def plot_graph():
    pass

def import_weapon():
    pass

def export_weapon():
    pass

def import_csv():
    pass

def export_csv():
    pass

# Function to load weapon presets from a JSON file
def load_weapon_presets():
    pass

# Function to save weapon presets to a JSON file
def save_weapon_presets():
    pass

# Function to export the calculated data to a CSV file
def export_to_csv():
    pass

# Function to import data from a CSV file and plot it
def import_csv_and_plot():
    pass

# Function to calculate and plot the DPS over time
def calculate_and_plot():
    pass
    

# Create the main application window
app = tk.Tk()
app.title("Weapon Damage Analysis")

# Configure the main window to be resizable
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Create the Matplotlib figure and axis
#fig, ax = plt.subplots(figsize=(6, 4))


# Create a canvas to display the Matplotlib figure in the Tkinter GUI
canvas = FigureCanvasTkAgg(fig, master=app)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

# Create the UI elements
frame = ttk.Frame(app)
frame.grid(row=0, column=1, padx=10, pady=10, sticky='n') # Sticks itself to the north section

# Configure the frame to be resizable
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(0, weight=1)

# Add input fields and labels
row_num = 0
weapon_name_label = ttk.Label(frame, text="Weapon Name")
weapon_name_label.grid(row=row_num, column=0, sticky='ew')
weapon_name_entry = ttk.Entry(frame)
weapon_name_entry.grid(row=row_num, column=1, sticky='ew')
row_num += 1

row_num += 1
fire_rate_label = ttk.Label(frame, text="Fire Rate")
fire_rate_label.grid(row=row_num, column=0)
fire_rate_entry = ttk.Entry(frame)
fire_rate_entry.grid(row=row_num, column=1)

row_num += 1
reload_time_label = ttk.Label(frame, text="Reload Time")
reload_time_label.grid(row=row_num, column=0)
reload_time_entry = ttk.Entry(frame)
reload_time_entry.grid(row=row_num, column=1)

row_num += 1
damage_per_shot_label = ttk.Label(frame, text="Damage per Shot")
damage_per_shot_label.grid(row=row_num, column=0)
damage_per_shot_entry = ttk.Entry(frame)
damage_per_shot_entry.grid(row=row_num, column=1)

row_num += 1
magazine_capacity_label = ttk.Label(frame, text="Magazine Capacity")
magazine_capacity_label.grid(row=row_num, column=0)
magazine_capacity_entry = ttk.Entry(frame)
magazine_capacity_entry.grid(row=row_num, column=1)

row_num += 1
ammo_reserve_label = ttk.Label(frame, text="Ammo Reserve")
ammo_reserve_label.grid(row=row_num, column=0)
ammo_reserve_entry = ttk.Entry(frame)
ammo_reserve_entry.grid(row=row_num, column=1)

row_num += 1
delay_first_shot_var = tk.BooleanVar()
delay_first_shot_checkbox = ttk.Checkbutton(frame, text="Delay First Shot", variable=delay_first_shot_var)
delay_first_shot_checkbox.grid(row=row_num, columnspan=2)

row_num += 1
perks_frame = ttk.LabelFrame(frame, text="Perks")
perks_frame.grid(row=row_num, columnspan=2)

perk1_var = tk.BooleanVar()
perk1_checkbox = ttk.Checkbutton(perks_frame, text="Perk 1", variable=perk1_var)
perk1_checkbox.grid(row=0, column=0)

perk2_var = tk.BooleanVar()
perk2_checkbox = ttk.Checkbutton(perks_frame, text="Perk 2", variable=perk2_var)
perk2_checkbox.grid(row=0, column=1)

#Buff Order as Follows:
#1 - Well of Radiance
#2 - 

row_num += 1
buffs_frame = ttk.LabelFrame(frame, text="Buffs")
buffs_frame.grid(row=row_num, columnspan=2)

buff1_var = tk.BooleanVar()
buff1_checkbox = ttk.Checkbutton(buffs_frame, text="Buff 1", variable=buff1_var)
buff1_checkbox.grid(row=0, column=0)

buff2_var = tk.BooleanVar()
buff2_checkbox = ttk.Checkbutton(buffs_frame, text="Buff 2", variable=buff2_var)
buff2_checkbox.grid(row=0, column=1)

buff3_var = tk.BooleanVar()
buff3_checkbox = ttk.Checkbutton(buffs_frame, text="Buff 3", variable=buff3_var)
buff3_checkbox.grid(row=0, column=2)

# ... add more buff checkboxes as needed


row_num += 1
add_weapon_btn = ttk.Button(frame, text="Add Weapon", command=add_weapon)
add_weapon_btn.grid(row=row_num, columnspan=2)

row_num += 1
plot_graph_btn = ttk.Button(frame, text="Calculate & Plot Graph", command=calculate_and_plot)
plot_graph_btn.grid(row=row_num, columnspan=2)

row_num += 1
import_weapon_btn = ttk.Button(frame, text="Import Weapon", command=import_weapon)
import_weapon_btn.grid(row=row_num, columnspan=2)

row_num += 1
export_weapon_btn = ttk.Button(frame, text="Export Weapon", command=export_weapon)
export_weapon_btn.grid(row=row_num, columnspan=2)

row_num += 1
import_csv_btn = ttk.Button(frame, text="Import CSV", command=import_csv)
import_csv_btn.grid(row=row_num, columnspan=2)

row_num += 1
export_csv_btn = ttk.Button(frame, text="Export CSV", command=export_csv)
export_csv_btn.grid(row=row_num, columnspan=2)

row_num += 1
export_csv_btn = ttk.Button(frame, text="debug", command=debug_print)
export_csv_btn.grid(row=row_num, columnspan=2)


app.mainloop()