import time
import tkinter as tk
import tkinter.colorchooser
import random
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import backend.backend as backend

class GraphMenu(tk.Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.config(**self.master.frame_style)
        self.pack()
        self.navname = 'Graph'

        self.frame_style = self.master.frame_style.copy()
        self.frame_style['highlightthickness'] = 0

        self.init_menu()

    def init_menu(self):
        self.wep_select_ui()
        self.graph_ui()
        self.set_numweapons()
        self.pack_forget()

    def wep_select_ui(self):
        self.config_frame = tk.Frame(self, **self.frame_style)
        self.config_frame.pack(side=tk.LEFT, fill=tk.Y)

        # No. of weps
        wep_count = [f'{i+1}' for i in range(10)]
        self.num_weps_label = tk.Label(self.config_frame, text='Number of Weapons', **self.master.label_style)
        self.num_weps_label.grid(row=0, column=0, **self.master.default_padding)

        self.num_weps_combo = ttk.Combobox(self.config_frame, values=wep_count, width=3, state='readonly')
        self.num_weps_combo.grid(row=0, column=1, **self.master.default_padding)
        self.num_weps_combo.set(wep_count[self.master.settings.graph_initial_slots - 1]) # Changed to use settings
        self.num_weps_combo.bind("<<ComboboxSelected>>", self.set_numweapons)

        def random_color():
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            return '#{:02x}{:02x}{:02x}'.format(r,g,b)

        # Save the colors in an array with random default colors
        # Now load from settings if exist
        if self.master.settings.graph_colors == 'random':
            self.colors = [random_color() for _ in range(10)]
        else:
            self.colors = self.master.settings.graph_colors.split(',')

        # Create square color picker buttons with a Label inside
        self.color_buttons = [
            tk.Button(
                self.config_frame,
                command=lambda i=i: self.get_color(i),
                width=2,
                bg=self.colors[i],
                **{k: v for k, v in self.master.button_style.items() if k not in ('bg', 'width')}
            ) 
            for i in range(10)
        ]

        # Build weapon select widgets
        self.wep_widgets = [
                ( tk.Label(self.config_frame, text=f'Weapon {i+1}', **self.master.label_style),
                ttk.Combobox(self.config_frame, **self.master.combo_style)
                ) for i in range(10)
            ]
        
        # Grid placement
        for idx, multi in enumerate(self.wep_widgets):
            label, combo = multi
            label.grid(row=(idx+1), column=0, **self.master.default_padding)
            combo.grid(row=(idx+1), column=1, **self.master.default_padding)
            combo.bind("<<ComboboxSelected>>",lambda e: self.focus())
            # Display specified from settings :)
            if idx > self.master.settings.graph_initial_slots - 1:
                label.grid_forget()
                combo.grid_forget()

        # Generate graph button
        self.generate_button = tk.Button(self.config_frame, text="Generate Graph",
                                            command=self.generate_graph, **self.master.button_style)
        self.generate_button.grid(row=15, column=0, padx=8, pady=5, sticky=tk.W)
        self.update_weapons()

        # Save graph button
        self.save_button = tk.Button(self.config_frame, text="Save Graph", 
                                           command=self.save_graph, **self.master.button_style)
        self.save_button.grid(row=15, column=1, padx=8, pady=5, sticky=tk.W)

    def get_color(self, index):
        color = tkinter.colorchooser.askcolor()[1]
        if color is not None:
            self.colors[index] = color
            self.color_buttons[index].config(bg=color)

    def graph_ui(self):
        self.graph_frame = tk.Frame(self, **self.frame_style)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.Y)

        mpl.rcParams['text.color'] = self.master.matplotlib_fg
        mpl.rcParams['axes.edgecolor'] = self.master.matplotlib_fg
        mpl.rcParams['xtick.color'] = self.master.matplotlib_fg
        mpl.rcParams['ytick.color'] = self.master.matplotlib_fg
        mpl.rcParams['axes.labelcolor'] = self.master.matplotlib_fg

        # Create a Matplotlib figure and canvas
        self.fig = Figure(figsize=(5, 4), dpi=117)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.ax.set_facecolor(self.master.matplotlib_bg)
        self.fig.set_facecolor(self.master.matplotlib_bg)

        # Set axis and labels
        self.ax.set_title(self.master.settings.graph_title)
        self.ax.set_xlabel(self.master.settings.graph_xlabel)
        self.ax.set_ylabel(self.master.settings.graph_ylabel, labelpad=-340, rotation='horizontal')
        self.ax.set_xlim(0, self.master.settings.graph_xlim)
        self.ax.set_ylim(0, self.master.settings.graph_ylim)

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def generate_graph(self):
        # Clear previous plot
        self.ax.clear()
        
        # Loop through weapon dropdowns
        seleced_weps = [
            (backend.weapons_list[dropdown.get()], self.colors[i]) 
            for i, (_, dropdown) in enumerate(self.wep_widgets) 
            if dropdown.winfo_viewable() and dropdown.get() != ''
        ]

        if seleced_weps:
            if self.master.settings.do_dmg_prints:
                totaltime_elapsed = time.time()
            try:
                for weapon, color in seleced_weps:
                    # Get damage values by for DamageCalculate
                    x, y = weapon.DamageCalculate()

                    # Plot the weapon damage
                    self.ax.plot(x, y, label=f'{weapon.name}', color=color)

                # Set the axis labels and title
                self.ax.set_xlabel(self.master.settings.graph_xlabel)
                self.ax.set_xlim(0, self.master.settings.graph_xlim)
                self.ax.set_ylabel(self.master.settings.graph_ylabel)
                self.ax.set_ylim(0, self.master.settings.graph_ylim)
                self.ax.set_title(self.master.settings.graph_title)

                # Add legend and re-draw
                self.ax.legend(facecolor=self.master.navbar_bg)
                self.canvas.draw()
                if self.master.settings.do_dmg_prints:
                    totaltime_elapsed = round(totaltime_elapsed - time.time(), 2) * -1
                    print(f'Total calculation time: {totaltime_elapsed} secs')
                print('Graph Generation exited with code 0: Success')
            except Exception as e:
                print('Error Occured during Graph Generation:')
                print(e)
        else:
            print('Graph Generation exited with code 1: No Selected Weapons')

    def save_graph(self):
        file_path = asksaveasfile(defaultextension='.png', filetypes=[('All Files', '*.*')], initialdir='./', initialfile='dps_graph.png')
        if file_path is None:
            return
        self.fig.savefig(file_path.name)
        print(f'Saved graph as "{file_path.name}"')

    def update_weapons(self):
        wep_names = list(backend.weapons_list.keys())
        for (_, dropdown) in self.wep_widgets:
            dropdown.config(values=wep_names)
        gen_but_enabled = 'normal' if wep_names else 'disabled'
        self.generate_button.config(state=gen_but_enabled)

    def set_numweapons(self, *_):
        # Get amount of weapons
        amount = int(self.num_weps_combo.get()) - 1

        # Redraw combos and color buttons based on amount
        for idx, tuple in enumerate(self.wep_widgets):
            label, combo = tuple
            color_button = self.color_buttons[idx]
            if idx <= amount:
                label.grid(row=(idx+1), column=0, **self.master.default_padding)
                combo.grid(row=(idx+1), column=1, **self.master.default_padding)
                color_button.grid(row=(idx+1), column=2, **self.master.default_padding)
            else:
                label.grid_forget()
                combo.grid_forget()
                color_button.grid_forget()
        self.focus()