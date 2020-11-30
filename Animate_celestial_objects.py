# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:32:21 2020

@author: Arthur
"""

import tkinter as tk
import math
import celestialobject as co
import numpy as np
import time

class Animate_celestial_objects():


    def __init__(self):
        #self.running = True
        self.start()




    def start(self):
        self.root = tk.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        # self.root.minsize(width=str(self.width), height=str(self.height))
        self.root.geometry("900x900")
        # self.minsize(1000,800)
        # self.root.geometry("1150x800")
        # self.root.attributes('-fullscreen', True)
        #Init slide variables
        self.delay = tk.DoubleVar()
        self.delay.set(0)
        self.alpha = tk.DoubleVar()
        self.alpha.set(2)
        self.Delta_t = tk.DoubleVar()
        self.Delta_t.set(.125)
        self.G = tk.DoubleVar()
        self.G.set(10)
        self.zoom_factor = .05
        self.current_zoom_factor = 1
        self.center = [500.,500.] # np.array([self.canvas.winfo_width(), self.canvas.winfo_height()])/2
        self.planets = []
        self.dropdown_list = ['COM','Absolute']
        self.center_CO = tk.StringVar()
        self.center_CO.set('COM')

        self.init_UI()
        self.initialise_planets()
        self.stop = False
        self.running = False
        self.step = 0
        self.celestial_initizalized = True
        self.loop()
        self.root.mainloop()



    def initialise_planets(self):
        # self.planets.append( co.celestialobject(11, 'red', self.canvas, self.center, [0., 0.], 'planet1') )
        # self.planets.append( co.celestialobject(400, 'red', self.canvas, self.center, [0., 0.], 'planet1') )
        # self.planets.append( co.celestialobject(11, 'blue', self.canvas, self.center+np.array([0,-150]), [math.sqrt(self.G.get()*self.planets[0].mass/150), 0.], 'planet2') )
        # self.planets.append( co.celestialobject(3, 'orange', self.canvas, self.center+np.array([0,160]), [-math.sqrt(self.G.get()*self.planets[0].mass/150), 0.], 'planet3') )
        # # self.planets.append( co.celestialobject(20, 'green', self.canvas, self.center+np.array([-80,40]), [1, 0.1], 'planet4') )
        # self.planets.append( co.celestialobject(20, 'green', self.canvas, self.center+np.array([-80,40]), [-1, 10], 'planet4') )
        # self.planets.append( co.celestialobject(50, 'purple', self.canvas, [0., 0.], [.1, .05], 'planet5') )
        # self.planets.append( co.celestialobject(268, 'magenta', self.canvas, [1000, 1000], [-.1, -.1], 'planet6') )
        # self.planets.append( co.celestialobject(250, 'brown', self.canvas, [500, 1000], [0, 1], 'planetX') )
        G = self.G.get()
        self.planets.append( co.celestialobject(1000, 'yellow', self.canvas, self.center, [0., 0.], 'planet1') )
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
                co.celestialobject.set_force_2_celestialobjects(self.planets[i], self.planets[j], G, alpha)

    def set_deltas(self, delta_t):
        option = self.center_CO.get()
        if option == 'COM':
            self.Delta = self.coordsCOMNew - self.coordsCOM
            if delta_t == 0:
                self.correction_velocity = np.array([0,0]).astype(np.double)
            else:
                self.correction_velocity = -self.Delta / delta_t
            self.correction_acceleration = np.array([0,0]).astype(np.double)
        elif option == 'Absolute':
            self.Delta = np.array([0,0]).astype(np.double)
            self.correction_velocity = np.array([0,0]).astype(np.double)
            self.correction_acceleration = np.array([0,0]).astype(np.double)
        else:
            planet = self.color_planet[option]
            self.Delta = planet.velocity * delta_t
            self.correction_velocity = -planet.velocity
            self.correction_acceleration = -planet.acceleration

    def next_step(self):
        self.calculate_forces()
        # deque(map(self.new_state_planets, self.planets))
        delta_t = self.Delta_t.get()
        for planet in self.planets:
            planet.new_state_planet(delta_t)

        self.coordsCOMNew = self.get_coords_com()
        self.set_deltas(delta_t)

        # deque(map(self.move_object, self.planets))
        for planet in self.planets:
            change =  (planet.velocity*delta_t - self.Delta)*self.current_zoom_factor
            planet.move_object(change)
            planet.draw_acceleration_arrow(correction=self.correction_acceleration)
            planet.draw_velocity_arrow(correction=self.correction_velocity )
        COM_change = (self.coordsCOMNew - self.coordsCOM - self.Delta)*self.current_zoom_factor
        self.canvas.move(self.COM, COM_change[0], COM_change[1])
        self.coordsCOM = self.coordsCOMNew

    def init_UI(self):

        # create frames
        self.frame_animation = tk.Frame(self.root, bd=1, relief="sunken")
        self.frame_controls = tk.Frame(self.root, bd=1, relief="sunken")

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


        self.UI_frame_animation_controls()

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, (1+self.zoom_factor), (1+self.zoom_factor))
            self.current_zoom_factor*= (1+self.zoom_factor)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, (1-self.zoom_factor), (1-self.zoom_factor))
            self.current_zoom_factor*= (1-self.zoom_factor)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def UI_frame_animation_controls(self):
        # controls frame
        self.frame_controls = tk.Frame(self.root, width=100, height=self.height)
        self.frame_controls.grid(row=0, column=1, sticky='nw')
        # play
        self.play = tk.Button(self.frame_controls, text="play", command=self.do_play)
        self.play.grid(column=0, row=0, sticky='w')
        # Pause
        self.pause = tk.Button(self.frame_controls, text="pause", command=self.do_pause)
        self.pause.grid(column=1, row=0, sticky='w')
        # Speed
        self.delay_slider = tk.Scale(
            self.frame_controls, from_=0, to=.75, resolution=.01, orient=tk.HORIZONTAL, variable=self.delay)
        self.delay_slider.grid(column=3, row=0, sticky='w')
        # G
        self.G_slider = tk.Scale(
            self.frame_controls, from_=0, to=100, resolution=.5, orient=tk.HORIZONTAL, variable=self.G)
        self.G_slider.grid(column=0, row=1, sticky='w')
        # alpha
        self.alpha_slider = tk.Scale(
            self.frame_controls, from_=-3, to=3, resolution=.01, orient=tk.HORIZONTAL, variable=self.alpha)
        self.alpha_slider.grid(column=0, row=2, sticky='w')
        # delta_t
        self.Delta_t_slider = tk.Scale(
            self.frame_controls, from_=-20, to=20, resolution=.001, orient=tk.HORIZONTAL, variable=self.Delta_t)
        self.Delta_t_slider.grid(column=0, row=3, sticky='w')

        self.button_shuffle_COM = tk.Button(self.frame_controls, text="COM")
        self.button_shuffle_COM.configure(command=self.pressed_shuffle_COM)
        self.button_shuffle_COM.configure(relief=tk.SUNKEN)
        self.button_shuffle_COM.grid(column=0, row=4, sticky='w')
        self.shuffle_COM = True

        # dropdown of center
        self.dropdown_center = tk.OptionMenu(self.frame_controls, self.center_CO, *self.dropdown_list )
        self.dropdown_center.configure(width=20)
        self.dropdown_center.grid(column=0, row=5, sticky='w')
        # information on the bodies

        # planet 1

        # self.label_planet_1_pos = tk.Label(self.frame_controls, text = '', width = 20)
        # self.label_planet_1_pos.grid(column=0, row=4, sticky='w')

        # self.label_planet_1_v = tk.Label(self.frame_controls, text = '', width = 20)
        # self.label_planet_1_v.grid(column=0, row=5, sticky='w')

        # self.label_COM_delta = tk.Label(self.frame_controls, text = '', width = 20)
        # self.label_COM_delta.grid(column=0, row=6, sticky='w')

        # self.label_COM = tk.Label(self.frame_controls, text = '', width = 20)
        # self.label_COM.grid(column=0, row=7, sticky='w')

    def pressed_shuffle_COM(self):
        if self.shuffle_COM:
            self.button_shuffle_COM.configure(relief=tk.RAISED)
            self.shuffle_COM = False
            print(self.shuffle_COM)
        else:
            self.button_shuffle_COM.configure(relief=tk.SUNKEN)
            self.shuffle_COM = True
            print(self.shuffle_COM)



    def loop(self):
        while True:
            # time.sleep(.5)
            if self.stop:
                print("stopped")
                break
            self.status = "continue_while_loop"
            while self.status == "continue_while_loop":
                self.status = "enter_for_loop_again"
                self.pause.update()
                self.play.update()
                if self.running:
                    self.next_step()
                    time.sleep(self.delay_slider.get())
                else:
                    self.status = "enter_for_loop_again"

    def do_stop(self):
        self.stop = True


    def do_pause(self):
        self.running = False
        # global running
        # running = False

    def do_play(self):
        self.running = True
        self.stop = False


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