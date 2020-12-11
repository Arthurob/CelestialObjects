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
import numba as nb
# import webcolors

class celestialobject:

    def __init__(self, mass, color, canvas, start_position=np.zeros((2,)), start_velocity=np.zeros((2,)), name='', radius=0):
        self.mass = mass
        if radius == 0:
            self.radius = 3*math.sqrt(mass)
        else:
            self.radius = radius
        self.position = np.array(start_position).astype(np.double)
        self.canvas_position = self.position
        self.velocity = np.array(start_velocity).astype(np.double)
        self.force = np.zeros((2,))
        self.acceleration = np.zeros((2,))
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
        distance = celestialobject_2.position - celestialobject_1.position
        F_12 = G * celestialobject_1.mass * celestialobject_2.mass /  np.sqrt(distance[0]*distance[0]+distance[1]*distance[1])**(alpha+1) * distance
        # F_12 = G * celestialobject_1.mass * celestialobject_2.mass /  norm(distance)**(alpha+1) * distance
        celestialobject_1.force = celestialobject_1.force + F_12
        celestialobject_2.force = celestialobject_2.force - F_12

    def reset_force(self):
        self.force = np.zeros((2,))

    # def update_parameters(self, position. )
    def move_object(self, change, colortrail=''):
        self.canvas.move(self.oval, change[0], change[1])
        self.canvas_position = self.get_center_oval()
        if colortrail == '':
            colortrail = self.color
        self.canvas.create_rectangle((self.canvas_position[0], self.canvas_position[1])*2,outline=colortrail)

    def get_center_oval(self):
        coords = self.canvas.coords(self.oval)
        return np.array([(coords[0] + coords[2])/2, (coords[1] + coords[3])/2], dtype = np.double)

    def get_phi(self):
        return self.angle_between(self.acceleration, self.velocity)

    def new_state_planet(self, delta_t):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration*delta_t
        self.position += self.velocity*delta_t

    def draw_acceleration_arrow(self, correction=np.zeros((2,)), factor = 140):
        start_point = self.canvas_position
        end_point = start_point + (self.acceleration + correction) * factor
        # print(start_point, (start_point + self.acceleration), end_point)
        self.canvas.coords(self.force_arrow,start_point[0], start_point[1], end_point[0], end_point[1])

    def draw_velocity_arrow(self, correction=np.zeros((2,)), factor = 40):
        start_point = self.canvas_position
        end_point = start_point + (self.velocity + correction) * factor
        self.canvas.coords(self.velocity_arrow,start_point[0], start_point[1], end_point[0], end_point[1])

    @classmethod
    def unit_vector(self, vector):
        return vector / np.linalg.norm(vector)

    @classmethod
    def angle_between(self, v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

@nb.njit(fastmath=True)
def norm(l):
    s = 0.
    for i in range(l.shape[0]):
        s += l[i]**2
    return np.sqrt(s)
