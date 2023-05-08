import sys
import os
import configparser
import pickle
import json
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfilename
from pprint import pprint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import backend as backend

# TODO
# 1. Default ini
# 2. Make graph menu functional // 50% done
# 3. Look into on-hover tooltips

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')
        self.check_and_create_settings_file(ini_path)
        with open(ini_path, 'r', encoding='utf-8') as f:
            self.config.read_file(f)
            self.config.read_file(f)
        self.interface_theme = self.config.get('Interface', 'theme')
        self.log_mode = self.config.get('Interface', 'log_mode')
        self.do_dmg_prints = self.config.getboolean('Interface', 'dmg_steps')
        self.do_auto_save = self.config.getboolean('AutoSave', 'enabled')
        self.auto_save_path = self.config.get('AutoSave', 'path')
        self.graph_title = self.config.get('Graph', 'title')
        self.graph_xlabel = self.config.get('Graph', 'xlabel')
        self.graph_xlim = self.config.getint('Graph', 'xlim')
        self.graph_ylabel = self.config.get('Graph', 'ylabel')
        self.graph_ylim = self.config.getint('Graph', 'ylim')

    def check_and_create_settings_file(self, ini_path): # You guys may want to take a look at this
        if not os.path.exists(ini_path):
            default_settings = {
                'Interface': {
                    'theme': 'Light',
                    'log_mode': 'App',
                    'dmg_steps': 'True'
                },
                'AutoSave': {
                    'enabled': 'False',
                    'path': ''
                },
                'Graph': {
                    'title': 'DPS Over Time',
                    'xlabel': 'Time (seconds)',
                    'xlim': '45',
                    'ylabel': 'DPS',
                    'ylim': '300000'
                }
            }

            for section, settings in default_settings.items():
                self.config.add_section(section)
                for key, value in settings.items():
                    self.config.set(section, key, value)

            with open(ini_path, 'w', encoding='utf-8') as f:
                self.config.write(f)

    def set_interface_theme(self, theme):
        self.interface_theme = theme

    def set_log_mode(self, value):
        self.log_mode = value

    def set_do_dmg_prints(self, value):
        self.do_dmg_prints = value

    def set_do_auto_save(self, value):
        self.do_auto_save = value

    def set_auto_save_path(self, value):
        self.auto_save_path = value

    def set_graph_title(self, value):
        self.graph_title = value

    def set_graph_xlabel(self, value):
        self.graph_xlabel = value

    def set_graph_xlim(self, value):
        self.graph_xlim = value

    def set_graph_ylabel(self, value):
        self.graph_ylabel = value

    def set_graph_ylim(self, value):
        self.graph_ylim = value

    def save_settings(self):
        self.config.set('Interface', 'theme', self.interface_theme)
        self.config.set('Interface', 'log_mode', self.log_mode)
        self.config.set('Interface', 'dmg_prints', str(self.do_dmg_prints))
        self.config.set('AutoSave', 'enabled', str(self.do_auto_save))
        self.config.set('AutoSave', 'path', self.auto_save_path)
        self.config.set('Graph', 'title', self.graph_title)
        self.config.set('Graph', 'xlabel', self.graph_xlabel)
        self.config.set('Graph', 'xlim', str(self.graph_xlim))
        self.config.set('Graph', 'ylabel', self.graph_ylabel)
        self.config.set('Graph', 'ylim', str(self.graph_ylim))

        with open('settings.ini', 'w') as f:
            self.config.write(f)
            f.close()

    def reset_settings(self):
        pass

    def restart_gui(self, root):
        # Close the tkinter window
        root.destroy()
        # Restart gui
        global_start_gui()

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Destiny2DPSGraphPY')
        self.master.resizable(False, False)
        self.pack()
        self.initGUI()

    def load_settings(self):
        # Instance settings
        self.settings = Settings()

        self.default_padding = {'padx': 5, 'pady': 5, 'sticky': tk.W}
        self.combo_style = {'width': 17, 'state': 'readonly'}
        # Access and apply settings
        if self.settings.interface_theme.lower() == 'dark':
            self.configure(bg='#1E1E1E')
            self.master.configure(bg='#1E1E1E', highlightthickness=2, highlightcolor='#000000')
            self.label_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC'}
            self.frame_style = {'bg': '#1E1E1E', 'highlightcolor': '#000000', 'highlightbackground': '#000000', 'highlightthickness': 2}
            self.frame_bg = "#1E1E1E"
            self.check_button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC', 'selectcolor': '#1E1E1E'}
            self.button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC', 'height': 1, 'width': 17}
            self.matplotlib_bg = "#1E1E1E"
            self.matplotlib_fg = "#CCCCCC"
            self.listbox_bg = "#808080"
            self.white_text = "#CCCCCC"
            self.navbar_bg = '#1E1E1E'
            self.navbar_fg = '#CCCCCC'
        else:
            # TODO Light mode should always be checked after changes to the ui
            self.configure(bg='#FFFFFF')
            self.master.configure(bg='#FFFFFF', highlightthickness=2, highlightcolor='#000000')
            self.label_style = {'bg': '#FFFFFF', 'fg': '#000000'}
            self.frame_style = {'bg': '#FFFFFF', 'highlightcolor': '#000000', 'highlightbackground': '#FFFFFF', 'highlightthickness': 2}
            self.frame_bg = "#FFFFFF"
            self.check_button_style = {}
            self.button_style = {}
            self.matplotlib_bg = "#FFFFFF"
            self.matplotlib_fg = "#000000"
            self.listbox_bg = "#808080"
            self.white_text = "#000000"
            self.navbar_bg = '#FFFFFF'
            self.navbar_fg = '#000000'

        self.navbar_style = {
            'bg': self.navbar_bg, 
            'fg': self.navbar_fg,
            'height': 5,
            'highlightthickness': 0,
            'borderwidth': 0,
            'highlightcolor': '#000000', #
            'selectbackground': self.listbox_bg, #808080
            'selectforeground': '#FFFFFF',
            'selectborderwidth': 0,
            'activestyle': 'none',
            'font': 20,
            'width': 10,
            'exportselection': False
        }

        backend.set_do_dmg_prints(self.settings.do_dmg_prints)

    def initGUI(self):
        self.load_settings()
        self.navbar()
        self.graph_menu()
        self.weapons_menu()
        self.options_menu()
        self.log_menu()

        redirect_logs(self.log_text, self.settings.log_mode)
        if self.settings.do_auto_save:
            self.options_import_weps_handler(self.settings.auto_save_path)

    def navbar(self):
        # Root frame
        self.nav_frame = tk.Frame(self, **self.frame_style)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create navbar and load options
        self.nav_listbox = tk.Listbox(self.nav_frame, **self.navbar_style)
        self.nav_listbox.pack()
        self.nav_listbox.insert(1, 'Graph')
        self.nav_listbox.insert(2, 'Weapons')
        self.nav_listbox.insert(3, 'Options')
        self.nav_listbox.insert(4, 'Log')

        # Set default selection to 'Graph'
        self.nav_listbox.select_set(0)
        # Handle clicks on the navbar
        self.nav_listbox.bind('<<ListboxSelect>>', self.navbar_toggle_menus)

    def navbar_toggle_menus(self, evt):
        # Grab which option was clicked
        index = int(evt.widget.curselection()[0])
        match index:
            case 0:
                target = self.graph_frame
            case 1:
                target = self.weapons_frame
            case 2:
                target = self.options_frame
            case 3:
                target = self.log_frame

        # Return if the clicked option is already being displayed
        if target.winfo_ismapped():
            return

        # Hardcoded? list of selectable menus
        # Hide all menus but the one selected, then show the selected menu
        menus = [
            self.graph_frame,
            self.weapons_frame,
            self.options_frame,
            self.log_frame,
        ]
        menus.remove(target)
        for menu in menus:
            menu.pack_forget()
        target.pack(side=tk.RIGHT, fill=tk.Y)

    def graph_menu(self):
        # Root frame
        self.graph_frame = tk.Frame(self, **self.frame_style)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Wep select frame
        self.graph_wep_frame = tk.Frame(self.graph_frame, bg=self.frame_bg)
        self.graph_wep_frame.pack(side=tk.LEFT, fill=tk.Y)

        # No. of weps
        wep_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.graph_wep_select_label = tk.Label(self.graph_wep_frame, text='Number of Weapons', **self.label_style)
        self.graph_wep_select_label.grid(row=0, column=0, **self.default_padding)
        self.graph_wep_select_combo = ttk.Combobox(self.graph_wep_frame, values=wep_count, width=3, state='readonly')
        self.graph_wep_select_combo.grid(row=0, column=1, **self.default_padding)
        self.graph_wep_select_combo.set(wep_count[0]) # Changed it to one wep by default
        self.graph_wep_select_combo.bind("<<ComboboxSelected>>", self.graph_numweapons)

        # Extract weapon names from the dictionary
        existing_weapons = list(backend.weapons_list.keys())

        # Build weapon select widgets
        self.graph_wep_widgets = [
                ( tk.Label(self.graph_wep_frame, text=f'Weapon {i+1}', **self.label_style),
                ttk.Combobox(self.graph_wep_frame, values=existing_weapons, **self.combo_style)
                ) for i in range(10)
            ]
        # Grid placement
        for idx, multi in enumerate(self.graph_wep_widgets):
            label, combo = multi
            label.grid(row=(idx+1), column=0, **self.default_padding)
            combo.grid(row=(idx+1), column=1, **self.default_padding)
            combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
            # Display only 3 by default - no more - K
            if idx > 0: # Changed it to one by default
                label.grid_forget()
                combo.grid_forget()

        # Generate graph button
        self.graph_generate_button = tk.Button(self.graph_wep_frame, text="Generate Graph",
                                                command=self.graph_generate_graph, **self.button_style)
        self.graph_generate_button.grid(row=15, column=0, padx=8, pady=5, sticky=tk.W)

        # Save graph button
        self.graph_save_button = tk.Button(self.graph_wep_frame, text="Save Graph", 
                                           command=self.graph_save_graph, **self.button_style)
        self.graph_save_button.grid(row=15, column=1, padx=8, pady=5, sticky=tk.W)

        mpl.rcParams['text.color'] = self.matplotlib_fg
        mpl.rcParams['axes.edgecolor'] = self.matplotlib_fg
        mpl.rcParams['xtick.color'] = self.matplotlib_fg
        mpl.rcParams['ytick.color'] = self.matplotlib_fg
        mpl.rcParams['axes.labelcolor'] = self.matplotlib_fg

        # Create a Matplotlib figure and canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.ax.set_facecolor(self.matplotlib_bg)
        self.fig.set_facecolor(self.matplotlib_bg)

        # Set axis and labels
        self.ax.set_title(self.settings.graph_title)
        self.ax.set_xlabel(self.settings.graph_xlabel)
        self.ax.set_ylabel(self.settings.graph_ylabel, labelpad=-340, rotation='horizontal')
        self.ax.set_xlim(0, self.settings.graph_xlim)
        self.ax.set_ylim(0, self.settings.graph_ylim)

        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

    def graph_generate_graph(self):
        # Clear previous plot
        self.ax.clear()
        
        # Loop through weapon dropdowns
        for (_, dropdown) in self.graph_wep_widgets:
            # Check if dropdown is visible
            if not dropdown.winfo_viewable():
                continue

            # Get selected weapon
            selected_weapon = dropdown.get()

            # Check if weapon is selected
            if not selected_weapon:
                continue

            # Get weapon object
            weapon = backend.weapons_list[selected_weapon]

            # Get damage values by calling the Damage class with the weapon object
            damage = backend.Damage(weapon)
            dps = damage.DamageCalculate()
            # del damage.x[-1]

            # Plot the weapon damage
            self.ax.plot(damage.x, dps, label=f'{selected_weapon}')

        # Set the axis labels and title
        self.ax.set_xlabel(self.settings.graph_xlabel)
        self.ax.set_xlim(0, self.settings.graph_xlim)
        self.ax.set_ylabel(self.settings.graph_ylabel)
        self.ax.set_ylim(0, self.settings.graph_ylim)
        self.ax.set_title(self.settings.graph_title)

        # Add legend and re-draw
        self.ax.legend(facecolor=self.navbar_bg)
        self.canvas.draw()

    def graph_save_graph(self):
        file_path = asksaveasfile(defaultextension='.png', filetypes=[('All Files', '*.*')], initialdir='./', initialfile='dps_graph.png')
        if file_path is None:
            return
        self.fig.savefig(file_path.name)
        print(f'Saved graph as "{file_path.name}"')

    def graph_update_weapons(self):
        wep_names = list(backend.weapons_list.keys())
        for (_, dropdown) in self.graph_wep_widgets:
            dropdown.config(values=wep_names)

    def graph_numweapons(self, evt):
        # Get ammount of weps requested
        ammount = int(self.graph_wep_select_combo.get()) - 1

        # Redraw combos based on ammount
        for idx, tuple in enumerate(self.graph_wep_widgets):
            label, combo = tuple
            if idx <= ammount:
                label.grid(row=(idx+1), column=0, **self.default_padding)
                combo.grid(row=(idx+1), column=1, **self.default_padding)
            else:
                label.grid_forget()
                combo.grid_forget()
        # Focus the frame, not the combo
        self.graph_frame.focus()

    def weapons_menu(self):
        # Root frame
        workingframe = self.weapons_frame = tk.Frame(self, **self.frame_style)
        self.weapons_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Combobox options
        type_options = ['Single Weapon', 'Weapon Swap']
        perk_choices = [value[0] for value in backend.PERKS_LIST.values()]

        # Input validation
        val_int = self.register(self.util_valint)
        val_float = self.register(self.util_valfloat)

        # Widget vars
        self.weapons_menu_vars = {
            'enhance1': tk.BooleanVar(),
            'enhance2': tk.BooleanVar(),
            'burst_wep': tk.BooleanVar(),
            'fusion_wep': tk.BooleanVar()
        }

        # Widgets
        self.weapons_menu_widgets = {
            'header': tk.Label(self.weapons_frame, text="Weapon Creation", **self.label_style),
            'type': (tk.Label(workingframe, text="Type", **self.label_style),
                    ttk.Combobox(workingframe, values=type_options, width=17, state='disabled')),
            'name': (tk.Label(workingframe, text="Name", **self.label_style),
                    tk.Entry(workingframe)),
            'fire_rate': (tk.Label(workingframe, text="Fire Rate", **self.label_style),
                          tk.Entry(workingframe, validate='key', validatecommand=(val_float, '%S'))),
            'reload_time': (tk.Label(workingframe, text="Reload Time", **self.label_style),
                            tk.Entry(workingframe, validate='key', validatecommand=(val_float, '%S'))),
            'damage_per_shot': (tk.Label(workingframe, text="Damage per Shot", **self.label_style),
                                tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'mag_size': (tk.Label(workingframe, text="Magazine Capacity", **self.label_style),
                         tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'reserve_ammo': (tk.Label(workingframe, text="Ammo Total", **self.label_style),
                             tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'perk1': (tk.Label(workingframe, text="Perk 1", **self.label_style),
                      ttk.Combobox(workingframe, values=perk_choices, **self.combo_style)),
            'perk2': (tk.Label(workingframe, text="Perk 2", **self.label_style),
                      ttk.Combobox(workingframe, values=perk_choices, **self.combo_style)),
            'enhance_toggle': (tk.Checkbutton(workingframe, text="Perk 1 Enhanced", 
                                              variable=self.weapons_menu_vars['enhance1'], **self.check_button_style),
                               tk.Checkbutton(workingframe, text="Perk 2 Enhanced", 
                                              variable=self.weapons_menu_vars['enhance2'], **self.check_button_style)),
            'burst_fusion_toggle': (tk.Checkbutton(workingframe, text="Burst Weapon", 
                                                   variable=self.weapons_menu_vars['burst_wep'],
                                                    command=self.weapons_toggle_burst, **self.check_button_style),
                                    tk.Checkbutton(workingframe, text="Fusion Weapon", 
                                                   variable=self.weapons_menu_vars['fusion_wep'], **self.check_button_style)),
            'burst_bullets': (tk.Label(workingframe, text="Bullets Per Burst", **self.label_style),
                              tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'create_wep': tk.Button(workingframe, text="Create Weapon", command=self.weapons_create_weapon_handler, **self.button_style)
        }

        # Default combobox vals
        self.weapons_menu_widgets['type'][1].set(type_options[0])
        self.weapons_menu_widgets['perk1'][1].set(perk_choices[0])
        self.weapons_menu_widgets['perk2'][1].set(perk_choices[0])

        # Grid placement
        for idx, keyval in enumerate(self.weapons_menu_widgets.copy().items()):
            key, multi = keyval
            # Just place single objects in (x, 0)
            if not type(multi) is tuple:
                multi.grid(row=(idx+1), column=0, **self.default_padding)
                # Save grid column into tuple
                self.weapons_menu_widgets[key] = (multi, idx+1)
                continue
            # Place tuples in (x, 0) (x, 1)
            label, usrinput = multi
            label.grid(row=(idx+1), column=0, **self.default_padding)
            usrinput.grid(row=(idx + 1), column=1, **self.default_padding)
            self.weapons_menu_widgets[key] = (label, usrinput, idx+1)
            # Bind defocus to combos
            if isinstance(usrinput, ttk.Combobox):
                usrinput.bind("<<ComboboxSelected>>",lambda e: self.weapons_frame.focus())

        # Hide on start
        self.weapons_menu_widgets['burst_bullets'][0].grid_forget()
        self.weapons_menu_widgets['burst_bullets'][1].grid_forget()
        self.weapons_frame.pack_forget()

    def weapons_menu_ext(self):
        # Root frame
        self.weapons_list_frame = tk.Frame(self, **self.frame_style)
        self.weapons_list_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # self.wep_type_label = tk.Label(self.weapons_frame, text="Type", **self.button_style)
        # self.wep_type_label.grid(row=0, column=0, **self.default_padding)

    def weapons_toggle_burst(self):
        label, entry, gridpos = self.weapons_menu_widgets['burst_bullets']
        if label.winfo_ismapped():
            label.grid_forget()
            entry.grid_forget()
        else:
            label.grid(row=gridpos, column=0, **self.default_padding)
            entry.grid(row=gridpos, column=1, **self.default_padding)

    def weapons_create_weapon_handler(self):
        exitcode = self.weapons_create_weapon()
        basestr = f'Weapon creation exited with code {exitcode}:'
        match exitcode:
            case 0:
                # NOTE Having a popup for a success is kinda aids ill work on something else
                messagebox.showinfo('Success', 'Weapon created successfully')
                print(f'{basestr} Success')
            case 1:
                messagebox.showerror('Name Error', 'Make sure the name for your weapon contains at least one letter')
                print(f'{basestr} Name Error')
            case 2:
                messagebox.showerror('Float Error', 'Make sure Fire Rate and Reload Time are valid numbers')
                print(f'{basestr} Floating Point Error')
            case 3:
                messagebox.showerror('Integer Error', 'Make sure Damage per Shot, Mag Size, and Ammo Total are valid numbers')
                print(f'{basestr} Integer Error')
            case _:
                messagebox.showerror('Creation Error', 'There was an error creating your weapon')
                print(f'{basestr} Unknown Error')
        
    def weapons_create_weapon(self):
        # Name validation
        name = self.weapons_menu_widgets['name'][1].get()
        if type(name) is str:
            if len(name) < 1:
                return 1
        else:
            return 1
        
        # Float validation
        def test_float(num):
            try:
                clean = float(num)
                if clean > 0:
                    return True
                else:
                    return False
            except ValueError:
                return False

        fire_rate = self.weapons_menu_widgets['fire_rate'][1].get()
        reload_time = self.weapons_menu_widgets['reload_time'][1].get()
        for x in [fire_rate, reload_time]:
            if not test_float(x):
                return 2

        # Integer validation
        damage_per_shot = self.weapons_menu_widgets['damage_per_shot'][1].get()
        mag_size = self.weapons_menu_widgets['mag_size'][1].get()
        reserve_ammo = self.weapons_menu_widgets['reserve_ammo'][1].get()
        ints = [damage_per_shot, mag_size, reserve_ammo]

        burst_wep = self.weapons_menu_vars['burst_wep'].get()
        if burst_wep:
            burst_bullets = self.weapons_menu_widgets['burst_bullets'][1].get()
            ints.append(burst_bullets)
        for x in ints:
            try:
                x = int(x)
                if x <= 0:
                    return 3
            except ValueError:
                return 3
    
        perk1 = self.weapons_menu_widgets['perk1'][1].get()
        perk2 = self.weapons_menu_widgets['perk2'][1].get()
        # THANKS K
        perk_indices = [index for index, perkname in backend.PERKS_LIST.items() if list(perkname)[0] in [perk1, perk2]]
        perk_indices = None if perk_indices == [0] else perk_indices

        enhance1 = self.weapons_menu_vars['enhance1'].get()
        enhance2 = self.weapons_menu_vars['enhance2'].get()
        fusion_wep = self.weapons_menu_vars['fusion_wep'].get()

        weapon_options = {
        'name': name,
        'fire_rate': float(fire_rate),
        'reload_time': float(reload_time),
        'damage_per_shot': int(damage_per_shot),
        'mag_cap': int(mag_size),
        'ammo_total': int(reserve_ammo),
        'fusion_weapon': bool(fusion_wep),
        'perk_indices': perk_indices
        }
        print('Attempting to create weapon with options:')
        pprint(weapon_options, sort_dicts=False)

        if backend.create_weapon(weapon_options):
            self.graph_update_weapons()
            if self.settings.do_auto_save and self.settings.auto_save_path:
                self.options_export_weps_handler(self.settings.auto_save_path)
            return 0
        else:
            return 4
        
    def options_menu(self):
        # Root frame
        workingframe = self.options_frame = tk.Frame(self, **self.frame_style)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Combobox options
        interface_theme_choices = ['Dark', 'Light']
        interface_logmode_choices = ['App', 'Console', 'Both']
        impexp_exp_exts = ['json', 'csv', 'pickle']

        # Input validation
        val_int = self.register(self.util_valint)

        # Widget vars
        self.options_menu_vars = {
            'autosave': tk.BooleanVar(value=self.settings.do_auto_save),
            'autosave_path': tk.StringVar(value=self.settings.auto_save_path),
            'graph_title': tk.StringVar(value=self.settings.graph_title),
            'graph_xlabel': tk.StringVar(value=self.settings.graph_xlabel),
            'graph_xlim': tk.IntVar(value=self.settings.graph_xlim),
            'graph_ylabel': tk.StringVar(value=self.settings.graph_ylabel),
            'graph_ylim': tk.IntVar(value=self.settings.graph_ylim)
        }
        # Widgets
        self.options_menu_widgets = {
            # Graph
            'graph': {
                'header': tk.Label(workingframe, text='Graph', **self.label_style),
                'title': (tk.Label(workingframe, text='Graph Title', **self.label_style),
                          tk.Entry(workingframe, textvariable=self.options_menu_vars['graph_title'])),
                'xlabel': (tk.Label(workingframe, text='X Axis Name', **self.label_style),
                        tk.Entry(workingframe, textvariable=self.options_menu_vars['graph_xlabel'])),
                'xlim': (tk.Label(workingframe, text='X Axis Upper Limit', **self.label_style),
                        tk.Entry(workingframe, textvariable=self.options_menu_vars['graph_xlim'],
                                 validate='key', validatecommand=(val_int, '%S'))),
                'ylabel': (tk.Label(workingframe, text='Y Axis Name', **self.label_style),
                        tk.Entry(workingframe, textvariable=self.options_menu_vars['graph_ylabel'])),
                'ylim': (tk.Label(workingframe, text='Y Axis Upper Limit', **self.label_style),
                        tk.Entry(workingframe, textvariable=self.options_menu_vars['graph_ylim'],
                                 validate='key', validatecommand=(val_int, '%S')))
            },
            # Import / Export
            'impexp': {
                'header': tk.Label(workingframe, text='Import / Export', **self.label_style),
                'export': (tk.Button(workingframe, text='Export As', 
                                     command=self.options_export_weps_handler, **self.button_style),
                        ttk.Combobox(workingframe, values=impexp_exp_exts, **self.combo_style)),
                'log_impff': (tk.Button(workingframe, text='Log Current Weapons', 
                                        command=self.options_print_weps, **self.button_style),
                            tk.Button(workingframe, text='Import From File', 
                                      command=self.options_import_weps_handler, **self.button_style)),
                'auto_save_toggle': tk.Checkbutton(workingframe, text='Auto Save / Load', variable=self.options_menu_vars['autosave'], 
                                                   command=self.options_toggle_autosave, **self.check_button_style),
                'auto_save_path': (tk.Button(workingframe, text='Auto-Save Path',
                                             command=self.options_set_auto_import_handler, **self.button_style),
                                  tk.Entry(workingframe, textvariable=self.options_menu_vars['autosave_path'], state='readonly'))
            },
            # GUI
            'interface': {
                'header': tk.Label(workingframe, text='Interface', **self.label_style),
                'theme': (tk.Label(workingframe, text='Theme', **self.label_style),
                        ttk.Combobox(workingframe, values=interface_theme_choices, **self.combo_style)),
                'logmode': (tk.Label(workingframe, text='Log Mode', **self.label_style),
                            ttk.Combobox(workingframe, values=interface_logmode_choices, **self.combo_style)),
                'testbut': tk.Button(workingframe, text='test_func :)', command=self.test_func, **self.button_style),
            },
        }

        # Default combobox vals
        self.options_menu_widgets['impexp']['export'][1].set(impexp_exp_exts[0])
        self.options_menu_widgets['interface']['theme'][1].set(self.settings.interface_theme)
        self.options_menu_widgets['interface']['logmode'][1].set(self.settings.log_mode)

        # Grid placement
        max_outer_column = 2
        chunks = [list(self.options_menu_widgets.copy().items())[x:x+max_outer_column] for x in range(0, len(self.options_menu_widgets), max_outer_column)]
        # Assuming 2: [ [ ( name1, { group1 } ), ( name2, { group2 } ) ], ... ]
        ro = 0
        for chunk in chunks:
            # Store current offset, add to total. This assures sections are alligned vertically
            cro = max([len(widgetgroup) for groupname, widgetgroup in chunk])
            ro += cro + 1
            # One grid space of padding after first outer column
            if not ro-cro-1 == 0:
                spacer = tk.Label(workingframe, text=' ', **self.label_style)
                spacer.grid(row=ro-cro-1, column=0, **self.default_padding)
            step = 0
            for combined in chunk:
                # Set columns stepping by 2 based on index of group
                groupname, widgetgroup = combined
                column = step
                step += 2
                for idz, widget_keyval in enumerate(widgetgroup.items()):
                    key, widget = widget_keyval
                    grid = ({'row': idz+(ro-cro), 'column': column},
                            {'row': idz+(ro-cro), 'column': column+1})
                    # Handle single elements first
                    if not type(widget) is tuple:
                        widget.grid(**grid[0], **self.default_padding)
                        self.options_menu_widgets[groupname][key] = (widget, grid[0])
                        continue
                    # Handle label + input elements
                    label, usrinput = widget
                    label.grid(**grid[0], **self.default_padding)
                    usrinput.grid(**grid[1], **self.default_padding)
                    self.options_menu_widgets[groupname][key] = (label, usrinput, grid)
                    # Bind defocus to combos
                    if isinstance(usrinput, ttk.Combobox):
                        usrinput.bind("<<ComboboxSelected>>",lambda e: self.options_frame.focus())

        # Final Spacer
        spacer = tk.Label(workingframe, text=' ', **self.label_style)
        spacer.grid(row=ro, column=0, **self.default_padding)
        # Apply settings button (Always oriented bottom left)
        self.options_apply_settings_button = tk.Button(workingframe, text='Apply Settings', 
                                                       command=self.options_apply_settings, **self.button_style)
        self.options_apply_settings_button.grid(row=ro+1, column=0, **self.default_padding)

        # Hide this menu on start
        if not self.settings.do_auto_save:
            self.options_menu_widgets['impexp']['auto_save_path'][0].grid_forget()
            self.options_menu_widgets['impexp']['auto_save_path'][1].grid_forget()
        self.options_frame.pack_forget()

    def test_func(self):
        balls = self.options_menu_vars['graph_xlim'].get()
        print(balls)
        pass

    def options_set_auto_import_handler(self):
        exitcode = self.options_set_auto_import()
        basestr = f'Set Auto Save exited with code {exitcode}:'
        match exitcode:
            case 0:
                messagebox.showinfo('Success', 'Auto Save Path set successfully\nMake sure to apply settings when finished.')
                print(f'{basestr} Success')
            case 1:
                print(f'{basestr} Operation Canceled')
            case 2:
                print(f'{basestr} No Path Selected')
            case 3:
                messagebox.showerror('Invalid File Type', 'Selected file must be of type: .pickle')
                print(f'{basestr} Invalid File Type')
            case 4:
                messagebox.showerror('Invalid Pickle Data', 'Pickle data selected for import is invalid.')
                print(f'{basestr} Invalid Pickle Data')
        return exitcode

    def options_set_auto_import(self):
        confirm = messagebox.askokcancel('Import Warning', 'Setting auto import path will clear your current list and import from the selected file' +
                                        '\nDoing so will irreversably clear your current list. Make sure to export if you would like to keep your current list.',)
        if not confirm:
            return 1
        # File dialogue
        file_path = askopenfilename(
            filetypes=(('Pickle Files', '*.pickle'), ('All Files', '*.*')),
            initialdir='./')
        if file_path is None:
            return 2
        if not file_path.endswith('.pickle'):
            return 3
        exitcode = self.options_import_weps_handler(file_path)
        if not exitcode == 0:
            return 4
        self.options_menu_vars['autosave_path'].set(file_path)
        return 0

    def options_import_weps_handler(self, path=None):
        exitcode = self.options_import_weps(path)
        basestr = f'Weapon Import exited with code {exitcode}:'
        match exitcode:
            case 0:
                if path is None:
                    messagebox.showinfo('Success', 'Weapon list imported successfully.')
                print(f'{basestr} Success')
            case 1:
                print(f'{basestr} Operation Canceled')
            case 2:
                print(f'{basestr} No Path Selected')
            case 3:
                messagebox.showerror('Invalid File Type', 'Selected file must be of type: (.json, .pickle)')
                print(f'{basestr} Invalid File Type')
            case 4:
                messagebox.showerror('Invalid Json Data', 'Json data selected for import is invalid.')
                print(f'{basestr} Invalid Json Data')
            case 5:
                messagebox.showerror('Invalid Pickle Data', 'Pickle data selected for import is invalid.')
                print(f'{basestr} Invalid Pickle Data')
            case 6:
                messagebox.showerror('Import Error', 'An unknown error occured while importing your weapons. Check log for more info.')
                print(f'{basestr} How did you get here?')
            case _:
                messagebox.showerror('Import Error', 'An error occured while importing your weapons. Check log for more info.')
                print(f'An exception occured during Weapon Import:')
                pprint(exitcode)
        return exitcode

    def options_import_weps(self, path=None):
        # Warn about current list deletion
        if path is None:
            confirm = messagebox.askokcancel('Import Warning', 'Are you sure you want to import a list of weapons?' +
                                            '\nDoing so will irreversably clear your current list. Make sure to export if you would like to keep your current list.',)
            if not confirm:
                return 1
            # File dialogue
            file_path = askopenfilename(
                filetypes=(('JSON Files', '*.json'), ('Pickle Files', '*.pickle'), ('All Files', '*.*')),
                initialdir='./')
            if file_path is None:
                return 2
            if not file_path.endswith(('.json','.pickle')):
                return 3
        else:
            file_path = path
        
        # Load backup back into memory on import fail
        def reclaim(backup):
            reclaimed = pickle.loads(backup)
            backend.weapons_list = reclaimed

        # Create a temporary backup of current list
        temp_bak = pickle.dumps(backend.weapons_list)

        try:
            # Import json
            if file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    backend.weapons_list = dict()
                    data = json.load(f)
                    for wepsettings in data:
                        success = backend.create_weapon(wepsettings)
                        if not success:
                            reclaim(temp_bak)
                            return 4
                    self.graph_update_weapons()
                    return 0
            # Import pickle
            elif file_path.endswith('.pickle'):
                with open(file_path, 'rb') as f:
                    backend.weapons_list = dict()
                    data = pickle.load(f)
                    for wep in data.values():
                        if not isinstance(wep, backend.Weapon):
                            reclaim(temp_bak)
                            return 5
                    backend.weapons_list = data
                    self.graph_update_weapons()
                    return 0
            else:
                return 6
        except Exception as e:
            reclaim(temp_bak)
            return e
    
    def options_export_weps_handler(self, path=None):
        exitcode = self.options_export_weps(path)
        basestr = f'Weapon Export exited with code {exitcode}:'
        match exitcode:
            case 0:
                # NOTE Having a popup for a success is kinda aids ill work on something else
                messagebox.showinfo('Success', 'Weapon list exported successfully')
                print(f'{basestr} Success')
            case 1:
                messagebox.showerror('Empty Weapon List', 'There are no weapons currently available to export')
                print(f'{basestr} Empty Weapon List')
            case 2:
                print(f'{basestr} No Path Selected')
            case _:
                messagebox.showerror('Creation Error', 'There was an error creating your weapon')
                print(f'An exception occured during Weapon Export:')
                pprint(exitcode)

    def options_export_weps(self, path=None):
        if path is None:
            if len(backend.weapons_list) < 0:
                return 1
            ext = self.options_menu_widgets['impexp']['export'][1].get()
            file_path = asksaveasfile(defaultextension=f'.{ext}', filetypes=[('All Files', '*.*')], initialdir='./', initialfile=f'saved_weapons.{ext}')
            if file_path is None:
                return 2
            fpathname = file_path.name
        else:
            ext = 'pickle'
            fpathname = path
        try:
            match ext:
                case 'json':
                    d = [weapon.get_pruned_settings() for weapon in backend.weapons_list.values()]
                    with open(fpathname, file_path.mode) as f:
                        json.dump(d, fp=f, indent=4)
                        f.close()
                    return 0
                case 'csv':
                    d = [weapon.get_full_settings() for weapon in backend.weapons_list.values()]
                    d_names = d[0].keys()
                    with open(fpathname, file_path.mode) as f:
                        writer = csv.DictWriter(f, fieldnames=d_names)
                        writer.writeheader()
                        writer.writerows(d)
                        f.close()
                    return 0
                case 'pickle' | _:
                    d = backend.weapons_list
                    with open(fpathname, 'wb') as f:
                        pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
                        f.close()
                    return 0
        except Exception as e:
            return e
    
    def options_toggle_autosave(self):
        label, entry, gridpos = self.options_menu_widgets['impexp']['auto_save_path']
        if label.winfo_ismapped():
            label.grid_forget()
            entry.grid_forget()
        else:
            grid1, grid2 = gridpos
            label.grid(**grid1, **self.default_padding)
            entry.grid(**grid2, **self.default_padding)

    def options_print_weps(self):
        print('Current list of weapons:\n')
        for weapon in backend.weapons_list.values():
            settings = weapon.get_pruned_settings()
            pprint(settings, sort_dicts=False)
            print()

    def options_apply_settings(self):
        self.settings.set_interface_theme(self.options_menu_widgets['interface']['theme'][1].get())
        self.settings.set_log_mode(self.options_menu_widgets['interface']['logmode'][1].get())
        self.settings.set_do_auto_save(self.options_menu_vars['autosave'].get())
        self.settings.set_auto_save_path(self.options_menu_vars['autosave_path'].get())
        self.settings.set_graph_title(self.options_menu_vars['graph_title'].get())
        self.settings.set_graph_xlabel(self.options_menu_vars['graph_xlabel'].get())
        self.settings.set_graph_xlim(self.options_menu_vars['graph_xlim'].get())
        self.settings.set_graph_ylabel(self.options_menu_vars['graph_ylabel'].get())
        self.settings.set_graph_ylim(self.options_menu_vars['graph_ylim'].get())
        self.settings.save_settings()
        self.settings.restart_gui(root)

    def log_menu(self):
        self.log_frame = tk.Frame(self, **self.frame_style)
        self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Define color variables
        background_color = self.matplotlib_bg
        text_color = self.white_text

        # Create a Text widget for displaying the console output
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, bg=background_color, fg=text_color)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the Text widget
        self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)

        # Hide the log frame on start
        self.log_frame.pack_forget()

    def util_valfloat(self, char):
        if char in '0123456789.':
            return True
        else:
            return False
        
    def util_valint(self, char):
        if char in '0123456789':
            return True
        else:
            return False

def redirect_logs(text_widget: tk.Widget, log_mode: str):
    
    def write_to_app(string):
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, string)
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)

    if log_mode in ['App', 'Both']:
        use_decorator = True if log_mode == 'Both' else False
    else:
        write_to_app('Log Menu will not print logs due to selecting "Console" for Log Mode option' +
                     '\nCheck your console for relevant logs')
        sys.stdout.write = stdoutwrite
        return

    def decorator(func):
        def inner(inpStr):
            try:
                write_to_app(inpStr)
                return func(inpStr)
            except:
                return func(inpStr)
        return inner
    
    if use_decorator:
        sys.stdout.write = decorator(stdoutwrite)
    else:
        sys.stdout.write = write_to_app

def global_start_gui():
    global root
    root = tk.Tk()
    app = GUI(master=root)
    app.mainloop()

stdoutwrite = sys.stdout.write
global_start_gui()