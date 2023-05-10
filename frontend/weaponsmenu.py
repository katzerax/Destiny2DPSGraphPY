import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pprint import pprint
import backend.backend as backend

class WeaponsMenu(tk.Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.config(**self.master.frame_style)
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.navname = 'Weapons'

        self.frame_style = self.master.frame_style.copy()
        self.frame_style['highlightthickness'] = 0

        self.init_menu()

    def init_menu(self):
        self.creation_ui()
        self.pack_forget()

    def creation_ui(self):
        # Base frame
        cf = self.creation_frame = tk.Frame(self, **self.frame_style)
        self.creation_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Combobox options
        type_options = ['Single Weapon', 'Weapon Swap']
        perk_choices = [value[0] for value in backend.PERKS_LIST.values()]

        # Input validation
        val_int = self.register(self.master.util_valint)
        val_float = self.register(self.master.util_valfloat)

        # Widget vars
        self.creation_vars = {
            'name': tk.StringVar(),
            'dmg_per_shot': tk.IntVar(),
            'mag_cap': tk.IntVar(),
            'ammo_total': tk.IntVar(),
            'enhance1': tk.BooleanVar(),
            'enhance2': tk.BooleanVar(),
            'burst_wep': tk.BooleanVar(),
            'burst_bullets': tk.IntVar(),
            'fusion_wep': tk.BooleanVar()
        }

        # Widgets
        self.creation_widgets = {
            'header': tk.Label(cf, text="Weapon Creation", **self.master.label_style),

            'type': (tk.Label(cf, text="Type", **self.master.label_style),
                    ttk.Combobox(cf, values=type_options, width=17, state='disabled')),

            'name': (tk.Label(cf, text="Name", **self.master.label_style),
                    tk.Entry(cf, textvariable=self.creation_vars['name'])),

            'fire_rate': (tk.Label(cf, text="Fire Rate", **self.master.label_style),
                          tk.Entry(cf, validate='key', validatecommand=(val_float, '%S'))),

            'reload_time': (tk.Label(cf, text="Reload Time", **self.master.label_style),
                            tk.Entry(cf, validate='key', validatecommand=(val_float, '%S'))),

            'dmg_per_shot': (tk.Label(cf, text="Damage per Shot", **self.master.label_style),
                                tk.Entry(cf, textvariable=self.creation_vars['dmg_per_shot'],
                                         validate='key', validatecommand=(val_int, '%S'))),

            'mag_cap': (tk.Label(cf, text="Magazine Capacity", **self.master.label_style),
                         tk.Entry(cf, textvariable=self.creation_vars['mag_cap'],
                                  validate='key', validatecommand=(val_int, '%S'))),

            'ammo_total': (tk.Label(cf, text="Ammo Total", **self.master.label_style),
                             tk.Entry(cf, textvariable=self.creation_vars['ammo_total'],
                                      validate='key', validatecommand=(val_int, '%S'))),

            'perk1': (tk.Label(cf, text="Perk 1", **self.master.label_style),
                      ttk.Combobox(cf, values=perk_choices, **self.master.combo_style)),

            'perk2': (tk.Label(cf, text="Perk 2", **self.master.label_style),
                      ttk.Combobox(cf, values=perk_choices, **self.master.combo_style)),

            'enhance': (tk.Checkbutton(cf, text="Perk 1 Enhanced", 
                                        variable=self.creation_vars['enhance1'], **self.master.check_button_style),
                        tk.Checkbutton(cf, text="Perk 2 Enhanced", 
                                        variable=self.creation_vars['enhance2'], **self.master.check_button_style)),

            'burst_fusion_toggle': (tk.Checkbutton(cf, text="Burst Weapon", variable=self.creation_vars['burst_wep'],
                                                    command=self.toggle_burst, **self.master.check_button_style),
                                    tk.Checkbutton(cf, text="Fusion Weapon", variable=self.creation_vars['fusion_wep'],
                                                   **self.master.check_button_style)),

            'burst_bullets': (tk.Label(cf, text="Bullets Per Burst", **self.master.label_style),
                              tk.Entry(cf, textvariable=self.creation_vars['burst_bullets'],
                                       validate='key', validatecommand=(val_int, '%S'))),

            'create_wep': tk.Button(cf, text="Create Weapon", command=self.create_weapon_hdlr, **self.master.button_style)
        }

        # Default vals
        self.creation_widgets['type'][1].set(type_options[0])
        self.creation_widgets['perk1'][1].set(perk_choices[0])
        self.creation_widgets['perk2'][1].set(perk_choices[0])
        self.creation_widgets['fire_rate'][1].insert(0, '0')
        self.creation_widgets['reload_time'][1].insert(0, '0')

        # Grid placement
        for idx, keyval in enumerate(self.creation_widgets.copy().items()):
            key, multi = keyval
            # Just place single objects in (x, 0)
            if not type(multi) is tuple:
                multi.grid(row=(idx+1), column=0, **self.master.default_padding)
                # Save grid column into tuple
                self.creation_widgets[key] = (multi, idx+1)
                continue
            # Place tuples in (x, 0) (x, 1)
            label, usrinput = multi
            label.grid(row=(idx+1), column=0, **self.master.default_padding)
            usrinput.grid(row=(idx + 1), column=1, **self.master.default_padding)
            self.creation_widgets[key] = (label, usrinput, idx+1)
            # Bind defocus to combos
            if isinstance(usrinput, ttk.Combobox):
                usrinput.bind("<<ComboboxSelected>>",lambda e: self.focus())

        # Hide on start
        self.creation_widgets['burst_bullets'][0].grid_forget()
        self.creation_widgets['burst_bullets'][1].grid_forget()

    def toggle_burst(self):
        label, entry, row = self.creation_widgets['burst_bullets']
        if label.winfo_viewable():
            label.grid_forget()
            entry.grid_forget()
        else:
            label.grid(row=row, column=0, **self.master.default_padding)
            entry.grid(row=row, column=1, **self.master.default_padding)

    def create_weapon_hdlr(self):
        exitcode = self.create_weapon()
        basestr = f'Weapon creation exited with code {exitcode}:'
        match exitcode:
            case 0:
                # NOTE by all means if you are gonna change this do so
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
        
    def create_weapon(self):
        # Strings
        name = self.creation_vars['name'].get()

        # Floats
        try:
            fire_rate = float(self.creation_widgets['fire_rate'][1].get())
            reload_time = float(self.creation_widgets['reload_time'][1].get())
        except ValueError:
            return 2

        # Integers
        dmg_per_shot = self.creation_vars['dmg_per_shot'].get()
        mag_cap = self.creation_vars['mag_cap'].get()
        ammo_total = self.creation_vars['ammo_total'].get()
        burst_bullets = self.creation_vars['burst_bullets'].get()

        # Bools
        enhance1 = self.creation_vars['enhance1'].get()
        enhance2 = self.creation_vars['enhance2'].get()
        burst_wep = self.creation_vars['burst_wep'].get()
        fusion_wep = self.creation_vars['fusion_wep'].get()

        # Validation
        for teststr in [name]:
            if not self.test_str(teststr):
                return 1

        for testfloat in [fire_rate, reload_time]:
            if not self.test_float(testfloat):
                return 2

        ints = [dmg_per_shot, mag_cap, ammo_total]
        if burst_wep:
            ints.append(burst_bullets)

        for testint in ints:
            if not self.test_int(testint):
                return 3
        
        # Perks
        perk1 = self.creation_widgets['perk1'][1].get()
        perk2 = self.creation_widgets['perk2'][1].get()
        perk_indices = [index for index, perkname in backend.PERKS_LIST.items() if list(perkname)[0] in [perk1, perk2]]
        perk_indices = None if perk_indices == [0] else perk_indices

        weapon_options = {
            'name': str(name),
            'fire_rate': float(fire_rate),
            'reload_time': float(reload_time),
            'damage_per_shot': int(dmg_per_shot),
            'mag_cap': int(mag_cap),
            'ammo_total': int(ammo_total),
            'fusion_weapon': bool(fusion_wep),
            'burst_weapon': bool(burst_wep),
            'burst_bullets': int(burst_bullets),
            'perk_indices': perk_indices,
            'enhance1': bool(enhance1),
            'enhance2': bool(enhance2)
        }
        print('Attempting to create weapon with options:')
        pprint(weapon_options, sort_dicts=False)

        if backend.create_weapon(weapon_options):
            self.master.graphmenu.update_weapons()
            if self.master.settings.do_auto_save and self.master.settings.auto_save_path:
                self.master.optionsmenu.export_weps_hdlr(self.master.settings.auto_save_path)
            return 0
        else:
            return 4
        
    def test_str(self, target):
        if len(target) < 1:
            return False
        else:
            return True

    def test_int(self, target):
        try:
            x = int(target)
            if x <= 0:
                return False
            else:
                return True
        except ValueError:
            return False

    def test_float(self, target):
        try:
            x = float(target)
            if x <= 0:
                return False
            else:
                return True
        except ValueError:
            return False