# -*- coding: utf-8 -*-
# pylint: disable=E1101
"""
Created on Mon Sep 20 23:08:18 2021


@author: Arthur
Two abbriviations are often used to reduce lengthy variables:
    cm for center of mass
    and co for Celestial Object
"""
# TODO: React to sound(chaning paraeters)
# FIXME: Zoom not woring with moving canvas

import sys
import traceback
import math
import numpy as np
import pygame
# import pygame_menu
# import pygame_widgets
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
          the previous zoom position in the celestial object frame
    """

    def __init__(self, step_factor=.05):
        """
        Initizalize the zoom parameters, which start in the unzoomed state.

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
        Update the zoom parameters after a zoom event has taken place.

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
        Yield the zoomed coordinates of any coordinate in the Celestial
        Object reference space.

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
    """
      This class animates the movement of Celestial bodies using Pygame.
      Attributes
    ----------
    orbited_celestial_objects: List of the Celestial objects
    which the new Celestial orbit will initially orbit.
    G: numerical value gravitational constant,
    direction: numerical
        direction(1 for clockwise, -1 for counterclockwise)]
    eccentricity: numerical
        the eccentricity, e,  of the orbit: 0: circular, 0<e<1: elliptical
        e>1: hyperbolic
    angle: numerical
        angle between the orbeting celestial objct and the semi-major axis of
        the trajectory

    """

    def __init__(self):
        SCREEN_SIZE = WIDTH, HEIGHT = (1000, 1000)

        # Initialization
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption('Celestial objects')
        self.fps = pygame.time.Clock()
        self.pause = False

        self.center = np.array([WIDTH, HEIGHT])/2
        # self.init_window()
        self.init_parameters()
        # self.init_UI()
        self.initialise_planets()
        self.celestial_initizalized = True
        self.mainloop()

    def init_parameters(self):
        # variables
        self.counter = 0
        # zoom
        self.zoom = Zoom()
        self.origin = np.zeros((2,))
        self.move = np.zeros((2,))
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
        # self.controlsmenu = ControlsMenu()

    def initialise_planets(self):
        self.celestialobjects = []
        # self.celestialobjects.append(
        # co.Celestialobject(
        #     1000,
        #     'yellow',
        #     self.center+np.array([-150., 0.]),
        #     np.array([0, 0.]),
        #     'celestial_object1'
        #     )

        # )

        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     400,
        #     'magenta',
        #     self.center+np.array([150., 0.]),
        #     co.Trajectory(
        #         self.celestialobjects[0], self.G
        #         ),
        #         'celestial_object2'
        #                           )
        #                     )
        # #Ellipse
        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     200,
        #     'blue',
        #     self.center+np.array([800, -200]),
        #     co.Trajectory(
        #         self.celestialobjects[0:2], self.G,
        #         eccentricity=.7, angle=math.pi/11,direction = -1
        #         ),
        #         'celestial_object4'
        #                           )
        #                     )
        # # planet+two moons
        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     100,
        #     'red',
        #     self.center+np.array([0., 1500]),
        #     co.Trajectory(
        #         self.celestialobjects[0:2], self.G,
        #         eccentricity=.3, angle=-math.pi/5
        #         ),
        #         'planet'
        #                           )
        #                     )

        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     10,
        #     'gold',
        #     self.center+np.array([150, 1500]),
        #     co.Trajectory(
        #         self.celestialobjects[3], self.G
        #         ),
        #         'moon'
        #                           )
        #                     )
        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     1,
        #     'green',
        #     self.center+np.array([150, 1500+20]),
        #     co.Trajectory(
        #         self.celestialobjects[4], self.G
        #         ),
        #         'moon 2'
        #                           )
        #                     )
        # #binary planets
        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     100,
        #     'coral',

        #     self.center+np.array([-1000,250]),
        #     co.Trajectory(
        #         self.celestialobjects[0:2], self.G,
        #         direction=-1
        #         ),
        #         'planet'
        #                           )
        #                     )
        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     76,
        #     'orange',

        #     self.center+np.array([-1000,100]),
        #     co.Trajectory(
        #         self.celestialobjects[6], self.G,
        #         direction=-1
        #         ),
        #         'planet'
        #                           )
        #                     )

        # self.celestialobjects.append(
        #     co.Celestialobject.fromtrajectory(
        #     1,
        #     'orange',
        #     self.center+np.array([-8070,100]),
        #     co.Trajectory(
        #         self.celestialobjects[0:2], self.G,
        #         direction=-1, eccentricity=2
        #         ),
        #         'planet'
        #                           )
        #                     )
        # shaped_planets = co.create_celestial_objects_in_geometric_shape(
        #     np.array([0,0]), 500, 2, 5, 200, 'purple')
        shaped_planets_1 = co.create_celestial_objects_in_geometric_shape(
            center=self.center,
            length=500,
            velocity_perpundicular=3,
            n_sides=5,
            mass=100,
            color='purple')
        shaped_planets_2 = co.create_celestial_objects_in_geometric_shape(
            center=self.center,
            length=1000,
            velocity_perpundicular=-4,
            n_sides=10,
            mass=50,
            color='white')
        self.celestialobjects = self.celestialobjects + \
            shaped_planets_1 + shaped_planets_2
        self.coordsCOM = co.get_center_of_mass_coordinates(
            self.celestialobjects)
        co.substract_centerofmass_velocity(self.celestialobjects)
        # self.init_COM()

    def mainloop(self):
        while True:
            if not self.pause:
                self.next_step()
                self.draw_all()
                pygame.time.delay(self.delay)
                self.handle_events()

    def handle_events(self):
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.move[0] = -1
                if event.key == pygame.K_LEFT:
                    self.move[0] = 1
                if event.key == pygame.K_UP:
                    self.move[1] = 1
                if event.key == pygame.K_DOWN:
                    self.move[1] = -1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                if event.key == pygame.K_RIGHT:
                    self.move[0] = 0
                if event.key == pygame.K_LEFT:
                    self.move[0] = 0
                if event.key == pygame.K_UP:
                    self.move[1] = 0
                if event.key == pygame.K_DOWN:
                    self.move[1] = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos = pygame.mouse.get_pos()
                    print("you clicked at:", pos, self.counter)

            elif event.type == pygame.MOUSEWHEEL:
                if ((event.y > 0 and self.zoom.factor <= 100) or
                        (event.y < 0 and .01 <= self.zoom.factor)):
                    self.zoom.update_parameters(
                        np.array(pygame.mouse.get_pos()),
                        event.y)

    def draw_all(self):
        width, height = self.screen.get_size()
        self.size_controls = 300
        self.draw_animation(np.array([width - self.size_controls, height]))
        self.draw_controls(np.array([width, height]))
        pygame.display.update()

    def draw_controls(self, size):
        self.controls_surface = pygame.Surface((self.size_controls, size[1]))
        self.controls_surface.fill(pygame.Color('white'))
        slider = Slider(
            self.controls_surface, 100, 100, 80, 40, min=0, max=99, step=1
            )
        output = TextBox(self.controls_surface, 475, 200, 50, 50, fontSize=30)
        output.setText(slider.getValue())
        # self.controlsmenu.menu.mainloop(self.controls_surface)
        self.screen.blit(self.controls_surface,
                         (size[0]-self.size_controls, 0))

    def update_origin(self):
        self.origin += 15 * self.move

    def draw_animation(self, size):
        # print("draw", self.counter)

        self.center = size/2
        self.animation_surface = pygame.Surface(size, pygame.SRCALPHA)
        self.animation_surface.fill(pygame.Color('black'))
        for planet in self.celestialobjects:
            if self.do_draw_tails:
                self.draw_tail(planet)

        for planet in self.celestialobjects:
            corrected_position = (
                self.zoom.get_zoomed_coordinate(planet.position)
                + self.origin
            )
            self.draw_celestialobjects(planet, corrected_position)
            if self.do_draw_arrows:
                self.draw_arrows(planet, corrected_position)
        self.screen.blit(self.animation_surface, (0, 0))
        # pygame.display.update()

    def draw_arrow(self, color, start, end):
        pygame.draw.aaline(self.animation_surface, color, start, end, 1)
        rotation = math.degrees(math.atan2(
            start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(self.animation_surface, color,
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
        self.draw_arrow(pygame.Color(planet.color), corrected_position,
                        corrected_position+(planet.velocity - self.correction_velocity)*10)

    def draw_celestialobjects(self, planet, corrected_position):
        color = pygame.Color(planet.color)
        x, y = int(corrected_position[0]), int(corrected_position[1])
        r = max(int(self.zoom.factor*planet.radius), 1)
        gfxdraw.filled_circle(self.animation_surface, x, y, r,  color)
        gfxdraw.aacircle(self.animation_surface, x, y, r, color)

    def draw_tail(self, planet):
        planet.update_tail(10000)
        color_rgb = pygame.Color(planet.color)
        length_tail = len(planet.tail)
        for i, pos in enumerate(planet.tail):
            color_rgb.a = int(255 * i / length_tail)
            self.animation_surface.fill(color_rgb, (
                self.zoom.get_zoomed_coordinate(pos)
                + self.origin,
                (1, 1))
            )

    def next_step(self):
        self.counter += 1
        co.set_new_state(self.celestialobjects, self.G, self.alpha,
                         self.delta_t, self.do_collide)
        self.update_origin()
        for planet in self.celestialobjects:
            if co.norm(planet.position) > self.limits:
                print("planet: " + planet.name + " will be removed")
                self.celestialobjects.remove(planet)


try:
    animation = AnimateCelestialobjects()
except:
    print("Unexpected error:", sys.exc_info())
    print(traceback.format_exc())
    pygame.quit()
    sys.exit()
    raise
