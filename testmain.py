import sys
import os
import configparser
import pickle
import json
import csv
import time
import tkinter as tk
import tkcap
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfilename
from pprint import pprint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import backend.backend as backend
from graph_menu import graph_menu

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

    # You guys may want to take a look at this
    #   YOU SET LIGHT MODE BY DEFAULT YOU MONSTER
    #   Other than that looks fine to me
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
                    'ylim': '300000'
                }
            }

            for section, settings in default_settings.items():
                self.config.add_section(section)
                for key, value in settings.items():
                    self.config.set(section, key, value)

            with open(ini_path, 'w', encoding='utf-8') as f:
                self.config.write(f)

    def reset_settings_to_defaults(self):
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

    def initGUI(self):
        self.load_settings()

        self.graphmenu = graph_menu(self)

def global_start_gui():
    global root
    root = tk.Tk()
    app = GUI(master=root)
    app.mainloop()

global firstrun
firstrun = True
stdoutwrite = sys.stdout.write
global_start_gui()