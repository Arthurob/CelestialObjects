# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:26:10 2020

@author: Arthur
"""
import numpy as np
import random
import string
import math

class celestialobject:

    def __init__(self, mass, color, start_position=np.zeros((2,)), start_velocity=np.zeros((2,)), name='', radius=0):
        self.mass = mass
        if radius == 0:
            # self.radius = max(2*math.sqrt(mass), 1)
            self.radius = 3*max(mass**(1/3), 1)
        else:
            self.radius = radius
        self.position = np.array(start_position).astype(np.float64)
        print(self.position)
        self.velocity = np.array(start_velocity).astype(np.float64)
        self.force = np.zeros((2,))
        self.acceleration = np.zeros((2,))
        self.color = color
        if name == '':
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            self.name = 'planet'+result_str
        else:
            self.name = name
        self.keep_history = True
        # self.maxsize
        self.speed_history = []
        self.acceleration_history = []
        self.phi_history = []
        self.tail=[]

    def reset_force(self):
        self.force = np.zeros((2,))

    def update_tail(self, tail_length=1000):
        self.tail.append(np.copy(self.position))
        if len(self.tail) > tail_length:
            del self.tail[0]

    def get_acceleration(self, correction=np.zeros((2,))):
        return norm(self.acceleration + correction)

    def get_speed(self, correction=np.zeros((2,))):
        return norm(self.velocity + correction)


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
        # Set positions at where the collison happened
        celestialobject_1.position -= t_c * celestialobject_1.velocity
        celestialobject_2.position -= t_c * celestialobject_2.velocity
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
        r_21_in_v_12 = np.dot(r_21, v_12)
    set_state_after_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, r_21_in_v_12)


    if not enterIsPossible:
        # Adjust positions to "current time"
        celestialobject_1.position += abs(delta_t - t_c) * celestialobject_1.velocity
        celestialobject_2.position += abs(delta_t - t_c) * celestialobject_2.velocity



def set_forces_2celestialobjects(celestialobject_1, celestialobject_2, G, delta_t, alpha=2, collisionsOn=True, enterIsPossible=False):
    r_21 = celestialobject_2.position - celestialobject_1.position
    r_21_norm = norm(r_21)
    R_12 = celestialobject_1.radius + celestialobject_2.radius
    collison = False
    # collisions
    if collisionsOn and r_21_norm <= R_12:
        collison = True
        handle_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, R_12, delta_t, enterIsPossible)
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
    F_12 = G * celestialobject_1.mass * celestialobject_2.mass /  r_21_norm**(alpha+1) * r_21
    celestialobject_1.force = celestialobject_1.force + F_12
    celestialobject_2.force = celestialobject_2.force - F_12
    return collison

def get_coords_com(celestialobjects):
        return sum([planet.mass*planet.position for planet in celestialobjects]) / sum([planet.mass for planet in celestialobjects])

    # def create_reandom_planet(range_mass=[1,20], range_size=[1,20], range_location=[100,800], range_velocity=[-5,5]):
    #     co.celestialobject(9, 8, self.center, [-.05, 0])



def set_new_state(celestialobjects, G, alpha, delta_t, collisionsOn=True, enterIsPossible=False):
    for planet in celestialobjects:
        planet.reset_force()

    if celestialobjects:
        for i, planet1 in enumerate(celestialobjects[:-1]):
            for planet2 in celestialobjects[i+1::]:
                collision = set_forces_2celestialobjects(
                    planet1, planet2, G, delta_t, alpha, collisionsOn, enterIsPossible)

    for planet in celestialobjects:
        planet.new_state_planet(delta_t)

    return collision

def unit_vector(vector):
    return vector / norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.inner(v1_u, v2_u))

def norm(v):
    return np.sqrt(np.inner(v, v))