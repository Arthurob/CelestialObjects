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


class Animate_celestialobjects_pygame():

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
        
    def init_vars(self):
        # variables
        self.counter = 0
        self.zoom_step_factor = .05
        self.zoom_factor = 1
        self.zoom_factor_old = 1
        self.zoom_position = np.zeros((2,))
        self.zoom_position_old = np.zeros((2,))
        self.zoom_position_cm_frame = np.zeros((2,))
        self.zoom_position_old_cm_frame = np.zeros((2,))
        self.do_draw_tails = True
        self.do_draw_arrows = True
        self.do_collide = True
        self.G = 15
        self.alpha = 2
        self.delta_t = 1
        self.delay = 0
        self.correction_velocity = np.zeros((2,))
        self.correction_acceleration = np.zeros((2,))
        self.limits = 10000

    def initialise_planets(self):
        self.celestialobjects = []
        self.celestialobjects.append( 
        co.Celestialobject(
            1000, 
            'yellow', 
            self.center+np.array([-150., 0.]), 
            np.array([0, 0.]), 
            'celestial_object1'
            )

        )

        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            400, 
            'magenta', 
            self.center+np.array([150., 0.]),
            co.Trajectory( 
                self.celestialobjects[0], self.G
                ),
                'celestial_object2'
                                  )
                            )
        #Ellipse
        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            200, 
            'blue', 
            self.center+np.array([800, -200]),
            co.Trajectory( 
                self.celestialobjects[0:2], self.G,
                eccentricity=.7, angle=math.pi/11,direction = -1
                ),
                'celestial_object4'
                                  )
                            )
        # planet+two moons
        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            100, 
            'red', 
            self.center+np.array([0., 1500]),
            co.Trajectory( 
                self.celestialobjects[0:2], self.G,
                eccentricity=.3, angle=-math.pi/5
                ),
                'planet'
                                  )
                            )



        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            10, 
            'gold', 
            self.center+np.array([150, 1500]),
            co.Trajectory( 
                self.celestialobjects[3], self.G
                ),
                'moon'
                                  )
                            )
        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            1, 
            'green', 
            self.center+np.array([150, 1500+10]),
            co.Trajectory( 
                self.celestialobjects[4], self.G
                ),
                'moon 2'
                                  )
                            )
        #binary planets
        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            100, 
            'coral', 
             
            self.center+np.array([-850,250]),
            co.Trajectory( 
                self.celestialobjects[0:2], self.G,
                direction=-1
                ),
                'planet'
                                  )
                            )        
        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            76, 
            'orange', 
             
            self.center+np.array([-870,100]),
            co.Trajectory( 
                self.celestialobjects[6], self.G,
                direction=-1
                ),
                'planet'
                                  )
                            )

        self.celestialobjects.append( 
            co.Celestialobject.fromtrajectory(
            1, 
            'orange', 
            self.center+np.array([-8070,100]),
            co.Trajectory( 
                self.celestialobjects[0:2], self.G,
                direction=-1, eccentricity=2
                ),
                'planet'
                                  )
                            )
        self.mass_of_all_planets = sum([planet.mass for planet in self.celestialobjects])
        self.coordsCOM = co.get_center_of_mass_coordinates(self.celestialobjects)
        co.substract_centerofmass_velocity(self.celestialobjects)
            # self.init_COM()

    def mainloop(self):
        while True:
            if not self.pause:
                self.next_step()
                self.draw_all()
                pygame.time.delay(self.delay)
            
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events()
                    
    def handle_events(self):
        if self.event.type == pygame.KEYUP:
                        if self.event.key == pygame.K_SPACE:
                            self.pause = not self.pause
        if self.event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print("you clicked at:", pos, self.counter)
        self.handle_zoom()

    def handle_zoom(self):
        if self.event.type == pygame.MOUSEWHEEL:
            if ((self.event.y>0 and self.zoom_factor <= 100) or 
                (self.event.y<0 and .01 <= self.zoom_factor)):
                self.zoom_position_old = self.zoom_position
                self.zoom_factor_old = self.zoom_factor
                self.zoom_position_old_cm_frame = self.zoom_position_cm_frame
                self.zoom_factor *= (1+self.event.y*self.zoom_step_factor)  
                self.zoom_position = np.array(pygame.mouse.get_pos())
                self.zoom_position_cm_frame = (
                      self.zoom_position - self.zoom_position_old
                    )/self.zoom_factor_old + self.zoom_position_old_cm_frame

    def draw_all(self):
        print("draw", self.counter)
        self.center = np.array(self.screen.get_size())/2
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.surface.fill(pygame.Color('black'))
        for planet in self.celestialobjects:
                    if self.do_draw_tails:
                        self.draw_tail(planet)

        for planet in self.celestialobjects:
            corrected_position = self.get_zoomed_coordinate(planet.position)
            self.draw_celestialobjects(planet, corrected_position)

            if self.do_draw_arrows:
                self.draw_arrows(planet, corrected_position)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

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

    def draw_arrows(self, planet, corrected_position):
        self.draw_arrow(
            pygame.Color(planet.color), 
            corrected_position,
            corrected_position + 
            (planet.force/planet.mass - self.correction_acceleration)*100
            )
        self.draw_arrow(pygame.Color(planet.color), corrected_position
                       , corrected_position+(planet.velocity - self.correction_velocity )*10)

    def draw_celestialobjects(self, planet, corrected_position):
        color = pygame.Color(planet.color)
        x, y = int(corrected_position[0]), int(corrected_position[1])
        r = max(int(self.zoom_factor*planet.radius), 1)
        gfxdraw.filled_circle(self.surface, x, y, r,  color)
        gfxdraw.aacircle(self.surface, x, y ,r , color)

    def draw_tail(self, planet):
        planet.update_tail(10000)
        color_rgb = pygame.Color(planet.color)
        length_tail = len(planet.tail)
        for i, pos in enumerate(planet.tail):
            color_rgb.a = int(255 * i / length_tail)
            self.surface.fill(color_rgb, (self.get_zoomed_coordinate(pos), (1, 1)))


    def get_zoomed_coordinate(self, coordinate):
        zoomed_coordinate = (
            self.zoom_factor * (coordinate - self.zoom_position_cm_frame) 
            + self.zoom_position
            )
        return zoomed_coordinate

    def next_step(self):
        self.counter += 1
        co.set_new_state(self.celestialobjects, self.G, self.alpha,
                         self.delta_t, self.do_collide)
        for planet in self.celestialobjects:
            if co.norm(planet.position) > self.limits:
                print("planet: "  + planet.name + " will be removed")
                self.celestialobjects.remove(planet)

try:
    animation = Animate_celestialobjects_pygame()
except:
    print("Unexpected error:", sys.exc_info())
    print(traceback.format_exc())
    pygame.quit()
    sys.exit()
    raise

