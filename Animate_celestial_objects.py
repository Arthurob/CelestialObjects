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


class Animate_celestial_objects():
    """
    Animates the celestial objects and creates the GUI to control the physics of the animation

    """


    def __init__(self):
        #self.running = True
        self.start()



    def start(self):
        """
        Setup all the variables

        Returns
        -------
        None.

        """

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
        self.G.set(20)
        self.zoom_factor = .05
        self.current_zoom_factor = 1
        self.center = [500.,500.] # np.array([self.canvas.winfo_width(), self.canvas.winfo_height()])/2
        self.celestial_objects = []
        self.dropdown_list = ['COM','Absolute']
        self.draw_graph = True
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
        self.initialise_celestial_objects()
        self.step = 0
        self.celestial_initizalized = True
        self.next_step()
        self.root.mainloop()



    def initialise_celestial_objects(self):
        """
        Create some celestial objects

        Returns
        -------
        None.

        """

        G = self.G.get() # Get current value of G for seting up circulair trajectorys
        #0
        self.celestial_objects.append( 
            co.Celestialobject(
                1000, 
                'yellow', 
                self.canvas, 
                self.center+np.array([-150., 0.]), 
                np.array([0, 0.]), 
                'celestial_object1'
                )
                                      
            )
        #1
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            700, 
            'magenta', 
            self.canvas, 
            self.center+np.array([150., 0.]),
            co.Trajectory( 
                self.celestial_objects[0], G
                ),
                'celestial_object2'
                                  )
                            )
        #Ellipse
        #2
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            200, 
            'blue', 
            self.canvas, 
            self.center+np.array([800, -200]),
            co.Trajectory( 
                self.celestial_objects[0:2], G,
                eccentricity=.7, angle=math.pi/11,direction = -1
                ),
                'celestial_object4'
                                  )
                            )
        # planet+two moons
        #3
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            100, 
            'red', 
            self.canvas, 
            self.center+np.array([0., 1500]),
            co.Trajectory( 
                self.celestial_objects[0:2], G,
                eccentricity=.5, angle=-math.pi/4
                ),
                'planet'
                                  )
                            )
        

        #4
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            10, 
            'gold', 
            self.canvas, 
            self.center+np.array([179, 1500]),
            co.Trajectory( 
                self.celestial_objects[3], G
                ),
                'moon'
                                  )
                            )
        #5
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            1, 
            'green', 
            self.canvas, 
            self.center+np.array([179-20, 1500+10]),
            co.Trajectory( 
                self.celestial_objects[4], G, direction=-1
                ),
                'moon 2'
                                  )
                            )
        #binary planets
        #6
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            100, 
            'coral', 
            self.canvas, 
            self.center+np.array([-850,250]),
            co.Trajectory( 
                self.celestial_objects[0:2], G,
                direction=-1
                ),
                'planet'
                                  )
                            )     
        #7
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            76, 
            'orange', 
            self.canvas, 
            self.center+np.array([-870,100]),
            co.Trajectory( 
                self.celestial_objects[6], G,
                direction=-1
                ),
                'planet'
                                  )
                            )
        
        #8
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            1, 
            'orange', 
            self.canvas, 
            self.center+np.array([-8070,100]),
            co.Trajectory( 
                self.celestial_objects[0:2], G,
                direction=-1, eccentricity=2
                ),
                'planet'
                                  )
                            )

        # # self.celestial_objects.append( co.Celestialobject(400, 'red', self.canvas, self.center+np.array([-100,-60]), [-10, 3], 'celestial_object1') )
        # # # self.celestial_objects.append( co.Celestialobject(11, 'blue', self.canvas, self.center+np.array([0,-150]), [math.sqrt(self.G.get()*self.celestial_objects[0].mass/150), 0.], 'celestial_object2') )
        # # self.celestial_objects.append( co.Celestialobject(3, 'orange', self.canvas, self.center+np.array([0,160]), [-math.sqrt(G*self.celestial_objects[0].mass/150), 0.], 'celestial_object3') )
        # # # # self.celestial_objects.append( co.Celestialobject(20, 'green', self.canvas, self.center+np.array([-80,40]), [1, 0.1], 'celestial_object4') )
        # # # self.celestial_objects.append( co.Celestialobject(20, 'green', self.canvas, self.center+np.array([-80,40]), [-1, 10], 'celestial_object4') )
        # # self.celestial_objects.append( co.Celestialobject(50, 'purple', self.canvas, [0., 0.], [.1, .05], 'celestial_object5') )
        # # # self.celestial_objects.append( co.Celestialobject(268, 'magenta', self.canvas, [1000, 1000], [-.1, -.1], 'celestial_object6') )
        # # self.celestial_objects.append( co.Celestialobject(10, 'blue', self.canvas, self.center+np.array([0,-150]), [math.sqrt(G*self.celestial_objects[0].mass/150), 0.1], 'celestial_object2') )
        # # self.celestial_objects.append( co.Celestialobject(5, 'green', self.canvas, self.center+np.array([0,400]), [math.sqrt(G*self.celestial_objects[0].mass/400)+1, -1], 'celestial_object3') )
        # # self.celestial_objects.append( co.Celestialobject(20, 'coral', self.canvas, self.center+np.array([-80,40]), [-1, 13], 'celestial_object4') )
        # # self.celestial_objects.append( co.Celestialobject(250, 'brown', self.canvas, [500, 1000], [-5, 1], 'celestial_objectX') )
        # # self.celestial_objects.append( co.Celestialobject(10, 'gold', self.canvas, [500+60, 1000], [-5.1,1 + math.sqrt(G*250/60)], 'celestial_objectXMoon'))
        # m1 = 100
        # m2 = 5
        # r = 1000
        # #Circulair        
        # self.celestial_objects.append( 
        #     co.Celestialobject(5, 'blue', self.canvas, 
        #                        self.center+np.array([r,-100]), [0.,  math.sqrt(G*m1*m1/(r*(m1+m2)))], 
        #                        'celestial_object2') 
        #     )
        #planet+two moons
        # self.celestial_objects.append( 
        #     co.Celestialobject(100, 'red', self.canvas, 
        #                         self.center+np.array([0,r]), [0., 0.], 
        #                         'celestial_object1',
        #                         trajectory={'name':'circulair',
        #                                     'orbited celestial objects': self.celestial_objects[0:2], 
        #                                     'G':G, 
        #                                     'direction': 1}
        #                         ) 
        #     )

        
        # self.celestial_objects.append( 
        #     co.Celestialobject(m2, 'blue', self.canvas, 
        #                         self.center+np.array([50,r]), [0., 0.], 
        #                         'celestial_object2',
        #                         trajectory={'name':'circulair',
        #                                     'orbited celestial objects': self.celestial_objects[3], 
        #                                     'G':G, 
        #                                     'direction': -1})
        #     )
        # self.celestial_objects.append( 
        #     co.Celestialobject(1, 'green', self.canvas, 
        #                         self.center+np.array([10,r+60]), [0., 0.], 
        #                         'celestial_object2',
        #                         trajectory={'name':or'circulair',
        #                                     'orbited celestial objects': self.celestial_objects[3:5], 
        #                                     'G':G, 
        #                                     'direction': 1})
        #     )
        # #binary planets
        # self.celestial_objects.append( 
        #     co.Celestialobject(75, 'coral', self.canvas, 
        #                         self.center+np.array([-450,250]), [0., 0.], 
        #                         'celestial_object1',
        #                         trajectory={'name':'circulair',
        #                                     'orbited celestial objects': self.celestial_objects[0:2], 
        #                                     'G':G, 
        #                                     'direction': 1}
        #                         ) 
        #     )        
        # self.celestial_objects.append( 
        #     co.Celestialobject(70, 'gold', self.canvas, 
        #                         self.center+np.array([-470,160]), [0., 0.], 
        #                         'celestial_object2',
        #                         trajectory={'name':'circulair',
        #                                     'orbited celestial objects': self.celestial_objects[6], 
        #                                     'G':G, 
        #                                     'direction': -1})
        #     )

        
        # # self.celestial_objects.append( 
        # #     co.Celestialobject(m, 'yellow', self.canvas, 
        # #                         self.center+np.array([-]), [0., -math.sqrt(G*m/(2*r))], 
        # #                         'celestial_object1') 
        # #     )
        # # self.celestial_objects.append( 
        # #     co.Celestialobject(m, 'green', self.canvas, 
        # #                         self.center+np.array([r,0]), [0.,  math.sqrt(G*m/(2*r))], 
        # #                         'celestial_object2') 
        # #     )
        

        self.celestial_objects_colors = [celestial_object.color for celestial_object in self.celestial_objects]
        self.dropdown_list += self.celestial_objects_colors
        menu = self.dropdown_center['menu']
        for color in self.celestial_objects_colors:
            menu.add_command(label=color, command=lambda value=color: self.center_CO.set(value))
        self.color_celestial_object = dict(zip(self.celestial_objects_colors, self.celestial_objects))
        # create center of mass marker
        self.coordsCOM = co.get_center_of_mass_coordinates(self.celestial_objects)
        self.COM = self.canvas.create_line(self.coordsCOM[0]-5, self.coordsCOM[1]-5, self.coordsCOM[0]+5, self.coordsCOM[1]+5, self.coordsCOM[0], self.coordsCOM[1], self.coordsCOM[0]-5, self.coordsCOM[1]+5, self.coordsCOM[0]+5, self.coordsCOM[1]-5, fill='white')
        self.next_step()

    def get_coords_com(self):
        """
        Get the center of mass (com) coordinates

        Returns
        -------
        array
            Get the center of mass (com) coordinates

        """
        return sum([celestial_object.mass*celestial_object.position for celestial_object in self.celestial_objects]) / sum([celestial_object.mass for celestial_object in self.celestial_objects])


    def set_new_state_celestial_objects(self, celestial_object):
        """
        Parameters
        ----------
        celestial_object : celestial_object
            Calculate and set the new state (acceleration, velocity and position).

        Returns
        -------
        None.

        """

        acceleration = celestial_object.force / celestial_object.mass
        delta_t = self.Delta_t.get()
        celestial_object.velocity += acceleration*delta_t
        celestial_object.position += celestial_object.velocity*delta_t


    def calculate_forces(self):
        """
        Calculate all the forces between the Celestial objects

        Returns
        -------
        None.

        """
        alpha = self.alpha.get()
        G = self.G.get()
        for celestial_object in self.celestial_objects:
            celestial_object.reset_force()
        for i in range(len(self.celestial_objects)-1):
            for j in range(i+1, len(self.celestial_objects)):
                co.set_force_2_celestialobjects(self.celestial_objects[i], self.celestial_objects[j], G, alpha)

    def set_corrections(self, delta_t):
        """
        Set the corrections for the graphics depending on which celestial objects is cenetered

        Parameters
        ----------
        delta_t : numerical
            the time interval

        Returns
        -------
        None.

        """
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
            celestial_object = self.color_celestial_object[option]
            self.Delta = celestial_object.velocity * delta_t
            self.correction_velocity = -celestial_object.velocity
            self.correction_acceleration = -celestial_object.acceleration

    def next_step(self):
        """
        orchestrates the cqlculations and drawing of the next step/interval

        Returns
        -------
        None.

        """
        self.calculate_forces()
        delta_t = self.Delta_t.get()
        self.time += delta_t
        self.time_list.append(self.time)
        for celestial_object in self.celestial_objects:
            celestial_object.new_state(delta_t)

        self.coordsCOMNew = co.get_center_of_mass_coordinates(self.celestial_objects)
        self.set_corrections(delta_t)
        self.plot_speed.clear()
        self.plot_acceleration.clear()
        self.plot_phi.clear()
        self.length_list = len(self.time_list)
        for celestial_object in self.celestial_objects:
            change =  (celestial_object.velocity*delta_t - self.Delta)*self.current_zoom_factor
            celestial_object.move_object(change, draw_tail=self.draw_tail)
            celestial_object.draw_acceleration_arrow(correction=self.correction_acceleration,
                                           factor=self.arrow_factor_acceleration.get()*self.current_zoom_factor)
            celestial_object.draw_velocity_arrow(correction=self.correction_velocity,
                                       factor=self.arrow_factor_velocity.get()*self.current_zoom_factor )

            self.update_data_graphs(celestial_object)

        if self.draw_graph:
            self.draw_graphs()


        COM_change = (self.coordsCOMNew - self.coordsCOM - self.Delta)*self.current_zoom_factor
        self.canvas.move(self.COM, COM_change[0], COM_change[1])
        self.coordsCOM = self.coordsCOMNew
        # continue or pause loop

        if self.running:
          self.root.after(self.delay_slider.get()+1, self.next_step)

    def update_data_graphs(self, celestial_object):
        """
        update the plotted data of a celestial object
        Parameters
        ----------
        celestial_object : celestial_object

        Returns
        -------
        None.

        """
        self.plot_speed.plot(
                 self.time_list[-min(self.length_list, MAX_PLOTLENGTH):],
                 celestial_object.speed_history[-min(self.length_list, MAX_PLOTLENGTH):], color=celestial_object.color)

        self.plot_acceleration.plot(
             self.time_list[-min(self.length_list, MAX_PLOTLENGTH):],
             celestial_object.acceleration_history[-min(self.length_list, MAX_PLOTLENGTH):], color=celestial_object.color)

        self.plot_phi.plot(
             self.time_list[-min(self.length_list, MAX_PLOTLENGTH):],
                celestial_object.phi_history[-min(self.length_list, MAX_PLOTLENGTH):], color=celestial_object.color)

    def draw_graphs(self):
        """
        Draw the graphs

        Returns
        -------
        None.

        """
        self.canvas_graph_speed.draw()
        self.canvas_graph_acceleration.draw()
        self.canvas_graph_phi.draw()

    def init_UI(self):
        """
        Initialize the UI

        Returns
        -------
        None.

        """

        # create frames
        self.frame_animation = tk.Frame(self.root, bd=1, relief="sunken")
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

        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<MouseWheel>",self.zoomer)

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


    def move_start(self, event):
        """
        Used to drag on the canvas

        Parameters
        ----------
        event : event
            tkinter event

        Returns
        -------
        None.

        """
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        """
        Used to drag on the canvas

        Parameters
        ----------
        event : event
            tkinter event

        Returns
        -------
        None.

        """
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def pressed_tail(self):
        """
        Used to enable drawing the tails/trails of the celestial through the GUI button

        Returns
        -------
        None.

        """
        if self.draw_tail:
            self.button_tail.configure(relief=tk.RAISED)
        else:
            self.button_tail.configure(relief=tk.SUNKEN)
        self.draw_tail = not self.draw_tail
        print(self.draw_tail)

    #windows zoom
    def zoomer(self,event):
        """
        Zoom action

        Parameters
        ----------
        event : event

        Returns
        -------
        None.

        """
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, (1+self.zoom_factor), (1+self.zoom_factor))
            self.current_zoom_factor *= (1+self.zoom_factor)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, (1-self.zoom_factor), (1-self.zoom_factor))
            self.current_zoom_factor *= (1-self.zoom_factor)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))


    def UI_frame_animation_controls(self):
        """
        setup the controls frame

        Returns
        -------
        None.

        """
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
        """
        setup the tab that controls the variables that are used in the calculation of
        the forces (G, delta_t, alpha)


        Returns
        -------
        None.

        """
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
            self.tab_physics, from_=-10, to=10, length = 200, tickinterval=2, resolution=.1,
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
            self.tab_physics, from_=0, to=1000, length = 200, tickinterval=100, resolution=5,
            orient=tk.HORIZONTAL, variable=self.arrow_factor_acceleration)
        self.arrow_factor_acceleration_slider.grid(row=row, column=0, sticky='w')

        # tails
        row+=1
        self.button_tail = tk.Button(self.tab_physics, text="tails")
        self.button_tail.configure(command=self.pressed_tail)
        self.button_tail.configure(relief=tk.RAISED)
        self.button_tail.grid(row=row, column=0, sticky='w')

    def UI_graphs(self):
        """
        Setup the UI that draws the graphs

        Returns
        -------
        None.

        """
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
        self.celestial_object_1 = co.Celestialobject(1, 10, self.center+np.array([0,0]))
        self.celestial_object_2 = co.Celestialobject(1, 10, self.center+np.array([1,-50]),[.5,0])

"""