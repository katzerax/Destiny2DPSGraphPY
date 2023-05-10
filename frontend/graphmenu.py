import time
import tkinter as tk
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
        self.pack_forget()

    def wep_select_ui(self):
        self.config_frame = tk.Frame(self, **self.frame_style)
        self.config_frame.pack(side=tk.LEFT, fill=tk.Y)

        # No. of weps
        wep_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.num_weps_label = tk.Label(self.config_frame, text='Number of Weapons', **self.master.label_style)
        self.num_weps_label.grid(row=0, column=0, **self.master.default_padding)

        self.num_weps_combo = ttk.Combobox(self.config_frame, values=wep_count, width=3, state='readonly')
        self.num_weps_combo.grid(row=0, column=1, **self.master.default_padding)
        self.num_weps_combo.set(wep_count[0]) # Changed it to one wep by default
        self.num_weps_combo.bind("<<ComboboxSelected>>", self.set_numweapons)

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
            combo.bind("<<ComboboxSelected>>",lambda e: self.graph_frame.focus())
            # Display only 3 by default - no more - K
            if idx > 0: # Changed it to one by default
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
        seleced_weps =\
            [backend.weapons_list[dropdown.get()] for (_, dropdown) in self.wep_widgets if dropdown.winfo_viewable() and dropdown.get() != '']

        if seleced_weps:
            if self.master.settings.do_dmg_prints:
                totaltime_elapsed = time.time()
            try:
                for weapon in seleced_weps:
                    # Get damage values by for DamageCalculate
                    x, y = weapon.DamageCalculate()

                    # Plot the weapon damage
                    self.ax.plot(x, y, label=f'{weapon.name}')

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

    def set_numweapons(self, evt):
        # Get ammount of weps requested
        ammount = int(self.num_weps_combo.get()) - 1

        # Redraw combos based on ammount
        for idx, tuple in enumerate(self.wep_widgets):
            label, combo = tuple
            if idx <= ammount:
                label.grid(row=(idx+1), column=0, **self.master.default_padding)
                combo.grid(row=(idx+1), column=1, **self.master.default_padding)
            else:
                label.grid_forget()
                combo.grid_forget()
        # Focus the frame, not the combo
        self.graph_frame.focus()