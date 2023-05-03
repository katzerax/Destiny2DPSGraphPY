import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import configparser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import weaponclassrewrite as backend


###############################
##  Myssto frontend concept  ## hi myssto :3 -k
###############################

# TODO
# 1. Default ini
# 2. Nav bar // DONE
# 3. Weapons menu // Talk to rox about multi-wep
# 4. Graph menu // Add wep selection
# 5. Settings menu
# 6. Log menu // normal vs verbose?
# 7. Make graph menu functional
# 8. Add graph config to settings or graph menu?

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')
        # Add check for existing settings // create default if not
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

    def restart_program(self, root):
        # Close the tkinter window
        root.destroy()

        # Re-run the script
        os.execl(sys.executable, sys.executable, *sys.argv)


class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Destiny2DPSGraphPY')
        self.master.resizable(False, False)
        self.pack()
        self.load_settings()
        self.initGUI()

    def load_settings(self):
        # Instance settings
        self.settings = Settings()
        # Access and apply settings
        if self.settings.interface_mode.lower() == 'dark':
            self.configure(bg='#1E1E1E')
            self.master.configure(bg='#1E1E1E', highlightthickness=2, highlightcolor='#000000')
            self.combo_style = {'width': 17, 'state': 'readonly'}
            self.frame_style = {'bg': '#1E1E1E', 'highlightcolor': '#000000', 'highlightbackground': '#000000', 'highlightthickness': 2}
            self.check_button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC', 'selectcolor': '#1E1E1E'}
            self.button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC'}
            self.matplotlibbg = "#1E1E1E"
            self.wep_frame = "#1E1E1E"
            self.listbox_bg = "#808080"
        else:
            self.check_button_style = {}
            self.button_style = {}
            self.matplotlibbg = "#FFFFFF"
            self.frame_style = {'bg': '#FFFFFF', 'highlightcolor': '#FFFFFF', 'highlightbackground': '#FFFFFF', 'highlightthickness': 2}
            self.combo_style = {'width': 17, 'state': 'readonly'}
            self.wep_frame = "#FFFFFF"
            self.listbox_bg = "#808080"

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

    def initGUI(self):
        self.navbar()
        self.graph_menu()
        self.weapons_menu()
        self.options_menu()

    def navbar(self):
        # Root frame
        self.nav_frame = tk.Frame(self, **self.frame_style)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Nice styling brother man
        listbox_style = {
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
        self.nav_listbox = tk.Listbox(self.nav_frame, **self.button_style, **listbox_style)
        self.nav_listbox.pack()
        self.nav_listbox.insert(1, 'Graph')
        self.nav_listbox.insert(2, 'Weapons')
        self.nav_listbox.insert(3, 'Options')
        self.nav_listbox.insert(4, 'Log')

        self.nav_listbox.select_set(0)
        self.nav_listbox.bind('<<ListboxSelect>>', self.toggle_menus)

    def toggle_menus(self, evt):
        index = int(evt.widget.curselection()[0])
        match index:
            case 0:
                target = self.graph_frame
            case 1:
                target = self.weapons_frame
            case 2:
                target = self.options_frame
            # case 4:
            #     target = self.log_frame

        if target.winfo_ismapped():
            return

        # Hardcoded? list of selectable menus
        menus = [
            self.graph_frame,
            self.weapons_frame,
            self.options_frame,
            # self.log_frame,
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
        self.graph_wep_frame = tk.Frame(self.graph_frame, bg=self.wep_frame)
        self.graph_wep_frame.pack(side=tk.LEFT, fill=tk.Y)

        # No. of weps
        wep_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.graph_wep_select_label = tk.Label(self.graph_wep_frame, text='Number of Weapons', **self.button_style)
        self.graph_wep_select_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep_select_combo = ttk.Combobox(self.graph_wep_frame, values=wep_count, width=3, state='readonly')
        self.graph_wep_select_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep_select_combo.set(wep_count[2])
        self.graph_wep_select_combo.bind("<<ComboboxSelected>>", self.toggle_weapon_combos)

        # Wep1
        #   This is where having a 'save weapons' system would come in handy
        self.graph_wep1_label = tk.Label(self.graph_wep_frame, text='Weapon 1', **self.button_style)
        self.graph_wep1_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep1_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep1_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep1_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())

        self.graph_wep2_label = tk.Label(self.graph_wep_frame, text='Weapon 2', **self.button_style)
        self.graph_wep2_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep2_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep2_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep2_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())

        self.graph_wep3_label = tk.Label(self.graph_wep_frame, text='Weapon 3', **self.button_style)
        self.graph_wep3_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep3_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep3_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep3_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())

        self.graph_wep4_label = tk.Label(self.graph_wep_frame, text='Weapon 4', **self.button_style)
        self.graph_wep4_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep4_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep4_combo.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep4_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep4_label.grid_forget()
        self.graph_wep4_combo.grid_forget()

        self.graph_wep5_label = tk.Label(self.graph_wep_frame, text='Weapon 5', **self.button_style)
        self.graph_wep5_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep5_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep5_combo.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep5_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep5_label.grid_forget()
        self.graph_wep5_combo.grid_forget()

        self.graph_wep6_label = tk.Label(self.graph_wep_frame, text='Weapon 6', **self.button_style)
        self.graph_wep6_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep6_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep6_combo.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep6_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep6_label.grid_forget()
        self.graph_wep6_combo.grid_forget()

        self.graph_wep7_label = tk.Label(self.graph_wep_frame, text='Weapon 7', **self.button_style)
        self.graph_wep7_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep7_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep7_combo.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep7_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep7_label.grid_forget()
        self.graph_wep7_combo.grid_forget()

        self.graph_wep8_label = tk.Label(self.graph_wep_frame, text='Weapon 8', **self.button_style)
        self.graph_wep8_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep8_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep8_combo.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep8_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep8_label.grid_forget()
        self.graph_wep8_combo.grid_forget()

        self.graph_wep9_label = tk.Label(self.graph_wep_frame, text='Weapon 9', **self.button_style)
        self.graph_wep9_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep9_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep9_combo.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep9_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep9_label.grid_forget()
        self.graph_wep9_combo.grid_forget()

        self.graph_wep10_label = tk.Label(self.graph_wep_frame, text='Weapon 10', **self.button_style)
        self.graph_wep10_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_wep10_combo = ttk.Combobox(self.graph_wep_frame, **self.combo_style)
        self.graph_wep10_combo.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        self.graph_wep10_combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
        self.graph_wep10_label.grid_forget()
        self.graph_wep10_combo.grid_forget()

        self.graph_generate_button = tk.Button(self.graph_wep_frame, text="Generate Graph", command=self.generate_graph, **self.button_style)
        self.graph_generate_button.grid(row=15, column=0, padx=8, pady=5, sticky=tk.W)

        # Create a Matplotlib figure and canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.ax.set_facecolor(self.matplotlibbg)
        self.fig.set_facecolor(self.matplotlibbg)

        # Set x and y axis and labels
        self.ax.set_title("DPS Over Time")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("DPS", labelpad=-340, rotation='horizontal')
        self.ax.set_xlim(0, 45)
        self.ax.set_ylim(0, 300000)

        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def generate_graph(self):
        pass

    # This feels really hacky ill probably figure out something smarter later
    # and by this I mean literally everything with the 10 combo boxes
    def toggle_weapon_combos(self, evt):
        ammount = int(self.graph_wep_select_combo.get()) - 1
        combos = [
            self.graph_wep1_combo, self.graph_wep2_combo,
            self.graph_wep3_combo, self.graph_wep4_combo,
            self.graph_wep5_combo, self.graph_wep6_combo,
            self.graph_wep7_combo, self.graph_wep8_combo,
            self.graph_wep9_combo, self.graph_wep10_combo,
        ]
        labels = [
            self.graph_wep1_label, self.graph_wep2_label,
            self.graph_wep3_label, self.graph_wep4_label,
            self.graph_wep5_label, self.graph_wep6_label,
            self.graph_wep7_label, self.graph_wep8_label,
            self.graph_wep9_label, self.graph_wep10_label,
        ]
        if ammount == 0:
            for combo in combos[1:]:
                combo.grid_forget()
            for label in labels[1:]:
                label.grid_forget()
        else:
            for idx, x in enumerate(combos):
                if idx <= ammount:
                    labels[idx].grid(row=(idx+1), column=0, padx=5, pady=5, sticky=tk.W)
                    x.grid(row=(idx+1), column=1, padx=5, pady=5, sticky=tk.W)
                else:
                    labels[idx].grid_forget()
                    x.grid_forget()

    def weapons_menu(self):
        # Root frame
        self.weapons_frame = tk.Frame(self, **self.frame_style)
        self.weapons_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Single or multi weapon
        #   Figure out why comboboxes change frame highlight when focused
        type_options = ['Single Weapon', 'Weapon Swap']
        self.type_label = tk.Label(self.weapons_frame, text="Type", **self.button_style)
        self.type_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.type_combo = ttk.Combobox(self.weapons_frame, values=type_options, **self.combo_style)
        self.type_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_combo.set(type_options[0])
        self.type_combo.bind("<<ComboboxSelected>>",lambda e: self.weapons_frame.focus())

        # Name
        self.name_label = tk.Label(self.weapons_frame, text="Name", **self.button_style)
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(self.weapons_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Fire rate
        self.fire_rate_label = tk.Label(self.weapons_frame, text="Fire Rate", **self.button_style)
        self.fire_rate_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.fire_rate_entry = tk.Entry(self.weapons_frame)
        self.fire_rate_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Reload Time
        self.reload_time_label = tk.Label(self.weapons_frame, text="Reload Time", **self.button_style)
        self.reload_time_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.reload_time_entry = tk.Entry(self.weapons_frame)
        self.reload_time_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # Damage per shot
        self.damage_per_shot_label = tk.Label(self.weapons_frame, text="Damage per Shot", **self.button_style)
        self.damage_per_shot_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.damage_per_shot_entry = tk.Entry(self.weapons_frame)
        self.damage_per_shot_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # Mag Size
        self.mag_cap_label = tk.Label(self.weapons_frame, text="Magazine Capacity", **self.button_style)
        self.mag_cap_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.mag_cap_entry = tk.Entry(self.weapons_frame)
        self.mag_cap_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # Reserve ammo
        self.ammo_total_label = tk.Label(self.weapons_frame, text="Ammo Total", **self.button_style)
        self.ammo_total_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.ammo_total_entry = tk.Entry(self.weapons_frame)
        self.ammo_total_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # Swap group
        self.swap_group_label = tk.Label(self.weapons_frame, text="Swap Group", **self.button_style)
        self.swap_group_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.swap_group_entry = tk.Entry(self.weapons_frame)
        self.swap_group_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

        # Swap time
        self.swap_time_label = tk.Label(self.weapons_frame, text="Swap Time (ms)", **self.button_style)
        self.swap_time_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.swap_time_entry = tk.Entry(self.weapons_frame)
        self.swap_time_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

        # Perk select
        perk_choices = [value[0] for value in backend.PERKS.values()]
        perk_tooltips = [value[1] for value in backend.PERKS.values()]

        self.perk1_label = tk.Label(self.weapons_frame, text="Perk 1", **self.button_style)
        self.perk1_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.perk1_combo = ttk.Combobox(self.weapons_frame, values=perk_choices, **self.combo_style)
        self.perk1_combo.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        self.perk1_combo.set(perk_choices[0])
        self.perk1_combo.bind("<<ComboboxSelected>>",lambda e: self.weapons_frame.focus())

        self.perk2_label = tk.Label(self.weapons_frame, text="Perk 2", **self.button_style)
        self.perk2_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.perk2_combo = ttk.Combobox(self.weapons_frame, values=perk_choices, **self.combo_style)
        self.perk2_combo.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        self.perk2_combo.set(perk_choices[0])
        self.perk2_combo.bind("<<ComboboxSelected>>",lambda e: self.weapons_frame.focus())

        # Enhanced perks
        self.Enhance1_var = tk.BooleanVar()
        self.Enhance1_button = tk.Checkbutton(self.weapons_frame, text="Perk 1 Enhanced", variable=self.Enhance1_var, **self.check_button_style)
        self.Enhance1_button.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)

        self.Enhance2_var = tk.BooleanVar()
        self.Enhance2_button = tk.Checkbutton(self.weapons_frame, text="Perk 2 Enhanced", variable=self.Enhance2_var, **self.check_button_style)
        self.Enhance2_button.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)

        # Burst Toggle
        self.burst_weapon_var = tk.BooleanVar()
        self.burst_weapon_check_button = tk.Checkbutton(self.weapons_frame, text="Burst Weapon", variable=self.burst_weapon_var, command=self.toggle_burst, **self.check_button_style)
        self.burst_weapon_check_button.grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)

        # Delay First
        self.delay_first_shot_var = tk.BooleanVar()
        self.delay_first_shot_button = tk.Checkbutton(self.weapons_frame, text="Delay First Shot", variable=self.delay_first_shot_var, **self.check_button_style)
        self.delay_first_shot_button.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)

        # Burst Bullets
        self.burst_bullets_label = tk.Label(self.weapons_frame, text="Burst Bullets", **self.button_style)
        self.burst_bullets_label.grid(row=13, column=0, padx=5, pady=5, sticky=tk.W)
        self.burst_bullets_entry = tk.Entry(self.weapons_frame)
        self.burst_bullets_entry.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
        # Hide on start
        self.burst_bullets_label.grid_forget()
        self.burst_bullets_entry.grid_forget()

        # Create a button to create a Weapon object
        self.create_weapon_button = tk.Button(self.weapons_frame, text="Create Weapon", **self.button_style)
        self.create_weapon_button.grid(row=15, column=0, padx=8, pady=5, sticky=tk.W)

        # Hide this menu on start
        self.weapons_frame.pack_forget()

    def toggle_burst(self):
        if self.burst_bullets_label.winfo_ismapped():
            self.burst_bullets_label.grid_forget()
            self.burst_bullets_entry.grid_forget()
        else:
            self.burst_bullets_label.grid(row=13, column=0, padx=5, pady=5, sticky=tk.W)
            self.burst_bullets_entry.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)

    # Placeholder for multi-wep
    def weapons_menu_ext(self):
        pass

    def apply_settings(self):
        self.settings.set_interface_mode(self.setting1_combo.get())
        self.settings.set_cmd_prints(self.setting2_combo.get())
        self.settings.set_multi_weapon(self.setting3_combo.get())
        self.settings.set_calc_when_damage_dealt(self.setting4_combo.get())
        self.settings.save_settings()
        self.settings.restart_program(root)

    def options_menu(self):
        # Root frame
        self.options_frame = tk.Frame(self, **self.frame_style)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Setting 1
        setting1_options = ['Light', 'Dark']
        self.setting1_label = tk.Label(self.options_frame, text="UI Mode", **self.button_style)
        self.setting1_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.setting1_combo = ttk.Combobox(self.options_frame, values=setting1_options, **self.combo_style)
        self.setting1_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.setting1_combo.set(self.settings.interface_mode)
        self.setting1_combo.bind("<<ComboboxSelected>>", lambda e: self.options_frame.focus())

        # Setting 2
        setting2_options = ['True', 'False']
        self.setting2_label = tk.Label(self.options_frame, text="CMD Prints", **self.button_style)
        self.setting2_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.setting2_combo = ttk.Combobox(self.options_frame, values=setting2_options, **self.combo_style)
        self.setting2_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.setting2_combo.set(str(self.settings.cmd_prints))
        self.setting2_combo.bind("<<ComboboxSelected>>", lambda e: self.options_frame.focus())

        # Setting 3
        setting3_options = ['True', 'False']
        self.setting3_label = tk.Label(self.options_frame, text="Multiweapon", **self.button_style)
        self.setting3_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.setting3_combo = ttk.Combobox(self.options_frame, values=setting3_options, **self.combo_style)
        self.setting3_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.setting3_combo.set(str(self.settings.multi_weapon))
        self.setting3_combo.bind("<<ComboboxSelected>>", lambda e: self.options_frame.focus())

        # Setting 4
        setting4_options = ['What', 'Is', 'This']
        self.setting4_label = tk.Label(self.options_frame, text="When Damage Dealt", **self.button_style)
        self.setting4_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.setting4_combo = ttk.Combobox(self.options_frame, values=setting4_options, **self.combo_style)
        self.setting4_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.setting4_combo.set(self.settings.calc_when_damage_dealt)
        self.setting4_combo.bind("<<ComboboxSelected>>", lambda e: self.options_frame.focus())

        # Apply Settings button
        self.apply_settings_button = tk.Button(self.options_frame, text="Apply Settings", command=self.apply_settings, **self.button_style)
        self.apply_settings_button.grid(row=4, column=0, padx=8, pady=5, sticky=tk.W)
        
        # Hide this menu on start
        self.options_frame.pack_forget()

    def log_menu(self):
        pass

    # def create_weapon(self):
    #     # Retrieve values from input boxes and checkboxes
    #     name = self.name_entry.get()
    #     fire_rate = float(self.fire_rate_entry.get())
    #     reload_time = float(self.reload_time_entry.get())
    #     damage_per_shot = float(self.damage_per_shot_entry.get())
    #     mag_cap = int(self.mag_cap_entry.get())
    #     ammo_total = int(self.ammo_total_entry.get())
    #     delay_first_shot = self.delay_first_shot_var.get()
    #     burst_weapon = self.burst_weapon_var.get()
    #     burst_bullets = int(self.burst_bullets_entry.get()) if burst_weapon else 1
    #     swap_group = int(self.swap_group_entry.get())
    #     swap_time = float(self.swap_time_entry.get())

    #     # Create the Weapon object using the retrieved values
    #     weapon = backend.Weapon(name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, burst_weapon, burst_bullets, swap_group, swap_time)

    #     # Print the weapon details for debugging purposes
    #     print("Created weapon: ", weapon.__dict__)



    #def plot_data(self):
        # Generate some random data and plot it
    #    x = [1, 2, 3, 4, 5]
    #    y = [random.randint(1, 10) for i in range(5)]
    #    self.ax.clear()
    #    self.ax.plot(x, y)
    #    self.canvas.draw()

    # def update_graph(self):
    #     print("burst:", self.burst_weapon_var.get())
    #     print("delay:", self.delay_first_shot_var.get())
    #     print("perk1:", self.triple_tap_var.get())
    #     print("perk2:", self.FTTC_var.get())

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