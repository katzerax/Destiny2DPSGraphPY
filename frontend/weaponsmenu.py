import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from math import prod
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
        # Combobox options
        self.perk_choices = [v[0] for v in backend.PERKS_LIST.values()]
        self.origin_choices = [v[0] for v in backend.ORIGIN_TRAITS_LIST.values()]

        self.buff_choices = {
            'buff': [v[0] for v in backend.BUFFS_LIST.values()],
            'deb': [v[0] for v in backend.DEBUFFS_LIST.values()],
            'wdmg': [v[0] for v in backend.WEAPON_BOOSTS_LIST.values()]
        }

        # Input validation
        val_int = self.register(self.master.util_valint)
        val_float = self.register(self.master.util_valfloat)

        # Widget vars
        self.menu_vars = {
            'creation': {
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
            },

            'buffcalc': {
                'deb_cnst': tk.BooleanVar(),
                'buff_cnst': tk.BooleanVar(),
                'wdmg_cnst': tk.BooleanVar(),
                'total': tk.StringVar()
            }
        }

        # Widgets
        self.menu_widgets = {
            # Create / edit / delete
            'creation': {
                'header': [tk.Label(self, text="Weapon Creation", **self.master.label_style)],

                'weapon': [tk.Label(self, text="Weapon", **self.master.label_style),
                           ttk.Combobox(self, **self.master.combo_style)],

                'name': [tk.Label(self, text="Name", **self.master.label_style),
                         tk.Entry(self, textvariable=self.menu_vars['creation']['name'])],

                'fire_rate': [tk.Label(self, text="Fire Rate", **self.master.label_style),
                              tk.Entry(self, textvariable=self.menu_vars['creation']['fire_rate'], 
                                     validate='key', validatecommand=(val_float, '%S'))],

                'reload_time': [tk.Label(self, text="Reload Time", **self.master.label_style),
                                tk.Entry(self, textvariable=self.menu_vars['creation']['reload_time'],
                                         validate='key', validatecommand=(val_float, '%S'))],

                'damage_per_shot': [tk.Label(self, text="Damage per Shot", **self.master.label_style),
                                    tk.Entry(self, textvariable=self.menu_vars['creation']['damage_per_shot'],
                                             validate='key', validatecommand=(val_int, '%S'))],

                'mag_cap': [tk.Label(self, text="Magazine Capacity", **self.master.label_style),
                            tk.Entry(self, textvariable=self.menu_vars['creation']['mag_cap'],
                                     validate='key', validatecommand=(val_int, '%S'))],

                'ammo_total': [tk.Label(self, text="Ammo Total", **self.master.label_style),
                               tk.Entry(self, textvariable=self.menu_vars['creation']['ammo_total'],
                                        validate='key', validatecommand=(val_int, '%S'))],

                'perk1': [tk.Label(self, text="Perk 1", **self.master.label_style),
                          ttk.Combobox(self, values=self.perk_choices, **self.master.combo_style)],

                'perk2': [tk.Label(self, text="Perk 2", **self.master.label_style),
                          ttk.Combobox(self, values=self.perk_choices, **self.master.combo_style)],

                'origin_trait': [tk.Label(self, text="Origin Trait", **self.master.label_style),
                                 ttk.Combobox(self, values=self.origin_choices, **self.master.combo_style)],

                'enhance': [tk.Checkbutton(self, text="Perk 1 Enhanced", 
                                           variable=self.menu_vars['creation']['enhance1'], **self.master.check_button_style),
                            tk.Checkbutton(self, text="Perk 2 Enhanced", 
                                           variable=self.menu_vars['creation']['enhance2'], **self.master.check_button_style)],

                'burst_fusion_toggle': [tk.Checkbutton(self, text="Burst Weapon", variable=self.menu_vars['creation']['burst_weapon'],
                                                       command=lambda: self.toggle_elements(group='creation', setname='burst_bullets'),
                                                       **self.master.check_button_style),
                                        tk.Checkbutton(self, text="Fusion Weapon ", variable=self.menu_vars['creation']['fusion_weapon'],
                                                       **self.master.check_button_style)],

                'burst_bullets': [tk.Label(self, text="Bullets Per Burst", **self.master.label_style),
                                  tk.Entry(self, textvariable=self.menu_vars['creation']['burst_bullets'],
                                           validate='key', validatecommand=(val_int, '%S'))],

                'interface': [tk.Button(self, text="Create Weapon", command=self.weapon_ecreate, **self.master.button_style),
                              tk.Button(self, text='Edit Weapon', command=lambda: self.weapon_ecreate(editing=True), **self.master.button_style),
                              tk.Button(self, text='Delete Weapon', command=self.weapon_del, **self.master.button_style)]
            },

            # Buff calculator
            'buffcalc': {
                'header': [tk.Label(self, text='Buff / Debuff Calculator', **self.master.label_style)],

                'deb': [tk.Label(self, text='Debuff', **self.master.label_style),
                        ttk.Combobox(self, values=self.buff_choices['deb'], **self.master.combo_style)],
                
                'deb_cnst': [tk.Checkbutton(self, variable=self.menu_vars['buffcalc']['deb_cnst'], 
                                            text='Constantly Applied', **self.master.check_button_style)],

                'buff': [tk.Label(self, text='Empower', **self.master.label_style),
                         ttk.Combobox(self, values=self.buff_choices['buff'], **self.master.combo_style)],

                'buff_cnst': [tk.Checkbutton(self, variable=self.menu_vars['buffcalc']['buff_cnst'], 
                                             text='Constantly Applied', **self.master.check_button_style)],

                'wdmg': [tk.Label(self, text='Weapon Damage', **self.master.label_style),
                         ttk.Combobox(self, values=self.buff_choices['wdmg'], **self.master.combo_style)],
                
                'wdmg_cnst': [tk.Checkbutton(self, variable=self.menu_vars['buffcalc']['wdmg_cnst'], 
                                             text='Constantly Applied', **self.master.check_button_style)],

                'misc': [tk.Label(self, text='Misc', **self.master.label_style)],

                'packhunter': [tk.Checkbutton(self, text='Wolfpack Rounds', **self.master.check_button_style)],

                'pad': [],

                'total': [tk.Label(self, text='Total Multiplier', **self.master.label_style),
                          ttk.Entry(self, textvariable=self.menu_vars['buffcalc']['total'], state="readonly")]
            }
        }

        # Grid placement
        max_outer_column = 2
        self.menu_containers = {}
        # Create 2D array with xlim of max_outer_column
        outer_columns =\
            [list(self.menu_widgets.items())[x:x+max_outer_column] for x in range(0, len(self.menu_widgets), max_outer_column)]
        # Outer x
        for idx, outer_row in enumerate(outer_columns):
            # Outer y
            for idy, (group, widgets) in enumerate(outer_row):
                # Create container frames for each group
                container = self.menu_containers[group] = tk.Frame(self, **self.frame_style)
                container.grid(row=idx, column=idy, sticky='NSEW')

                # Grid each widget to its container
                rewind = 0
                for idz, (setname, widgset) in enumerate(widgets.items()):

                    # Padding
                    if 'pad' in setname:
                        continue

                    # Grid overides
                    if ':go' in setname:
                        origname = setname.split(':go')[0]
                        for idc, obj in enumerate(widgets[origname]):
                            obj.grid_configure(**widgset[idc])
                        rewind += 1
                        continue

                    # Default gridding
                    gi = {'in_': container, 'row': idz-rewind, 'padx': 5, 'pady': 5}
                    for idc, obj in enumerate(widgset):
                        sticky = 'NSW' if idc % 2 == 0 else 'NSE'   
                        if isinstance(obj, ttk.Combobox):
                            obj.bind("<<ComboboxSelected>>", lambda _: self.focus())
                        obj.grid(**gi, column=idc, sticky=sticky)
                        obj.lift()

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

        # Bind extra functions
        for k in ['deb', 'buff', 'wdmg']:
            self.menu_widgets['buffcalc'][k][1].bind('<<ComboboxSelected>>', lambda _: self.update_multitotal())
        self.menu_widgets['creation']['weapon'][1].bind('<<ComboboxSelected>>', lambda _: self.select_weapon())

    def update_weapons(self, first:bool=False):
        wep_names = list(backend.weapons_list.keys())
        # Disable selection if no weapons
        state = 'disabled' if not wep_names else 'readonly'

        wep_names.append('New Weapon')
        self.menu_widgets['creation']['weapon'][1].config(values=wep_names, state=state)
        if first:
            self.menu_widgets['creation']['weapon'][1].set(wep_names[-1])

    def select_weapon(self, name:str=None, *_):
        wep_name = self.menu_widgets['creation']['weapon'][1].get() if name is None else name
        current_weps = list(backend.weapons_list.keys())

        if not wep_name in current_weps:
            self.show_new_weapon()
        else:
            self.menu_widgets['creation']['weapon'][1].set(wep_name)
            self.show_existing_weapon(weapon=backend.weapons_list[wep_name])

        self.focus()

    def show_new_weapon(self):
        # How many weapons exist named 'New Weapon {x}'
        new_weps_count = len([name for name in backend.weapons_list.keys() if name.startswith('New Weapon')]) + 1

        # Tk vars
        for varset in self.menu_vars.values():
            for var in varset.values():
                if isinstance(var, tk.StringVar):
                    var.set(str(0))
                    continue
                var.set(0)

        self.menu_vars['buffcalc']['total'].set(1.00)
        self.menu_vars['creation']['name'].set(f'New Weapon {new_weps_count}')

        # Listboxes
        self.menu_widgets['creation']['perk1'][1].set(self.perk_choices[0])
        self.menu_widgets['creation']['perk2'][1].set(self.perk_choices[0])
        self.menu_widgets['creation']['origin_trait'][1].set(self.origin_choices[0])
        for k in ['deb', 'buff', 'wdmg']:
            self.menu_widgets['buffcalc'][k][1].set(self.buff_choices[k][0])

        # Show creation buttons
        self.menu_widgets['creation']['interface'][0].grid(column=0)
        self.menu_widgets['creation']['interface'][1].grid_remove()
        self.menu_widgets['creation']['interface'][2].grid_remove()

        self.toggle_elements(group='creation', setname='burst_bullets', force='hide')

    def show_existing_weapon(self, weapon:backend.Weapon):
        wep_settings = weapon.get_full_settings()

        # Tk vars
        for set_name, value in wep_settings.items():
            if set_name in self.menu_vars['creation'].keys():
                if isinstance(self.menu_vars['creation'][set_name], tk.StringVar):
                    self.menu_vars['creation'][set_name].set(str(value))
                if type(value) is bool:
                    value = 0 if value == False else 1
                self.menu_vars['creation'][set_name].set(value)

        # Perks
        if wep_settings['perk_indices']:
            if len(wep_settings['perk_indices']) == 1:
                self.menu_widgets['creation']['perk1'][1].set(self.perk_choices[wep_settings['perk_indices'][0]])
                self.menu_widgets['creation']['perk2'][1].set(self.perk_choices[0])
            else:
                for idx, index in enumerate(wep_settings['perk_indices']):
                    self.menu_widgets['creation'][f'perk{idx+1}'][1].set(self.perk_choices[index])
        else:
            self.menu_widgets['creation']['perk1'][1].set(self.perk_choices[0])
            self.menu_widgets['creation']['perk2'][1].set(self.perk_choices[0])

        # Buffs
        if wep_settings['buff_indices']:
            for k in ['deb', 'buff', 'wdmg']:
                if k in wep_settings['buff_indices']:
                    self.menu_widgets['buffcalc'][k][1].set(self.buff_choices[k][wep_settings['buff_indices'][k][0]])
                    self.menu_vars['buffcalc'][f'{k}_cnst'].set(wep_settings['buff_indices'][k][1])
                else:
                    self.menu_widgets['buffcalc'][k][1].set(self.buff_choices[k][0])
                    self.menu_vars['buffcalc'][f'{k}_cnst'].set(0)
        else:
            for k in ['deb', 'buff', 'wdmg']:
                self.menu_widgets['buffcalc'][k][1].set(self.buff_choices[k][0])
                self.menu_vars['buffcalc'][f'{k}_cnst'].set(0)
        self.update_multitotal()

        # Origin trait
        if wep_settings['origin_trait']:
                self.menu_widgets['creation']['origin_trait'][1].set(self.origin_choices[wep_settings['origin_trait']])
        else:
            self.menu_widgets['creation']['origin_trait'][1].set(self.origin_choices[0])

        # Show or hide burst bullets
        force = 'show' if wep_settings['burst_weapon'] else 'hide'
        self.toggle_elements(group='creation', setname='burst_bullets', force=force)

        # Show edit / delete button
        self.menu_widgets['creation']['interface'][0].grid_remove()
        self.menu_widgets['creation']['interface'][1].grid(column=0)
        self.menu_widgets['creation']['interface'][2].grid(column=1)

    def toggle_elements(self, group:str, setname:str, force:str='toggle'):
        for obj in self.menu_widgets[group][setname]:
            match force:
                case 'toggle':
                    obj.grid_remove() if obj.winfo_viewable() else obj.grid()
                case 'show':
                    obj.grid()
                case 'hide':
                    obj.grid_remove()

    def weapon_ecreate_hdlr(self, exitcode, editing, verb=None, wepname=None):
        if editing:
            basestr = f'Weapon Edit exited with code {exitcode}:'
        else:
            basestr = f'Weapon Creation exited with code {exitcode}:'

        match exitcode:
            case 0:
                messagebox.showinfo('Success', f'Successfully {verb} weapon: {wepname}')
                print(f'{basestr} Success')
            case 1:
                messagebox.showerror('Name Error', 'The name "New Weapon" is not allowed.')
                print(f'{basestr} Name Error')
            case 2:
                print(f'{basestr} Edit Denied')
            case 3:
                messagebox.showerror('Name Error', 'Make sure the name for your weapon contains at least one letter.')
                print(f'{basestr} Name Error')
            case 4:
                messagebox.showerror('Float Error', 'Make sure Fire Rate and Reload Time are valid numbers.')
                print(f'{basestr} Float Error')
            case 5:
                messagebox.showerror('Integer Error', 'Make sure Damage per Shot, Mag Size, and Ammo Total are valid numbers.')
                print(f'{basestr} Integer Error')
            case 6:
                messagebox.showerror('Edit Error', 'You should not have hit this error! Please report this on Github or Discord!')
                print(f'{basestr} Unknown Error')
            case 7:
                messagebox.showerror('Creation Error', 'You should not have hit this error! Please report this on Github or Discord!')
                print(f'{basestr} Unknown Error')

    def weapon_ecreate(self, editing:bool=False):
        # Strings
        verb = 'created'

        name = self.menu_vars['creation']['name'].get().strip()
        if name == 'New Weapon':
            return self.weapon_ecreate_hdlr(1, editing)
        
        if editing:
            verb = 'edited'
            oldname = self.menu_widgets['creation']['weapon'][1].get()
            namechange = True if name != oldname else False

            confirm = messagebox.askokcancel('Edit Warning', f'Are you sure you want to edit "{oldname}"?\nProceeding will permanently overwrite the configuration of "{oldname}".')
            if not confirm:
                return self.weapon_ecreate_hdlr(2, editing)

        # Validate name
        for teststr in [name]:
            if not self.test_str(teststr):
                return self.weapon_ecreate_hdlr(3, editing)

        # Floats
        try:
            fire_rate = float(self.menu_vars['creation']['fire_rate'].get())
            reload_time = float(self.menu_vars['creation']['reload_time'].get())
            for testfloat in [fire_rate, reload_time]:
                if not self.test_float(testfloat):
                    return self.weapon_ecreate_hdlr(4, editing)
        except ValueError:
            return self.weapon_ecreate_hdlr(4, editing)

        # Integers
        damage_per_shot = self.menu_vars['creation']['damage_per_shot'].get()
        mag_cap = self.menu_vars['creation']['mag_cap'].get()
        ammo_total = self.menu_vars['creation']['ammo_total'].get()
        burst_bullets = self.menu_vars['creation']['burst_bullets'].get()

        # Bools
        enhance1 = self.menu_vars['creation']['enhance1'].get()
        enhance2 = self.menu_vars['creation']['enhance2'].get()
        burst_weapon = self.menu_vars['creation']['burst_weapon'].get()
        fusion_weapon = self.menu_vars['creation']['fusion_weapon'].get()

        # Integers (continued)
        ints = [damage_per_shot, mag_cap, ammo_total]
        if burst_weapon:
            ints.append(burst_bullets)
        for testint in ints:
            if not self.test_int(testint):
                return self.weapon_ecreate_hdlr(5, editing)

        # Perks
        perk1 = self.menu_widgets['creation']['perk1'][1].get()
        perk2 = self.menu_widgets['creation']['perk2'][1].get()
        perk_indices = [index for index, perkname in backend.PERKS_LIST.items() if list(perkname)[0] in [perk1, perk2]]
        perk_indices = None if perk_indices == [0] else perk_indices

        # Buffs
        buff_indices = {}
        for flag, choice in {'deb': backend.DEBUFFS_LIST, 'buff': backend.BUFFS_LIST, 'wdmg': backend.WEAPON_BOOSTS_LIST}.items():
            index = [k for k, (name, _, _) in choice.items() if name == self.menu_widgets['buffcalc'][flag][1].get()]
            buff_indices[flag] = [index[0] if index else 0, self.menu_vars['buffcalc'][f'{flag}_cnst'].get()]

        for k, v in buff_indices.copy().items():
            if not v[0]:
                del buff_indices[k]

        # Origin Trait
        origin_trait = self.menu_widgets['creation']['origin_trait'][1].get()
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
            'origin_trait': int(origin_trait),
            'buff_indices': buff_indices
        }

        if editing and namechange:
            if not backend.delete_weapon(oldname):
                return self.weapon_ecreate_hdlr(6, editing)

        if backend.create_weapon(weapon_options):
            self.master.util_update_wep_names()
            if self.master.settings.do_auto_save and self.master.settings.auto_save_path:
                self.master.optionsmenu.export_weps_hdlr(self.master.settings.auto_save_path)
            self.menu_widgets['creation']['weapon'][1].set(name)
            self.select_weapon(name=name)
            return self.weapon_ecreate_hdlr(0, editing, verb, name) 
        else:
            return self.weapon_ecreate_hdlr(7, editing)
        
    def weapon_del(self):
        name = self.menu_widgets['creation']['weapon'][1].get()

        confirm = messagebox.askokcancel('Deletion Warning', f'Are you sure you want to delete "{name}"?\nProceeding will permanently delete the configuration of "{name}".')
        if not confirm:
            print('Weapon Deletion exited with code 1: Deletion Denied')
            return
        
        if backend.delete_weapon(name):
            self.master.util_update_wep_names()
            if self.master.settings.do_auto_save and self.master.settings.auto_save_path:
                self.master.optionsmenu.export_weps_hdlr(self.master.settings.auto_save_path)
            self.show_new_weapon()
            self.update_weapons(first=True)
            messagebox.showinfo('Success', f'Weapon deleted successfully')
            print('Weapon Deletion exited with code 0: Success')
        else:
            messagebox.showinfo('Deletion Error', 'You should not have hit this error! Please report this on Github or Discord!')
            print('Weapon Deletion exited with code 2: Unknown Error')

    def update_multitotal(self):
        vals = [ref.multiplier
                for choices in [backend.DEBUFFS_LIST.values(),
                                backend.BUFFS_LIST.values(),
                                backend.WEAPON_BOOSTS_LIST.values()]
                for (name, _, ref) in choices
                for n1 in [self.menu_widgets['buffcalc'][n2][1].get() for n2 in ['deb', 'buff', 'wdmg']]
                if name == n1 and name != 'Null']

        self.menu_vars['buffcalc']['total'].set(str(round(prod(vals), 2)))
        self.focus()

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