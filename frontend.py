import sys
import os
import configparser
import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import weaponclassrewrite as backend

# TODO
# 1. Default ini
# 2. Weapons menu // Talk to rox about multi-wep
# 3. Log menu // normal vs verbose? (see log_menu comments)
# 4. Make graph menu functional // 50% done
# 5. Add graph config to settings or graph menu?
# 6. Look into on-hover tooltips

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')
        # Add check for existing settings // create default if not
        with open(ini_path, 'r', encoding='utf-8') as f:
            self.config.read_file(f)
        self.interface_theme = self.config.get('Interface', 'Theme')
        self.cmd_prints = self.config.getboolean('Interface', 'CMDPrints')

    def set_interface_theme(self, theme):
        self.interface_theme = theme

    def set_cmd_prints(self, value):
        self.cmd_prints = value

    def set_calc_when_damage_dealt(self, value):
        self.calc_when_damage_dealt = value

    def save_settings(self):
        self.config.set('Interface', 'Theme', self.interface_theme)
        self.config.set('Interface', 'CMDPrints', str(self.cmd_prints))

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

    def reset_settings(self):
        pass

    def restart_program(self, root):
        # Close the tkinter window
        root.destroy()

        # Re-run the script
            # NOTE execl as an executable is really volatile
            # maybe we look into another way to reload app? -mys
            # yeah prolly, I just wrote this quickly to have something that works but by all means do it better
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
        sys.stdout = TextRedirector(self.log_text)

    def load_settings(self):
        # Instance settings
        self.settings = Settings()
        self.default_padding = {'padx': 5, 'pady': 5, 'sticky': tk.W}
        # Access and apply settings
        if self.settings.interface_theme.lower() == 'dark':
            self.configure(bg='#1E1E1E')
            self.master.configure(bg='#1E1E1E', highlightthickness=2, highlightcolor='#000000')
            self.combo_style = {'width': 17, 'state': 'readonly'}
            self.frame_style = {'bg': '#1E1E1E', 'highlightcolor': '#000000', 'highlightbackground': '#000000', 'highlightthickness': 2}
            self.check_button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC', 'selectcolor': '#1E1E1E'}
            self.button_style = {'bg': '#1E1E1E', 'fg': '#CCCCCC'}
            self.matplotlib_bg = "#1E1E1E"
            self.matplotlib_fg = "#CCCCCC"
            self.wep_frame_bg = "#1E1E1E"
            self.listbox_bg = "#808080"
            self.white_text = "#CCCCCC"
        else:
            self.check_button_style = {}
            self.button_style = {}
            self.matplotlib_bg = "#FFFFFF"
            self.frame_style = {'bg': '#FFFFFF', 'highlightcolor': '#FFFFFF', 'highlightbackground': '#FFFFFF', 'highlightthickness': 2}
            self.combo_style = {'width': 17, 'state': 'readonly'}
            self.wep_frame_bg = "#FFFFFF"
            self.listbox_bg = "#808080"
            self.white_text = "#000000"
            self.matplotlib_fg = "#000000"

        if self.settings.cmd_prints == 'True':
            pass
        else:
            pass

    def initGUI(self):
        self.navbar()
        self.graph_menu()
        self.weapons_menu()
        self.options_menu()
        self.log_menu()

    def navbar(self):
        # Root frame
        self.nav_frame = tk.Frame(self, **self.frame_style)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)

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
        # Create navbar and load options
        self.nav_listbox = tk.Listbox(self.nav_frame, **self.button_style, **listbox_style)
        self.nav_listbox.pack()
        self.nav_listbox.insert(1, 'Graph')
        self.nav_listbox.insert(2, 'Weapons')
        self.nav_listbox.insert(3, 'Options')
        self.nav_listbox.insert(4, 'Log')

        # Set default selection to 'Graph'
        self.nav_listbox.select_set(0)
        # Handle clicks on the navbar
        self.nav_listbox.bind('<<ListboxSelect>>', self.toggle_menus)

    def toggle_menus(self, evt):
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
        self.graph_wep_frame = tk.Frame(self.graph_frame, bg=self.wep_frame_bg)
        self.graph_wep_frame.pack(side=tk.LEFT, fill=tk.Y)

        # No. of weps
        wep_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.graph_wep_select_label = tk.Label(self.graph_wep_frame, text='Number of Weapons', **self.button_style)
        self.graph_wep_select_label.grid(row=0, column=0, **self.default_padding)
        self.graph_wep_select_combo = ttk.Combobox(self.graph_wep_frame, values=wep_count, width=3, state='readonly')
        self.graph_wep_select_combo.grid(row=0, column=1, **self.default_padding)
        self.graph_wep_select_combo.set(wep_count[2])
        self.graph_wep_select_combo.bind("<<ComboboxSelected>>", self.toggle_weapon_combos)

        # Build weapon select widgets
        self.graph_wep_widgets = [
                ( tk.Label(self.graph_wep_frame, text=f'Weapon {i+1}', **self.button_style),
                ttk.Combobox(self.graph_wep_frame, **self.combo_style)
                ) for i in range(10)
            ]
        # Grid placement
        for idx, multi in enumerate(self.graph_wep_widgets):
            label, combo = multi
            label.grid(row=(idx+1), column=0, **self.default_padding)
            combo.grid(row=(idx+1), column=1, **self.default_padding)
            combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
            # Display only 3 by default
            if idx > 2:
                label.grid_forget()
                combo.grid_forget()

        # Generate graph button
        self.graph_generate_button = tk.Button(self.graph_wep_frame, text="Generate Graph", command=self.generate_graph, **self.button_style)
        self.graph_generate_button.grid(row=15, column=0, padx=8, pady=5, sticky=tk.W)

        # Save graph button
        self.graph_save_button = tk.Button(self.graph_wep_frame, text="Save Graph", command=self.save_graph, **self.button_style)
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

        # Set default axis and labels
        self.ax.set_title("DPS Over Time")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("DPS", labelpad=-340, rotation='horizontal')
        self.ax.set_xlim(0, 45)
        self.ax.set_ylim(0, 300000)

        self.matplotlib_fg

        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

    def generate_graph(self):
        pass

    def save_graph(self):
        file_path = asksaveasfile(defaultextension='.png', filetypes=[('All Files', '*.*')], initialdir='./', initialfile='dps_graph.png')
        if file_path is None:
            return
        self.fig.savefig(file_path.name)

    def toggle_weapon_combos(self, evt):
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

        # Input validation
        val_float = (self.register(self.validate_float))
        val_int = (self.register(self.validate_int))

        # Combobox options
        type_options = ['Single Weapon', 'Weapon Swap']
        perk_choices = [value[0] for value in backend.PERKS_LIST.values()]

        # Widget vars
        self.weapons_menu_vars = {
            'enhance1': tk.BooleanVar(),
            'enhance2': tk.BooleanVar(),
            'burst_wep': tk.BooleanVar(),
            'fusion_wep': tk.BooleanVar()
        }

        # Widgets
        self.weapons_menu_widgets = {
            'header': tk.Label(self.weapons_frame, text="Weapon Creation", **self.button_style),
            'type': (tk.Label(workingframe, text="Type", **self.button_style),
                    ttk.Combobox(workingframe, values=type_options, width=17, state='disabled')),
            'name': (tk.Label(workingframe, text="Name", **self.button_style),
                    tk.Entry(workingframe)),
            'fire_rate': (tk.Label(workingframe, text="Fire Rate", **self.button_style),
                          tk.Entry(workingframe, validate='key', validatecommand=(val_float, '%S'))),
            'reload_time': (tk.Label(workingframe, text="Reload Time", **self.button_style),
                            tk.Entry(workingframe, validate='key', validatecommand=(val_float, '%S'))),
            'damage_per_shot': (tk.Label(workingframe, text="Damage per Shot", **self.button_style),
                                tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'mag_size': (tk.Label(workingframe, text="Magazine Capacity", **self.button_style),
                         tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'reserve_ammo': (tk.Label(workingframe, text="Ammo Total", **self.button_style),
                             tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'perk1': (tk.Label(workingframe, text="Perk 1", **self.button_style),
                      ttk.Combobox(workingframe, values=perk_choices, **self.combo_style)),
            'perk2': (tk.Label(workingframe, text="Perk 2", **self.button_style),
                      ttk.Combobox(workingframe, values=perk_choices, **self.combo_style)),
            'enhance_toggle': (tk.Checkbutton(workingframe, text="Perk 1 Enhanced", variable=self.weapons_menu_vars['enhance1'], **self.check_button_style),
                               tk.Checkbutton(workingframe, text="Perk 2 Enhanced", variable=self.weapons_menu_vars['enhance2'], **self.check_button_style)),
            'burst_fusion_toggle': (tk.Checkbutton(workingframe, text="Burst Weapon", variable=self.weapons_menu_vars['burst_wep'], command=self.toggle_burst, **self.check_button_style),
                                    tk.Checkbutton(workingframe, text="Fusion Weapon", variable=self.weapons_menu_vars['fusion_wep'], **self.check_button_style)),
            'burst_bullets': (tk.Label(workingframe, text="Bullets Per Burst", **self.button_style),
                              tk.Entry(workingframe, validate='key', validatecommand=(val_int, '%S'))),
            'create_wep': tk.Button(workingframe, text="Create Weapon", command=self.create_weapon_handler, **self.button_style)
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

    def toggle_burst(self):
        label, entry, gridpos = self.weapons_menu_widgets['burst_bullets']
        if label.winfo_ismapped():
            label.grid_forget()
            entry.grid_forget()
        else:
            label.grid(row=gridpos, column=0, **self.default_padding)
            entry.grid(row=gridpos, column=1, **self.default_padding)

    def validate_float(self, char):
        if char in '0123456789.':
            return True
        else:
            return False
        
    def validate_int(self, char):
        if char in '0123456789':
            return True
        else:
            return False

    def create_weapon_handler(self):
        exitcode = self.create_weapon()
        print(exitcode)
        match exitcode:
            case 0:
                # NOTE Having a popup for a success is kinda aids ill work on something else
                messagebox.showinfo('Success', 'Weapon created successfully')
                print('Weapon created successfully')
            case 1:
                messagebox.showerror('Name Error', 'Make sure the name for your weapon contains at least one letter')
                print('Make sure the name for your weapon contains at least one letter')
            case 2:
                messagebox.showerror('Float Error', 'Make sure Fire Rate and Reload Time are valid numbers')
                print('Make sure Fire Rate and Reload Time are valid numbers')
            case 3:
                messagebox.showerror('Integer Error', 'Make sure Damage per Shot, Mag Size, and Ammo Total are valid numbers')
                print('Make sure Damage per Shot, Mag Size, and Ammo Total are valid numbers')
            case _:
                messagebox.showerror('Creation Error', 'There was an error creating your weapon')
                print('There was an error creating your weapon')
        
    def create_weapon(self):
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
        perk2 = self.weapons_menu_widgets['perk1'][1].get()

        perk_indices = []
        for (index, perkname) in backend.PERKS_LIST.items():
            if list(perkname)[0] in [perk1, perk2]:
                perk_indices.append(index)

        # TODO figure out a working list comprehension for this its annoying me
        perk_indices = [index for index, perkname in backend.PERKS_LIST.items() if perkname[0] in [perk1, perk2]]

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
        'delay_first_shot': bool(fusion_wep),
        'perk_indices': perk_indices
        }
        print(weapon_options)

        if backend.create_weapon(weapon_options):
            print(backend.weapons_list)
            return 0
        else:
            print(backend.weapons_list)
            return 4
        
    def options_menu(self):
        # Root frame
        self.options_frame = tk.Frame(self, **self.frame_style)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Setting 1 (ui theme)
        setting1_options = ['Light', 'Dark']
        self.setting1_label = tk.Label(self.options_frame, text="UI Mode", **self.button_style)
        self.setting1_label.grid(row=0, column=0, **self.default_padding)
        self.setting1_combo = ttk.Combobox(self.options_frame, values=setting1_options, **self.combo_style)
        self.setting1_combo.grid(row=0, column=1, **self.default_padding)
        self.setting1_combo.set(self.settings.interface_theme)
        self.setting1_combo.bind("<<ComboboxSelected>>", lambda e: self.options_frame.focus())

        # Setting 2 (cmd prints)
        setting2_options = ['True', 'False']
        self.setting2_label = tk.Label(self.options_frame, text="CMD Prints", **self.button_style)
        self.setting2_label.grid(row=1, column=0, **self.default_padding)
        self.setting2_combo = ttk.Combobox(self.options_frame, values=setting2_options, **self.combo_style)
        self.setting2_combo.grid(row=1, column=1, **self.default_padding)
        self.setting2_combo.set(str(self.settings.cmd_prints))
        self.setting2_combo.bind("<<ComboboxSelected>>", lambda e: self.options_frame.focus())

        # Apply Settings button
        self.apply_settings_button = tk.Button(self.options_frame, text="Apply Settings", command=self.apply_settings, **self.button_style)
        self.apply_settings_button.grid(row=4, column=0, padx=8, pady=5, sticky=tk.W)
        
        # Hide this menu on start
        self.options_frame.pack_forget()

    def apply_settings(self):
        self.settings.set_interface_theme(self.setting1_combo.get())
        self.settings.set_cmd_prints(self.setting2_combo.get())
        self.settings.save_settings()
        self.settings.restart_program(root)

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

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def flush(self):
        pass



root = tk.Tk()
app = GUI(master=root)
app.mainloop()