import os
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
import backend.backend as backend

class OptionsMenu(tk.Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.config(**self.master.frame_style)
        self.pack()
        self.navname = 'Options'

        self.frame_style = self.master.frame_style.copy()
        self.frame_style['highlightthickness'] = 0

        self.init_menu()

    def init_menu(self):
        self.options_ui()
        self.pack_forget()

    def options_ui(self):
        # Combobox options
        interface_theme_choices = ['Dark', 'Light']
        interface_logmode_choices = ['App', 'Console', 'Both']
        exp_exts = ['json', 'csv', 'pickle']
        graph_initial_slot_choices = [str(i+1) for i in range(10)]
        graph_saved_colors = False if self.master.settings.graph_colors == 'random' else True

        # Input validation
        val_int = self.register(self.master.util_valint)

        # Widget vars
        self.menu_vars = {
            'autosave': tk.BooleanVar(value=self.master.settings.do_auto_save),
            'autosave_path': tk.StringVar(value=self.master.settings.auto_save_path),
            'debug_mode': tk.BooleanVar(value=self.master.settings.debug_mode),
            'dmg_prints': tk.BooleanVar(value=self.master.settings.do_dmg_prints),
            'graph_title': tk.StringVar(value=self.master.settings.graph_title),
            'graph_xlabel': tk.StringVar(value=self.master.settings.graph_xlabel),
            'graph_xlim': tk.IntVar(value=self.master.settings.graph_xlim),
            'graph_ylabel': tk.StringVar(value=self.master.settings.graph_ylabel),
            'graph_ylim': tk.IntVar(value=self.master.settings.graph_ylim),
            'graph_initial_slots': tk.IntVar(value=self.master.settings.graph_initial_slots),
            'graph_colors': tk.BooleanVar(value=graph_saved_colors)
        }
        # Widgets
        self.menu_widgets = {
            # Graph
            'graph': {
                'header': [tk.Label(self, text='Graph', **self.master.label_style)],

                'title': [tk.Label(self, text='Graph Title', **self.master.label_style),
                          tk.Entry(self, textvariable=self.menu_vars['graph_title'])],

                'xlabel': [tk.Label(self, text='X Axis Name', **self.master.label_style),
                           tk.Entry(self, textvariable=self.menu_vars['graph_xlabel'])],

                'xlim': [tk.Label(self, text='X Axis Upper Limit', **self.master.label_style),
                         tk.Entry(self, textvariable=self.menu_vars['graph_xlim'],
                                 validate='key', validatecommand=(val_int, '%S'))],

                'ylabel': [tk.Label(self, text='Y Axis Name', **self.master.label_style),
                           tk.Entry(self, textvariable=self.menu_vars['graph_ylabel'])],

                'ylim': [tk.Label(self, text='Y Axis Upper Limit', **self.master.label_style),
                         tk.Entry(self, textvariable=self.menu_vars['graph_ylim'],
                                 validate='key', validatecommand=(val_int, '%S'))],

                'initial_slots': [tk.Label(self, text='Initial Weapon Slots', **self.master.label_style),
                                  ttk.Combobox(self, values=graph_initial_slot_choices, width=3, state='readonly')],
                
                'initial_slots:go': [{}, {'sticky': 'NSW'}],

                'colors': [tk.Checkbutton(self, text='Save Current Colors',
                                          variable=self.menu_vars['graph_colors'], **self.master.check_button_style)],
            },
            # Import / Export
            'impexp': {
                'header': [tk.Label(self, text='Import / Export', **self.master.label_style)],

                'export': [tk.Button(self, text='Export As', 
                                     command=self.export_weps_hdlr, **self.master.button_style),
                           ttk.Combobox(self, values=exp_exts, **self.master.combo_style)],

                'export:go': [{}, {'sticky': 'NSEW'}],

                'log_impff': [tk.Button(self, text='Log Current Weapons', 
                                        command=self.print_weps, **self.master.button_style),
                              tk.Button(self, text='Import From File', 
                                        command=self.import_weps_hdlr, **self.master.button_style)],

                'auto_save_toggle': [tk.Checkbutton(self, text='Auto Save / Load', variable=self.menu_vars['autosave'], 
                                                   command=self.toggle_autosave, **self.master.check_button_style)],

                'auto_save_path': [tk.Button(self, text='Auto-Save Path',
                                             command=self.set_auto_import_hdlr, **self.master.button_style),
                                   tk.Entry(self, textvariable=self.menu_vars['autosave_path'], state='readonly')],

                'auto_save_path:go': [{}, {'sticky': 'NSEW'}]
            },
            # GUI
            'interface': {
                'header': [tk.Label(self, text='Interface', **self.master.label_style)],

                'theme': [tk.Label(self, text='Theme', **self.master.label_style),
                          ttk.Combobox(self, values=interface_theme_choices, **self.master.combo_style)],

                'logmode': [tk.Label(self, text='Log Mode', **self.master.label_style),
                            ttk.Combobox(self, values=interface_logmode_choices, **self.master.combo_style)],

                'debugmode_dmgprints': [tk.Checkbutton(self, text='Debug Mode', **self.master.check_button_style,
                                                       variable=self.menu_vars['debug_mode']),
                                        tk.Checkbutton(self, text='Print Dmg Steps', **self.master.check_button_style,
                                                       variable=self.menu_vars['dmg_prints'])]
            },
        }

        # Debug mode widgets
        if self.master.settings.debug_mode:
            self.menu_widgets['debug'] = {
                'header': [tk.Label(self, text='Debug', **self.master.label_style)],

                'clearcache': [tk.Button(self, text='Clear Graph Cache',
                                        command=self.debug_ccache, **self.master.button_style),
                                tk.Button(self, text='testfunc :)',
                                          command=self.debug_testfunc, **self.master.button_style)]
            }

        # Default combobox vals
        self.menu_widgets['impexp']['export'][1].set(exp_exts[0])
        self.menu_widgets['interface']['theme'][1].set(self.master.settings.interface_theme)
        self.menu_widgets['interface']['logmode'][1].set(self.master.settings.log_mode)
        self.menu_widgets['graph']['initial_slots'][1].set(self.master.settings.graph_initial_slots)

        # Bind extra functions
        self.menu_widgets['impexp']['auto_save_path'][0].bind('<Button-3>', self.clear_auto_import)

        # Grid placement
        max_outer_column = 2
        self.menu_containers = {}
        # Create 2D array with xlim of max_outer_column
        outer_columns =\
            [list(self.menu_widgets.copy().items())[x:x+max_outer_column] for x in range(0, len(self.menu_widgets), max_outer_column)]
        # Outer x
        for idx, outer_row in enumerate(outer_columns):
            # Outer y
            for idy, (group, widgets) in enumerate(outer_row):
                # Create container frames for each group
                container = self.menu_containers[group] = tk.Frame(self, **self.frame_style)
                container.grid(row=idx, column=idy, sticky='NSEW')

                # Grid each widget to its container
                rewind = 0
                offset = 1 if idx > 0 else 0
                for idz, (setname, widgset) in enumerate(widgets.items()):

                    # Grid overides
                    if ':go' in setname:
                        origname = setname.split(':go')[0]
                        for idc, obj in enumerate(widgets[origname]):
                            obj.grid_configure(**widgset[idc])
                        rewind += 1
                        continue

                    # Default gridding
                    gi = {'in_': container, 'row': offset+idz-rewind, 'padx': 5, 'pady': 5}
                    for idc, obj in enumerate(widgset):
                        sticky = 'NSW' if idc % 2 == 0 else 'NSE'   
                        if isinstance(obj, ttk.Combobox):
                            obj.bind("<<ComboboxSelected>>", lambda _: self.focus())
                        obj.grid(**gi, column=idc, sticky=sticky)
                        obj.lift()

            # Add interact buttons manually-ish
            if outer_row == outer_columns[-1]:
                fcont = self.menu_containers['interact_buttons'] = tk.Frame(self, **self.frame_style)
                fcont.grid(column=0, row=len(self.menu_containers)-1)
                for idv, obj in enumerate([tk.Button(fcont, text='Apply Settings', command=self.apply_settings, **self.master.button_style),
                                           tk.Button(fcont, text='Reset Settings', command=self.reset_settings, **self.master.button_style)]):
                    obj.grid(row=1, column=idv, padx=5, pady=5)

        for container in self.menu_containers.values():
            cols, rows = container.grid_size()
            for i in range(rows):
                container.grid_rowconfigure(
                    index=i,
                    minsize=36
                )
            for i in range(cols):
                container.grid_columnconfigure(
                    index=i,
                    weight=1
                )

        # Hide on start
        if not self.master.settings.do_auto_save:
            self.menu_widgets['impexp']['auto_save_path'][0].grid_remove()
            self.menu_widgets['impexp']['auto_save_path'][1].grid_remove()

    def clear_auto_import(self, *_):
        confirm = messagebox.askokcancel('Auto Save / Load Warning', 'Are you sure you want to clear your Auto Save / Load path?')
        if not confirm:
            return
        self.menu_vars['autosave_path'].set('')
        print('Auto Import path successfully cleared')

    def set_auto_import_hdlr(self):
        exitcode = self.set_auto_import()
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
                messagebox.showerror('Invalid File Type', 'Selected file must be of types: (.pickle, .json)')
                print(f'{basestr} Invalid File Type')
            case 4:
                messagebox.showerror('Invalid Pickle Data', 'Pickle data selected for import is invalid.')
                print(f'{basestr} Invalid Pickle Data')
        return exitcode

    def set_auto_import(self):
        confirm = messagebox.askokcancel('Import Warning', 'Setting auto import path will clear your current list and import from the selected file' +
                                        '\nDoing so will irreversably clear your current list. Make sure to export if you would like to keep your current list.',)
        if not confirm:
            return 1
        # File dialogue
        file_path = askopenfilename(filetypes=(('JSON Files', '*.json'), ('Pickle Files', '*.pickle'), ('All Files', '*.*')))
        if file_path == '':
            return 2
        if not file_path.endswith(('.pickle', '.json')):
            return 3
        exitcode = self.import_weps_hdlr(file_path)
        if not exitcode == 0:
            return 4
        self.menu_vars['autosave_path'].set(file_path)
        return 0

    def import_weps_hdlr(self, path:str=None):
        data = self.import_weps(path)
        if type(data) is tuple:
            exitcode, version = data
        else:
            exitcode = data
        basestr = f'Weapon Import exited with code {exitcode}:'
        match exitcode:
            case 0:
                if not path:
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
                messagebox.showerror('Pickle Version Mismatch', f'Pickle data was created with an outdated version of the program\n\
                                     You can fix this by importing this backup in version {version}, and exporting it to JSON. \
                                     This will result in an unavoidable loss of any cached weapon data')
                print(f'{basestr} Pickle Version Mismatch')
            case 7:
                messagebox.showerror('Import Error', 'An unknown error occured while importing your weapons. Check log for more info.')
                print(f'{basestr} How did you get here?')
            case _:
                messagebox.showerror('Import Error', 'An error occured while importing your weapons. Check log for more info.')
                print(f'An exception occured during Weapon Import:')
                pprint(exitcode)
        return exitcode

    def import_weps(self, path:str=None):
        # Warn about current list deletion
        if path is None:
            confirm = messagebox.askokcancel('Import Warning', 'Are you sure you want to import a list of weapons? \
                                            Doing so will irreversably clear your current list. Make sure to export if you would like to keep your current list.',)
            if not confirm:
                return 1
            # File dialogue
            file_path = askopenfilename(filetypes=(('JSON Files', '*.json'), ('Pickle Files', '*.pickle'), ('All Files', '*.*')))
            if file_path == '':
                return 2
            if not file_path.endswith(('.json', '.pickle')):
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
                    self.master.util_update_wep_names()
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
                        if not wep.backend_version == backend.VERSION:
                            reclaim(temp_bak)
                            return (6, wep.backend_version)
                    backend.weapons_list = data
                    self.master.util_update_wep_names()
                    return 0
            else:
                return 7
        except Exception as e:
            reclaim(temp_bak)
            return e
    
    def export_weps_hdlr(self, path:str=None):
        exitcode = self.export_weps(path)
        basestr = f'Weapon Export exited with code {exitcode}:'
        match exitcode:
            case 0:
                # NOTE Having a popup for a success is kinda aids ill work on something else
                if not path:
                    messagebox.showinfo('Success', 'Weapon list exported successfully')
                print(f'{basestr} Success')
            case 1:
                if not path:
                    messagebox.showerror('Empty Weapon List', 'There are no weapons currently available to export.')
                print(f'{basestr} Empty Weapon List')
            case 2:
                print(f'{basestr} No Path Selected')
            case 3:
                print(f'{basestr} Expected file at {self.master.settings.auto_save_path} that did not exist')
            case _:
                messagebox.showerror('Export Error', 'An error occured while exporting weapons. Check log for more info.')
                print(f'An exception occured during Weapon Export:')
                pprint(exitcode)

    def export_weps(self, path:str=None):
        if path is None:
            if len(backend.weapons_list) < 0:
                return 1
            ext = self.menu_widgets['impexp']['export'][1].get()
            file_path = asksaveasfile(defaultextension=f'.{ext}', filetypes=[('All Files', '*.*')], initialdir='./', initialfile=f'saved_weapons.{ext}')
            if file_path is None:
                return 2
            fpathname, ext = os.path.splitext(file_path.name) 
        else:
            if not os.path.exists(path):
                return 3
            fpathname, ext = os.path.splitext(path)
        try:
            match ext:
                case '.json':
                    d = [weapon.get_pruned_settings() for weapon in backend.weapons_list.values()]
                    with open(fpathname+ext, 'w') as f:
                        json.dump(d, f, indent=4)
                    return 0
                case '.csv':
                    d = [weapon.get_full_settings() for weapon in backend.weapons_list.values()]
                    d_names = d[0].keys()
                    with open(fpathname+ext, 'w', newline='') as f:  # 'newline=""' is often used to avoid extra newline on Windows
                        writer = csv.DictWriter(f, fieldnames=d_names)
                        writer.writeheader()
                        writer.writerows(d)
                    return 0
                case '.pickle' | _:
                    d = backend.weapons_list
                    with open(fpathname+ext, 'wb') as f:
                        pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
                    return 0
        except Exception as e:
            return e
    
    def toggle_autosave(self):
        label, entry, gridpos = self.menu_widgets['impexp']['auto_save_path']
        if label.winfo_viewable():
            label.grid_forget()
            entry.grid_forget()
        else:
            grid1, grid2 = gridpos
            label.grid(**grid1, **self.master.default_padding)
            entry.grid(**grid2, **self.master.default_padding)

    def print_weps(self):
        print('Current list of weapons:\n')
        for weapon in backend.weapons_list.values():
            settings = weapon.get_pruned_settings()
            pprint(settings, sort_dicts=False)
            print()

    def apply_settings(self):
        self.master.settings.interface_theme = self.menu_widgets['interface']['theme'][1].get()
        self.master.settings.log_mode = self.menu_widgets['interface']['logmode'][1].get()
        self.master.settings.debug_mode = self.menu_vars['debug_mode'].get()
        self.master.settings.do_dmg_prints = self.menu_vars['dmg_prints'].get()
        self.master.settings.do_auto_save = self.menu_vars['autosave'].get()
        self.master.settings.auto_save_path = self.menu_vars['autosave_path'].get()
        self.master.settings.graph_title = self.menu_vars['graph_title'].get()
        self.master.settings.graph_xlabel = self.menu_vars['graph_xlabel'].get()
        self.master.settings.graph_xlim = self.menu_vars['graph_xlim'].get()
        self.master.settings.graph_ylabel = self.menu_vars['graph_ylabel'].get()
        self.master.settings.graph_ylim = self.menu_vars['graph_ylim'].get()
        self.master.settings.graph_initial_slots = self.menu_widgets['graph']['initial_slots'][1].get()
        if self.menu_vars['graph_colors'].get():
            self.master.settings.graph_colors = ''.join(f'{e},' for e in self.master.graphmenu.colors).strip(',')
        else:
            self.master.settings.graph_colors = 'random'

        self.master.settings.save_settings()
        self.master.settings.restart_gui(self.master.master)

    def reset_settings(self):
        self.master.settings.reset_to_defaults()
        self.master.settings.restart_gui(self.master.master)

    def debug_ccache(self):
        if backend.weapons_list:
            for weapon in backend.weapons_list.values():
                if weapon.cached_graph_data:
                    weapon.cached_graph_data = None
                    print(f'Debug: Cached graph data cleared for: {weapon.name}')
    
    def debug_ssgui(self, *_):
        fname = f'./{str(time.time())}.png'
        cap = tkcap.CAP(self.master.master)
        cap.capture(fname)

    def debug_testfunc(self):
        pass