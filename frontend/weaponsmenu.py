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
        self.buff_ui()
        self.pack_forget()

    def creation_ui(self):
        # Base frame
        cf = self.creation_frame = tk.Frame(self, **self.frame_style)
        self.creation_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Combobox options
        self.perk_choices = [value[0] for value in backend.PERKS_LIST.values()]
        self.origin_choices = [value[0] for value in backend.ORIGIN_TRAITS_LIST.values()]

        # Input validation
        val_int = self.register(self.master.util_valint)
        val_float = self.register(self.master.util_valfloat)

        # Widget vars
        self.creation_vars = {
            'name': tk.StringVar(),
            'fire_rate': tk.StringVar(),
            'reload_time': tk.StringVar(),
            'damage_per_shot': tk.IntVar(),
            'mag_cap': tk.IntVar(),
            'ammo_total': tk.IntVar(),
            'enhance1': tk.BooleanVar(),
            'enhance2': tk.BooleanVar(),
            'burst_weapon': tk.BooleanVar(),
            'burst_bullets': tk.IntVar(),
            'fusion_weapon': tk.BooleanVar()
        }

        # Widgets
        self.creation_widgets = {
            'header': tk.Label(cf, text="Weapon Creation", **self.master.label_style),

            'weapon': (tk.Label(cf, text="Weapon", **self.master.label_style),
                    ttk.Combobox(cf, **self.master.combo_style)),

            'name': (tk.Label(cf, text="Name", **self.master.label_style),
                    tk.Entry(cf, textvariable=self.creation_vars['name'])),

            'fire_rate': (tk.Label(cf, text="Fire Rate", **self.master.label_style),
                          tk.Entry(cf, textvariable=self.creation_vars['fire_rate'], 
                                    validate='key', validatecommand=(val_float, '%S'))),

            'reload_time': (tk.Label(cf, text="Reload Time", **self.master.label_style),
                            tk.Entry(cf, textvariable=self.creation_vars['reload_time'],
                                     validate='key', validatecommand=(val_float, '%S'))),

            'damage_per_shot': (tk.Label(cf, text="Damage per Shot", **self.master.label_style),
                                tk.Entry(cf, textvariable=self.creation_vars['damage_per_shot'],
                                         validate='key', validatecommand=(val_int, '%S'))),

            'mag_cap': (tk.Label(cf, text="Magazine Capacity", **self.master.label_style),
                         tk.Entry(cf, textvariable=self.creation_vars['mag_cap'],
                                  validate='key', validatecommand=(val_int, '%S'))),

            'ammo_total': (tk.Label(cf, text="Ammo Total", **self.master.label_style),
                             tk.Entry(cf, textvariable=self.creation_vars['ammo_total'],
                                      validate='key', validatecommand=(val_int, '%S'))),

            'perk1': (tk.Label(cf, text="Perk 1", **self.master.label_style),
                      ttk.Combobox(cf, values=self.perk_choices, **self.master.combo_style)),

            'perk2': (tk.Label(cf, text="Perk 2", **self.master.label_style),
                      ttk.Combobox(cf, values=self.perk_choices, **self.master.combo_style)),

            'origin_trait': (tk.Label(cf, text="Origin Trait", **self.master.label_style),
                             ttk.Combobox(cf, values=self.origin_choices, **self.master.combo_style)),

            'enhance': (tk.Checkbutton(cf, text="Perk 1 Enhanced", 
                                        variable=self.creation_vars['enhance1'], **self.master.check_button_style),
                        tk.Checkbutton(cf, text="Perk 2 Enhanced", 
                                        variable=self.creation_vars['enhance2'], **self.master.check_button_style)),

            'burst_fusion_toggle': (tk.Checkbutton(cf, text="Burst Weapon", variable=self.creation_vars['burst_weapon'],
                                                    command=self.toggle_burst, **self.master.check_button_style),
                                    tk.Checkbutton(cf, text="Fusion Weapon", variable=self.creation_vars['fusion_weapon'],
                                                   **self.master.check_button_style)),

            'burst_bullets': (tk.Label(cf, text="Bullets Per Burst", **self.master.label_style),
                              tk.Entry(cf, textvariable=self.creation_vars['burst_bullets'],
                                       validate='key', validatecommand=(val_int, '%S'))),

            'interface': (tk.Button(cf, text="Create Weapon", command=self.create_weapon_hdlr, **self.master.button_style),
                          tk.Button(cf, text='Edit Weapon', command=lambda: self.create_weapon_hdlr(editing=True), **self.master.button_style),
                          tk.Button(cf, text='Delete Weapon', command=self.delete_weapon, **self.master.button_style))
        }

        # Grid placement
        for idx, (name, widgset) in enumerate(self.creation_widgets.copy().items()):
            # Deal with interface buttons later
            if name == 'interface':
                continue
            # Single objects
            grid = ({'row': idx, 'column': 0},
                    {'row': idx, 'column': 1})
            if not type(widgset) is tuple:
                widgset.grid(**grid[0], **self.master.default_padding)
                self.creation_widgets[name] = (widgset, grid[0])
                continue
            # Multi objects
            for idy, widget in enumerate(widgset):
                widget.grid(**grid[idy], **self.master.default_padding)
                # Bind defocus to combos
                if isinstance(widget, ttk.Combobox):
                    widget.bind("<<ComboboxSelected>>",lambda e: self.focus())
            obj1, obj2 = widgset
            self.creation_widgets[name] = (obj1, obj2, grid)

        # Bind extra functions
        self.creation_widgets['weapon'][1].bind('<<ComboboxSelected>>', lambda _: self.select_weapon())

    def buff_ui(self):
        cf = self.buff_frame = tk.Frame(self, **self.frame_style)
        self.buff_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.buff_widgets = {
            'header': tk.Label(cf, text='Buff / Debuff Calculator', **self.master.label_style),

            'deb': (tk.Label(cf, text='Debuff', **self.master.label_style),
                       ttk.Combobox(cf, **self.master.combo_style)),
            
            'deb_opt': tk.Checkbutton(cf, text='Constantly Applied', **self.master.check_button_style),

            'buff': (tk.Label(cf, text='Empower', **self.master.label_style),
                     ttk.Combobox(cf, **self.master.combo_style)),

            'buff_opt': tk.Checkbutton(cf, text='Constantly Applied', **self.master.check_button_style),

            'wdmg': (tk.Label(cf, text='Weapon Damage', **self.master.label_style),
                       ttk.Combobox(cf, **self.master.combo_style)),
            
            'wdmg_opt': tk.Checkbutton(cf, text='Constantly Applied', **self.master.check_button_style),

            'header2': tk.Label(cf, text='Misc', **self.master.label_style),

            'packhunter': tk.Checkbutton(cf, text='Wolfpack Rounds', **self.master.check_button_style),

            'pad': tk.Label(cf, text='', **self.master.label_style),

            'total': (tk.Label(cf, text='Total Multiplier', **self.master.label_style),
                     ttk.Entry(cf))
        }

        for idx, (name, widgset) in enumerate(self.buff_widgets.copy().items()):
            # Deal with interface buttons later
            if name == 'interface':
                continue
            # Single objects
            grid = ({'row': idx, 'column': 0},
                    {'row': idx, 'column': 1})
            if not type(widgset) is tuple:
                widgset.grid(**grid[0], **self.master.default_padding)
                self.buff_widgets[name] = (widgset, grid[0])
                continue
            # Multi objects
            for idy, widget in enumerate(widgset):
                widget.grid(**grid[idy], **self.master.default_padding)
                # Bind defocus to combos
                if isinstance(widget, ttk.Combobox):
                    widget.bind("<<ComboboxSelected>>",lambda e: self.focus())
            obj1, obj2 = widgset
            self.buff_widgets[name] = (obj1, obj2, grid)

    def update_weapons(self, first:bool=False):
        wep_names = list(backend.weapons_list.keys())
        # Disable selection if no weapons
        state = 'disabled' if not wep_names else 'readonly'

        wep_names.append('New Weapon')
        self.creation_widgets['weapon'][1].config(values=wep_names, state=state)
        if first:
            self.creation_widgets['weapon'][1].set(wep_names[-1])

    def select_weapon(self, name:str=None, *_):
        wep_name = self.creation_widgets['weapon'][1].get() if name is None else name
        current_weps = list(backend.weapons_list.keys())

        if not wep_name in current_weps:
            self.show_new_weapon()
        else:
            self.creation_widgets['weapon'][1].set(wep_name)
            self.show_existing_weapon(weapon=backend.weapons_list[wep_name])

        self.focus()

    def show_new_weapon(self):
        # How many weapons exist named 'New Weapon {x}'
        new_weps_count = len([name for name in backend.weapons_list.keys() if name.startswith('New Weapon')]) + 1

        # Tk vars
        for var in self.creation_vars.values():
            if isinstance(var, tk.StringVar):
                var.set(str(0))
            var.set(0)
        self.creation_vars['name'].set(f'New Weapon {new_weps_count}')

        # Listboxes
        self.creation_widgets['perk1'][1].set(self.perk_choices[0])
        self.creation_widgets['perk2'][1].set(self.perk_choices[0])
        self.creation_widgets['origin_trait'][1].set(self.origin_choices[0])

        # Hide
        self.creation_widgets['burst_bullets'][0].grid_forget()
        self.creation_widgets['burst_bullets'][1].grid_forget()

        # Show creation button
        if self.creation_widgets['interface'][1].winfo_viewable():
            self.creation_widgets['interface'][1].grid_forget()
            self.creation_widgets['interface'][2].grid_forget()
        row = len(self.creation_widgets) + 1
        self.creation_widgets['interface'][0].grid(row=row, column=0, **self.master.default_padding)

    def show_existing_weapon(self, weapon:backend.Weapon):
        wep_settings = weapon.get_full_settings()

        # Tk vars
        for set_name, value in wep_settings.items():
            if set_name in self.creation_vars.keys():
                if isinstance(self.creation_vars[set_name], tk.StringVar):
                    self.creation_vars[set_name].set(str(value))
                if type(value) is bool:
                    value = 0 if value == False else 1
                self.creation_vars[set_name].set(value)

        # Perks
        if wep_settings['perk_indices']:
            if len(wep_settings['perk_indices']) == 1:
                self.creation_widgets['perk1'][1].set(self.perk_choices[wep_settings['perk_indices'][0]])
                self.creation_widgets['perk2'][1].set(self.perk_choices[0])
            else:
                for idx, index in enumerate(wep_settings['perk_indices']):
                    self.creation_widgets[f'perk{idx+1}'][1].set(self.perk_choices[index])
        else:
            self.creation_widgets['perk1'][1].set(self.perk_choices[0])
            self.creation_widgets['perk2'][1].set(self.perk_choices[0])

        # Origin Traits
        if wep_settings['origin_trait']:
                self.creation_widgets['origin_trait'][1].set(self.origin_choices[wep_settings['origin_trait']])
        else:
            self.creation_widgets['origin_trait'][1].set(self.origin_choices[0])

        # Show or hide burst bullets
        if wep_settings['burst_weapon']:
            if not self.creation_widgets['burst_bullets'][0].winfo_viewable():
                self.toggle_burst()
        else:
            if self.creation_widgets['burst_bullets'][0].winfo_viewable():
                self.toggle_burst()

        # Show edit / delete buttons
        if self.creation_widgets['interface'][0].winfo_viewable():
            self.creation_widgets['interface'][0].grid_forget()
        row = len(self.creation_widgets) + 1
        self.creation_widgets['interface'][1].grid(row=row, column=0, **self.master.default_padding)
        self.creation_widgets['interface'][2].grid(row=row, column=1, **self.master.default_padding)
  
    def toggle_burst(self):
        label, entry, (grid1, grid2) = self.creation_widgets['burst_bullets']
        if label.winfo_viewable():
            label.grid_forget()
            entry.grid_forget()
        else:
            label.grid(**grid1, **self.master.default_padding)
            entry.grid(**grid2, **self.master.default_padding)

    def create_weapon_hdlr(self, editing:bool=False):
        exitcode = self.create_weapon(editing=editing)
        verb1, verb2, verb3 = ('Edit', 'edited', 'editing') if editing else ('Creation', 'created', 'creating')
        basestr = f'Weapon {verb1} exited with code {exitcode}:'
        match exitcode:
            case 0:
                # NOTE by all means if you are gonna change this do so
                messagebox.showinfo('Success', f'Weapon {verb2} successfully')
                print(f'{basestr} Success')
            case 1:
                messagebox.showerror('Name Error', 'The name "New Weapon" is not allowed.')
                print(f'{basestr} Name Error')
            case 2:
                print(f'{basestr} Overwrite Denied')
            case 3:
                messagebox.showerror('Name Error', 'Make sure the name for your weapon contains at least one letter.')
                print(f'{basestr} Name Error')
            case 4:
                messagebox.showerror('Float Error', 'Make sure Fire Rate and Reload Time are valid numbers.')
                print(f'{basestr} Floating Point Error')
            case 5:
                messagebox.showerror('Integer Error', 'Make sure Damage per Shot, Mag Size, and Ammo Total are valid numbers.')
                print(f'{basestr} Integer Error')
            case 6:
                messagebox.showerror('Deletion Error', 'You should have never hit this error! Please report this as an issue on Github!')
                print(f'{basestr} Unknown Error')
            case _:
                messagebox.showerror(f'{verb1} Error', f'There was an error {verb3} your weapon')
                print(f'{basestr} Unknown Error')
        
    # NOTE I merged creation with editing but they could (and probably should) be split
    # result would likely be 5 methods (2 already): gather_fields, create, create_hdlr, edit, edit_hdlr
    def create_weapon(self, editing:bool=False):
        # Strings
        name = self.creation_vars['name'].get().strip()
        if name == 'New Weapon':
            return 1
        if not editing:
            if name in backend.weapons_list.keys():
                confirm = messagebox.askokcancel('Creation Warning', f'A weapon named "{name}" already exists!\nProceeding will overwrite the configuration of "{name}".')
                if not confirm:
                    return 2
            name_change = False
        else:
            old_name = self.creation_widgets['weapon'][1].get()
            confirm = messagebox.askokcancel('Edit Warning', f'Are you sure you want to edit "{old_name}"?\nProceeding will overwrite the configuration of "{old_name}".')
            if not confirm:
                return 2
            name_change = False if name == old_name else True

        # Validate name
        for teststr in [name]:
            if not self.test_str(teststr):
                return 3

        # Floats
        try:
            fire_rate = float(self.creation_vars['fire_rate'].get())
            reload_time = float(self.creation_vars['reload_time'].get())
            for testfloat in [fire_rate, reload_time]:
                if not self.test_float(testfloat):
                    return 4
        except ValueError:
            return 4

        # Integers
        damage_per_shot = self.creation_vars['damage_per_shot'].get()
        mag_cap = self.creation_vars['mag_cap'].get()
        ammo_total = self.creation_vars['ammo_total'].get()
        burst_bullets = self.creation_vars['burst_bullets'].get()

        # Bools
        enhance1 = self.creation_vars['enhance1'].get()
        enhance2 = self.creation_vars['enhance2'].get()
        burst_weapon = self.creation_vars['burst_weapon'].get()
        fusion_weapon = self.creation_vars['fusion_weapon'].get()

        # Integers (continued)
        ints = [damage_per_shot, mag_cap, ammo_total]
        if burst_weapon:
            ints.append(burst_bullets)
        for testint in ints:
            if not self.test_int(testint):
                return 5

        # Perks
        perk1 = self.creation_widgets['perk1'][1].get()
        perk2 = self.creation_widgets['perk2'][1].get()
        perk_indices = [index for index, perkname in backend.PERKS_LIST.items() if list(perkname)[0] in [perk1, perk2]]
        perk_indices = None if perk_indices == [0] else perk_indices

        # Origin Trait
        origin_trait = self.creation_widgets['origin_trait'][1].get()
        for idx, (otname, _, _ ) in backend.ORIGIN_TRAITS_LIST.items():
            if origin_trait == otname:
                origin_trait = idx
                break

        weapon_options = {
            'name': str(name),
            'fire_rate': float(fire_rate),
            'reload_time': float(reload_time),
            'damage_per_shot': int(damage_per_shot),
            'mag_cap': int(mag_cap),
            'ammo_total': int(ammo_total),
            'fusion_weapon': bool(fusion_weapon),
            'burst_weapon': bool(burst_weapon),
            'burst_bullets': int(burst_bullets),
            'perk_indices': perk_indices,
            'enhance1': bool(enhance1),
            'enhance2': bool(enhance2),
            'origin_trait': origin_trait
        }

        verb = 'edit' if editing else 'create'
        print(f'Attempting to {verb} weapon with options:')
        pprint(weapon_options, sort_dicts=False)

        if name_change:
                if backend.delete_weapon(old_name):
                    if backend.create_weapon(weapon_options):
                        self.master.util_update_wep_names()
                        if self.master.settings.do_auto_save and self.master.settings.auto_save_path:
                            self.master.optionsmenu.export_weps_hdlr(self.master.settings.auto_save_path)
                        self.select_weapon(name=name)
                        return 0
                    else:
                        return 5
                else:
                    return 6

        if backend.create_weapon(weapon_options):
            self.master.util_update_wep_names()
            if self.master.settings.do_auto_save and self.master.settings.auto_save_path:
                self.master.optionsmenu.export_weps_hdlr(self.master.settings.auto_save_path)
            self.select_weapon(name=name)
            return 0
        else:
            return 5
        
    # NOTE Probably should use a handler for this but its literally 2 possible errors
    # and second error case should never happen anyway
    def delete_weapon(self):
        name = self.creation_vars['name'].get()

        confirm = messagebox.askokcancel('Deletion Warning', f'Are you sure you want to delete "{name}"?\nProceeding will permanently delete the configuration of "{name}".')
        if not confirm:
            print('Weapon Deletion exited with code 1: Deletion Denied')
            return
        
        if backend.delete_weapon(name):
            messagebox.showinfo('Success', f'Weapon deleted successfully')
            self.master.util_update_wep_names()
            if self.master.settings.do_auto_save and self.master.settings.auto_save_path:
                self.master.optionsmenu.export_weps_hdlr(self.master.settings.auto_save_path)
            self.show_new_weapon()
            self.update_weapons(first=True)
            print('Weapon Deletion exited with code 0: Success')
            return
        else:
            messagebox.showinfo('Deletion Error', 'You should have never hit this error! Please report this as an issue on Github!')
            print('Weapon Deletion exited with code 2: Unknown Error')
            return

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