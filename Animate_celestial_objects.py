# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 23:08:18 2021

@author: Arthur
"""
import pygame
import sys
import celestialobject as co
import numpy as np
import math
import pygame_widgets
from pygame import gfxdraw
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import traceback


class Animate_celestial_objects_pygame():

    def __init__(self):
        SCREEN_SIZE = WIDTH, HEIGHT = (1000, 1000)

        # Initialization
        pygame.init()
        # self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE, pygame.HWSURFACE) #,  pygame.SRCALPHA)
        # self.screen = pygame.display.set_mode((1000, 1000), pygame.SCALED)
        pygame.display.set_caption('Celestial objects')
        self.fps = pygame.time.Clock()
        self.pause = False

        self.center = np.array([WIDTH,HEIGHT])/2
        # self.init_window()
        self.init_vars()
        # self.init_UI()
        self.initialise_planets()
        self.celestial_initizalized = True
        self.mainloop()

    def mainloop(self):
        #Mainloop
        while True:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events()
            if not self.pause:
                self.next_step()
                self.draw_all()
                # self.fps.tick(60)
                pygame.time.delay(self.delay)

    def handle_events(self):
        if self.event.type == pygame.KEYUP:
                        if self.event.key == pygame.K_SPACE:
                            self.pause = not self.pause
        if self.event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
        self.handle_zoom()

    def handle_zoom(self):
        if self.event.type == pygame.MOUSEWHEEL:
            if (self.event.y>0 and self.zoom_factor <= 10) or (self.event.y<0 and .1 <= self.zoom_factor):
                self.zoom_factor *= (1+self.event.y*self.zoom_step_factor)
                x, y = pygame.mouse.get_pos()
                self.zoom_position = np.array([x,y]).astype(np.float32)






    def init_vars(self):
        # variables
        self.counter = 0
        self.limits = 30000
        # self.delay = tk.IntVar()
        # self.delay.set(0)
        # self.alpha = tk.DoubleVar()
        # self.alpha.set(2)
        # self.Delta_t = tk.DoubleVar()
        # self.Delta_t.set(.1)
        # self.G = tk.IntVar()
        # self.G.set(10)
        self.zoom_step_factor = .05
        self.zoom_factor = 1
        self.zoom_position = [0,0]
        # self.self.center = [500.,500.] # np.array([self.canvas.winfo_width(), self.canvas.winfo_height()])/2

        # self.dropdown_list_center = ['COM','Absolute']
        # self.dropdown_list_stats = ['Absolute']
        # self.draw_graph = False
        # self.center_CO = tk.StringVar()
        # self.center_CO.set('COM')
        # self.stats_CO = tk.StringVar()
        # self.stats_CO.set('Absolute')
        # self.arrow_factor_velocity = tk.IntVar()
        # self.arrow_factor_velocity.set(10)
        # self.arrow_factor_acceleration = tk.IntVar()
        # self.arrow_factor_acceleration.set(180)
        # self.time_list = []
        # self.time = 0
        self.do_draw_tails = True
        self.do_draw_arrows = True
        # self.running = False
        # self.do_display_stats = False
        self.do_collide = True
        self.G = 15
        self.alpha = 2.1
        self.delta_t = .1
        self.delay = 20
        self.correction_velocity = np.zeros((2,))
        self.correction_acceleration = np.zeros((2,))

    def initialise_planets(self):


            self.planets = []
            self.planets.append( co.celestialobject(1000, 'yellow',   self.center+np.array([152,160]), [-3., -2.], 'planet1') )
            self.planets.append( co.celestialobject(1000, 'gray',  self.center+np.array([20,-10]), [10,30], 'planet24') ) #+np.array([-250,-160]), [.2,-.1]
            self.planets.append( co.celestialobject(2000, 'pink',  self.center, [.0001,-.0002], 'planet242') )
            self.planets.append( co.celestialobject(400, 'red',  self.center+np.array([432,160]), [0.,3], 'planet1') )
            self.planets.append( co.celestialobject(3, 'orange',  self.center+np.array([0,160]), [-math.sqrt(self.G*self.planets[0].mass/150), 0.], 'planet3') )
            self.planets.append( co.celestialobject(50, 'purple',   [0., 0.], [.1, .05], 'planet5') )
            self.planets.append( co.celestialobject(268, 'magenta',   [1000, 1000], [-.1, -.1], 'planet6') )
            self.planets.append( co.celestialobject(250, 'brown',   [500, 1000], [-5, 1], 'planetX') )
            self.planets.append( co.celestialobject(10, 'gold',   [500+60, 1000], [-5.1,1 + math.sqrt(self.G*250/60)], 'planetXMoon'))
            self.planets.append( co.celestialobject(1, 'blue',   self.center+np.array([0,-150]), [math.sqrt(self.G*self.planets[0].mass/150), 0.1], 'planet2') )
            self.planets.append( co.celestialobject(5, 'green',  self.center+np.array([0,400]), [math.sqrt(self.G*self.planets[0].mass/400)+1, -1], 'planet3') )
            # self.planets.append( co.celestialobject(20, 'coral',   self.center+np.array([-80,40]), [-1, 1.3], 'planet4') )
            self.mass_of_all_planets = sum([planet.mass for planet in self.planets])
            self.coordsCOM = co.get_coords_com(self.planets)
            # self.init_COM()

    def draw_arrow(self, color, start, end):
        pygame.draw.aaline(self.surface, color, start, end, 1)
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(self.surface, color, ((end[0]+2*math.sin(math.radians(rotation)), end[1]+2*math.cos(math.radians(rotation))), (end[0]+2*math.sin(math.radians(rotation-120)), end[1]+2*math.cos(math.radians(rotation-120))), (end[0]+2*math.sin(math.radians(rotation+120)), end[1]+2*math.cos(math.radians(rotation+120)))))

    def draw_all(self):
        width, height = self.screen.get_size()
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.surface.fill(pygame.Color('black'))
        for planet in self.planets:
                    if self.do_draw_tails:
                self.draw_tail(planet)

        for planet in self.planets:
            corrected_position = self.get_zoomed_coordinates(planet.position - self.Delta)
            self.draw_COs(planet, corrected_position)
            # surface_mother.blit(self.surface, (0,0))

            if self.do_draw_arrows:
                self.draw_arrows(planet, corrected_position)



        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def get_zoomed_coordinates(self, coordinate):
        return self.zoom_factor*(coordinate - self.zoom_position) + self.zoom_position


    def draw_arrows(self, planet, corrected_position):
        self.draw_arrow(pygame.Color(planet.color), corrected_position
                       , corrected_position+(planet.force/planet.mass - self.correction_acceleration )*100)
        self.draw_arrow(pygame.Color(planet.color), corrected_position
                       , corrected_position+(planet.velocity - self.correction_velocity )*10)

    def draw_COs(self, planet, corrected_position):
        color = pygame.Color(planet.color)
        x, y = int(corrected_position[0]), int(corrected_position[1])
        r = int(self.zoom_factor*planet.radius)
        gfxdraw.filled_circle(self.surface, x, y,r,  color)
        gfxdraw.aacircle(self.surface, x, y ,r , color)

    # def draw_COM(self):
    #     self.


    def draw_tail(self, planet):
        planet.update_tail(1000)
        color_rgb = pygame.Color(planet.color)
        length_tail = len(planet.tail)
        for i, pos in enumerate(planet.tail):
            color_rgb.a = int(255 * i / length_tail)
            self.surface.fill(color_rgb, (self.get_zoomed_coordinates(pos), (1, 1)))


    def next_step(self):
        # self.counter += 1
        # delta_t = Delta_t.get()
        # time += delta_t
        # time_list.append(time)

        # self.get_coords_com()

        co.set_new_state(self.planets, self.G, self.alpha,
                         self.delta_t, self.do_collide)
        for planet in self.planets:
            if co.norm(planet.position) > self.limits:
                print("planet: "  +planet.name + " will be removed")
                self.planets.remove(planet)
        self.coordsCOMNew = co.get_coords_com(self.planets)
        self.set_deltas()
        # set_deltas()
        # plot_speed.clear()
        # plot_acceleration.clear()
        # plot_phi.clear()
        # length_list = len(time_list)

        self.coordsCOM = self.coordsCOMNew


        # if do_display_stats:
        #     display_stats()
        # if collision:
        #         # running = False
        #         collision = False
        # if running:
        #     master.after(max(delay_slider.get(),1), next_step)


    def set_deltas(self):
        option = 'COM'
        if option == 'COM':
            self.Delta = self.coordsCOMNew - self.coordsCOM
            if self.delta_t == 0:
                self.correction_velocity = np.zeros((2,))
                self.correction_acceleration = np.zeros((2,))
            else:
                self.correction_velocity = -self.Delta / self.delta_t
                self.correction_acceleration = -self.Delta / (self.delta_t * self.delta_t)
            self.correction_acceleration = np.zeros((2,))
        elif option == 'Absolute':
            self.Delta = np.zeros((2,))
            self.correction_velocity = np.zeros((2,))
            self.correction_acceleration = np.zeros((2,))
        else:
            planet = self.color_planet[option]
            self.Delta = planet.velocity * self.delta_t
            self.correction_velocity = -planet.velocity
            self.correction_acceleration = -planet.acceleration


try:
    animation = Animate_celestial_objects_pygame()
except:
    print("Unexpected error:", sys.exc_info())
    print(traceback.format_exc())
    pygame.quit()
    sys.exit()
    raise

