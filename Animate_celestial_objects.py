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
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
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
        while True:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events()
            if not self.pause:
                self.next_step()
                self.draw_all()
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
        self.zoom_step_factor = .05
        self.zoom_factor = 1
        self.zoom_position = [0,0]
        self.do_draw_tails = True
        self.do_draw_arrows = True
        self.do_collide = True
        self.G = 15
        self.alpha = 2.1
        self.delta_t = .1
        self.delay = 20
        self.correction_velocity = np.zeros((2,))
        self.correction_acceleration = np.zeros((2,))

    def initialise_planets(self):
        self.celestial_objects = []
        self.celestial_objects.append( 
        co.Celestialobject(
            1000, 
            'yellow', 
            self.center+np.array([-150., 0.]), 
            np.array([0, 0.]), 
            'celestial_object1'
            )

        )
        print(self.celestial_objects[0], self.G)
        testtraj = co.Trajectory( 
            self.celestial_objects[0], self.G
            )
        print(testtraj.G, testtraj.orbited_celestial_objects,
              testtraj.angle, testtraj.direction, testtraj.eccentricity)

        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            700, 
            'magenta', 
            self.center+np.array([150., 0.]),
            co.Trajectory( 
                self.celestial_objects[0], self.G
                ),
                'celestial_object2'
                                  )
                            )
        #Ellipse
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            200, 
            'blue', 
            self.center+np.array([800, -200]),
            co.Trajectory( 
                self.celestial_objects[0:2], self.G,
                eccentricity=.7, angle=math.pi/11,direction = -1
                ),
                'celestial_object4'
                                  )
                            )
        # planet+two moons
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            100, 
            'red', 
            self.center+np.array([0., 1500]),
            co.Trajectory( 
                self.celestial_objects[0:2], self.G
                ),
                'planet'
                                  )
                            )



        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            10, 
            'gold', 
            self.center+np.array([150, 1500]),
            co.Trajectory( 
                self.celestial_objects[3], self.G
                ),
                'moon'
                                  )
                            )
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            1, 
            'green', 
            self.center+np.array([150, 1500+10]),
            co.Trajectory( 
                self.celestial_objects[4], self.G
                ),
                'moon 2'
                                  )
                            )
        #binary planets
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            100, 
            'coral', 
             
            self.center+np.array([-850,250]),
            co.Trajectory( 
                self.celestial_objects[0:2], self.G,
                direction=-1
                ),
                'planet'
                                  )
                            )        
        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            76, 
            'orange', 
             
            self.center+np.array([-870,100]),
            co.Trajectory( 
                self.celestial_objects[6], self.G,
                direction=-1
                ),
                'planet'
                                  )
                            )

        self.celestial_objects.append( 
            co.Celestialobject.fromtrajectory(
            1, 
            'orange', 
            self.center+np.array([-8070,100]),
            co.Trajectory( 
                self.celestial_objects[0:2], self.G,
                direction=-1, eccentricity=2
                ),
                'planet'
                                  )
                            )
        self.mass_of_all_planets = sum([planet.mass for planet in self.planets])
        self.coordsCOM = co.get_coords_com(self.planets)
            # self.init_COM()

    def draw_arrow(self, color, start, end):
        pygame.draw.aaline(self.surface, color, start, end, 1)
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(self.surface, color, 
                            (
            (end[0]+2*math.sin(math.radians(rotation)), 
             end[1]+2*math.cos(math.radians(rotation))),
            (end[0]+2*math.sin(math.radians(rotation-120)), 
             end[1]+2*math.cos(math.radians(rotation-120))),
            (end[0]+2*math.sin(math.radians(rotation+120)), 
             end[1]+2*math.cos(math.radians(rotation+120))))
                    )

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

    def draw_tail(self, planet):
        planet.update_tail(1000)
        color_rgb = pygame.Color(planet.color)
        length_tail = len(planet.tail)
        for i, pos in enumerate(planet.tail):
            color_rgb.a = int(255 * i / length_tail)
            self.surface.fill(color_rgb, (self.get_zoomed_coordinates(pos), (1, 1)))


    def next_step(self):
        co.set_new_state(self.planets, self.G, self.alpha,
                         self.delta_t, self.do_collide)
        for planet in self.planets:
            if co.norm(planet.position) > self.limits:
                print("planet: "  +planet.name + " will be removed")
                self.planets.remove(planet)
        self.coordsCOMNew = co.get_coords_com(self.planets)
        self.set_deltas()

        self.coordsCOM = self.coordsCOMNew


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

