# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:32:21 2020

@author: Arthur
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import math
import celestialobject as co
import numpy as np
import time
import random
from datetime import datetime



class Animate_celestial_objects():


    def __init__(self):
        #self.running = True
        self.start()



    def start(self):
        self.root = tk.Tk()
        # self.root.resizable(0,0)
        # self.root.wm_attributes("-topmost", 1)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        # self.root.minsize(width=str(self.width), height=str(self.height))
        self.root.geometry("1000x1000")
        # self.minsize(1000,800)
        # self.root.geometry("1150x800")
        # self.root.attributes('-fullscreen', True)
        #Init slide variables
        self.delay = tk.IntVar()
        self.delay.set(0)
        self.alpha = tk.DoubleVar()
        self.alpha.set(2)
        self.Delta_t = tk.DoubleVar()
        self.Delta_t.set(.1)
        self.G = tk.IntVar()
        self.G.set(10)
        self.zoom_factor = .05
        self.current_zoom_factor = 1
        self.center = [500.,500.] # np.array([self.canvas.winfo_width(), self.canvas.winfo_height()])/2
        self.planets = []
        self.dropdown_list = ['COM','Absolute']
        self.draw_graph = False
        self.center_CO = tk.StringVar()
        self.center_CO.set('COM')
        self.arrow_factor_velocity = tk.IntVar()
        self.arrow_factor_velocity.set(10)
        self.arrow_factor_acceleration = tk.IntVar()
        self.arrow_factor_acceleration.set(180)
        self.time_list = []
        self.time = 0
        self.draw_tail = False

        self.init_UI()
        self.running = False
        self.initialise_planets()
        self.step = 0
        self.celestial_initizalized = True
        self.next_step()
        self.root.mainloop()



    def initialise_planets(self):
        G = self.G.get()
        # self.planets.append( co.celestialobject(11, 'red', self.canvas, self.center, [0., 0.], 'planet1') )
        self.planets.append( co.celestialobject(1000, 'yellow', self.canvas, self.center, [0., 0.], 'planet1') )
        # self.planets.append( co.celestialobject(400, 'red', self.canvas, self.center, [0., 0.], 'planet1') )
        # self.planets.append( co.celestialobject(11, 'blue', self.canvas, self.center+np.array([0,-150]), [math.sqrt(self.G.get()*self.planets[0].mass/150), 0.], 'planet2') )
        # self.planets.append( co.celestialobject(3, 'orange', self.canvas, self.center+np.array([0,160]), [-math.sqrt(G*self.planets[0].mass/150), 0.], 'planet3') )
        # # self.planets.append( co.celestialobject(20, 'green', self.canvas, self.center+np.array([-80,40]), [1, 0.1], 'planet4') )
        # self.planets.append( co.celestialobject(20, 'green', self.canvas, self.center+np.array([-80,40]), [-1, 10], 'planet4') )
        self.planets.append( co.celestialobject(50, 'purple', self.canvas, [0., 0.], [.1, .05], 'planet5') )
        # self.planets.append( co.celestialobject(268, 'magenta', self.canvas, [1000, 1000], [-.1, -.1], 'planet6') )
        self.planets.append( co.celestialobject(250, 'brown', self.canvas, [500, 1000], [-5, 1], 'planetX') )
        self.planets.append( co.celestialobject(10, 'gold', self.canvas, [500+60, 1000], [-5.1,1 + math.sqrt(G*250/60)], 'planetXMoon'))
        self.planets.append( co.celestialobject(1, 'blue', self.canvas, self.center+np.array([0,-150]), [math.sqrt(G*self.planets[0].mass/150), 0.1], 'planet2') )
        self.planets.append( co.celestialobject(5, 'green', self.canvas, self.center+np.array([0,400]), [math.sqrt(G*self.planets[0].mass/400)+1, -1], 'planet3') )
        self.planets.append( co.celestialobject(20, 'coral', self.canvas, self.center+np.array([-80,40]), [-1, 13], 'planet4') )

        self.planets_colors = [planet.color for planet in self.planets]
        self.dropdown_list += self.planets_colors
        menu = self.dropdown_center['menu']
        for color in self.planets_colors:
            menu.add_command(label=color, command=lambda value=color: self.center_CO.set(value))
        self.color_planet = dict(zip(self.planets_colors, self.planets))
        print(list(self.color_planet))
        # create COm marker
        self.coordsCOM = self.get_coords_com()
        self.COM = self.canvas.create_line(self.coordsCOM[0]-5, self.coordsCOM[1]-5, self.coordsCOM[0]+5, self.coordsCOM[1]+5, self.coordsCOM[0], self.coordsCOM[1], self.coordsCOM[0]-5, self.coordsCOM[1]+5, self.coordsCOM[0]+5, self.coordsCOM[1]-5, fill='white')
        self.next_step()
        print(self.planets[2].get_phi())

    def get_coords_com(self):
        return sum([planet.mass*planet.position for planet in self.planets]) / sum([planet.mass for planet in self.planets])

    # def create_reandom_planet(range_mass=[1,20], range_size=[1,20], range_location=[100,800], range_velocity=[-5,5]):
    #     co.celestialobject(9, 8, self.center, [-.05, 0])



    def new_state_planets(self, planet):
        acceleration = planet.force / planet.mass
        delta_t = self.Delta_t.get()
        planet.velocity += acceleration*delta_t
        planet.position += planet.velocity*delta_t


    def calculate_forces(self):
        alpha = self.alpha.get()
        G = self.G.get()
        for planet in self.planets:
            planet.reset_force()
        for i in range(len(self.planets)-1):
            for j in range(i+1, len(self.planets)):
                co.set_force_2_celestialobjects(self.planets[i], self.planets[j], G, alpha)

    def set_deltas(self, delta_t):
        option = self.center_CO.get()
        if option == 'COM':
            self.Delta = self.coordsCOMNew - self.coordsCOM
            if delta_t == 0:
                self.correction_velocity = np.zeros((2,))
            else:
                self.correction_velocity = -self.Delta / delta_t
            self.correction_acceleration = np.zeros((2,))
        elif option == 'Absolute':
            self.Delta = np.zeros((2,))
            self.correction_velocity = np.zeros((2,))
            self.correction_acceleration = np.zeros((2,))
        else:
            planet = self.color_planet[option]
            self.Delta = planet.velocity * delta_t
            self.correction_velocity = -planet.velocity
            self.correction_acceleration = -planet.acceleration

    def next_step(self):
        t_i = datetime.now()
        self.calculate_forces()
        t_f_cf = datetime.now()
        print(f'\n Calculate forces: {t_f_cf - t_i}')
        delta_t = self.Delta_t.get()
        self.time += delta_t
        self.time_list.append(self.time)
        t_i_ns  = datetime.now()
        print(f'get delta t  {t_i_ns - t_f_cf}')
        for planet in self.planets:
            planet.new_state_planet(delta_t)
        t_f_ns = datetime.now()
        print(f'Calculate new state: {t_f_ns - t_i_ns}')

        self.coordsCOMNew = self.get_coords_com()
        self.set_deltas(delta_t)
        self.plot_speed.clear()
        self.plot_acceleration.clear()
        self.plot_phi.clear()
        self.length_list = len(self.time_list)
        t_i_draw = datetime.now()
        print(f'3  {t_i_draw - t_f_ns}')
        for planet in self.planets:
            change =  (planet.velocity*delta_t - self.Delta)*self.current_zoom_factor
            planet.move_object(change, draw_tail=self.draw_tail)
            planet.draw_acceleration_arrow(correction=self.correction_acceleration,
                                           factor=self.arrow_factor_acceleration.get()*self.current_zoom_factor)
            planet.draw_velocity_arrow(correction=self.correction_velocity,
                                       factor=self.arrow_factor_velocity.get()*self.current_zoom_factor )

            self.update_data_graphs(planet)

        t_f_draw = datetime.now()
        print(f'draw planets: {t_f_draw - t_i_draw}')
        if self.draw_graph:
            self.draw_graphs()
        t_f_draw_graphs = datetime.now()
        print(f'draw graphs: {t_f_draw_graphs - t_f_draw }')

        COM_change = (self.coordsCOMNew - self.coordsCOM - self.Delta)*self.current_zoom_factor
        self.canvas.move(self.COM, COM_change[0], COM_change[1])
        self.coordsCOM = self.coordsCOMNew
        t_f_COM = datetime.now()
        print(f'COM: {t_f_COM - t_f_draw_graphs}')
        # continue or pause loop
        t_f = t_f_COM
        if self.running:
            print(f'Total1: {t_f-t_i}')
            # self.canvas.itemconfig(
            #     self.text_id3,
            #     text=f'positions moon: oval={self.planets[3].get_center_oval()}, {self.planets[3].position}'
            #    )
            # print(f'Total2: {t_f-t_i}')
            self.root.after(self.delay_slider.get()+1, self.next_step)

    def update_data_graphs(self, planet):
        self.plot_speed.plot(
                 self.time_list[-min(self.length_list, MAX_PLOTLENGTH):],
                 planet.speed_history[-min(self.length_list, MAX_PLOTLENGTH):], color=planet.color)

        self.plot_acceleration.plot(
             self.time_list[-min(self.length_list, MAX_PLOTLENGTH):],
             planet.acceleration_history[-min(self.length_list, MAX_PLOTLENGTH):], color=planet.color)

        self.plot_phi.plot(
             self.time_list[-min(self.length_list, MAX_PLOTLENGTH):],
                planet.phi_history[-min(self.length_list, MAX_PLOTLENGTH):], color=planet.color)

    def draw_graphs(self):
        self.canvas_graph_speed.draw()
        self.canvas_graph_acceleration.draw()
        self.canvas_graph_phi.draw()

    def init_UI(self):

        # create frames
        self.frame_animation = tk.Frame(self.root, bd=1, relief="sunken")
        # self.frame_controls = tk.Frame(self.root, bd=1, relief="sunken")
        self.frame_controls = ttk.Notebook(self.root)

        self.frame_animation.grid(row=0, column=0, rowspan=1, sticky='nsew')
        self.frame_controls.grid(row=0, column=1, sticky='nsew')
        # Determine size of frames
        l_animation = 9
        l_controls = 1
        self.root.grid_columnconfigure(0, weight=l_animation)# weight=l_animation)
        self.root.grid_columnconfigure(1, weight=l_controls)#weight=l_controls)

        self.canvas_width = self.width-100
        self.canvas = tk.Canvas(self.frame_animation, width=self.canvas_width, height=1000, bg='black') #, width=self.canvas_width, height=self.height, bg="gray")
        self.canvas.grid(column=0, row=0)

        self.xsb = tk.Scrollbar(self.frame_animation, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self.frame_animation, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,self.canvas_width,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.frame_animation.grid_rowconfigure(0, weight=1)
        self.frame_animation.grid_columnconfigure(0, weight=1)

         # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<MouseWheel>",self.zoomer)
        # Set default font
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=7)

        # self.canvas.bind("<Button-1>", self.canvas_onclick)
        # fontStyle = tkFont.Font(family="Lucida Grande", size=12)
        # self.text_id = self.canvas.create_text(500, 600, anchor='se', fill='red', font=fontStyle)
        # self.canvas.itemconfig(self.text_id, text='hello')
        # self.text_id2 = self.canvas.create_text(530, 630, anchor='se', fill='red', font=fontStyle)
        # self.canvas.itemconfig(self.text_id2, text='hello2')
        # self.text_id3 = self.canvas.create_text(560, 660, anchor='se', fill='red', font=fontStyle)
        # self.canvas.itemconfig(self.text_id3, text='hello3')



        self.UI_frame_animation_controls()

    def canvas_onclick(self, event):
        self.canvas.itemconfig(
            self.text_id,
            text= f'You clicked at ({event.x}, {event.y})'
        )
        self.canvas.itemconfig(
            self.text_id2,
            text= f'You clicked at ({self.canvas.canvasx(event.x)}, {self.canvas.canvasy(event.y)})'
        )
    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def pressed_tail(self):
        if self.draw_tail:
            self.button_tail.configure(relief=tk.RAISED)
        else:
            self.button_tail.configure(relief=tk.SUNKEN)
        self.draw_tail = not self.draw_tail
        print(self.draw_tail)

    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, (1+self.zoom_factor), (1+self.zoom_factor))
            self.current_zoom_factor *= (1+self.zoom_factor)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, (1-self.zoom_factor), (1-self.zoom_factor))
            self.current_zoom_factor *= (1-self.zoom_factor)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))


    def UI_frame_animation_controls(self):
        # controls frame
        self.frame_controls = tk.Frame(self.root, width=200, height=self.height)
        self.frame_controls.grid(row=0, column=1, sticky='nw')
        # Add notebook for tabs
        self.physics = ttk.Notebook(self.frame_controls, width=200 )
        self.physics.grid(row=1,column=1)
        # physics controls tab
        self.tab_physics = ttk.Frame(self.physics )
        self.physics.add(self.tab_physics, text='physics', compound=tk.TOP)
        # Graphs tabb
        self.graphs_tab = ttk.Frame(self.physics )
        self.physics.add(self.graphs_tab, text='graphs', compound=tk.TOP)
        self.UI_physics_tab()
        self.UI_graphs()

    def UI_physics_tab(self):
        # play
        row=0
        self.play = tk.Button(self.tab_physics, text="play", command=self.do_play)
        self.play.grid(row=row, column=0, sticky='w')
        # Pause
        self.pause = tk.Button(self.tab_physics, text="pause", command=self.do_pause)
        self.pause.grid(row=row, column=1, sticky='w')
        # Speed
        self.delay_slider = tk.Scale(
            self.tab_physics, from_=0, to=1000, resolution=100, orient=tk.HORIZONTAL, variable=self.delay)
        self.delay_slider.grid(row=row, column=3, sticky='w')
        # G
        row+=1
        self.G_slider = tk.Scale(
            self.tab_physics, from_=-50, to=50, length = 200, tickinterval=10, resolution= 1,
            orient=tk.HORIZONTAL, variable=self.G)
        self.G_slider.grid(row=row, column=0, sticky='w')
        # alpha
        row+=1
        self.alpha_slider = tk.Scale(
            self.tab_physics, from_=-3, to=3, length = 200, tickinterval=1, resolution=.01,
            orient=tk.HORIZONTAL, variable=self.alpha, font=self.default_font)
        self.alpha_slider.grid(row=row, column=0, sticky='w')
        # delta_t
        row+=1
        self.Delta_t_slider = tk.Scale(
            self.tab_physics, from_=-5, to=5, length = 200, tickinterval=1, resolution=.1,
            orient=tk.HORIZONTAL, variable=self.Delta_t)
        self.Delta_t_slider.grid(row=row, column=0, sticky='w')


        # dropdown of center
        row+=1
        self.dropdown_center = tk.OptionMenu(self.tab_physics, self.center_CO, *self.dropdown_list )
        self.dropdown_center.configure(width=20)
        self.dropdown_center.grid(row=row, column=0, sticky='w')


        # arrow lengths
        row+=1
        self.arrow_factor_velocity_slider = tk.Scale(
            self.tab_physics, from_=0, to=50, length = 200, tickinterval=10, resolution=1,
            orient=tk.HORIZONTAL, variable=self.arrow_factor_velocity)
        self.arrow_factor_velocity_slider.grid(row=row, column=0, sticky='w')
        # delta_t
        row+=1
        self.arrow_factor_acceleration_slider = tk.Scale(
            self.tab_physics, from_=0, to=300, length = 200, tickinterval=50, resolution=5,
            orient=tk.HORIZONTAL, variable=self.arrow_factor_acceleration)
        self.arrow_factor_acceleration_slider.grid(row=row, column=0, sticky='w')

        # tails
        row+=1
        self.button_tail = tk.Button(self.tab_physics, text="tails")
        self.button_tail.configure(command=self.pressed_tail)
        self.button_tail.configure(relief=tk.RAISED)
        self.button_tail.grid(row=row, column=0, sticky='w')

    def UI_graphs(self):
        # graphs
        plt.style.use('ggplot')
        #speed
        row = 0
        self.f_speed = Figure(figsize=(2,2), dpi=100)
        self.plot_speed = self.f_speed.add_subplot(111)
        self.canvas_graph_speed = FigureCanvasTkAgg(self.f_speed, self.graphs_tab)
        self.canvas_graph_speed.draw()
        row+=1
        self.canvas_graph_speed.get_tk_widget().grid(row=row, column=0)
        toolbarFrame_speed = tk.Frame(master=self.graphs_tab)
        toolbarFrame_speed.grid(row=row,column=0)

        # acceleration
        self.f_acceleration = Figure(figsize=(2,2), dpi=100)
        self.plot_acceleration = self.f_acceleration.add_subplot(111)
        self.canvas_graph_acceleration = FigureCanvasTkAgg(self.f_acceleration, self.graphs_tab)
        self.canvas_graph_acceleration.draw()
        row+=1
        self.canvas_graph_acceleration.get_tk_widget().grid(row=row, column=0)
        toolbarFrame_acceleration = tk.Frame(master=self.graphs_tab)
        toolbarFrame_acceleration.grid(row=row,column=0)

        # phi
        self.f_phi = Figure(figsize=(2,2), dpi=100)
        self.plot_phi = self.f_phi.add_subplot(111)
        self.canvas_graph_phi = FigureCanvasTkAgg(self.f_phi, self.graphs_tab)
        self.canvas_graph_phi.draw()
        row+=1
        self.canvas_graph_phi.get_tk_widget().grid(row=row, column=0)
        toolbarFrame_phi = tk.Frame(master=self.graphs_tab)
        toolbarFrame_phi.grid(row=row,column=0)


    def do_pause(self):
        self.running = False


    def do_play(self):
        self.running = True
        self.next_step()

MAX_PLOTLENGTH = 3000
animation = Animate_celestial_objects()

"""
Interesting settings:
    self.alpha = 2
        self.Delta_t = .1
        self.G = 30
self.center = np.array([500,500])
        self.planet_1 = co.celestialobject(1, 10, self.center+np.array([0,0]))
        self.planet_2 = co.celestialobject(1, 10, self.center+np.array([1,-50]),[.5,0])

"""