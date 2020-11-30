# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:26:10 2020

@author: Arthur
"""
import numpy as np
import random
import string
import tkinter as tk
import math
# import webcolors

class celestialobject:

    def __init__(self, mass, color, canvas, start_position=[0,0], start_velocity=[0,0], name='', radius=0):
        self.mass = mass
        if radius == 0:
            self.radius = 3*math.sqrt(mass)
        else:
            self.radius = radius
        self.position = np.array(start_position).astype(np.double)
        self.velocity = np.array(start_velocity).astype(np.double)
        self.force = np.array([0,0]).astype(np.double)
        self.acceleration = np.array([0,0]).astype(np.double)
        self.color = color
        if name == '':
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            self.name = 'planet'+result_str
        coords_circle = [start_position[0]-self.radius/2, start_position[1]-self.radius/2, start_position[0]+self.radius/2, start_position[1]+self.radius/2]
        self.canvas = canvas
        self.oval = canvas.create_oval(coords_circle[0], coords_circle[1], coords_circle[2], coords_circle[3], fill=color)
        self.force_arrow = canvas.create_line(coords_circle[0], coords_circle[1], coords_circle[2], coords_circle[3], arrow=tk.LAST, fill=self.color)
        self.velocity_arrow = canvas.create_line(coords_circle[0], coords_circle[1], coords_circle[2], coords_circle[3], arrow=tk.LAST, fill=self.color)

    @classmethod
    def set_force_2_celestialobjects(cls, celestialobject_1, celestialobject_2, G, alpha=2):
        distance = celestialobject_2.position -celestialobject_1.position
        F_12 = G *celestialobject_1.mass * celestialobject_2.mass /  np.linalg.norm(distance)**(alpha+1) * distance
        celestialobject_1.force = celestialobject_1.force + F_12
        celestialobject_2.force = celestialobject_2.force - F_12

    def reset_force(self):
        self.force = np.array([0,0]).astype(np.double)

    # def update_parameters(self, position. )
    def move_object(self, change, colortrail=''):
        self.canvas.move(self.oval, change[0], change[1])
        r = self.get_center_oval()
        if colortrail == '':
            colortrail = self.color
        self.canvas.create_rectangle(r[0], r[1], r[0], r[1], outline=colortrail)

    def get_center_oval(self):
        coords = self.canvas.coords(self.oval)
        return np.array([(coords[0] + coords[2])/2, (coords[1] + coords[3])/2])

    def get_phi(self):
        return np.outer(self.acceleration, self.velocity)

    def new_state_planet(self, delta_t):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration*delta_t
        self.position += self.velocity*delta_t

    def draw_acceleration_arrow(self, correction=np.array([0,0]).astype(np.double), factor = 140):
        start_point = self.get_center_oval()
        end_point = start_point + (self.acceleration + correction) * factor
        # print(start_point, (start_point + self.acceleration), end_point)
        self.canvas.coords(self.force_arrow,start_point[0], start_point[1], end_point[0], end_point[1])

    def draw_velocity_arrow(self, correction=np.array([0,0]).astype(np.double), factor = 40):
        start_point = self.get_center_oval()
        end_point = start_point + (self.velocity + correction) * factor
        self.canvas.coords(self.velocity_arrow,start_point[0], start_point[1], end_point[0], end_point[1])

