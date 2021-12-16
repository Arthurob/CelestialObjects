# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 23:08:18 2021

@author: Arthur
Two abbriviations are often used to reduce lengthy variables:
    cm for center of mass
    and co for Celestial Object
"""
import sys
import traceback
import numpy as np
import math
import pygame
import pygame_widgets
from pygame import gfxdraw
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import celestialobject as co

class Zoom():
    """
    The zoom class handles all the parameters used for zooming.

    Attributes
  ----------       
  step_factor : nummerical
      used to change the zoom factor in steps.
  factor : nummerical
      the zoom factor.
  factor_prev : nummerical
      the previous zoom factor
  position : nummerical
      The on screen position of where to zoom on in/out.
  position_prev : nummerical
      the previous on screen position.
  position_co_frame : nummerical
      the zoom position in the celestial object frame.
  position_prev_co_frame : nummerical
      the previous zoom position in the celestial object frame.
    
    """
    def __init__(self, step_factor=.05):
        """
        initizalize the zoom parameters, which start in the unzoomed state

        Parameters
        ----------
        step_factor : nummerical, optional
            used to change the zoom factor in steps . The default is .05.

        Returns
        -------
        None.

        """
        self.step_factor = step_factor
        self.factor = 1
        self.factor_prev = 1
        self.position = np.zeros((2,))
        self.position_prev = np.zeros((2,))
        self.position_co_frame = np.zeros((2,))
        self.position_prev_co_frame = np.zeros((2,))
        
    def update_parameters(self, position, direction):
        """
        Updates the zoom parameters after a zoom event has taken place

        Parameters
        ----------
        position : nummerical 
        The on screen position of where to zoom on in/out..
        direction : nummerical
            +1 for zooming in, -1 for zooming out.

        Returns
        -------
        None.

        """
        self.position_prev = self.position
        self.factor_prev = self.factor
        self.position_prev_co_frame = self.position_co_frame
        self.position = position
        self.factor *= (1 + direction * self.step_factor)  
        self.position_co_frame = (
              self.position - self.position_prev
            )/self.factor_prev + self.position_prev_co_frame
        
    def get_zoomed_coordinate(self, coordinate):
        """
        yields the zoomed in coordinates of any coordinate in the Celestial
        Object reference space

        Parameters
        ----------
        coordinate : numpy array
             coordinate in the Celestial
             Object reference space .

        Returns
        -------
        zoomed_coordinate : numpy array
        the zoomed in coordinates of any coordinate in the Celestial
        Object reference space.

        """
        zoomed_coordinate = (
            self.factor * (coordinate - self.position_co_frame) 
            + self.position
            )
        return zoomed_coordinate

class AnimateCelestialobjects():

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
        self.init_parameters()
        # self.init_UI()
        self.initialise_planets()
        self.celestial_initizalized = True
        self.mainloop()
        
    def init_parameters(self):
        # variables
        self.counter = 0
        #zoom
        self.zoom = Zoom()
        print(self.zoom)
        self.do_draw_tails = True
        self.do_draw_arrows = True
        self.do_collide = True
        self.G = 15
        self.alpha = 2
        self.delta_t = .5
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
            self.center+np.array([150, 1500+20]),
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
             
            self.center+np.array([-1000,250]),
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
             
            self.center+np.array([-1000,100]),
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
            if ((self.event.y>0 and self.zoom.factor <= 100) or 
                (self.event.y<0 and .01 <= self.zoom.factor)):
                self.zoom.update_parameters(
                    np.array(pygame.mouse.get_pos()),
                    self.event.y)

    def draw_all(self):
        # print("draw", self.counter)
        self.center = np.array(self.screen.get_size())/2
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.surface.fill(pygame.Color('black'))
        for planet in self.celestialobjects:
            if self.do_draw_tails:
                self.draw_tail(planet)

        for planet in self.celestialobjects:
            corrected_position = self.zoom.get_zoomed_coordinate(planet.position)
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
        r = max(int(self.zoom.factor*planet.radius), 1)
        gfxdraw.filled_circle(self.surface, x, y, r,  color)
        gfxdraw.aacircle(self.surface, x, y ,r , color)

    def draw_tail(self, planet):
        planet.update_tail(10000)
        color_rgb = pygame.Color(planet.color)
        length_tail = len(planet.tail)
        for i, pos in enumerate(planet.tail):
            color_rgb.a = int(255 * i / length_tail)
            self.surface.fill(color_rgb, (self.zoom.get_zoomed_coordinate(pos), (1, 1)))

    def next_step(self):
        self.counter += 1
        co.set_new_state(self.celestialobjects, self.G, self.alpha,
                         self.delta_t, self.do_collide)
        for planet in self.celestialobjects:
            if co.norm(planet.position) > self.limits:
                print("planet: "  + planet.name + " will be removed")
                self.celestialobjects.remove(planet)

try:
    animation = AnimateCelestialobjects()
except:
    print("Unexpected error:", sys.exc_info())
    print(traceback.format_exc())
    pygame.quit()
    sys.exit()
    raise

