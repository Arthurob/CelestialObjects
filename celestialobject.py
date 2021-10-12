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
# import numba as nb
# import webcolors

class celestialobject:

    def __init__(self, mass, color, canvas_animation, canvas_graph, start_position=np.zeros((2,)), start_velocity=np.zeros((2,)), name='', radius=0):
        self.mass = mass
        if radius == 0:
            self.radius = max(2*math.sqrt(mass), 1)
        else:
            self.radius = radius
        self.position = np.array(start_position).astype(np.float64)
        self.canvas_position = self.position
        self.velocity = np.array(start_velocity).astype(np.float64)
        self.force = np.zeros((2,))
        self.acceleration = np.zeros((2,))
        self.color = color
        if name == '':
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            self.name = 'planet'+result_str
        coords_circle = [start_position[0]-self.radius, start_position[1]-self.radius,
                         start_position[0]+self.radius, start_position[1]+self.radius]
        self.canvas_animation = canvas_animation
        self.canvas_graph = canvas_graph
        self.oval = canvas_animation.create_oval(coords_circle[0], coords_circle[1],
                                                 coords_circle[2], coords_circle[3], fill=color)
        self.force_arrow_on_planet = canvas_animation.create_line(coords_circle[0], coords_circle[1],
                                                        coords_circle[2], coords_circle[3],
                                                        arrow=tk.LAST, fill=self.color)


        self.velocity_arrow_on_planet = canvas_animation.create_line(coords_circle[0], coords_circle[1],
                                                           coords_circle[2], coords_circle[3],
                                                           arrow=tk.LAST, fill=self.color)
        self.force_arrow_on_graph = canvas_graph.create_line(150, 150, 150, 250,
                                                        arrow=tk.LAST, fill=self.color)

        self.velocity_arrow_on_graph = canvas_graph.create_line(150, 150, 150, 250,
                                                        arrow=tk.LAST, fill=self.color)
        self.keep_history = True
        # self.maxsize
        self.speed_history = []
        self.acceleration_history = []
        self.phi_history = []
        self.tail=[]
        self.canvas_animation.tag_bind(self.oval, "<Any-Enter>", self.mouseEnter)
        self.canvas_animation.tag_bind(self.oval, "<Any-Leave>", self.mouseLeave)

    def mouseEnter(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
	# this happens automatically.
    	self.canvas_animation.itemconfig(self.oval, fill="firebrick1")

    def mouseLeave(self, event):
	# the CURRENT tag is applied to the object the cursor is over.
	# this happens automatically.
    	self.canvas_animation.itemconfig(self.oval, fill=self.color)



    def reset_force(self):
        self.force = np.zeros((2,))

    # def update_parameters(self, position. )
    def move_object(self, change, draw_tail=True, tail_length=1000, color_trail=''):
        self.canvas_animation.move(self.oval, change[0], change[1])
        self.canvas_position = self.get_center_oval()
        if draw_tail: # and norm(change)>.5:
            if color_trail == '':
                color_trail = self.color
            rect = self.canvas_animation.create_rectangle(
                (self.canvas_position[0], self.canvas_position[1])*2
                                         ,outline=color_trail)
            self.tail.insert(0, rect)
            if len(self.tail) > tail_length:
                self.canvas_animation.delete(self.tail[-1])
                del self.tail[-1]

    def get_acceleration(self, correction=np.zeros((2,))):
        return norm(self.acceleration + correction)

    def get_speed(self, correction=np.zeros((2,))):
        return norm(self.velocity + correction)

    def get_center_oval(self):
        coords = self.canvas_animation.coords(self.oval)
        return np.array([(coords[0] + coords[2])/2, (coords[1] + coords[3])/2])

    def get_phi(self):
        return angle_between(self.acceleration, self.velocity)

    def new_state_planet(self, delta_t):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * delta_t
        self.position += self.velocity * delta_t
        if self.keep_history:
            self.speed_history.append(self.get_speed())
            self.acceleration_history.append(self.get_acceleration())
            self.phi_history.append(self.get_phi())


    def draw_acceleration_arrow_on_planet(self, correction=np.zeros((2,)), factor = 160):
        # if factor != 0:
        start_point = self.canvas_position
        end_point = start_point + (self.acceleration + correction) * factor
        # print(start_point, (start_point + self.acceleration), end_point)
        self.canvas_animation.coords(self.force_arrow_on_planet,start_point[0], start_point[1],
                           end_point[0], end_point[1])

    def draw_velocity_arrow_on_planet(self, correction=np.zeros((2,)), factor = 30):
        # if factor != 0:
            start_point = self.canvas_position
            end_point = start_point + (self.velocity + correction) * factor
            self.canvas_animation.coords(self.velocity_arrow_on_planet,start_point[0], start_point[1],
                               end_point[0], end_point[1])

    def draw_acceleration_arrow_on_graph(self, correction=np.zeros((2,)), factor = 160):
        # if factor != 0:
            start_point = np.array([150,150])
            end_point = start_point + (self.acceleration + correction) * factor
            # print(start_point, (start_point + self.acceleration), end_point)
            self.canvas_graph.coords(self.force_arrow_on_graph,start_point[0], start_point[1],
                               end_point[0], end_point[1])

    def draw_velocity_arrow_on_graph(self, correction=np.zeros((2,)), factor = 30):
        # if factor != 0:
            start_point = np.array([150,150])
            end_point = start_point + (self.velocity + correction) * factor
            self.canvas_graph.coords(self.velocity_arrow_on_graph,start_point[0], start_point[1],
                               end_point[0], end_point[1])

def set_state_after_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, r_21_in_v_12):
    vector = 2*r_21_in_v_12/((celestialobject_1.mass + celestialobject_2.mass)*r_21_norm**2)*r_21
    celestialobject_1.velocity -= celestialobject_2.mass*vector
    celestialobject_2.velocity += celestialobject_1.mass*vector


def handle_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, R_12, delta_t, enterIsPossible):
    v_12 = celestialobject_1.velocity - celestialobject_2.velocity
    r_21_in_v_12 = np.dot(r_21, v_12)
    v_12_2 = np.dot(v_12, v_12)
    if not enterIsPossible:
        # calculate time where collision happened
        t_c = (math.sqrt(r_21_in_v_12**2 - v_12_2*(r_21_norm**2 - R_12**2)) - r_21_in_v_12)/ v_12_2
        print('1', delta_t, t_c, r_21_norm, r_21_norm-R_12)
        # Set positions at where the collison happened
        celestialobject_1.position -= t_c * celestialobject_1.velocity
        celestialobject_2.position -= t_c * celestialobject_2.velocity
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
        r_21_in_v_12 = np.dot(r_21, v_12)
        print('r_21 - R_12 = ', r_21_norm - R_12)
    set_state_after_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, r_21_in_v_12)


    if not enterIsPossible:
        # Adjust positions to "current time"
        celestialobject_1.position += abs(delta_t - t_c) * celestialobject_1.velocity
        celestialobject_2.position += abs(delta_t - t_c) * celestialobject_2.velocity
        print('R_12 = ', celestialobject_2.radius + celestialobject_1.radius)
        print('Positions and distances  = ',celestialobject_1.position, celestialobject_2.position, r_21, r_21_norm)
        print('Velocities:', celestialobject_1.velocity, celestialobject_2.velocity)


def calculate_force_and_collisions_2_celestialobjects(celestialobject_1, celestialobject_2, G, delta_t, alpha=2, collisionsOn=True, enterIsPossible=False):
    r_21 = celestialobject_2.position - celestialobject_1.position
    r_21_norm = norm(r_21)
    R_12 = celestialobject_1.radius + celestialobject_2.radius
    collison = False
    # collisions
    if collisionsOn and r_21_norm <= R_12:
        collison = True
        print(f'collision between {celestialobject_1.color} and {celestialobject_2.color}')
        print('R_12 = ', celestialobject_2.radius + celestialobject_1.radius)
        print('Positions and distances  = ',celestialobject_1.position, celestialobject_2.position, r_21, r_21_norm)
        print('Velocities:', celestialobject_1.velocity, celestialobject_2.velocity)
        handle_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, R_12, delta_t, enterIsPossible)
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
    F_12 = G * celestialobject_1.mass * celestialobject_2.mass /  r_21_norm**(alpha+1) * r_21
    celestialobject_1.force = celestialobject_1.force + F_12
    celestialobject_2.force = celestialobject_2.force - F_12
    return collison

def unit_vector(vector):
    return vector / norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(inner(v1_u, v2_u))

# @nb.njit(fastmath=True)
def norm(v):
    return np.sqrt(np.inner(v, v))

def inner(u, v):
    return np.inner(u, v)
