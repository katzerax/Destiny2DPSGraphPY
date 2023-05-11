import sys
import os
import configparser
import tkinter as tk

from frontend.graphmenu import GraphMenu
from frontend.weaponsmenu import WeaponsMenu
from frontend.optionsmenu import OptionsMenu
from frontend.logemenu import LogMenu
from frontend.navbar import NavBar

import backend.backend as backend

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend/settings.ini')
        self.check_and_create_settings_file(ini_path)
        with open(ini_path, 'r', encoding='utf-8') as f:
            self.config.read_file(f)

        self.interface_theme = self.config.get('Interface', 'theme')
        self.log_mode = self.config.get('Interface', 'log_mode')
        self.do_dmg_prints = self.config.getboolean('Interface', 'dmg_prints')
        self.debug_mode = self.config.getboolean('Interface', 'debug_mode')
        self.do_auto_save = self.config.getboolean('AutoSave', 'enabled')
        self.auto_save_path = self.config.get('AutoSave', 'path')
        self.graph_title = self.config.get('Graph', 'title')
        self.graph_xlabel = self.config.get('Graph', 'xlabel')
        self.graph_xlim = self.config.getint('Graph', 'xlim')
        self.graph_ylabel = self.config.get('Graph', 'ylabel')
        self.graph_ylim = self.config.getint('Graph', 'ylim')
        self.graph_initial_slots = self.config.getint('Graph', 'initial_slots')
        self.graph_colors = self.config.get('Graph', 'colors')

    def check_and_create_settings_file(self, ini_path):
        if not os.path.exists(ini_path):
            default_settings = {
                'Interface': {
                    'theme': 'Dark',
                    'log_mode': 'App',
                    'dmg_steps': 'False',
                    'debug_mode': 'False'
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
                    'ylim': '300000',
                    'initial_wep_slots': '3',
                    'slot_colors': ''
                }
            }

            for section, settings in default_settings.items():
                self.config.add_section(section)
                for key, value in settings.items():
                    self.config.set(section, key, value)

            with open(ini_path, 'w', encoding='utf-8') as f:
                self.config.write(f)

    def reset_to_defaults(self):
        self.interface_theme = 'Dark'
        self.log_mode = 'App'
        self.do_dmg_prints = False
        self.debug_mode = False
        self.do_auto_save = False
        self.auto_save_path = ''
        self.graph_title = 'DPS Over Time'
        self.graph_xlabel = 'Time (seconds)'
        self.graph_xlim = 45
        self.graph_ylabel = 'DPS'
        self.graph_ylim = 300000
        self.graph_initial_slots = 3
        self.graph_colors = ''

        self.save_settings()

    def save_settings(self):
        self.config.set('Interface', 'theme', self.interface_theme)
        self.config.set('Interface', 'log_mode', self.log_mode)
        self.config.set('Interface', 'dmg_prints', str(self.do_dmg_prints))
        self.config.set('Interface', 'debug_mode', str(self.debug_mode))
        self.config.set('AutoSave', 'enabled', str(self.do_auto_save))
        self.config.set('AutoSave', 'path', self.auto_save_path)
        self.config.set('Graph', 'title', self.graph_title)
        self.config.set('Graph', 'xlabel', self.graph_xlabel)
        self.config.set('Graph', 'xlim', str(self.graph_xlim))
        self.config.set('Graph', 'ylabel', self.graph_ylabel)
        self.config.set('Graph', 'ylim', str(self.graph_ylim))
        self.config.set('Graph', 'initial_slots', str(self.graph_initial_slots))
        self.config.set('Graph', 'colors', self.graph_colors)

        with open('backend/settings.ini', 'w') as f:
            self.config.write(f)
            f.close()

    def restart_gui(self, root):
        # Close the tkinter window
        global firstrun
        firstrun = False
        root.destroy()
        # Restart gui
        global_start_gui()

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.master.iconbitmap("icon_transparent-01.ico")
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

        # Enable window screenshots in debug mode
        if self.settings.debug_mode:
            self.master.bind('<Control-s>', lambda e: self.optionsmenu.debug_ssgui(e))

        backend.set_do_dmg_prints(self.settings.do_dmg_prints)

    def initGUI(self):
        # Load settings
        self.load_settings()

        # Load menus
        self.graphmenu = GraphMenu(self)
        self.weaponsmenu = WeaponsMenu(self)
        self.optionsmenu = OptionsMenu(self)
        self.logmenu = LogMenu(self)

        self.navbar = NavBar(self, [
            self.graphmenu,
            self.weaponsmenu,
            self.optionsmenu,
            self.logmenu,
        ])

        # Log mode
        redirect_logs(self.logmenu.log_text, self.settings.log_mode)
        # Auto import
        if firstrun:
            if self.settings.do_auto_save:
                if os.path.exists(self.settings.auto_save_path):
                    self.optionsmenu.import_weps_hdlr(self.settings.auto_save_path)
                else:
                    print(f'Auto Import Error: Expected file at `{self.settings.auto_save_path}` and none existed')
        
        # Initial weaponsmenu
        self.util_update_wep_names(first=True)
        self.weaponsmenu.show_new_weapon()

        # Display navbar and first menu
        self.navbar.pack(side=tk.LEFT, fill=tk.Y)
        self.graphmenu.pack(side=tk.RIGHT, fill=tk.Y)

    def util_update_wep_names(self, first:bool=False):
        self.graphmenu.update_weapons()
        self.weaponsmenu.update_weapons(first=first)

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
    # Use PhotoImage to open the PNG file
    img = tk.PhotoImage(file='images/simpleicon-notext.png')
    # Set the window icon
    root.iconphoto(False, img)
    #root.iconbitmap("icon_transparent-01.ico")
    app = GUI(master=root)
    app.mainloop()

global firstrun
firstrun = True
stdoutwrite = sys.stdout.write
global_start_gui()